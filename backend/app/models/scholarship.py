from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey("universities.id"), nullable=False)

    name = Column(String, nullable=False)
    coverage = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    eligibility = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    source = Column(String, nullable=True)

    university = relationship("University")
