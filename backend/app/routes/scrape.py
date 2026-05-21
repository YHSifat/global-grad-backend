from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core import security
from app.models.job import Job
from app.routes.jobs import JobRead
from pydantic import BaseModel
from app.scrapers.runner import SCRAPERS

router = APIRouter(prefix="/scrape", tags=["scrape"])


class ScrapeUniversitiesRequest(BaseModel):
    sources: Optional[List[str]] = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/universities", response_model=JobRead)
def trigger_university_scrape(
    request: ScrapeUniversitiesRequest | None = None,
    db: Session = Depends(get_db),
    _=Depends(security.get_current_active_admin),
):
    sources = (request.sources if request else None) or ["unimelb", "oxford", "nus"]
    invalid_sources = [source for source in sources if source.lower() not in SCRAPERS]
    if invalid_sources:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown scrape sources: {', '.join(invalid_sources)}",
        )
    job = Job(type="scrape_universities", payload={"sources": sources}, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
