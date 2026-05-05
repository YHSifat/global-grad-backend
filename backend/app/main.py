from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User
from app.models.program import Program

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}