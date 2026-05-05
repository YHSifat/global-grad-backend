from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.email import Email
from app.schemas.email import EmailCreate, EmailRead
from app.core import security

router = APIRouter(prefix="/emails", tags=["emails"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EmailRead)
def send_email(e: EmailCreate, db: Session = Depends(get_db), current_user = Depends(security.get_current_user)):
    email = Email(sender_id=current_user.id, recipient_professor_id=e.recipient_professor_id, program_id=e.program_id, subject=e.subject, body=e.body)
    db.add(email)
    db.commit()
    db.refresh(email)
    return email


@router.get("/", response_model=List[EmailRead])
def list_emails(mine: Optional[bool] = False, db: Session = Depends(get_db), current_user = Depends(security.get_current_user)):
    q = db.query(Email)
    if mine:
        q = q.filter(Email.sender_id == current_user.id)
    return q.all()
