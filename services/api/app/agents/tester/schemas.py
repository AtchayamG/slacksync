from __future__ import annotations

from typing import List

from pydantic import BaseModel


class TesterInput(BaseModel):
    repo: str = "atchayamg/slacksync"
    file_path: str = "services/api/app/slack/command_parser.py"
    branch: str = "main"
    test_framework: str = "pytest"
    coverage_target: int = 80


class TestFile(BaseModel):
    file_path: str
    content: str
    test_count: int
    is_syntax_valid: bool


class TestResult(BaseModel):
    kind: str = "tests"
    status: str = "success"
    source_file: str
    test_files: List[TestFile]
    coverage_estimate: int
    summary: str
    execution_ms: int = 510

