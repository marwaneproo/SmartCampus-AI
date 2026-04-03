# API Documentation and Examples

## Base URL
```
http://localhost:8000
```

## Authentication
Not implemented yet (to be added by another developer)

---

## 1. ROOMS ENDPOINTS

### 1.1 Get All Rooms
```http
GET /rooms
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "A101",
    "capacity": 30,
    "floor": 1,
    "type": "classroom"
  },
  {
    "id": 2,
    "name": "Lab-2",
    "capacity": 20,
    "floor": 2,
    "type": "lab"
  }
]
```

### 1.2 Get Room by ID
```http
GET /rooms/1
```

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "A101",
  "capacity": 30,
  "floor": 1,
  "type": "classroom"
}
```

**Response** (404 Not Found):
```json
{
  "detail": "Room with id 999 not found"
}
```

### 1.3 Create Room
```http
POST /rooms
Content-Type: application/json

{
  "name": "A101",
  "capacity": 30,
  "floor": 1,
  "type": "classroom"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "name": "A101",
  "capacity": 30,
  "floor": 1,
  "type": "classroom"
}
```

**Response** (400 Bad Request):
```json
{
  "detail": "Room with name 'A101' already exists"
}
```

### 1.4 Delete Room
```http
DELETE /rooms/1
```

**Response** (204 No Content):
(Empty body)

**Response** (409 Conflict):
```json
{
  "detail": "Cannot delete room with active reservations"
}
```

---

## 2. RESERVATIONS ENDPOINTS

### 2.1 Create Reservation
```http
POST /reservations
Content-Type: application/json

