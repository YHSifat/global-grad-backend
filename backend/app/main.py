import time

from fastapi import FastAPI, Request
from sqlalchemy import text, inspect
from prometheus_client import make_asgi_app

from app.core.database import Base, engine
from app.core.metrics import HTTP_REQUEST_DURATION_SECONDS, HTTP_REQUESTS_TOTAL

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
from app.routes.feedback import router as feedback_router

Base.metadata.create_all(bind=engine)


def sync_schema():
    inspector = inspect(engine)

    column_additions = {
        "universities": {
            "ranking": "INTEGER",
            "location": "VARCHAR",
            "country": "VARCHAR",
            "city": "VARCHAR",
            "website": "VARCHAR",
        },
        "programs": {
            "duration": "VARCHAR",
            "requirements": "VARCHAR",
            "min_gpa": "FLOAT",
            "min_ielts": "FLOAT",
        },
        "professors": {
            "title": "VARCHAR",
            "department": "VARCHAR",
            "website": "VARCHAR",
            "research_area": "VARCHAR",
        },
        "scholarships": {
            "coverage": "VARCHAR",
            "eligibility": "TEXT",
            "link": "VARCHAR",
            "source": "VARCHAR",
        },
        "jobs": {
            "started_at": "TIMESTAMP",
            "finished_at": "TIMESTAMP",
        },
    }

    with engine.begin() as connection:
        for table_name, columns in column_additions.items():
            if table_name not in inspector.get_table_names():
                continue
            existing_columns = {column["name"] for column in inspector.get_columns(table_name)}
            for column_name, column_type in columns.items():
                if column_name in existing_columns:
                    continue
                connection.execute(
                    text(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}')
                )


sync_schema()

app = FastAPI()
app.mount("/metrics", make_asgi_app())


@app.middleware("http")
async def record_http_metrics(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    HTTP_REQUESTS_TOTAL.labels(method=request.method, path=path, status=str(response.status_code)).inc()
    HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, path=path).observe(time.perf_counter() - start_time)
    return response

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
app.include_router(feedback_router)


@app.get("/")
def root():
    return {"status": "running"}