from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

professor_program = Table(
    "professor_program",
    Base.metadata,
    Column("professor_id", Integer, ForeignKey("professors.id"), primary_key=True),
    Column("program_id", Integer, ForeignKey("programs.id"), primary_key=True),
)


class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    title = Column(String, nullable=True)
    department = Column(String, nullable=True)
    website = Column(String, nullable=True)
    research_area = Column(String, nullable=True)

    university_id = Column(Integer, ForeignKey("universities.id"), nullable=True)

    programs = relationship("Program", secondary=professor_program, back_populates="professors")
