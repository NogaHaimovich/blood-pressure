import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from controller import BloodPressureController
from models import BloodPressure
from schemas import BloodPressureCreate, MonthlyUserReport


class TestBloodPressureController:
    def setup_method(self):
        mock_service = Mock()
        self.controller = BloodPressureController(mock_service)

    def test_add_blood_pressure_success(self):
        bp_data = BloodPressureCreate(
            systolic=120,
            diastolic=80,
            timestamp=datetime.now()
        )

        with patch.object(self.controller.service, 'add_bp_record') as mock_add:
            mock_record = BloodPressure(1, 120, 80, datetime.now())
            mock_add.return_value = mock_record

            result = self.controller.add_blood_pressure(1, bp_data)

            assert result.message == "Blood pressure record added successfully"
            mock_add.assert_called_once_with(1, bp_data)

    def test_add_blood_pressure_invalid_user_id(self):
        bp_data = BloodPressureCreate(
            systolic=120,
            diastolic=80,
            timestamp=datetime.now()
        )

        with pytest.raises(Exception) as exc_info:
            self.controller.add_blood_pressure(0, bp_data)
        assert "User ID must be a positive integer" in str(exc_info.value)

    def test_get_monthly_report_success(self):
        mock_reports = [
            MonthlyUserReport(
                user_id=1,
                measurements_count=5,
                average_systolic=125.0,
                average_diastolic=82.0,
                systolic_std=5.0,
                diastolic_std=3.0,
                pulse_pressure_avg=43.0,
                high_records_count=1,
                low_records_count=0
            )
        ]

        with patch.object(self.controller.service, 'calc_data_for_month_report') as mock_calc:
            mock_calc.return_value = mock_reports

            result = self.controller.get_monthly_report(2024, 1)

            assert len(result) == 1
            assert result[0].user_id == 1

