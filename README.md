# SlackSync

SlackSync is a Slack-native agent operations center for engineering teams. It routes `/sync` commands and App Home actions into specialized agents for code review, test generation, documentation updates, and CI failure triage.

Built for the Slack Agent Builder Challenge with:

- Slack Agent Builder and Slack app surfaces: slash commands, App Home, modals, Block Kit.
- Slack MCP-ready integration layer for GitHub and Jira workflows.
- Slack Real-Time Search-ready client for retrieving workspace context.
- A polished local demo console for judges and video capture when sandbox access is pending.

## Quick Start

```bash
cp .env.example .env
python -m venv .venv
.venv\Scripts\pip install -r services/api/requirements.txt
.venv\Scripts\python -m pytest
npm install
npm run dev
```

The web console runs at `http://127.0.0.1:5174/`. The app runs in demo mode without secrets. Real Slack mode requires the Slack app credentials in `.env`.

## Project Map

- `apps/web` - judge-facing demo console and UI reference implementation.
- `services/api` - FastAPI backend, Slack endpoints, agent orchestration, and demo data.
- `packages/contracts` - shared typed contracts for frontend/backend payloads.
- `docs` - hackathon requirements, architecture, imported docs, agent briefs, and submission checklist.
- `docs/08-handoff` - reviewer handoff notes for Claude or another external reviewer.
- `assets/diagrams` - submission-ready architecture diagram in SVG and PNG form.
- `ops` - Slack app manifest and deployment configuration references.

## Status

Devpost registration and project draft are complete. Slack Developer Program membership is active. The SlackSync sandbox is provisioned, judge invites were sent, and the installed Slack app responds to `/sync` commands through the FastAPI webhook.
