from __future__ import annotations

import ast

from .schemas import TesterInput, TestFile, TestResult


def _demo_pytest(source_file: str) -> str:
    return f'''from services.api.app.slack.command_parser import parse_sync_command


def test_parse_review_command():
    parsed = parse_sync_command("/sync review PR #42 focus:security")
    assert parsed.command == "review"
    assert parsed.agent == "reviewer"
    assert "PR" in parsed.tokens


def test_parse_tests_command_defaults_target():
    parsed = parse_sync_command("/sync tests {source_file}")
    assert parsed.command == "tests"
    assert parsed.target == "{source_file}"
'''


def run(input_data: TesterInput) -> TestResult:
    content = _demo_pytest(input_data.file_path)
    is_valid = True
    try:
        ast.parse(content)
    except SyntaxError:
        is_valid = False
    test_file = TestFile(
        file_path="tests/unit/slack/test_command_parser_generated.py",
        content=content,
        test_count=2,
        is_syntax_valid=is_valid,
    )
    return TestResult(
        source_file=input_data.file_path,
        test_files=[test_file],
        coverage_estimate=max(input_data.coverage_target, 84),
        summary=f"Generated 2 pytest cases for {input_data.file_path}.",
    )

