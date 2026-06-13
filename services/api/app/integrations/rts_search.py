from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchHit:
    channel: str
    snippet: str
    score: int


def search_slack_context(command: str, target: str) -> list[SearchHit]:
    query = f"{command} {target}".lower()
    if "status" in query:
        return [
            SearchHit("#dev-agent-ops", "CI failed after auth fixture drift; rollback not needed.", 93),
            SearchHit("#release", "Mainline deploy remains healthy after the previous patch.", 88),
        ]
    if "docs" in query:
        return [
            SearchHit("#dev-agent-ops", "Document the new slash-command install path.", 92),
            SearchHit("#launch", "Keep demo copy focused on sandbox proof and judge access.", 87),
        ]
    return [
        SearchHit("#dev-agent-ops", "Security focus requested for PR review before merge.", 95),
        SearchHit("#backend", "Replay protection tests passed on the latest branch.", 90),
    ]

