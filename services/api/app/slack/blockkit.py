"""Block Kit formatter layer.

Agent results are data contracts first; Slack-facing presentation lives here so
the orchestrator and agents never hardcode Block Kit JSON. The formatter accepts
the camelCase result payload produced by ``maestro.router`` and returns a list of
Block Kit blocks that ``/slack/commands`` can post back to the source thread.
"""

from __future__ import annotations

from typing import Any

SEVERITY_ICON = {
    "error": ":red_circle:",
    "warning": ":large_orange_diamond:",
    "suggestion": ":bulb:",
    "info": ":information_source:",
}

STATUS_ICON = {
    "success": ":large_green_circle:",
    "partial": ":large_yellow_circle:",
    "error": ":red_circle:",
    "failure": ":red_circle:",
}


def _section(text: str) -> dict[str, Any]:
    return {"type": "section", "text": {"type": "mrkdwn", "text": text}}


def _context(elements: list[str]) -> dict[str, Any]:
    return {
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": el} for el in elements],
    }


def _header(text: str) -> dict[str, Any]:
    # Slack header blocks are plain_text and cap at 150 chars.
    return {"type": "header", "text": {"type": "plain_text", "text": text[:150], "emoji": True}}


def _status_icon(status: str) -> str:
    return STATUS_ICON.get(status, ":white_circle:")


def _review_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    score = payload.get("overallScore", 0)
    verdict = "Merge ready" if score >= 80 else "Needs changes" if score >= 50 else "High risk"
    blocks: list[dict[str, Any]] = [
        _header(f"Reviewer · {payload.get('prTitle', 'Pull request')}"),
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Score*\n{score}/100 · {verdict}"},
                {"type": "mrkdwn", "text": f"*PR*\n<{payload.get('prUrl', '#')}|View on GitHub>"},
            ],
        },
        _section(payload.get("summary", "")),
    ]
    for comment in payload.get("comments", [])[:6]:
        icon = SEVERITY_ICON.get(comment.get("severity", "info"), ":information_source:")
        loc = comment.get("filePath", "")
        if comment.get("lineNumber"):
            loc += f":{comment['lineNumber']}"
        line = f"{icon} *{comment.get('category', 'note')}* `{loc}`\n{comment.get('message', '')}"
        if comment.get("suggestedFix"):
            line += f"\n> _Fix:_ {comment['suggestedFix']}"
        blocks.append(_section(line))
    return blocks


def _tests_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = [
        _header(f"Tester · {payload.get('sourceFile', 'target file')}"),
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Coverage est.*\n{payload.get('coverageEstimate', 0)}%"},
                {
                    "type": "mrkdwn",
                    "text": f"*Generated*\n{sum(f.get('testCount', 0) for f in payload.get('testFiles', []))} cases",
                },
            ],
        },
        _section(payload.get("summary", "")),
    ]
    for test_file in payload.get("testFiles", [])[:4]:
        valid = ":white_check_mark:" if test_file.get("isSyntaxValid") else ":x:"
        blocks.append(
            _section(
                f"{valid} `{test_file.get('filePath', '')}` · {test_file.get('testCount', 0)} cases"
            )
        )
    return blocks


def _docs_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = [
        _header(f"Scribe · {payload.get('docType', 'doc')} update"),
        _section(payload.get("summary", "")),
        _context([f"*Word count:* {payload.get('wordCount', 0)}"]),
    ]
    for section in payload.get("sections", [])[:4]:
        blocks.append(
            _section(f"*{section.get('sectionName', 'Section')}*\n{section.get('after', '')}")
        )
    return blocks


def _status_blocks(payload: dict[str, Any]) -> list[dict[str, Any]]:
    runs = payload.get("ciRuns", [])
    failures = sum(1 for run in runs if run.get("status") == "failure")
    blocks: list[dict[str, Any]] = [
        _header("Watchdog · CI triage"),
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Recent runs*\n{len(runs)}"},
                {"type": "mrkdwn", "text": f"*Failures*\n{failures}"},
            ],
        },
        _section(payload.get("summary", "")),
    ]
    if payload.get("rootCause"):
        blocks.append(_section(f":mag: *Likely cause*\n{payload['rootCause']}"))
    if payload.get("fixSuggestion"):
        blocks.append(_section(f":wrench: *Suggested fix*\n{payload['fixSuggestion']}"))
    for run in runs[:4]:
        icon = _status_icon(run.get("status", ""))
        blocks.append(
            _context(
                [
                    f"{icon} `{run.get('branch', '')}` · {run.get('commitSha', '')[:7]} "
                    f"· {run.get('commitMessage', '')}"
                    + (f" · failed at *{run['failedStep']}*" if run.get("failedStep") else "")
                ]
            )
        )
    return blocks


_BUILDERS = {
    "review": _review_blocks,
    "tests": _tests_blocks,
    "docs": _docs_blocks,
    "status": _status_blocks,
}


def _evidence_block(payload: dict[str, Any]) -> dict[str, Any] | None:
    context = payload.get("context") or {}
    parts: list[str] = []
    for artifact in context.get("mcp", [])[:2]:
        parts.append(f":link: MCP `{artifact.get('source', '')}` · {artifact.get('title', '')}")
    for hit in context.get("rts", [])[:1]:
        parts.append(f":mag_right: RTS `{hit.get('channel', '')}` · {hit.get('snippet', '')}")
    return _context(parts) if parts else None


def format_result(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Render an agent result payload into Slack Block Kit blocks."""

    kind = payload.get("kind", "review")
    builder = _BUILDERS.get(kind, _review_blocks)
    blocks = builder(payload)
    evidence = _evidence_block(payload)
    if evidence:
        blocks.append({"type": "divider"})
        blocks.append(evidence)
    blocks.append(
        _context([f"{_status_icon(payload.get('status', 'success'))} SlackSync · demo mode"])
    )
    return blocks
