from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.room import Room
from app.schemas.room_schema import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomResponse])
async def list_rooms(db: Session = Depends(get_db)):
    """
    Get all rooms in the campus.
    
    Returns:
        list: List of all rooms
    """
    rooms = db.query(Room).all()
    return rooms


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: Session = Depends(get_db)):
    """
    Get a specific room by ID.
    
    Args:
        room_id: ID of the room
        
    Returns:
        RoomResponse: Room details
        
    Raises:
        HTTPException: 404 if room not found
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )
    return room


@router.post("", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    Create a new room.
    
    Args:
        room: Room creation data
        
    Returns:
        RoomResponse: Created room details
        
    Raises:
        HTTPException: 400 if room name already exists
    """
    # Check if room with same name already exists
    existing_room = db.query(Room).filter(Room.name == room.name).first()
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Room with name '{room.name}' already exists"
        )
    
    db_room = Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int, db: Session = Depends(get_db)):
    """
    Delete a room by ID.
    
    Args:
        room_id: ID of the room to delete
        
    Raises:
        HTTPException: 404 if room not found
        HTTPException: 409 if room has active reservations
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {room_id} not found"
        )
    
    # Check if room has any pending or approved reservations
    from app.models.reservation import Reservation, ReservationStatus
    active_reservations = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.APPROVED])
    ).count()
    
    if active_reservations > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete room with active reservations"
        )
    
    db.delete(room)
    db.commit()
