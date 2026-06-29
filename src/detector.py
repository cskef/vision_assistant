from ultralytics import YOLO

from src.models import Detection


class VehicleDetector:
    def __init__(self, model_path, config):
        self.config = config
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model.predict(frame, verbose=False, conf=self.config.confidence_threshold)
        detections = []

        if not results:
            return detections

        names = results[0].names
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            label = names[class_id]
            confidence = float(box.conf[0])

            if label not in self.config.vehicle_classes:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(
                Detection(
                    label=label,
                    confidence=confidence,
                    bbox=(int(x1), int(y1), int(x2), int(y2)),
                )
            )

        return detections
