from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    confidence_threshold: float = 0.45
    approach_growth_ratio: float = 1.22
    danger_area_ratio: float = 0.18
    voice_cooldown_seconds: float = 2.5
    repeated_object_cooldown_seconds: float = 7.0

    vehicle_classes: tuple[str, ...] = (
        "car",
        "bus",
        "truck",
        "motorcycle",
        "bicycle",
    )

