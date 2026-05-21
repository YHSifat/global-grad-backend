from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.models.feedback import Feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FeedbackCreate(BaseModel):
    entity_type: str
    entity_id: int
    field: str | None = None
    original_value: str | None = None
    suggested_value: str | None = None
    notes: str | None = None


@router.post("/", status_code=201)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    fb = Feedback(
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        field=payload.field,
        original_value=payload.original_value,
        suggested_value=payload.suggested_value,
        notes=payload.notes,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return {"status": "received", "id": fb.id}
