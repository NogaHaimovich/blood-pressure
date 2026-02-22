from unittest.mock import patch

import pytest

from bp_service import BloodPressureService
from models import BloodPressure
from datetime import datetime

from schemas import BloodPressureCreate


class TestBloodPressureService:
    def setup_method(self):
        self.service = BloodPressureService()


    def test_calculate_user_stats(self):
        records = [
            BloodPressure(1, 120, 80, datetime.now()),
            BloodPressure(1, 130, 85, datetime.now()),
            BloodPressure(1, 145, 95, datetime.now())
        ]
        stats = self.service._calculate_user_stats(records)

        assert pytest.approx(stats["average_systolic"], rel=1e-2) == 131.67
        assert pytest.approx(stats["average_diastolic"], rel=1e-2) == 86.67
        assert stats["high_readings_count"] == 1
        assert stats["low_readings_count"] == 0
        assert "pulse_pressure_avg" in stats

    @patch('storage.storage.add_record')
    def test_add_bp_record(self, mock_add_record):
        bp_create = BloodPressureCreate(
            systolic=120,
            diastolic=80,
            timestamp=datetime.now()
        )
        result = self.service.add_bp_record(1, bp_create)

        assert result.user_id == 1
        assert result.systolic == 120
        assert result.diastolic == 80
        mock_add_record.assert_called_once()
