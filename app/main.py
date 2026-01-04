"""
Main entry point for the Candidate Application API.

Responsibilities:
- Initialize FastAPI application
- Create database tables
- Seed sample job data on startup
- Expose REST endpoints for jobs and applications
"""

from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan replaces the deprecated @app.on_event("startup") approach.

    We use this to:
    1) Create tables
    2) Seed sample job rows if none exist
    """
    # 1) Create database tables if they do not already exist.
    Base.metadata.create_all(bind=engine)

    # 2) Seed sample jobs if table is empty (reviewer-friendly demo data)
    db = SessionLocal()
    try:
        if db.query(models.Job).count() == 0:
            sample_jobs = [
                models.Job(
                    title="Software Engineer",
                    department="Engineering",
                    description="Build and maintain backend services",
                    is_active=True,
                ),
                models.Job(
                    title="Product Manager",
                    department="Product",
                    description="Own product roadmap and requirements",
                    is_active=True,
                ),
            ]
            db.add_all(sample_jobs)
            db.commit()
    finally:
        db.close()

    # Start serving requests
    yield

    # (Optional) any shutdown cleanup could go here


# Initialize FastAPI application with metadata
app = FastAPI(title="Candidate Application API", lifespan=lifespan)


@app.get("/api/jobs/", response_model=List[schemas.JobOut])
def list_jobs(
    page: int = 1,
    per_page: int = 10,
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of active job openings.

    Query parameters:
    - page: page number (1-indexed)
    - per_page: number of results per page (max 100)

    Returns HTTP 400 for invalid pagination values.
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")

    if per_page < 1 or per_page > 100:
        raise HTTPException(
            status_code=400,
            detail="per_page must be between 1 and 100",
        )

    skip = (page - 1) * per_page
    return crud.get_jobs(db, skip=skip, limit=per_page)


@app.post(
    "/api/applications/",
    response_model=schemas.ApplicationOut,
    status_code=status.HTTP_201_CREATED,
)
def submit_application(
    application_in: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
):
    """
    Submit a new job application.

    Validation:
    - Required fields are enforced by Pydantic
    - Email format is validated automatically
    - job_id existence is validated in CRUD layer

    Returns:
    - 201 Created on success
    - 404 if the referenced job does not exist
    """
    try:
        return crud.create_application(db, application_in)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc


@app.get(
    "/api/applications/{application_id}/",
    response_model=schemas.ApplicationOut,
)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single application by ID.
    """
    application = crud.get_application(db, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application
