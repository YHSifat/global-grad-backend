from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User
from app.models.program import Program
from app.models.university import University
from app.models.professor import Professor
from app.models.email import Email
from app.models.job import Job
from app.models.scholarship import Scholarship

from app.routes.users import router as users_router
from app.routes.auth import router as auth_router
from app.routes.universities import router as universities_router
from app.routes.programs import router as programs_router
from app.routes.professors import router as professors_router
from app.routes.emails import router as emails_router
from app.routes.recommendations import router as recommendations_router
from app.routes.jobs import router as jobs_router
from app.routes.scrape import router as scrape_router
from app.routes.scholarships import router as scholarships_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(universities_router)
app.include_router(programs_router)
app.include_router(professors_router)
app.include_router(emails_router)
app.include_router(recommendations_router)
app.include_router(jobs_router)
app.include_router(scrape_router)
app.include_router(scholarships_router)


@app.get("/")
def root():
    return {"status": "running"}