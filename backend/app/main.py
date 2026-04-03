from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import (
    Room, Reservation, Exam, DocumentRequest
)
from app.routers import rooms, reservations, admin, exams, documents

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="EMSI ClassFlow API",
    description="Backend REST API for campus management platform",
    version="1.0.0",
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rooms.router)
app.include_router(reservations.router)
app.include_router(admin.router)
app.include_router(exams.router)
app.include_router(documents.router)


@app.get("/", tags=["root"])
async def root():
    """
    Welcome endpoint for the API.
    """
    return {
        "message": "Welcome to EMSI ClassFlow API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "message": "EMSI ClassFlow API is running"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the server with: uvicorn app.main:app --reload
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
