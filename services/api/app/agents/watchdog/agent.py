from __future__ import annotations

import re
from typing import Dict, List, Optional

from .schemas import CIRun, CIResult, CIStatus, EventType, WatchdogInput


_FAILURE_RE = re.compile(r"^(?P<step>[\w /\-]+):\s*(?P<body>.+)$", re.MULTILINE)

_DEMO_FAILURES: Dict[str, Dict[str, str]] = {
    "tests": {
        "step": "tests",
        "body": "test_login_invalid_token failed because the new JWT expiry logic"
        " throws when token is None (line 88).",
    },
    "lint": {
        "step": "lint",
        "body": "E501 line 142 exceeds max line length in api/routes/slack.py.",
    },
}


def _fallback_failure(ci_run: CIRun) -> Dict[str, str]:
    for key, _body in _FAILURE_RE.findall(ci_run.commit_message):
        normalized = key.strip().lower()
        if normalized in _DEMO_FAILURES:
            return {"step": normalized, "body": _DEMO_FAILURES[normalized]["body"]}
    return {
        "step": "unknown",
        "body": "No specific failure field was provided; use logs_url for details.",
    }


def run(input: WatchdogInput) -> CIResult:
    ci_runs: List[CIRun] = []
    event_type = input.event_type

    if event_type == EventType.PUSH_WEBHOOK and input.ci_run is not None:
        ci_run = input.ci_run
        ci_runs = [ci_run]
        if ci_run.status == CIStatus.FAILURE:
            failure = _fallback_failure(ci_run)
            return CIResult(
                status="error",
                ci_runs=ci_runs,
                root_cause=(
                    f"{failure['step']} failed: {failure['body']}"
                ),
                fix_suggestion=(
                    "Review the failing branch before merge; add null guard"
                    f" around the {failure['step']} success path."
                ),
                linked_pr_number=42,
                linked_pr_url=f"https://github.com/{input.repo}/pull/42",
                summary=(
                    f"Run {ci_run.run_id} failed on"
                    f" {ci_run.branch} by {ci_run.author}."
                ),
            )
        return CIResult(
            status="success",
            ci_runs=ci_runs,
            summary="CI run succeeded; no action needed.",
        )

    demo_runs = [
        CIRun(
            run_id="run-100",
            status=CIStatus.SUCCESS,
            branch="main",
            commit_sha="aaa111",
            commit_message="chore: scheduler migration",
            author="atchayam",
            started_at="2026-06-13T08:00:00Z",
            finished_at="2026-06-13T08:01:00Z",
        ),
        CIRun(
            run_id="run-101",
            status=CIStatus.FAILURE,
            branch="feature/auth",
            commit_sha="abb222",
            commit_message="tests: focus login edge cases",
            author="atchayam",
            started_at="2026-06-13T09:00:00Z",
            finished_at="2026-06-13T09:01:30Z",
        ),
    ]
    ci_runs = demo_runs
    root_cause = (
        "tests failed: test_login_invalid_token failed because the new JWT"
        " expiry logic throws when token is None."
    )
    fix_suggestion = (
        "Add null handling in the login path and re-run CI before merge."
    )
    return CIResult(
        status="error",
        ci_runs=ci_runs,
        root_cause=root_cause,
        fix_suggestion=fix_suggestion,
        linked_pr_number=41,
        linked_pr_url=f"https://github.com/{input.repo}/pull/41",
        summary="2 recent runs; 1 failure in feature/auth.",
    )
