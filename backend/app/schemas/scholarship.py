from pydantic import BaseModel
from typing import Optional


class ScholarshipBase(BaseModel):
    university_id: int
    name: str
    coverage: Optional[str] = None
    deadline: Optional[str] = None
    eligibility: Optional[str] = None
    link: Optional[str] = None
    source: Optional[str] = None


class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipRead(ScholarshipBase):
    id: int
    model_config = {"from_attributes": True}
