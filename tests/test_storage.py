
from datetime import datetime
from models import BloodPressure
from storage import BloodPressureStorage

class TestBloodPressureStorage:
    def setup_method(self):
        self.storage = BloodPressureStorage()

    def test_add_record(self):
        record = BloodPressure(1, 120, 80, datetime(2024, 1, 15))
        self.storage.add_record(record)

        records = self.storage.get_records_for_month(1, 2024)
        assert len(records) == 1
        assert records[1][0].systolic == 120
        assert records[1][0].diastolic == 80

    def test_get_records_for_month_empty(self):
        records = self.storage.get_records_for_month(1, 2024)
        assert len(records) == 0

    def test_get_records_for_month_multiple_users(self):
        record1 = BloodPressure(1, 120, 80, datetime(2024, 1, 15))
        record2 = BloodPressure(2, 130, 85, datetime(2024, 1, 16))

        self.storage.add_record(record1)
        self.storage.add_record(record2)

        records = self.storage.get_records_for_month(1, 2024)
        assert len(records) == 2
