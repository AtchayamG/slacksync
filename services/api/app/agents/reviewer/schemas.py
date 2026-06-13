from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    SUGGESTION = "suggestion"
    INFO = "info"


class ReviewInput(BaseModel):
    repo: str = "atchayamg/slacksync"
    pr_number: int = 42
    focus_areas: List[str] = Field(default_factory=list)


class ReviewComment(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    severity: Severity
    category: str
    message: str
    suggested_fix: Optional[str] = None


class ReviewResult(BaseModel):
    kind: str = "review"
    status: str = "success"
    pr_title: str
    pr_url: str
    overall_score: int
    comments: List[ReviewComment]
    summary: str
    execution_ms: int = 420

