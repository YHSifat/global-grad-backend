from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.program import Program
from app.models.university import University
from app.schemas.program import ProgramCreate, ProgramRead
from app.core import security

router = APIRouter(prefix="/programs", tags=["programs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProgramRead)
def create_program(p: ProgramCreate, db: Session = Depends(get_db), _=Depends(security.get_current_active_admin)):
    uni = db.query(University).filter(University.id == p.university_id).first()
    if not uni:
        raise HTTPException(status_code=400, detail="University does not exist")
    prog = Program(name=p.name, tuition=p.tuition, deadline=p.deadline, university_id=p.university_id)
    db.add(prog)
    db.commit()
    db.refresh(prog)
    return prog


@router.get("/", response_model=List[ProgramRead])
def list_programs(db: Session = Depends(get_db)):
    return db.query(Program).all()


@router.get("/{program_id}", response_model=ProgramRead)
def get_program(program_id: int, db: Session = Depends(get_db)):
    prog = db.query(Program).filter(Program.id == program_id).first()
    if not prog:
        raise HTTPException(status_code=404, detail="Program not found")
    return prog
