from typing import List, Dict
from collections import defaultdict
from models import BloodPressure

class BloodPressureStorage:
    def __init__(self):
        self._records: Dict[str, Dict[int, List[BloodPressure]]] = defaultdict(lambda: defaultdict(list))

    def add_record(self, reading: BloodPressure) -> None:
        year_month = f"{reading.timestamp.year}-{reading.timestamp.month:02d}"
        self._records[year_month][reading.user_id].append(reading)

    def get_records_for_month(self, year: int, month: int) -> Dict[int, List[BloodPressure]]:
        year_month = f"{year}-{month:02d}"
        return self._records[year_month]

storage = BloodPressureStorage()