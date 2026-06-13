from __future__ import annotations

from dataclasses import dataclass


COMMAND_ROUTES = {
    "review": "reviewer",
    "tests": "tester",
    "docs": "scribe",
    "status": "watchdog",
}


@dataclass(frozen=True)
class CommandParseResult:
    command: str
    agent: str
    target: str
    tokens: list[str]


def parse_sync_command(text: str) -> CommandParseResult:
    parts = text.strip().split()
    if len(parts) < 2 or parts[0] != "/sync":
        raise ValueError("Command must start with /sync")
    command = parts[1].lower()
    if command not in COMMAND_ROUTES:
        raise ValueError(f"Unsupported /sync command: {command}")
    tokens = parts[2:]
    return CommandParseResult(
        command=command,
        agent=COMMAND_ROUTES[command],
        target=" ".join(tokens) or "workspace",
        tokens=tokens,
    )

