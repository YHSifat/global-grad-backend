from pydantic import BaseModel, EmailStr
from typing import Optional, List


class ProfessorBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    title: Optional[str] = None
    department: Optional[str] = None
    website: Optional[str] = None
    research_area: Optional[str] = None
    university_id: Optional[int] = None
    program_ids: Optional[List[int]] = []


class ProfessorCreate(ProfessorBase):
    pass


class ProfessorRead(ProfessorBase):
    id: int

    model_config = {"from_attributes": True}
