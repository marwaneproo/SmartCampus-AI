from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.exam import Exam
from app.models.room import Room
from app.schemas.exam_schema import ExamCreate, ExamUpdate, ExamResponse

router = APIRouter(prefix="/exams", tags=["exams"])


@router.post("", response_model=ExamResponse, status_code=status.HTTP_201_CREATED)
async def create_exam(
    exam: ExamCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new exam record.
    
    Args:
        exam: Exam creation data
        
    Returns:
        ExamResponse: Created exam details
        
    Raises:
        HTTPException: 404 if room not found
    """
    # Check if room exists
    room = db.query(Room).filter(Room.id == exam.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {exam.room_id} not found"
        )
    
    db_exam = Exam(**exam.model_dump())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


@router.get("", response_model=list[ExamResponse])
async def list_exams(db: Session = Depends(get_db)):
    """
    Get all exams.
    
    Returns:
        list: List of all exams
    """
    exams = db.query(Exam).all()
    return exams


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific exam by ID.
    
    Args:
        exam_id: ID of the exam
        
    Returns:
        ExamResponse: Exam details
        
    Raises:
        HTTPException: 404 if exam not found
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    return exam


@router.get("/student/{student_id}", response_model=list[ExamResponse])
async def get_student_exams(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all exams for a specific student.
    
    Args:
        student_id: ID of the student
        
    Returns:
        list: List of exams for the student
    """
    exams = db.query(Exam).filter(Exam.student_id == student_id).all()
    return exams


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: int,
    exam_update: ExamUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an exam record.
    
    Args:
        exam_id: ID of the exam to update
        exam_update: Updated exam data
        
    Returns:
        ExamResponse: Updated exam details
        
    Raises:
        HTTPException: 404 if exam not found
        HTTPException: 404 if new room not found
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    # If room_id is being updated, verify the room exists
    update_data = exam_update.model_dump(exclude_unset=True)
    if "room_id" in update_data:
        room = db.query(Room).filter(Room.id == update_data["room_id"]).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Room with id {update_data['room_id']} not found"
            )
    
    for key, value in update_data.items():
        setattr(exam, key, value)
    
    db.commit()
    db.refresh(exam)
    return exam


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam(
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an exam record.
    
    Args:
        exam_id: ID of the exam to delete
        
    Raises:
        HTTPException: 404 if exam not found
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exam with id {exam_id} not found"
        )
    
    db.delete(exam)
    db.commit()
