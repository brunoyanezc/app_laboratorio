from dataclasses import dataclass


@dataclass
class Peak:
    compound: str
    area: float
    ppm: float


@dataclass
class Sample:
    sample_id: str
    total_peak_response: float
    area_c23: float | None
    peaks: list[Peak]
