from pydantic import BaseModel, Field
from typing import Optional


class ExamCreate(BaseModel):
    """Schema for creating a new exam"""
    subject: str = Field(..., min_length=1, max_length=100)
    room_id: int = Field(..., gt=0)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="Date format: YYYY-MM-DD")
    time: str = Field(..., pattern=r"^\d{2}:\d{2}:\d{2}$", description="Time format: HH:MM:SS")
    student_id: int = Field(..., gt=0)
    table_number: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Mathematics",
                "room_id": 1,
                "date": "2024-04-20",
                "time": "09:00:00",
                "student_id": 456,
                "table_number": 5
            }
        }


class ExamUpdate(BaseModel):
    """Schema for updating exam information"""
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    room_id: Optional[int] = Field(None, gt=0)
    date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}:\d{2}$")
    student_id: Optional[int] = Field(None, gt=0)
    table_number: Optional[int] = Field(None, gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "table_number": 10
            }
        }


class ExamResponse(BaseModel):
    """Schema for exam response"""
    id: int
    subject: str
    room_id: int
    date: str
    time: str
    student_id: int
    table_number: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "subject": "Mathematics",
                "room_id": 1,
                "date": "2024-04-20",
                "time": "09:00:00",
                "student_id": 456,
                "table_number": 5
            }
        }
