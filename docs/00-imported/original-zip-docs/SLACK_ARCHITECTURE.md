# ARCHITECTURE.md - Imported Reference Summary

This file preserves the useful intent from the original architecture note in a compact, public-repo-safe form.

## Product Shape

SlackSync is a Slack-native engineering workflow agent. Engineers interact with it through `/sync`, mentions, and App Home style surfaces. The product routes requests to specialized agents for code review, test planning, documentation support, and deployment/CI monitoring.

## Core Flow

1. A user sends a Slack command such as `/sync review PR #42`.
2. Slack calls the FastAPI webhook receiver.
3. The command parser extracts intent, target, and optional focus terms.
4. Maestro routes the task to the correct agent.
5. Agents return structured results.
6. SlackSync responds in Slack and the web console mirrors the same workflow state.

## Agents

- Reviewer: summarizes PR risk, findings, and suggested next actions.
- Tester: proposes test targets and runnable test strategy.
- Scribe: produces documentation updates from project context.
- Watchdog: identifies failed or risky delivery signals and suggests remediation.

## Slack Surface

- Slash command: `/sync`
- Recommended usage hints: `review PR #42`, `tests services/api`, `docs readme`, `status`
- App Home can show active workflows, approvals, and recent agent activity.

## Production Notes

- Verify Slack signatures when a signing secret is configured.
- Keep the webhook response under Slack time limits.
- Avoid committing token values, OAuth codes, payment details, or workspace secrets.
- The hackathon demo should show a working sandbox install, an architecture diagram, and a short walkthrough.