{
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "purpose": "Team meeting"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "purpose": "Team meeting",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

**Response** (409 Conflict):
```json
{
  "detail": "Room is not available for the requested time slot"
}
```

### 2.2 Get All Reservations
```http
GET /reservations
```

**Query Parameters**:
- `user_id` (optional): Filter by user ID
- `status` (optional): Filter by status (pending, approved, rejected)

**Example with filters**:
```http
GET /reservations?user_id=123&status=pending
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "room_id": 1,
    "user_id": 123,
    "date": "2024-03-15",
    "start_time": "09:00:00",
    "end_time": "11:00:00",
    "purpose": "Team meeting",
    "status": "pending",
    "created_at": "2024-03-08T10:30:00"
  }
]
```

### 2.3 Get Reservation by ID
```http
GET /reservations/1
```

**Response** (200 OK):
```json
{
  "id": 1,
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "purpose": "Team meeting",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

### 2.4 Update Reservation
```http
PUT /reservations/1
Content-Type: application/json

{
  "purpose": "Updated team meeting",
  "start_time": "10:00:00",
  "end_time": "12:00:00"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "10:00:00",
  "end_time": "12:00:00",
  "purpose": "Updated team meeting",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

**Response** (400 Bad Request):
```json
{
  "detail": "Cannot update a approved reservation"
}
```

### 2.5 Delete Reservation
```http
DELETE /reservations/1
```

**Response** (204 No Content):
(Empty body)

---

## 3. ADMIN RESERVATIONS ENDPOINTS

### 3.1 Get Pending Reservations
```http
GET /admin/reservations/pending
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "room_id": 1,
    "user_id": 123,
    "date": "2024-03-15",
    "start_time": "09:00:00",
    "end_time": "11:00:00",
    "purpose": "Team meeting",
    "status": "pending",
    "created_at": "2024-03-08T10:30:00"
  }
]
```

### 3.2 Approve Reservation
```http
PUT /admin/reservations/1/approve
```

**Response** (200 OK):
```json
{
  "id": 1,
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "purpose": "Team meeting",
  "status": "approved",
  "created_at": "2024-03-08T10:30:00"
}
```

### 3.3 Reject Reservation
```http
PUT /admin/reservations/1/reject
```

**Response** (200 OK):
```json
{
  "id": 1,
  "room_id": 1,
  "user_id": 123,
  "date": "2024-03-15",
  "start_time": "09:00:00",
  "end_time": "11:00:00",
  "purpose": "Team meeting",
  "status": "rejected",
  "created_at": "2024-03-08T10:30:00"
}
```

---

## 4. EXAMS ENDPOINTS

### 4.1 Create Exam
```http
POST /exams
Content-Type: application/json

{
  "subject": "Mathematics",
  "room_id": 1,
  "date": "2024-04-20",
  "time": "09:00:00",
  "student_id": 456,
  "table_number": 5
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "subject": "Mathematics",
  "room_id": 1,
  "date": "2024-04-20",
  "time": "09:00:00",
  "student_id": 456,
  "table_number": 5
}
```

### 4.2 Get All Exams
```http
GET /exams
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "subject": "Mathematics",
    "room_id": 1,
    "date": "2024-04-20",
    "time": "09:00:00",
    "student_id": 456,
    "table_number": 5
  }
]
```

### 4.3 Get Exam by ID
```http
GET /exams/1
```

**Response** (200 OK):
```json
{
  "id": 1,
  "subject": "Mathematics",
  "room_id": 1,
  "date": "2024-04-20",
  "time": "09:00:00",
  "student_id": 456,
  "table_number": 5
}
```

### 4.4 Get Exams by Student ID
```http
GET /exams/student/456
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "subject": "Mathematics",
    "room_id": 1,
    "date": "2024-04-20",
    "time": "09:00:00",
    "student_id": 456,
    "table_number": 5
  },
  {
    "id": 2,
    "subject": "Physics",
    "room_id": 2,
    "date": "2024-04-21",
    "time": "14:00:00",
    "student_id": 456,
    "table_number": 3
  }
]
```

### 4.5 Update Exam
```http
PUT /exams/1
Content-Type: application/json

{
  "table_number": 10
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "subject": "Mathematics",
  "room_id": 1,
  "date": "2024-04-20",
  "time": "09:00:00",
  "student_id": 456,
  "table_number": 10
}
```

### 4.6 Delete Exam
```http
DELETE /exams/1
```

**Response** (204 No Content):
(Empty body)

---


## 5. DOCUMENTS ENDPOINTS

### 5.1 Request Document
```http
POST /documents
Content-Type: application/json

{
  "student_id": 123,
  "document_type": "transcript"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "student_id": 123,
  "document_type": "transcript",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

### 5.2 Get All Document Requests
```http
GET /documents
```

**Query Parameters**:
- `status` (optional): Filter by status (pending, approved, rejected)

**Example with filter**:
```http
GET /documents?status=pending
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "student_id": 123,
    "document_type": "transcript",
    "status": "pending",
    "created_at": "2024-03-08T10:30:00"
  }
]
```

### 5.3 Get Document Request by ID
```http
GET /documents/1
```

**Response** (200 OK):
```json
{
  "id": 1,
  "student_id": 123,
  "document_type": "transcript",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

### 5.4 Get Document Requests by Student
```http
GET /documents/student/123
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "student_id": 123,
    "document_type": "transcript",
    "status": "pending",
    "created_at": "2024-03-08T10:30:00"
  },
  {
    "id": 2,
    "student_id": 123,
    "document_type": "certificate",
    "status": "approved",
    "created_at": "2024-03-07T14:20:00"
  }
]
```

### 5.5 Update Document Request
```http
PUT /documents/1
Content-Type: application/json

{
  "document_type": "certificate"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "student_id": 123,
  "document_type": "certificate",
  "status": "pending",
  "created_at": "2024-03-08T10:30:00"
}
```

### 5.6 Approve Document Request
```http
PUT /documents/1/approve
```

**Response** (200 OK):
```json
{
  "id": 1,
  "student_id": 123,
  "document_type": "certificate",
  "status": "approved",
  "created_at": "2024-03-08T10:30:00"
}
```

### 5.7 Reject Document Request
```http
PUT /documents/1/reject
```

**Response** (200 OK):
```json
{
  "id": 1,
  "student_id": 123,
  "document_type": "certificate",
  "status": "rejected",
  "created_at": "2024-03-08T10:30:00"
}
```

### 5.8 Delete Document Request
```http
DELETE /documents/1
```

**Response** (204 No Content):
(Empty body)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 404 Not Found
```json
{
  "detail": "Resource with id 999 not found"
}
```

### 409 Conflict
```json
{
  "detail": "Room is not available for the requested time slot"
}
```

### 422 Unprocessable Entity (Validation Error)
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Tips

1. **Time Format**: Use `HH:MM:SS` (24-hour format)
2. **Date Format**: Use `YYYY-MM-DD`
3. **Status Values**: Use exact values: pending, approved, rejected, reported, analyzed, resolved
4. **Room Types**: Use exact values: classroom, lab, amphitheater
5. **All endpoints return timestamps in ISO 8601 format**: `2024-03-08T10:30:00`
