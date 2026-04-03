from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reservation import Reservation, ReservationStatus
from app.schemas.reservation_schema import ReservationResponse

router = APIRouter(prefix="/admin/reservations", tags=["admin"])


@router.get("/pending", response_model=list[ReservationResponse])
async def get_pending_reservations(db: Session = Depends(get_db)):
    """
    Get all pending reservations.
    
    Returns:
        list: List of pending reservations
    """
    reservations = db.query(Reservation).filter(
        Reservation.status == ReservationStatus.PENDING
    ).all()
    return reservations


@router.put("/{reservation_id}/approve", response_model=ReservationResponse)
async def approve_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Approve a pending reservation.
    
    Args:
        reservation_id: ID of the reservation to approve
        
    Returns:
        ReservationResponse: Updated reservation details
        
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
    
    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve a {reservation.status} reservation. Only pending reservations can be approved."
        )
    
    reservation.status = ReservationStatus.APPROVED
    db.commit()
    db.refresh(reservation)
    return reservation


@router.put("/{reservation_id}/reject", response_model=ReservationResponse)
async def reject_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    """
    Reject a pending reservation.
    
    Args:
        reservation_id: ID of the reservation to reject
        
    Returns:
        ReservationResponse: Updated reservation details
        
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
    
    if reservation.status != ReservationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject a {reservation.status} reservation. Only pending reservations can be rejected."
        )
    
    reservation.status = ReservationStatus.REJECTED
    db.commit()
    db.refresh(reservation)
    return reservation
