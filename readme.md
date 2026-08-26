**Runnin backend**

through docker:

cd backend
docker compose build

manually:

cd backend
uvicorn app.main:app --reload