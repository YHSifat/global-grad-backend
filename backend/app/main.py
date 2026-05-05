from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User
from app.models.program import Program

from app.routes.users import router as users_router
from app.routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "running"}