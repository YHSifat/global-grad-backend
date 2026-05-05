from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, unique=True)

    gpa = Column(Float)
    ielts = Column(Float)