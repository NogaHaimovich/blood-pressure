import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends
from typing import Annotated, List

from logging_config import setup_logging
from controller import BloodPressureController
from bp_service import BloodPressureService
from schemas import BloodPressureCreate, StatusResponse, MonthlyUserReport

setup_logging(log_level="INFO", log_file="logs/bp_app.log")
logger = logging.getLogger(__name__)

bp_service = BloodPressureService()
bp_controller = BloodPressureController(bp_service)


def get_bp_controller() -> BloodPressureController:
    return bp_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Blood Pressure Service starting up")
    yield
    logger.info("Blood Pressure Service shutting down")

app = FastAPI(
    title="Blood Pressure Reporting Service",
    description="API for recording and reporting blood pressure measurements",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    logger.info("Health check endpoint accessed")
    return {"message": "Blood Pressure Service is running"}


@app.post("/users/{user_id}/blood-pressure", response_model=StatusResponse)
def add_bp(
    user_id: int,
    bp: BloodPressureCreate,
    controller: BloodPressureController = Depends(get_bp_controller)
):
    logger.info(f"Adding BP for user {user_id}")
    return controller.add_blood_pressure(user_id, bp)


@app.get("/reports/monthly", response_model=List[MonthlyUserReport])
def get_monthly_report(
    year: Annotated[int, Query(ge=1900, le=2100)],
    month: Annotated[int, Query(ge=1, le=12)],
    controller: BloodPressureController = Depends(get_bp_controller)
):
    return controller.get_monthly_report(year, month)


