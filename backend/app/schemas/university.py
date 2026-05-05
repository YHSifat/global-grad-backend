from pydantic import BaseModel
from typing import Optional, List


class UniversityBase(BaseModel):
    name: str
    country: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None


class UniversityCreate(UniversityBase):
    pass


class UniversityRead(UniversityBase):
    id: int
    class Config:
        orm_mode = True
