from pydantic import BaseModel
from typing import Optional


class ProgramBase(BaseModel):
    name: str
    tuition: Optional[float] = None
    deadline: Optional[str] = None
    university_id: int
    min_gpa: Optional[float] = None
    min_ielts: Optional[float] = None


class ProgramCreate(ProgramBase):
    pass


class ProgramRead(ProgramBase):
    id: int

    model_config = {"from_attributes": True}
