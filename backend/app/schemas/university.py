from pydantic import BaseModel
from typing import Optional, List


class UniversityBase(BaseModel):
    name: str
    ranking: Optional[int] = None
    location: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    website: Optional[str] = None


class UniversityCreate(UniversityBase):
    pass


class UniversityRead(UniversityBase):
    id: int

    model_config = {"from_attributes": True}
