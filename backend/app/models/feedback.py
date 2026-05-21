from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    field = Column(String, nullable=True)
    original_value = Column(String, nullable=True)
    suggested_value = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
