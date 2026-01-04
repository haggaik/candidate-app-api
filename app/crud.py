from typing import List

from sqlalchemy.orm import Session

from . import models, schemas


def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 10,
) -> List[models.Job]:
    return (
        db.query(models.Job)
        .filter(models.Job.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_job(
    db: Session,
    job_id: int,
) -> models.Job | None:
    return (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )


def create_application(
    db: Session,
    application_in: schemas.ApplicationCreate,
) -> models.Application:
    job = get_job(db, application_in.job_id)
    if not job:
        raise ValueError("Job not found")

    application = models.Application(
        job_id=application_in.job_id,
        candidate_name=application_in.candidate_name,
        email=str(application_in.email),
        resume_file_path=application_in.resume_file_path,
        cover_letter=application_in.cover_letter,
    )

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def get_application(
    db: Session,
    application_id: int,
) -> models.Application | None:
    return (
        db.query(models.Application)
        .filter(models.Application.id == application_id)
        .first()
    )
