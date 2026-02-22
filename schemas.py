from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class BloodPressureCreate(BaseModel):
    systolic: int = Field(..., gt=0, le=300, description="Systolic pressure value (mmHg)")
    diastolic: int = Field(..., gt=0, le=200, description="Diastolic pressure value (mmHg)")
    timestamp: datetime

    @model_validator(mode='after')
    def validate_systolic_greater_than_diastolic(self):
        if self.systolic <= self.diastolic:
            raise ValueError(
                f"Systolic pressure ({self.systolic}) must be greater than "
                f"diastolic pressure ({self.diastolic})"
            )
        return self


class StatusResponse(BaseModel):
    status: str = Field(default="success", description="Operation status")
    message: str = Field(default="Blood pressure record added successfully", description="Status message")


class MonthlyUserReport(BaseModel):
    user_id: int
    measurements_count: int

    average_systolic: float
    average_diastolic: float
    systolic_std: float
    diastolic_std: float

    pulse_pressure_avg: float  # systolic  - diastolic
    high_readings_count: int  #  > 140/90
    low_readings_count: int  #  < 100/60
