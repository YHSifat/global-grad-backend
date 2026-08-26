from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException

from app.core import security
from app.routes.jobs import JobRead

from pydantic import BaseModel

from app.scrapers.runner import SCRAPERS
from app.broker.client import submit_job


router = APIRouter(
    prefix="/scrape",
    tags=["scrape"]
)


class ScrapeUniversitiesRequest(BaseModel):
    sources: Optional[List[str]] = None


@router.post(
    "/universities",
    response_model=JobRead,
)
async def trigger_university_scrape(

    request: ScrapeUniversitiesRequest | None = None,

    _=Depends(
        security.get_current_active_admin
    ),
):

    sources = (
        request.sources
        if request
        else None
    ) or ["unimelb", "oxford", "nus"]

    invalid_sources = [
        source
        for source in sources
        if source.lower() not in SCRAPERS
    ]

    if invalid_sources:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unknown scrape sources: "
                f"{', '.join(invalid_sources)}"
            ),
        )

    print(f"Triggering scrape for sources: {sources}")

    result = await submit_job(
        job_type="scrape_universities",
        payload={
            "sources": sources
        },
    )

    print(f"Scrape job submitted, result: {result}")

    return result