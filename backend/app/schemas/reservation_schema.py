from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.reservation import ReservationStatus


class ReservationCreate(BaseModel):
    """Schema for creating a new reservation"""
    room_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date format: YYYY-MM-DD")
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}:\d{2}$", description="Time format: HH:MM:SS")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}:\d{2}$", description="Time format: HH:MM:SS")
    purpose: str = Field(..., min_length=1, max_length=255)

    @field_validator("end_time")
    @classmethod
    def validate_time_range(cls, v, info):
        """Validate that end_time is after start_time"""
        if "start_time" in info.data:
            start = info.data["start_time"]
            if v <= start:
                raise ValueError("end_time must be after start_time")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "room_id": 1,
                "user_id": 123,
                "date": "2024-03-15",
                "start_time": "09:00:00",
                "end_time": "11:00:00",
                "purpose": "Team meeting"
            }
        }


class ReservationUpdate(BaseModel):
    """Schema for updating a reservation"""
    date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}:\d{2}$")
    end_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}:\d{2}$")
    purpose: Optional[str] = Field(None, min_length=1, max_length=255)

    class Config:
        json_schema_extra = {
            "example": {
                "purpose": "Updated purpose"
            }
        }


class ReservationResponse(BaseModel):
    """Schema for reservation response"""
    id: int
    room_id: int
    user_id: int
    date: str
    start_time: str
    end_time: str
    purpose: str
    status: ReservationStatus
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "room_id": 1,
                "user_id": 123,
                "date": "2024-03-15",
                "start_time": "09:00:00",
                "end_time": "11:00:00",
                "purpose": "Team meeting",
                "status": "pending",
                "created_at": "2024-03-08T10:30:00"
            }
        }
