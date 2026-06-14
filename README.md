# SlackSync

**A Slack-native agent operations center for engineering teams.** One `/sync`
command routes work into specialized agents for code review, test generation,
documentation updates, and CI failure triage — and posts the result back into
Slack as Block Kit, with the context evidence behind every answer.

![CI](https://github.com/AtchayamG/slacksync/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/AtchayamG/slacksync/actions/workflows/pages.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

Built for the **Slack Agent Builder Challenge** (Devpost). Primary track: New
Slack Agent.

## Why SlackSync

Engineering teams already live in Slack, but the work — PR review, tests, docs,
CI triage — lives everywhere else. SlackSync turns Slack into the command
surface and the audit trail for that work. Every action is one slash command,
every answer is a threaded, scannable Block Kit message, and every answer
carries the MCP and Real-Time Search context it was based on so the team can
trust it.

## What It Does

A deterministic **Maestro** router parses `/sync <command>` and dispatches to one
of four agents:

| Command | Agent | Output |
|---|---|---|
| `/sync review PR #42` | **Reviewer** | Severity-ranked review notes + merge-readiness score |
| `/sync tests services/auth.py` | **Tester** | Syntax-valid test scaffold + coverage estimate |
| `/sync docs changelog` | **Scribe** | README / changelog section drafted from repo activity |
| `/sync status` | **Watchdog** | CI run summary, likely root cause, suggested fix |

Each result is a typed data contract first; a dedicated **Block Kit formatter
layer** (`services/api/app/slack/blockkit.py`) turns it into Slack blocks, so
presentation never leaks into agent logic.

## How It Uses the Required Technologies

- **Slack Agent / Agent Builder surface** — an installed Slack app answers the
  `/sync` slash command through the FastAPI webhook, returning Block Kit.
- **MCP integration** — `integrations/mcp_context.py` is the GitHub/Jira MCP
  context boundary; its evidence is attached to every routed result.
- **Real-Time Search** — `integrations/rts_search.py` retrieves workspace
  channel context and attaches the matching Slack snippets.

In **demo mode** these adapters return deterministic, clearly-labeled fixtures so
the project runs and demos with **zero secrets**. In **real mode** the Slack
webhook verifies request signatures before processing, and the adapter
boundaries are where live MCP/RTS clients plug in.

## Architecture

```
Slack (slash command / App Home)
        │  signed request
        ▼
   FastAPI webhook  ──►  Maestro router  ──►  Reviewer · Tester · Scribe · Watchdog
        │                     │
        │                     ├─► MCP context adapter (GitHub / Jira)
        │                     └─► Real-Time Search adapter (#channels)
        ▼
   Block Kit formatter  ──►  threaded Slack response
```

Full diagram: `assets/diagrams/architecture.png` / `.svg`.

## Quick Start

```bash
cp .env.example .env

# Backend (FastAPI)
python -m venv .venv
.venv/bin/pip install -r services/api/requirements.txt
.venv/bin/python -m pytest -q          # 15 passing

# Frontend (judge console)
npm install
npm run build                          # typecheck + production bundle
npm run test
npm run dev                            # http://127.0.0.1:5174/
```

The console runs in demo mode without any secrets. Start the API with
`uvicorn services.api.app.main:app --reload` to see the console switch from
"Deterministic demo fallback" to the live FastAPI route.

## Live Judge Console

The web console deploys to GitHub Pages from `main` via
`.github/workflows/pages.yml`. When hosted statically it runs fully on the
bundled deterministic data, so judges can click through every agent without
running anything locally.

## Project Map

- `services/api` — FastAPI backend: Slack endpoints, signature verification,
  Maestro router, four agents, MCP/RTS adapters, Block Kit formatter.
- `apps/web` — judge-facing demo console (React + Vite + TypeScript).
- `packages/contracts` — shared typed contracts for frontend/backend payloads.
- `assets/diagrams` — submission architecture diagram (SVG + PNG).
- `assets/demo-video` — demo video and render pipeline assets.
- `ops/slack-app-manifest.json` — Slack app manifest.
- `docs` — requirements, architecture, agent briefs, demo script, and the
  submission evidence checklist.

## Testing & CI

`.github/workflows/ci.yml` runs backend `pytest`, the frontend build + tests,
and a secret-pattern scan on every push and pull request to `main`.

## Security & Guardrails

- Slack request signatures are verified with a 5-minute replay window before any
  webhook is processed.
- Demo mode is deterministic and never loads Slack, GitHub, Jira, or LLM
  secrets.
- No secrets are committed; CI fails the build if a secret pattern appears.

## License

MIT — see `LICENSE`.
