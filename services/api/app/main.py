from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.api.app.demo_data import demo_state
from services.api.app.maestro.router import run_command
from services.api.app.slack.signature import verify_signature


class CommandRequest(BaseModel):
    text: str


app = FastAPI(title="SlackSync API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "mode": os.getenv("APP_ENV", "demo")}


@app.get("/api/demo/state")
def get_demo_state() -> dict:
    return demo_state()


@app.post("/api/commands")
def post_command(payload: CommandRequest) -> dict:
    try:
        return run_command(payload.text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/slack/commands")
async def slack_commands(
    request: Request,
    x_slack_request_timestamp: str | None = Header(default=None),
    x_slack_signature: str | None = Header(default=None),
) -> dict:
    body = await request.body()
    secret = os.getenv("SLACK_SIGNING_SECRET", "")
    if secret and not verify_signature(secret, x_slack_request_timestamp, body, x_slack_signature):
        raise HTTPException(status_code=401, detail="Invalid Slack signature")
    form = await request.form()
    text = f"/sync {form.get('text', '')}".strip()
    result = run_command(text)
    payload = result["result"]
    return {
        "response_type": "ephemeral",
        "text": payload["summary"],
        "blocks": payload.get("blocks", []),
    }
