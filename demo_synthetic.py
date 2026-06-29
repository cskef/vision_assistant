import time

import cv2
import numpy as np

from src.alerts import AlertEngine
from src.config import AppConfig
from src.models import Detection
from src.speaker import Speaker
from src.tracker import CentroidTracker
from src.utils import draw_tracked_object


def synthetic_detections(frame_index):
    growth = frame_index * 5
    return [
        Detection(
            label="car",
            confidence=0.92,
            bbox=(250 - growth, 170 - growth // 2, 390 + growth, 280 + growth),
        ),
        Detection(
            label="bus",
            confidence=0.88,
            bbox=(30, 140, 170, 300),
        ),
    ]


def main():
    config = AppConfig()
    tracker = CentroidTracker(max_missing_frames=5, max_distance=120)
    alerts = AlertEngine(config)
    speaker = Speaker(enabled=False)

    for frame_index in range(35):
        frame = np.full((480, 640, 3), 245, dtype=np.uint8)
        cv2.putText(
            frame,
            "Demo synthetique - detection vehicules",
            (28, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (30, 30, 30),
            2,
            cv2.LINE_AA,
        )

        detections = synthetic_detections(frame_index)
        objects = tracker.update(detections)
        messages = alerts.evaluate(objects, frame.shape)

        for obj in objects:
            draw_tracked_object(frame, obj)

        for index, message in enumerate(messages[:2]):
            cv2.putText(
                frame,
                message,
                (28, 420 + index * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 200),
                2,
                cv2.LINE_AA,
            )
            speaker.say(message)

        cv2.imshow("Demo synthetique", frame)
        if cv2.waitKey(80) & 0xFF == ord("q"):
            break
        time.sleep(0.03)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
