from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class CIStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"


class CIRun(BaseModel):
    run_id: str = Field(..., json_schema_extra={"example": "run-001"})
    status: CIStatus
    branch: str = "main"
    commit_sha: str = "abc123"
    commit_message: str = "fix: login token edge case"
    author: str = "atchayam"
    started_at: str = "2026-06-13T10:00:00Z"
    finished_at: Optional[str] = "2026-06-13T10:02:00Z"
    logs_url: Optional[str] = None
    failed_step: Optional[str] = None


class EventType(str, Enum):
    PUSH_WEBHOOK = "push_webhook"
    MANUAL_STATUS = "manual_status"


class WatchdogInput(BaseModel):
    repo: str = "org/project"
    event_type: EventType = EventType.PUSH_WEBHOOK
    ci_run: Optional[CIRun] = None


class CIResult(BaseModel):
    status: str = "success"
    ci_runs: List[CIRun] = []
    root_cause: Optional[str] = None
    fix_suggestion: Optional[str] = None
    linked_pr_number: Optional[int] = None
    linked_pr_url: Optional[str] = None
    summary: str = ""
    error_message: Optional[str] = None
