from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.scrapers.runner import run_scrapers


async def handle_job(job_type: str, payload: Dict[str, Any] | None, db: Session):
    if job_type == "scrape_universities":
        source_keys = (payload or {}).get("sources") or ["unimelb", "oxford", "nus"]
        if isinstance(source_keys, str):
            source_keys = [source_keys]
        results = run_scrapers(db, list(source_keys))
        return {"status": "finished", "results": results}
    return {"status": "ignored", "detail": f"No handler for job type {job_type}"}
