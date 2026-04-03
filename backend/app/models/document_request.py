from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.database import Base
import enum


class DocumentStatus(str, enum.Enum):
    """Document request status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class DocumentRequest(Base):
    """
    DocumentRequest model for managing student document requests.
    Students can request documents like transcripts, certificates, etc.
    
    Attributes:
        id: Unique identifier for the document request
        student_id: ID of the student requesting the document
        document_type: Type of document requested (e.g., "transcript", "certificate")
        status: Current status (pending, approved, rejected)
        created_at: Timestamp when request was created
    """
    __tablename__ = "document_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False, index=True)
    document_type = Column(String(100), nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<DocumentRequest(id={self.id}, student_id={self.student_id}, document_type={self.document_type}, status={self.status})>"
