from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    ranking = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    website = Column(String, nullable=True)

    programs = relationship("Program", back_populates="university")
