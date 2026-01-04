from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JobOut(BaseModel):
    id: int
    title: str
    department: str
    description: Optional[str] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ApplicationCreate(BaseModel):
    job_id: int = Field(
        ...,
        ge=1,
        description="ID of the job being applied to",
    )

    candidate_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Candidate full name",
    )

    email: EmailStr

    resume_file_path: Optional[str] = Field(
        None,
        max_length=500,
        description="Simulated file upload path (string only)",
    )

    cover_letter: Optional[str] = Field(
        None,
        max_length=5000,
        description="Optional cover letter text",
    )


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_name: str
    email: EmailStr
    resume_file_path: Optional[str] = None
    cover_letter: Optional[str] = None
    submitted_date: datetime

    model_config = ConfigDict(from_attributes=True)
