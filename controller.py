import logging
from datetime import datetime
from fastapi import HTTPException, status
from typing import List
from bp_service import BloodPressureService
from schemas import BloodPressureCreate, StatusResponse, MonthlyUserReport

logger = logging.getLogger(__name__)

class BloodPressureController:
    def __init__(self, service: BloodPressureService):
        self.service = service

    def add_blood_pressure(self, user_id: int, bp_data: BloodPressureCreate) -> StatusResponse:
        logger.info(f"Request to add BP for user {user_id}")

        if user_id <= 0:
            logger.warning(f"Invalid user ID provided: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID must be a positive integer"
            )

        try:
            self.service.add_bp_record(user_id, bp_data)
            logger.info(f"Successfully added BP reading for user {user_id}")
            return StatusResponse(
                status="success",
                message="Blood pressure record added successfully"
            )
        except ValueError as e:
            logger.error(f"Validation error for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error adding BP for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_monthly_report(self, year: int, month: int) -> List[MonthlyUserReport]:
        logger.info(f"Request for monthly report: {year}-{month:02d}")

        current_date = datetime.now()
        if year > current_date.year or (year == current_date.year and month > current_date.month):
            logger.warning(f"Future date requested: {year}-{month:02d}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot request reports for future dates"
            )

        try:
            reports = self.service.calc_data_for_month_report(month, year)
            logger.info(f"Successfully generated monthly report with {len(reports)} entries")
            return reports
        except ValueError as e:
            logger.error(f"Validation error for monthly report {year}-{month:02d}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error generating monthly report {year}-{month:02d}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )