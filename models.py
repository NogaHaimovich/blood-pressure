from dataclasses import dataclass
from datetime import datetime


@dataclass
class BloodPressure:
    user_id: int
    systolic: int
    diastolic: int
    timestamp: datetime