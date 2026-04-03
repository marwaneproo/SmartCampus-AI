from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.document_request import DocumentStatus


class DocumentRequestCreate(BaseModel):
    """Schema for creating a new document request"""
    student_id: int = Field(..., gt=0)
    document_type: str = Field(..., min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 123,
                "document_type": "transcript"
            }
        }


class DocumentRequestUpdate(BaseModel):
    """Schema for updating document request information"""
    document_type: Optional[str] = Field(None, min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "document_type": "certificate"
            }
        }


class DocumentRequestResponse(BaseModel):
    """Schema for document request response"""
    id: int
    student_id: int
    document_type: str
    status: DocumentStatus
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "student_id": 123,
                "document_type": "transcript",
                "status": "pending",
                "created_at": "2024-03-08T10:30:00"
            }
        }
