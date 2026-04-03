# EMSI ClassFlow Backend API

A comprehensive REST API for campus management built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**.

## Features

- **Room Management**: Create, read, and manage campus rooms with capacity and type information
- **Reservation System**: Book rooms with conflict detection and availability checking
- **Exam Management**: Schedule and track student exams
- **Document Requests**: Handle student document requests with approval workflow
- **Admin Dashboard**: Approve or reject pending reservations

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and session management
├── models/                 # SQLAlchemy ORM models
│   ├── room.py            # Room model
│   ├── reservation.py      # Reservation model
│   ├── exam.py            # Exam model
│   ├
│   ├── document_request.py # Document request model
│   └── __init__.py
├── schemas/               # Pydantic validation schemas
│   ├── room_schema.py
│   ├── reservation_schema.py
│   ├── exam_schema.py
│   ├
│   ├── document_schema.py
│   └── __init__.py
└── routers/              # API endpoint implementations
    ├── rooms.py          # /rooms endpoints
    ├── reservations.py   # /reservations endpoints
    ├── admin.py          # /admin/reservations endpoints
    ├── exams.py          # /exams endpoints
    ├
    ├── documents.py      # /documents endpoints
    └── __init__.py
```

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip or conda

## Installation

### 1. Clone the Repository
```bash
cd EmsiClassFlowBackEnd
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a `.env` file in the project root with your PostgreSQL credentials:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/emsi_classflow
```

Or update the `DATABASE_URL` directly in [app/database.py](app/database.py):
```python
DATABASE_URL = "postgresql://user:password@localhost:5432/emsi_classflow"
```

### 5. Create Database
```bash
# First, create the database in PostgreSQL
createdb emsi_classflow
```

## Running the Server

Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Rooms
```
GET    /rooms              - Get all rooms
GET    /rooms/{id}         - Get a specific room
```

### Reservations
```
POST   /reservations       - Create a reservation
GET    /reservations       - Get all reservations (optional filters: user_id, status)
GET    /reservations/{id}  - Get a specific reservation
PUT    /reservations/{id}  - Update a reservation
DELETE /reservations/{id}  - Delete a reservation
```

### Admin Reservation Management
```
GET    /admin/reservations/pending        - Get pending reservations
PUT    /admin/reservations/{id}/approve   - Approve a reservation
PUT    /admin/reservations/{id}/reject    - Reject a reservation
```

### Exams
```
GET    /exams              - Get all exams
GET    /exams/{id}         - Get a specific exam
GET    /exams/student/{student_id} - Get exams for a student
POST   /exams              - Create an exam
PUT    /exams/{id}         - Update an exam
DELETE /exams/{id}         - Delete an exam
```

### Documents
```
POST   /documents              - Request a document
GET    /documents              - Get all document requests (optional filter: status)
GET    /documents/{id}         - Get a specific request
GET    /documents/student/{student_id} - Get requests by student
PUT    /documents/{id}         - Update a request
PUT    /documents/{id}/approve - Approve a request
PUT    /documents/{id}/reject  - Reject a request
DELETE /documents/{id}         - Delete a request
```

## Database Models

### Room
- `id`: Primary key
- `name`: Unique room identifier (e.g., "A101")
- `capacity`: Maximum occupancy
- `floor`: Floor number
- `type`: Enum (classroom, lab, amphitheater)

### Reservation
- `id`: Primary key
- `room_id`: Foreign key to Room
- `user_id`: User making the reservation
- `date`: YYYY-MM-DD format
- `start_time`: HH:MM:SS format
- `end_time`: HH:MM:SS format
- `purpose`: Reason for reservation
- `status`: Enum (pending, approved, rejected)
- `created_at`: Timestamp

### Exam
- `id`: Primary key
- `subject`: Subject being examined
- `room_id`: Foreign key to Room
- `date`: YYYY-MM-DD format
- `time`: HH:MM:SS format
- `student_id`: Student taking the exam
- `table_number`: Seating assignment


### DocumentRequest
- `id`: Primary key
- `student_id`: Requesting student
- `document_type`: Type of document
- `status`: Enum (pending, approved, rejected)
- `created_at`: Timestamp