from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class McpArtifact:
    source: str
    title: str
    relevance: int


def collect_mcp_context(command: str, target: str) -> list[McpArtifact]:
    normalized = f"{command} {target}".lower()
    artifacts = [
        McpArtifact("github", "PR diff, touched files, and reviewer history", 94),
        McpArtifact("jira", "Linked delivery ticket and acceptance criteria", 86),
    ]
    if "docs" in normalized:
        artifacts.append(McpArtifact("github", "README and changelog sections", 91))
    if "status" in normalized:
        artifacts.append(McpArtifact("github-actions", "Latest workflow run and failed step", 96))
    return artifacts

