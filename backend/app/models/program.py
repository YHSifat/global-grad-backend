from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)

    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)
    university = relationship("University", back_populates="programs")

    name = Column(String, nullable=False)

    tuition = Column(Float)
    deadline = Column(String)

    min_gpa = Column(Float, nullable=True)
    min_ielts = Column(Float, nullable=True)
    professors = relationship("Professor", secondary="professor_program", back_populates="programs")