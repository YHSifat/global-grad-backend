import asyncio
import json
import logging
import time
from typing import Any
import websockets
from websockets import WebSocketServerProtocol
from prometheus_client import start_http_server
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.metrics import JOB_PROCESSING_DURATION_SECONDS, JOBS_CREATED_TOTAL, JOBS_PENDING_GAUGE, JOBS_PROCESSED_TOTAL
from app.models.job import Job
from datetime import datetime
from app.jobs.scheduler import handle_job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("broker")

WS_PORT = 8765
METRICS_PORT = 8001


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def process_job(job_id: int):
    db = SessionLocal()
    job_type = "unknown"
    status = "error"
    started = time.perf_counter()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.warning("Job %s disappeared before processing", job_id)
            return
        job_type = job.type

        logger.info(f"Starting job {job.id} type={job.type}")
        job.status = "running"
        job.started_at = datetime.utcnow()
        db.add(job)
        db.commit()

        try:
            if job.type == "sleep":
                secs = job.payload.get("seconds", 1) if job.payload else 1
                await asyncio.sleep(secs)
            elif job.type in {"scrape_universities", "scrape_university"}:
                result = await handle_job(job.type, job.payload, db)
                logger.info("Scrape result: %s", result)
            elif job.type == "send_email":
                await asyncio.sleep(0.5)
            else:
                await asyncio.sleep(0.1)
            job.status = "finished"
            status = "finished"
        except Exception:
            job.status = "error"
            status = "error"
            logger.exception("Job processing failed")
        finally:
            job.finished_at = datetime.utcnow()
            db.add(job)
            db.commit()
            logger.info(f"Finished job {job.id} status={job.status}")
    finally:
        JOBS_PROCESSED_TOTAL.labels(type=job_type, status=status).inc()
        JOB_PROCESSING_DURATION_SECONDS.labels(type=job_type, status=status).observe(time.perf_counter() - started)
        db.close()


async def worker_loop(stop_event: asyncio.Event):
    logger.info("Worker loop started")
    while not stop_event.is_set():
        db = SessionLocal()
        try:
            pending_count = db.query(Job).filter(Job.status == "pending").count()
            JOBS_PENDING_GAUGE.set(pending_count)
            if not pending_count:
                await asyncio.sleep(0.5)
                continue
            pending = db.query(Job).filter(Job.status == "pending").order_by(Job.created_at).limit(5).all()
            for job in pending:
                await process_job(job.id)
        except Exception:
            logger.exception("Worker loop error")
        finally:
            db.close()
    logger.info("Worker loop stopped")


class BrokerServer:
    def __init__(self):
        self.stop_event = asyncio.Event()

    async def handler(self, websocket: WebSocketServerProtocol, path: str):
        logger.info(f"Client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                except Exception:
                    await websocket.send(json.dumps({"error": "invalid json"}))
                    continue
                # Accept job submission
                if data.get("action") == "submit_job":
                    job_type = data.get("type")
                    payload = data.get("payload")
                    db = SessionLocal()
                    job = Job(type=job_type, payload=payload, status="pending")
                    db.add(job)
                    db.commit()
                    db.refresh(job)
                    db.close()
                    JOBS_CREATED_TOTAL.labels(type=job_type, source="broker").inc()
                    await websocket.send(json.dumps({"status": "submitted", "job_id": job.id}))
                else:
                    await websocket.send(json.dumps({"error": "unknown action"}))
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")

    async def run(self):
        logger.info(f"Starting broker websocket server on port {WS_PORT}")
        stop_event = self.stop_event
        Base.metadata.create_all(bind=engine)
        start_http_server(METRICS_PORT)
        server = await websockets.serve(self.handler, "0.0.0.0", WS_PORT)
        worker = asyncio.create_task(worker_loop(stop_event))
        await stop_event.wait()
        worker.cancel()
        server.close()
        await server.wait_closed()


def main():
    broker = BrokerServer()
    try:
        asyncio.run(broker.run())
    except KeyboardInterrupt:
        logger.info("Broker stopping")


if __name__ == "__main__":
    main()
