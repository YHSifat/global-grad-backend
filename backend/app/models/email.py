from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_professor_id = Column(Integer, ForeignKey("professors.id"), nullable=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=True)

    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    status = Column(String, nullable=True)
    sent_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User")
    recipient_professor = relationship("Professor")
    program = relationship("Program")
