from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
import enum
from app.core.database import Base


class Role(enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, unique=True)

    hashed_password = Column(String, nullable=True)

    role = Column(SQLEnum(Role), default=Role.STUDENT, nullable=False)

    gpa = Column(Float)
    ielts = Column(Float)