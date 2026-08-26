**Runnin backend**

through docker:

cd backend
docker compose up --build

manually:

cd backend
uvicorn app.main:app --reload