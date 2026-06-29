import cv2


COLORS = {
    "car": (0, 180, 255),
    "bus": (255, 100, 0),
    "truck": (0, 120, 255),
    "motorcycle": (255, 0, 180),
    "bicycle": (50, 220, 50),
}


def draw_tracked_object(frame, obj):
    x1, y1, x2, y2 = obj.bbox
    color = COLORS.get(obj.label, (0, 255, 0))
    text = f"#{obj.object_id} {obj.label} {obj.confidence:.2f}"

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        frame,
        text,
        (x1, max(20, y1 - 8)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )

