from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum


class RoomType(str, enum.Enum):
    """Room type enumeration"""
    CLASSROOM = "classroom"
    LAB = "lab"
    AMPHITHEATER = "amphitheater"


class Room(Base):
    """
    Room model representing physical spaces in the campus.
    
    Attributes:
        id: Unique identifier for the room
        name: Room name/identifier (e.g., "A101", "Lab-2")
        capacity: Maximum number of occupants
        floor: Floor number where the room is located
        type: Type of room (classroom, lab, amphitheater)
    """
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    type = Column(Enum(RoomType), nullable=False)

    def __repr__(self):
        return f"<Room(id={self.id}, name={self.name}, capacity={self.capacity}, type={self.type})>"
