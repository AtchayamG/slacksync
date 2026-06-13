# SlackSync Implementation Plan

## Goal

Ship a full demo-ready Slack agent product with a real Slack-ready backend, deterministic demo mode, polished web console, and submission assets.

## Architecture

SlackSync has three surfaces:

- Slack app surface: slash commands, Events API, App Home, modals, and Block Kit output.
- Backend surface: FastAPI routes, signature verification, deterministic router, agent modules, MCP/RTS adapters.
- Web demo surface: Vite/React console that mirrors Slack workflows for judges and video capture.

## Work Slices

1. Foundation: repo files, environment template, contracts, backend app shell, demo data.
2. Slack layer: signature verification, slash command parser, App Home and Block Kit builders.
3. Agent layer: Reviewer, Tester, Scribe, Watchdog with typed inputs/outputs and fallback demo responses.
4. Web UI: operational dashboard, command simulator, thread preview, architecture/proof panels.
5. Delivery: Docker/Render-ready config, README, install guide, demo script, submission text.
6. Verification: unit tests, line-count audit, secrets scan, browser screenshots, final CTO review.

## Quality Gates

- Local demo starts with no secrets.
- `pytest` passes.
- `npm run build` passes.
- No source file exceeds 250 lines unless logged in `docs/07-reviews/cto-review-log.md`.
- No secrets in git.
- Submission checklist distinguishes real proof from demo proof.

