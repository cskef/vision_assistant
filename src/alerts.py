import time


LABELS_FR = {
    "car": "voiture",
    "bus": "bus",
    "truck": "camion",
    "motorcycle": "moto",
    "bicycle": "velo",
}


class AlertEngine:
    def __init__(self, config):
        self.config = config
        self.last_message_by_object = {}

    def evaluate(self, tracked_objects, frame_shape):
        height, width = frame_shape[:2]
        messages = []

        for obj in tracked_objects:
            label = LABELS_FR.get(obj.label, obj.label)
            position = self._horizontal_position(obj.bbox, width)
            close = self._is_close(obj.bbox, width, height)
            approaching = self._is_approaching(obj)

            if approaching and position == "centre":
                message = f"Attention, {label} en approche devant vous"
            elif close:
                message = f"{label.capitalize()} proche a {position}"
            else:
                message = f"{label.capitalize()} a {position}"

            if self._can_repeat(obj.object_id, message):
                messages.append(message)

        return messages

    def _can_repeat(self, object_id, message):
        now = time.time()
        previous = self.last_message_by_object.get(object_id)
        if previous is None:
            self.last_message_by_object[object_id] = (message, now)
            return True

        previous_message, previous_time = previous
        if message != previous_message:
            self.last_message_by_object[object_id] = (message, now)
            return True

        if now - previous_time >= self.config.repeated_object_cooldown_seconds:
            self.last_message_by_object[object_id] = (message, now)
            return True

        return False

    @staticmethod
    def _horizontal_position(bbox, frame_width):
        x1, _, x2, _ = bbox
        center_x = (x1 + x2) / 2
        if center_x < frame_width * 0.35:
            return "gauche"
        if center_x > frame_width * 0.65:
            return "droite"
        return "centre"

    def _is_close(self, bbox, frame_width, frame_height):
        x1, y1, x2, y2 = bbox
        object_area = max(0, x2 - x1) * max(0, y2 - y1)
        frame_area = frame_width * frame_height
        return object_area / frame_area >= self.config.danger_area_ratio

    def _is_approaching(self, obj):
        if obj.previous_area is None or obj.previous_area <= 0:
            return False
        return obj.area / obj.previous_area >= self.config.approach_growth_ratio

