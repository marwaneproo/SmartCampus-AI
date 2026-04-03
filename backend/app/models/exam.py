from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Exam(Base):
    """
    Exam model for managing student examinations.
    
    Attributes:
        id: Unique identifier for the exam
        subject: Subject being examined (e.g., "Mathematics", "Physics")
        room_id: ID of the room where exam takes place (foreign key)
        date: Date of the exam (YYYY-MM-DD)
        time: Time of the exam (HH:MM:SS)
        student_id: ID of the student taking the exam
        table_number: Assigned seating table number for the student
    """
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(100), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False, index=True)
    date = Column(String, nullable=False)  # Format: YYYY-MM-DD
    time = Column(String, nullable=False)  # Format: HH:MM:SS
    student_id = Column(Integer, nullable=False, index=True)
    table_number = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Exam(id={self.id}, subject={self.subject}, student_id={self.student_id}, date={self.date})>"