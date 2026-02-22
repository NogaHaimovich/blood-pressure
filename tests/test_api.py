from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from schemas import StatusResponse

class TestAPI:
    def setup_method(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Blood Pressure Service is running"}

    def test_add_bp_endpoint_success(self):
        bp_data = {
            "systolic": 120,
            "diastolic": 80,
            "timestamp": "2024-01-15T10:00:00"
        }

        with patch('main.bp_controller.add_blood_pressure') as mock_add:
            mock_response = StatusResponse(
                status="success",
                message="Blood pressure record added successfully"
            )
            mock_add.return_value = mock_response

            response = self.client.post("/users/1/blood-pressure", json=bp_data)
            assert response.status_code == 200
            assert response.json() == {
                "status": "success",
                "message": "Blood pressure record added successfully"
            }

    def test_add_bp_endpoint_invalid_data(self):
        bp_data = {
            "systolic": 80,  # Invalid: systolic <= diastolic
            "diastolic": 120,
            "timestamp": "2024-01-15T10:00:00"
        }

        response = self.client.post("/users/1/blood-pressure", json=bp_data)
        assert response.status_code == 422

    def test_monthly_report_endpoint_success(self):
        with patch('main.bp_controller.get_monthly_report') as mock_report:
            mock_report.return_value = []

            response = self.client.get("/reports/monthly?year=2024&month=1")
            assert response.status_code == 200

    def test_monthly_report_future_date(self):
        response = self.client.get("/reports/monthly?year=2030&month=1")
        assert response.status_code == 400
        assert "Cannot request reports for future dates" in response.json()["detail"]

    def test_monthly_report_invalid_month(self):
        response = self.client.get("/reports/monthly?year=2024&month=13")
        assert response.status_code == 422
