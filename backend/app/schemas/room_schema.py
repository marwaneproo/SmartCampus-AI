from pydantic import BaseModel, Field
from typing import Optional
from app.models.room import RoomType


class RoomCreate(BaseModel):
    """Schema for creating a new room"""
    name: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., gt=0, description="Room capacity must be greater than 0")
    floor: int = Field(..., ge=0, description="Floor number must be non-negative")
    type: RoomType

    class Config:
        json_schema_extra = {
            "example": {
                "name": "A101",
                "capacity": 30,
                "floor": 1,
                "type": "classroom"
            }
        }


class RoomUpdate(BaseModel):
    """Schema for updating room information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    capacity: Optional[int] = Field(None, gt=0)
    floor: Optional[int] = Field(None, ge=0)
    type: Optional[RoomType] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "A101",
                "capacity": 35
            }
        }


class RoomResponse(BaseModel):
    """Schema for room response"""
    id: int
    name: str
    capacity: int
    floor: int
    type: RoomType

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "A101",
                "capacity": 30,
                "floor": 1,
                "type": "classroom"
            }
        }
