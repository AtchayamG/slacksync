from __future__ import annotations

import re
from typing import Any

from services.api.app.agents.reviewer.agent import run as run_reviewer
from services.api.app.agents.reviewer.schemas import ReviewInput
from services.api.app.agents.scribe.agent import run as run_scribe
from services.api.app.agents.scribe.schemas import DocType, ScribeInput
from services.api.app.agents.tester.agent import run as run_tester
from services.api.app.agents.tester.schemas import TesterInput
from services.api.app.agents.watchdog.agent import run as run_watchdog
from services.api.app.agents.watchdog.schemas import EventType, WatchdogInput
from services.api.app.integrations.mcp_context import collect_mcp_context
from services.api.app.integrations.rts_search import search_slack_context
from services.api.app.slack.blockkit import format_result
from services.api.app.slack.command_parser import parse_sync_command


def _camel(name: str) -> str:
    head, *tail = name.split("_")
    return head + "".join(part.capitalize() for part in tail)


def _to_camel(value: Any) -> Any:
    if isinstance(value, list):
        return [_to_camel(item) for item in value]
    if isinstance(value, dict):
        return {_camel(key): _to_camel(item) for key, item in value.items()}
    return value


def _pr_number(tokens: list[str]) -> int:
    for token in tokens:
        match = re.search(r"#?(\d+)", token)
        if match:
            return int(match.group(1))
    return 42


def run_command(text: str) -> dict[str, Any]:
    parsed = parse_sync_command(text)
    if parsed.command == "review":
        result = run_reviewer(ReviewInput(pr_number=_pr_number(parsed.tokens)))
    elif parsed.command == "tests":
        result = run_tester(TesterInput(file_path=parsed.target))
    elif parsed.command == "docs":
        doc_type = DocType.CHANGELOG if "changelog" in parsed.tokens else DocType.README
        result = run_scribe(ScribeInput(repo="atchayamg/slacksync", doc_type=doc_type))
    elif parsed.command == "status":
        result = run_watchdog(
            WatchdogInput(repo="atchayamg/slacksync", event_type=EventType.MANUAL_STATUS)
        )
    else:
        raise ValueError(f"Unsupported command: {parsed.command}")
    payload = _to_camel(result.model_dump(mode="json"))
    payload["kind"] = parsed.command if parsed.command != "status" else "status"
    payload["context"] = {
        "mcp": _to_camel([artifact.__dict__ for artifact in collect_mcp_context(parsed.command, parsed.target)]),
        "rts": _to_camel([hit.__dict__ for hit in search_slack_context(parsed.command, parsed.target)]),
    }
    payload["blocks"] = format_result(payload)
    return {"parsed": parsed.__dict__, "result": payload}
