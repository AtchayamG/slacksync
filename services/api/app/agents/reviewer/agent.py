from __future__ import annotations

from .schemas import ReviewComment, ReviewInput, ReviewResult, Severity


def run(input_data: ReviewInput) -> ReviewResult:
    focus = ", ".join(input_data.focus_areas) or "security, tests, maintainability"
    comments = [
        ReviewComment(
            file_path="services/api/app/slack/signature.py",
            line_number=34,
            severity=Severity.WARNING,
            category="security",
            message="Signature verification must reject stale timestamps.",
            suggested_fix="Keep the five-minute replay window and test skewed requests.",
        ),
        ReviewComment(
            file_path="apps/web/src/App.tsx",
            line_number=88,
            severity=Severity.SUGGESTION,
            category="ux",
            message="Long agent summaries should remain scannable on mobile.",
            suggested_fix="Clamp secondary metadata and move details into the thread preview.",
        ),
        ReviewComment(
            file_path="services/api/app/maestro/router.py",
            severity=Severity.INFO,
            category="architecture",
            message=f"Review focus covered {focus} using demo MCP and RTS context.",
        ),
    ]
    return ReviewResult(
        pr_title="Add SlackSync command orchestration",
        pr_url=f"https://github.com/{input_data.repo}/pull/{input_data.pr_number}",
        overall_score=87,
        comments=comments,
        summary=(
            "The PR is merge-ready after confirming replay protection tests. "
            "Architecture is clean, and the Slack output path is easy to follow."
        ),
    )

