from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.professor import Professor, professor_program
from app.models.program import Program
from app.schemas.professor import ProfessorCreate, ProfessorRead
from app.core import security

router = APIRouter(prefix="/professors", tags=["professors"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProfessorRead)
def create_professor(p: ProfessorCreate, db: Session = Depends(get_db), _=Depends(security.get_current_active_admin)):
    prof = Professor(name=p.name, email=p.email, university_id=p.university_id)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof


@router.get("/", response_model=List[ProfessorRead])
def list_professors(db: Session = Depends(get_db)):
    return db.query(Professor).all()


@router.get("/{professor_id}", response_model=ProfessorRead)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    prof = db.query(Professor).filter(Professor.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof


@router.post("/{professor_id}/programs")
def assign_program(professor_id: int, program_id: int, db: Session = Depends(get_db), _=Depends(security.get_current_active_admin)):
    prof = db.query(Professor).filter(Professor.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    prog = db.query(Program).filter(Program.id == program_id).first()
    if not prog:
        raise HTTPException(status_code=404, detail="Program not found")
    prof.programs.append(prog)
    db.commit()
    return {"detail": "assigned"}
