from src.alerts import AlertEngine
from src.config import AppConfig
from src.models import Detection
from src.tracker import CentroidTracker


def test_tracker_keeps_same_id_for_nearby_vehicle():
    tracker = CentroidTracker(max_distance=80)

    first = tracker.update([Detection("car", 0.9, (100, 100, 200, 200))])
    second = tracker.update([Detection("car", 0.9, (110, 108, 210, 208))])

    assert len(first) == 1
    assert len(second) == 1
    assert first[0].object_id == second[0].object_id


def test_alert_engine_detects_approaching_center_vehicle():
    config = AppConfig(approach_growth_ratio=1.10)
    tracker = CentroidTracker(max_distance=120)
    alerts = AlertEngine(config)

    tracker.update([Detection("car", 0.9, (260, 190, 360, 290))])
    objects = tracker.update([Detection("car", 0.9, (235, 165, 385, 315))])

    messages = alerts.evaluate(objects, (480, 640, 3))

    assert any("en approche" in message for message in messages)
