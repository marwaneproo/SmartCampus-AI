from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from datetime import datetime
from app.database import Base
import enum


class ReservationStatus(str, enum.Enum):
    """Reservation status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Reservation(Base):
    """
    Reservation model for booking rooms.
    
    Attributes:
        id: Unique identifier for the reservation
        room_id: ID of the reserved room (foreign key)
        user_id: ID of the user making the reservation
        date: Date of the reservation (YYYY-MM-DD)
        start_time: Start time of the reservation (HH:MM:SS)
        end_time: End time of the reservation (HH:MM:SS)
        purpose: Purpose of the reservation (e.g., "Class", "Meeting")
        status: Current status (pending, approved, rejected)
        created_at: Timestamp when reservation was created
    """
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    date = Column(String, nullable=False)  # Format: YYYY-MM-DD
    start_time = Column(String, nullable=False)  # Format: HH:MM:SS
    end_time = Column(String, nullable=False)  # Format: HH:MM:SS
    purpose = Column(String(255), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Reservation(id={self.id}, room_id={self.room_id}, user_id={self.user_id}, status={self.status})>"
