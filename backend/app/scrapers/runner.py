from time import perf_counter
from typing import Dict, Iterable, List
from sqlalchemy.orm import Session
from app.models.university import University
from app.models.program import Program
from app.models.professor import Professor
from app.models.scholarship import Scholarship
from app.scrapers.base import ScrapedUniversity, UniversityScraper
from app.scrapers.universities.unimelb import UniMelbScraper
from app.scrapers.universities.oxford import OxfordScraper
from app.scrapers.universities.nus import NusScraper
from app.core.metrics import SCRAPE_DURATION_SECONDS, SCRAPE_RUNS_TOTAL

SCRAPERS: Dict[str, type[UniversityScraper]] = {
    "unimelb": UniMelbScraper,
    "oxford": OxfordScraper,
    "nus": NusScraper,
}


def get_scraper(source_key: str) -> UniversityScraper:
    scraper_cls = SCRAPERS.get(source_key.lower())
    if not scraper_cls:
        raise ValueError(f"Unknown scraper source: {source_key}")
    return scraper_cls()


def upsert_university(db: Session, scraped: ScrapedUniversity) -> University:
    university = db.query(University).filter(University.name == scraped.name).first()
    if not university:
        university = University(name=scraped.name)
    university.ranking = scraped.ranking
    university.location = scraped.location
    university.website = scraped.website
    university.country = scraped.country
    university.city = scraped.city
    db.add(university)
    db.commit()
    db.refresh(university)
    return university


def upsert_programs(db: Session, university_id: int, programs: Iterable[dict]):
    for program_data in programs:
        name = program_data.get("name")
        if not name:
            continue
        program = db.query(Program).filter(Program.university_id == university_id, Program.name == name).first()
        if not program:
            program = Program(university_id=university_id, name=name)
        program.tuition = program_data.get("tuition")
        program.duration = program_data.get("duration")
        program.requirements = program_data.get("requirements")
        program.deadline = program_data.get("deadline")
        program.min_gpa = program_data.get("min_gpa")
        program.min_ielts = program_data.get("min_ielts")
        db.add(program)
    db.commit()


def upsert_professors(db: Session, university_id: int, professors: Iterable[dict]):
    for professor_data in professors:
        name = professor_data.get("name")
        if not name:
            continue
        professor = db.query(Professor).filter(Professor.university_id == university_id, Professor.name == name).first()
        if not professor:
            professor = Professor(university_id=university_id, name=name)
        professor.email = professor_data.get("email")
        professor.title = professor_data.get("title")
        professor.department = professor_data.get("department")
        professor.website = professor_data.get("website")
        professor.research_area = professor_data.get("research_area")
        db.add(professor)
    db.commit()


def upsert_scholarships(db: Session, university_id: int, scholarships: Iterable[dict]):
    for scholarship_data in scholarships:
        name = scholarship_data.get("name")
        if not name:
            continue
        scholarship = db.query(Scholarship).filter(Scholarship.university_id == university_id, Scholarship.name == name).first()
        if not scholarship:
            scholarship = Scholarship(university_id=university_id, name=name)
        scholarship.coverage = scholarship_data.get("coverage")
        scholarship.deadline = scholarship_data.get("deadline")
        scholarship.eligibility = scholarship_data.get("eligibility")
        scholarship.link = scholarship_data.get("link")
        scholarship.source = scholarship_data.get("source")
        db.add(scholarship)
    db.commit()


def run_scraper(db: Session, source_key: str) -> dict:
    started = perf_counter()
    status = "success"
    try:
        scraper = get_scraper(source_key)
        scraped = scraper.scrape()
        university = upsert_university(db, scraped)
        upsert_programs(db, university.id, scraped.programs)
        upsert_professors(db, university.id, scraped.professors)
        upsert_scholarships(db, university.id, scraped.scholarships)
        return {"source": source_key, "university_id": university.id, "name": university.name}
    except Exception:
        status = "error"
        raise
    finally:
        SCRAPE_RUNS_TOTAL.labels(source=source_key, status=status).inc()
        SCRAPE_DURATION_SECONDS.labels(source=source_key, status=status).observe(perf_counter() - started)


def run_scrapers(db: Session, source_keys: List[str]) -> List[dict]:
    results = []
    for source_key in source_keys:
        results.append(run_scraper(db, source_key))
    return results
