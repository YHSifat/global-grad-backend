from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    gpa: Optional[float] = None
    ielts: Optional[float] = None
    role: Optional[Role] = Role.student


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    role: Role

    model_config = {"from_attributes": True}


class UserUpdate(UserBase):
    password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[Role] = None
