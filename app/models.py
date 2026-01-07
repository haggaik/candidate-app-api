from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    # Explicit lengths communicate constraints clearly to reviewers
    title = Column(String(200), nullable=False)
    department = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Non-null ensures reliable filtering for active jobs
    is_active = Column(Boolean, nullable=False, default=True)

    # Cascading deletes keep ORM behavior predictable
    applications = relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            "<Job "
            f"id={self.id} "
            f"title={self.title!r} "
            f"dept={self.department!r} "
            f"active={self.is_active}>"
        )


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    # CASCADE preserves referential integrity at DB level
    job_id = Column(
        Integer,
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    candidate_name = Column(String(200), nullable=False)

    # Email validation belongs in Pydantic, not ORM
    email = Column(String(254), nullable=False, index=True)

    resume_file_path = Column(String(500), nullable=True)
    cover_letter = Column(Text, nullable=True)

    # Stored as naive UTC (acceptable for assessment scope)
    submitted_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    job = relationship("Job", back_populates="applications")

    def __repr__(self) -> str:
        return (
            "<Application "
            f"id={self.id} "
            f"job_id={self.job_id} "
            f"email={self.email!r}>"
        )


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(128), nullable=False, unique=True, index=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<ApiKey id={self.id} active={self.is_active}>"
