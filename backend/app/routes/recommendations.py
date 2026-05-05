from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.program import Program
from pydantic import BaseModel

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RecommendRequest(BaseModel):
    gpa: float
    ielts: float
    top_n: int = 10


class RecommendItem(BaseModel):
    program_id: int
    name: str
    university_id: int
    score: float


@router.post("/", response_model=List[RecommendItem])
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    progs = db.query(Program).all()

    def score_program(p: Program) -> float:
        score = 0.0
        # prefer programs that student meets requirements
        if p.min_gpa is None or req.gpa >= p.min_gpa:
            score += 1.0
        if p.min_ielts is None or req.ielts >= p.min_ielts:
            score += 1.0
        # small bonus for lower tuition
        if p.tuition:
            score += max(0.0, 1.0 - (p.tuition / 100000.0))
        return score

    scored = [ (p, score_program(p)) for p in progs ]
    scored.sort(key=lambda x: x[1], reverse=True)
    items = []
    for p, s in scored[:req.top_n]:
        items.append(RecommendItem(program_id=p.id, name=p.name, university_id=p.university_id, score=s))
    return items
