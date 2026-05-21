from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.scholarship import Scholarship
from app.schemas.scholarship import ScholarshipRead

router = APIRouter(prefix="/scholarships", tags=["scholarships"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[ScholarshipRead])
def list_scholarships(university_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Scholarship)
    if university_id is not None:
        query = query.filter(Scholarship.university_id == university_id)
    return query.all()


@router.get("/{scholarship_id}", response_model=ScholarshipRead)
def get_scholarship(scholarship_id: int, db: Session = Depends(get_db)):
    scholarship = db.query(Scholarship).filter(Scholarship.id == scholarship_id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship
