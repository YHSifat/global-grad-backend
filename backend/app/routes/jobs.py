from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.job import Job
from pydantic import BaseModel
from app.core import security

router = APIRouter(prefix="/jobs", tags=["jobs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class JobCreate(BaseModel):
    type: str
    payload: Any = None


class JobRead(BaseModel):
    id: int
    type: str
    payload: Any = None
    status: str

    class Config:
        orm_mode = True


@router.post("/", response_model=JobRead)
def create_job(j: JobCreate, db: Session = Depends(get_db), _=Depends(security.get_current_user)):
    job = Job(type=j.type, payload=j.payload, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: int, db: Session = Depends(get_db), _=Depends(security.get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.get("/", response_model=list[JobRead])
def list_jobs(db: Session = Depends(get_db), _=Depends(security.get_current_active_admin)):
    return db.query(Job).all()
