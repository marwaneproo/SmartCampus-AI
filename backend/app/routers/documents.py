from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document_request import DocumentRequest, DocumentStatus
from app.schemas.document_schema import DocumentRequestCreate, DocumentRequestUpdate, DocumentRequestResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_document_request(
    request: DocumentRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new document request.
    
    Args:
        request: Document request creation data
        
    Returns:
        DocumentRequestResponse: Created request details
    """
    db_request = DocumentRequest(
        **request.model_dump(),
        status=DocumentStatus.PENDING
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("", response_model=list[DocumentRequestResponse])
async def list_document_requests(
    status: DocumentStatus = None,
    db: Session = Depends(get_db)
):
    """
    Get all document requests with optional filtering by status.
    
    Args:
        status: Filter by status (optional)
        
    Returns:
        list: List of document requests
    """
    query = db.query(DocumentRequest)
    
    if status:
        query = query.filter(DocumentRequest.status == status)
    
    return query.all()


@router.get("/{request_id}", response_model=DocumentRequestResponse)
async def get_document_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific document request by ID.
    
    Args:
        request_id: ID of the document request
        
    Returns:
        DocumentRequestResponse: Request details
        
    Raises:
        HTTPException: 404 if request not found
    """
    request = db.query(DocumentRequest).filter(DocumentRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document request with id {request_id} not found"
        )
    return request


@router.get("/student/{student_id}", response_model=list[DocumentRequestResponse])
async def get_student_document_requests(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all document requests for a specific student.
    
    Args:
        student_id: ID of the student
        
    Returns:
        list: List of document requests for the student
    """
    requests = db.query(DocumentRequest).filter(
        DocumentRequest.student_id == student_id
    ).all()
    return requests


@router.put("/{request_id}", response_model=DocumentRequestResponse)
async def update_document_request(
    request_id: int,
    request_update: DocumentRequestUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a document request. Only pending requests can be updated.
    
    Args:
        request_id: ID of the document request to update
        request_update: Updated request data
        
    Returns:
        DocumentRequestResponse: Updated request details
        
    Raises:
        HTTPException: 404 if request not found
        HTTPException: 400 if request is not pending
    """
    request = db.query(DocumentRequest).filter(DocumentRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document request with id {request_id} not found"
        )
    
    # Only allow updating pending requests
    if request.status != DocumentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update a {request.status} request"
        )
    
    update_data = request_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(request, key, value)
    
    db.commit()
    db.refresh(request)
    return request


@router.put("/{request_id}/approve", response_model=DocumentRequestResponse)
async def approve_document_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Approve a pending document request.
    
    Args:
        request_id: ID of the document request to approve
        
    Returns:
        DocumentRequestResponse: Updated request details
        
    Raises:
        HTTPException: 404 if request not found
        HTTPException: 400 if request is not pending
    """
    request = db.query(DocumentRequest).filter(DocumentRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document request with id {request_id} not found"
        )
    
    if request.status != DocumentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot approve a {request.status} request. Only pending requests can be approved."
        )
    
    request.status = DocumentStatus.APPROVED
    db.commit()
    db.refresh(request)
    return request


@router.put("/{request_id}/reject", response_model=DocumentRequestResponse)
async def reject_document_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Reject a pending document request.
    
    Args:
        request_id: ID of the document request to reject
        
    Returns:
        DocumentRequestResponse: Updated request details
        
    Raises:
        HTTPException: 404 if request not found
        HTTPException: 400 if request is not pending
    """
    request = db.query(DocumentRequest).filter(DocumentRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document request with id {request_id} not found"
        )
    
    if request.status != DocumentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot reject a {request.status} request. Only pending requests can be rejected."
        )
    
    request.status = DocumentStatus.REJECTED
    db.commit()
    db.refresh(request)
    return request


@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a document request. Only pending requests can be deleted.
    
    Args:
        request_id: ID of the document request to delete
        
    Raises:
        HTTPException: 404 if request not found
        HTTPException: 400 if request is not pending
    """
    request = db.query(DocumentRequest).filter(DocumentRequest.id == request_id).first()
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document request with id {request_id} not found"
        )
    
    if request.status != DocumentStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete a {request.status} request"
        )
    
    db.delete(request)
    db.commit()
