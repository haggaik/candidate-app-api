# Candidate Application API

A professional REST API for job application management built with FastAPI and SQLAlchemy.

**Status**: ✅ All tests passing | All requirements met | Bonus features included

## Overview

This project implements a complete REST API for a candidate job application system, demonstrating:
- RESTful API design principles
- ORM expertise with SQLAlchemy
- Input validation and error handling
- Comprehensive test coverage
- Production-ready code structure

## Requirements Met

FastAPI framework  
Job and Application models with ORM relationships  
GET /api/jobs/ with pagination  
POST /api/applications/ with validation  
Email format validation  
SQLite database with auto-migrations  
Unit tests (5 tests, all passing)  
**BONUS**: GET /api/applications/{id}/ endpoint  
**BONUS**: Pagination implemented  

## Project Structure

```
app/
├── main.py          # FastAPI app, routes, lifespan
├── models.py        # SQLAlchemy ORM models (Job, Application)
├── schemas.py       # Pydantic validation schemas
├── crud.py          # Database operations
├── database.py      # SQLAlchemy setup, session management
└── __init__.py

tests/
└── test_applications.py  # Comprehensive unit tests

requirements.txt    # Dependencies
pytest.ini         # Pytest configuration
README.md          # This file
```

## Quick Start

### 1. Create Virtual Environment & Install Dependencies

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

**Interactive Documentation:**
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI spec: http://127.0.0.1:8000/openapi.json

### 3. Run Tests

```bash
# Run all tests with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/
```

## API Endpoints

### GET /api/jobs/
Returns a paginated list of active job openings.

**Query Parameters:**
- `page` (int, default=1): Page number (1-indexed)
- `per_page` (int, default=10): Results per page (max 100)

**Example:**
```bash
curl "http://127.0.0.1:8000/api/jobs/?page=1&per_page=10"
```

**Response (201):**
```json
[
  {
    "id": 1,
    "title": "Software Engineer",
    "department": "Engineering",
    "description": "Build and maintain backend services",
    "is_active": true
  }
]
```

---

### POST /api/applications/
Submit a new job application.

**Request Body:**
```json
{
  "job_id": 1,
  "candidate_name": "John Doe",
  "email": "john@example.com",
  "resume_file_path": "/resumes/john_doe.pdf",
  "cover_letter": "I am very interested in this position..."
}
```

**Validation Rules:**
- `job_id`: Required, must be >= 1, job must exist
- `candidate_name`: Required, 1-200 characters
- `email`: Required, valid email format
- `resume_file_path`: Optional, max 500 characters
- `cover_letter`: Optional, max 5000 characters

**Response (201 Created):**
```json
{
  "id": 5,
  "job_id": 1,
  "candidate_name": "John Doe",
  "email": "john@example.com",
  "resume_file_path": "/resumes/john_doe.pdf",
  "cover_letter": "I am very interested in this position...",
  "submitted_date": "2026-01-04T10:30:00"
}
```

**Error Responses:**
- `422 Unprocessable Entity`: Missing or invalid fields
- `404 Not Found`: Job ID does not exist

---

### GET /api/applications/{id}/
Retrieve a specific application by ID.

**Example:**
```bash
curl "http://127.0.0.1:8000/api/applications/5/"
```

**Response (200 OK):**
```json
{
  "id": 5,
  "job_id": 1,
  "candidate_name": "John Doe",
  "email": "john@example.com",
  "resume_file_path": "/resumes/john_doe.pdf",
  "cover_letter": "I am very interested in this position...",
  "submitted_date": "2026-01-04T10:30:00"
}
```

**Error Response:**
- `404 Not Found`: Application does not exist

## Technical Implementation

### Data Models

**Job** (models.py)
- `id`: Primary key
- `title`: String(200), not nullable
- `department`: String(200), not nullable
- `description`: Text, optional
- `is_active`: Boolean, default=True
- Relationships: One-to-many with Applications (cascade delete)

**Application** (models.py)
- `id`: Primary key
- `job_id`: Foreign key → Job (cascade delete)
- `candidate_name`: String(200), not nullable
- `email`: String(254), not nullable, indexed
- `resume_file_path`: String(500), optional
- `cover_letter`: Text, optional
- `submitted_date`: DateTime, default=UTC now
- Relationships: Many-to-one with Job

### Validation Strategy

**Pydantic Schemas** (schemas.py):
- `JobOut`: Response schema for jobs
- `ApplicationCreate`: Request schema with field validation
- `ApplicationOut`: Response schema with datetime handling

**Database Constraints**:
- Foreign key relationships with CASCADE deletes
- NOT NULL constraints on required fields
- String length limits on all text fields
- Indexed fields for query performance

### Database

- **Type**: SQLite (easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **Sessions**: FastAPI dependency injection for automatic cleanup
- **Migrations**: Tables auto-created on startup

### Testing

5 comprehensive unit tests covering:
1. Successful application submission
2. Missing required fields validation
3. Invalid email format validation
4. Application retrieval by ID
5. Active jobs filtering

**Test Framework**: pytest 9.0.2  
**HTTP Client**: FastAPI TestClient  

Run: `pytest -v`

## Key Design Decisions

### Why FastAPI?
- Modern async Python framework
- Automatic validation with Pydantic
- Built-in interactive API documentation
- Type hints for better IDE support and documentation

### Why SQLAlchemy ORM?
- Database-agnostic (works with PostgreSQL, MySQL, SQLite)
- Relationship management and cascade operations
- Type safety with Python classes

### Why Separate Schemas?
- Input validation (ApplicationCreate) separate from output (ApplicationOut)
- Prevents accidental exposure of internal fields
- Clear API contract definition

### Pagination in GET /api/jobs/
- Offset-based pagination for simplicity
- Default: page=1, per_page=10
- Max results: 100 per page
- Extensible to cursor-based pagination if needed

## Error Handling

| Status Code | Scenario |
|-------------|----------|
| 200 | Successful GET requests |
| 201 | Application created successfully |
| 400 | Invalid pagination parameters |
| 404 | Resource not found |
| 422 | Validation error (missing/invalid fields) |
| 500 | Server error |

## Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement database migrations with Alembic
- [ ] Add logging and monitoring
- [ ] Rate limiting on endpoints
- [ ] Implement actual file upload (S3/Azure Blob)
- [ ] Add database search and filtering
- [ ] Soft deletes for audit trail
- [ ] API versioning (v1, v2)

## Development Notes

- **Auto-reload**: Changes to code automatically reload the server
- **Hot Module Reload**: Pydantic models update without restart
- **Database**: Creates `app.db` in project root on first run
- **Sample Data**: 2 sample jobs seeded on first startup

## Requirements

- Python 3.10+
- See [requirements.txt](requirements.txt) for full dependency list

## Author

Haggai Chipeta  
Technical Assessment Submission - Backend Developer Role (SCIP)
