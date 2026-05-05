from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.university import University
from app.schemas.university import UniversityCreate, UniversityRead
from app.core import security

router = APIRouter(prefix="/universities", tags=["universities"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UniversityRead)
def create_university(u: UniversityCreate, db: Session = Depends(get_db), _=Depends(security.get_current_active_admin)):
    existing = db.query(University).filter(University.name == u.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="University already exists")
    uni = University(name=u.name, country=u.country, city=u.city, website=u.website)
    db.add(uni)
    db.commit()
    db.refresh(uni)
    return uni


@router.get("/", response_model=List[UniversityRead])
def list_universities(db: Session = Depends(get_db)):
    return db.query(University).all()


@router.get("/{university_id}", response_model=UniversityRead)
def get_university(university_id: int, db: Session = Depends(get_db)):
    uni = db.query(University).filter(University.id == university_id).first()
    if not uni:
        raise HTTPException(status_code=404, detail="University not found")
    return uni
