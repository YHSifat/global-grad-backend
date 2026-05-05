from pydantic import BaseModel, EmailStr
from typing import Optional, List


class ProfessorBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    university_id: Optional[int] = None
    program_ids: Optional[List[int]] = []


class ProfessorCreate(ProfessorBase):
    pass


class ProfessorRead(ProfessorBase):
    id: int

    class Config:
        orm_mode = True
