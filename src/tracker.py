from dataclasses import dataclass, field
from math import hypot


@dataclass
class TrackedObject:
    object_id: int
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    previous_area: float | None = None
    missing_frames: int = 0
    area_history: list[float] = field(default_factory=list)

    @property
    def centroid(self):
        x1, y1, x2, y2 = self.bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    @property
    def area(self):
        x1, y1, x2, y2 = self.bbox
        return max(0, x2 - x1) * max(0, y2 - y1)


class CentroidTracker:
    def __init__(self, max_missing_frames=10, max_distance=80):
        self.max_missing_frames = max_missing_frames
        self.max_distance = max_distance
        self.next_id = 1
        self.objects = {}

    def update(self, detections):
        if not detections:
            self._mark_missing()
            return self._active_objects()

        unmatched_detection_indexes = set(range(len(detections)))
        unmatched_object_ids = set(self.objects.keys())

        pairs = []
        for object_id, tracked in self.objects.items():
            for index, detection in enumerate(detections):
                if tracked.label != detection.label:
                    continue
                distance = self._distance(tracked.bbox, detection.bbox)
                pairs.append((distance, object_id, index))

        for distance, object_id, index in sorted(pairs):
            if distance > self.max_distance:
                continue
            if object_id not in unmatched_object_ids or index not in unmatched_detection_indexes:
                continue

            self._update_object(object_id, detections[index])
            unmatched_object_ids.remove(object_id)
            unmatched_detection_indexes.remove(index)

        for object_id in unmatched_object_ids:
            self.objects[object_id].missing_frames += 1

        for index in unmatched_detection_indexes:
            self._register(detections[index])

        self._remove_lost_objects()
        return self._active_objects()

    def _register(self, detection):
        self.objects[self.next_id] = TrackedObject(
            object_id=self.next_id,
            label=detection.label,
            confidence=detection.confidence,
            bbox=detection.bbox,
            area_history=[self._area(detection.bbox)],
        )
        self.next_id += 1

    def _update_object(self, object_id, detection):
        tracked = self.objects[object_id]
        tracked.previous_area = tracked.area
        tracked.bbox = detection.bbox
        tracked.confidence = detection.confidence
        tracked.missing_frames = 0
        tracked.area_history.append(tracked.area)
        tracked.area_history = tracked.area_history[-8:]

    def _mark_missing(self):
        for tracked in self.objects.values():
            tracked.missing_frames += 1
        self._remove_lost_objects()

    def _remove_lost_objects(self):
        lost = [
            object_id
            for object_id, tracked in self.objects.items()
            if tracked.missing_frames > self.max_missing_frames
        ]
        for object_id in lost:
            del self.objects[object_id]

    def _active_objects(self):
        return [obj for obj in self.objects.values() if obj.missing_frames == 0]

    @staticmethod
    def _distance(bbox_a, bbox_b):
        ax1, ay1, ax2, ay2 = bbox_a
        bx1, by1, bx2, by2 = bbox_b
        acx, acy = (ax1 + ax2) / 2, (ay1 + ay2) / 2
        bcx, bcy = (bx1 + bx2) / 2, (by1 + by2) / 2
        return hypot(acx - bcx, acy - bcy)

    @staticmethod
    def _area(bbox):
        x1, y1, x2, y2 = bbox
        return max(0, x2 - x1) * max(0, y2 - y1)

