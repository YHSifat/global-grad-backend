from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmailBase(BaseModel):
    recipient_professor_id: Optional[int] = None
    program_id: Optional[int] = None
    subject: Optional[str] = None
    body: Optional[str] = None


class EmailCreate(EmailBase):
    pass


class EmailRead(EmailBase):
    id: int
    sender_id: int
    sent_at: Optional[datetime] = None

    class Config:
        orm_mode = True
