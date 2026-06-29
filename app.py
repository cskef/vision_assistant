import argparse
import time

import cv2

from src.alerts import AlertEngine
from src.config import AppConfig
from src.detector import VehicleDetector
from src.speaker import Speaker
from src.tracker import CentroidTracker
from src.utils import draw_tracked_object


def parse_args():
    parser = argparse.ArgumentParser(
        description="Agent intelligent de vision assistee: detection de vehicules."
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Camera index, URL de flux, ou chemin video. Exemple: 0 ou demo.mp4",
    )
    parser.add_argument("--model", default="yolov8n.pt", help="Modele YOLO a utiliser.")
    parser.add_argument("--confidence", type=float, default=0.45, help="Seuil de confiance.")
    parser.add_argument("--mute", action="store_true", help="Desactive la synthese vocale.")
    parser.add_argument("--no-window", action="store_true", help="N'affiche pas la fenetre video.")
    return parser.parse_args()


def normalize_source(value):
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def main():
    args = parse_args()
    config = AppConfig(confidence_threshold=args.confidence)

    detector = VehicleDetector(model_path=args.model, config=config)
    tracker = CentroidTracker(max_missing_frames=12, max_distance=90)
    alerts = AlertEngine(config=config)
    speaker = Speaker(enabled=not args.mute)

    cap = cv2.VideoCapture(normalize_source(args.source))
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la source video: {args.source}")

    last_spoken_at = 0.0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        detections = detector.detect(frame)
        tracked_objects = tracker.update(detections)
        messages = alerts.evaluate(tracked_objects, frame.shape)

        now = time.time()
        if messages and now - last_spoken_at >= config.voice_cooldown_seconds:
            speaker.say(messages[0])
            last_spoken_at = now

        if not args.no_window:
            for obj in tracked_objects:
                draw_tracked_object(frame, obj)

            for index, message in enumerate(messages[:2]):
                cv2.putText(
                    frame,
                    message,
                    (20, 35 + index * 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("Agent Vision Assistee - Vehicules", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    speaker.close()


if __name__ == "__main__":
    main()

