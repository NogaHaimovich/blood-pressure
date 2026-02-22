import pytest
from datetime import datetime
from schemas import BloodPressureCreate



class TestSchemas:
    def test_blood_pressure_create_valid(self):
        bp = BloodPressureCreate(
            systolic=120,
            diastolic=80,
            timestamp=datetime.now()
        )
        assert bp.systolic == 120
        assert bp.diastolic == 80

    def test_blood_pressure_create_invalid_systolic_diastolic(self):
        with pytest.raises(ValueError) as exc_info:
            BloodPressureCreate(
                systolic=80,
                diastolic=120,
                timestamp=datetime.now()
            )
        assert "must be greater than" in str(exc_info.value)

    def test_blood_pressure_create_out_of_range(self):
        with pytest.raises(ValueError):
            BloodPressureCreate(
                systolic=400,  # Too high
                diastolic=80,
                timestamp=datetime.now()
            )