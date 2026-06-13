from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DocType(str, Enum):
    README = "readme"
    CHANGELOG = "changelog"


class ScribeInput(BaseModel):
    repo: str = Field(..., json_schema_extra={"example": "org/project"})
    branch: str = "main"
    doc_type: DocType = DocType.README
    commit_range: Optional[str] = None
    existing_doc: Optional[str] = None


class DocSection(BaseModel):
    section_name: str
    before: Optional[str] = None
    after: Optional[str] = None
    changed: bool = False


class DocResult(BaseModel):
    status: str = "success"
    doc_type: DocType
    sections: List[DocSection] = []
    full_content: str = ""
    word_count: int = 0
    summary: str = ""
    error_message: Optional[str] = None
