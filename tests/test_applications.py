from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app import models

client = TestClient(app)


def create_job(title: str = "Test Job", is_active: bool = True) -> models.Job:
    db = SessionLocal()
    try:
        job = models.Job(
            title=title,
            department="Test",
            description="desc",
            is_active=is_active,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    finally:
        db.close()


def test_create_application_success():
    job = create_job()
    payload = {
        "job_id": job.id,
        "candidate_name": "Alice",
        "email": "alice@example.com",
        "resume_file_path": "C:/resumes/alice.pdf",
        "cover_letter": "I am interested",
    }
    resp = client.post("/api/applications/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["candidate_name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["job_id"] == job.id


def test_create_application_missing_fields():
    resp = client.post("/api/applications/", json={"candidate_name": "Bob"})
    assert resp.status_code == 422


def test_create_application_invalid_email():
    job = create_job("Job2")
    payload = {
        "job_id": job.id,
        "candidate_name": "Bob",
        "email": "not-an-email",
    }
    resp = client.post("/api/applications/", json=payload)
    assert resp.status_code == 422


def test_get_application_by_id():
    job = create_job("Job3")
    payload = {
        "job_id": job.id,
        "candidate_name": "Cathy",
        "email": "cathy@example.com",
    }
    resp = client.post("/api/applications/", json=payload)
    assert resp.status_code == 201
    app_id = resp.json()["id"]

    get_resp = client.get(f"/api/applications/{app_id}/")
    assert get_resp.status_code == 200
    assert get_resp.json()["candidate_name"] == "Cathy"


def test_list_jobs_returns_active_only():
    create_job(title="Active Job", is_active=True)
    create_job(title="Inactive Job", is_active=False)

    resp = client.get("/api/jobs/?page=1&per_page=10")
    assert resp.status_code == 200

    titles = [j["title"] for j in resp.json()]
    assert "Active Job" in titles
    assert "Inactive Job" not in titles
