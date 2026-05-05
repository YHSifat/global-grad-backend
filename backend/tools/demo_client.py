"""
Demo client to exercise jobs via REST and WebSocket.

Usage: run with the API and broker running locally (docker-compose up).
It will:
 - create a demo user
 - obtain a token via /auth/token
 - submit a REST job to /jobs
 - submit a websocket job to ws://localhost:8765
 - poll job statuses until finished
"""

import asyncio
import json
import time
from typing import Any, Dict

import requests
import websockets

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8765"


def create_user(email: str, password: str, name: str = "Demo User", role: str = "student") -> Dict[str, Any]:
    r = requests.post(f"{BASE_URL}/users/", json={"email": email, "password": password, "name": name, "role": role})
    r.raise_for_status()
    return r.json()


def get_token(email: str, password: str) -> str:
    data = {"username": email, "password": password}
    r = requests.post(f"{BASE_URL}/auth/token", data=data)
    r.raise_for_status()
    return r.json()["access_token"]


def submit_rest_job(token: str, job_type: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(f"{BASE_URL}/jobs/", json={"type": job_type, "payload": payload}, headers=headers)
    r.raise_for_status()
    return r.json()


async def submit_ws_job(job_type: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps({"action": "submit_job", "type": job_type, "payload": payload}))
        resp = await ws.recv()
        return json.loads(resp)


def get_job_status(token: str, job_id: int) -> Dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/jobs/{job_id}", headers=headers)
    r.raise_for_status()
    return r.json()


def poll_job(token: str, job_id: int, timeout: int = 30):
    start = time.time()
    while time.time() - start < timeout:
        j = get_job_status(token, job_id)
        print(f"Job {job_id} status={j['status']}")
        if j["status"] in ("finished", "error"):
            return j
        time.sleep(1)
    raise TimeoutError("Job did not finish in time")


async def main():
    email = "demo_user@example.com"
    password = "password123"

    print("Creating demo user (may already exist)...")
    try:
        user = create_user(email, password)
        print("Created user:", user.get("id"))
    except requests.HTTPError as e:
        print("Create user failed (maybe exists):", e)

    print("Getting token...")
    token = get_token(email, password)
    print("Token obtained (truncated):", token[:20])

    print("Submitting REST job (sleep 2s)")
    rest_job = submit_rest_job(token, "sleep", {"seconds": 2})
    rest_job_id = rest_job["id"]
    print("REST job id:", rest_job_id)

    print("Submitting WS job (sleep 3s)")
    ws_resp = await submit_ws_job("sleep", {"seconds": 3})
    print("WS response:", ws_resp)
    ws_job_id = ws_resp.get("job_id")

    print("Polling REST job")
    poll_job(token, rest_job_id, timeout=20)

    if ws_job_id:
        print("Polling WS job")
        poll_job(token, ws_job_id, timeout=30)
    else:
        print("No ws job id returned")

    print("Done")


if __name__ == "__main__":
    asyncio.run(main())
