import os
import json
import websockets

from app.routes.jobs import JobRead

BROKER_URL = os.getenv(
    "BROKER_URL",
    "ws://localhost:8765"
)


async def submit_job(
    job_type: str,
    payload: dict | None = None,
):
    async with websockets.connect(BROKER_URL) as websocket:

        await websocket.send(
            json.dumps({
                "action": "submit_job",
                "type": job_type,
                "payload": payload or {},
            })
        )
        

        response = await websocket.recv()
        print(f"Received response from broker: {response}")

        response = json.loads(response)

        job_response = {
            "id": response.get("job_id"),
            "type": job_type,
            "payload": payload,
            "status": response.get("status", "unknown"),
        }

        return job_response