from __future__ import annotations


def demo_state() -> dict:
    return {
        "workspace": "SlackSync Demo Workspace",
        "agents": [
            {"name": "Maestro", "role": "Orchestrator", "status": "ready", "score": 97},
            {"name": "Reviewer", "role": "Code Review", "status": "ready", "score": 92},
            {"name": "Tester", "role": "Test Generation", "status": "ready", "score": 89},
            {"name": "Scribe", "role": "Documentation", "status": "ready", "score": 91},
            {"name": "Watchdog", "role": "CI Triage", "status": "ready", "score": 94},
        ],
        "proof": {
            "developerProgram": "active",
            "sandbox": "active: SlackSync Sandbox, judges invited",
            "repo": "public: github.com/AtchayamG/slacksync (MIT)",
        },
    }

