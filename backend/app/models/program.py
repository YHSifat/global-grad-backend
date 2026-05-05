from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)

    university = Column(String)
    name = Column(String)

    tuition = Column(Float)

    deadline = Column(String)