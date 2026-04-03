from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.models.room import Room
from app.schemas.reservation_schema import ReservationCreate, ReservationUpdate, ReservationResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])


def check_room_availability(
    room_id: int,
    date: str,
    start_time: str,
    end_time: str,
    db: Session,
    exclude_reservation_id: int = None
) -> bool:
    """
    Check if a room is available for the given time slot.
    
    Args:
        room_id: ID of the room
        date: Date of reservation (YYYY-MM-DD)
        start_time: Start time (HH:MM:SS)
        end_time: End time (HH:MM:SS)
        db: Database session
        exclude_reservation_id: ID of reservation to exclude (for updates)
        
    Returns:
        bool: True if room is available, False otherwise
    """
    query = db.query(Reservation).filter(
        Reservation.room_id == room_id,
        Reservation.date == date,
        Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.APPROVED])
    )
    
    if exclude_reservation_id:
        query = query.filter(Reservation.id != exclude_reservation_id)
    
    conflicting_reservations = query.all()
    
    for res in conflicting_reservations:
        # Check if time slots overlap
        if not (end_time <= res.start_time or start_time >= res.end_time):
            return False
    
    return True


@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new reservation for a room.
    
    Args:
        reservation: Reservation creation data
        
    Returns:
        ReservationResponse: Created reservation details
        
    Raises:
        HTTPException: 404 if room not found
        HTTPException: 409 if room is not available for the time slot
    """
    # Check if room exists
    room = db.query(Room).filter(Room.id == reservation.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {reservation.room_id} not found"
        )
    
    # Check room availability
    if not check_room_availability(
        reservation.room_id,
        reservation.date,
        reservation.start_time,
        reservation.end_time,
        db
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Room is not available for the requested time slot"
        )
    
    # Create reservation with pending status
    db_reservation = Reservation(
        **reservation.model_dump(),
        status=ReservationStatus.PENDING
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.get("", response_model=list[ReservationResponse])
async def list_reservations(
    user_id: int = None,
    status: ReservationStatus = None,
    db: Session = Depends(get_db)
):
    """
    Get all reservations with optional filtering.
    
    Args:
        user_id: Filter by user ID (optional)
        status: Filter by status (optional)
        
    Returns:
        list: List of reservations
    """
    query = db.query(Reservation)
    
    if user_id:
        query = query.filter(Reservation.user_id == user_id)
    
    if status:
        query = query.filter(Reservation.status == status)
    
    return query.all()


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific reservation by ID.
    
    Args:
        reservation_id: ID of the reservation
        
    Returns:
        ReservationResponse: Reservation details
        
    Raises:
        HTTPException: 404 if reservation not found
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    return reservation


@router.put("/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: int,
    reservation_update: ReservationUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a reservation. Only pending reservations can be updated.
    
    Args:
        reservation_id: ID of the reservation to update
        reservation_update: Updated reservation data
        
    Returns:
        ReservationResponse: Updated reservation details
        
    Raises:
        HTTPException: 404 if reservation not found
        HTTPException: 400 if reservation is not pending
        HTTPException: 409 if new time slot is not available
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    
    # Only allow updating pending reservations
    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update a {reservation.status} reservation"
        )
    
    # If date or time is being updated, check availability
    update_data = reservation_update.model_dump(exclude_unset=True)
    if any(key in update_data for key in ["date", "start_time", "end_time"]):
        new_date = update_data.get("date", reservation.date)
        new_start_time = update_data.get("start_time", reservation.start_time)
        new_end_time = update_data.get("end_time", reservation.end_time)
        
        if not check_room_availability(
            reservation.room_id,
            new_date,
            new_start_time,
            new_end_time,
            db,
            exclude_reservation_id=reservation_id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Room is not available for the requested time slot"
            )
    
    # Update reservation
    for key, value in update_data.items():
        setattr(reservation, key, value)
    
    db.commit()
    db.refresh(reservation)
    return reservation


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a reservation. Only pending reservations can be deleted.
    
    Args:
        reservation_id: ID of the reservation to delete
        
    Raises:
        HTTPException: 404 if reservation not found
        HTTPException: 400 if reservation is not pending
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with id {reservation_id} not found"
        )
    
    # Only allow deleting pending reservations
    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete a {reservation.status} reservation"
        )
    
    db.delete(reservation)
    db.commit()
