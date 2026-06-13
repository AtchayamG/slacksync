# REVIEW_LOG.md — Claude Fable Quality Gate

> Claude Fable is the final owner and reviewer of ALL code.
> No file merges to `main` without a sign-off entry here.

---

## Review Checklist (Applied to Every File)

- [ ] File is ≤ 250 lines (`wc -l filename.py`)
- [ ] No hardcoded secrets or token-shaped placeholders.
- [ ] Pydantic models have field types on every attribute
- [ ] All async functions have `asyncio.wait_for` or explicit timeout
- [ ] Slack signature verified before processing any payload
- [ ] Corresponding test file exists and passes
- [ ] No wildcard imports (`from x import *`)
- [ ] No bare `except:` clauses — all exceptions typed

---

## Phase 0 — Bootstrap

| Date | Reviewer | Item | Status | Notes |
|------|----------|------|--------|-------|
| TBD | Atchayam | Slack App created at api.slack.com | PENDING | |
| TBD | Atchayam | Sandbox workspace accessible | PENDING | |
| TBD | Atchayam | GitHub repo created + public | PENDING | |
| TBD | Atchayam | `.env` filled from `.env.example` | PENDING | |

## Phase 1A — FastAPI Backend

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | api/main.py | PENDING | |
| TBD | Claude Fable | api/routes/slack.py | PENDING | |
| TBD | Claude Fable | api/routes/webhook.py | PENDING | |
| TBD | Claude Fable | api/middleware/signature.py | PENDING | |

## Phase 1B — Slack Layer

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | slack/event_handler.py | PENDING | |
| TBD | Claude Fable | slack/command_parser.py | PENDING | |
| TBD | Claude Fable | slack/message_builder.py | PENDING | |
| TBD | Claude Fable | slack/oauth.py | PENDING | |

## Phase 1C — LLM Client

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | ai/llm_client.py | PENDING | |
| TBD | Claude Fable | ai/prompts.py | PENDING | |

## Phase 1D — MCP Wrappers

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | mcp/github_mcp.py | PENDING | |
| TBD | Claude Fable | mcp/jira_mcp.py | PENDING | |

## Phase 1E — RTS Client

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | rts/search_client.py | PENDING | |

## Phase 2 — Maestro

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | maestro/schemas.py | PENDING | |
| TBD | Claude Fable | maestro/router.py | PENDING | |
| TBD | Claude Fable | maestro/formatter.py | PENDING | |
| TBD | Claude Fable | maestro/orchestrator.py | PENDING | |

## Phase 3 — Reviewer Agent

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | agents/reviewer/* (all 4 files) | PENDING | |

## Phase 4 — Tester Agent

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | agents/tester/* (all 4 files) | PENDING | |

## Phase 5 — Scribe Agent

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | agents/scribe/* (all 4 files) | PENDING | |

## Phase 6 — Watchdog Agent

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | agents/watchdog/* (all 4 files) | PENDING | |

## Phase 7 — App Home

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | frontend/app_home/home_view.py | PENDING | |
| TBD | Claude Fable | frontend/app_home/modals.py | PENDING | |

## Phase 8 — Infra

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | Dockerfile, docker-compose.yml, render.yaml, ci.yml, manifest.json | PENDING | |

## Phase 9 — Demo + Docs

| Date | Reviewer | Files | Status | Notes |
|------|----------|-------|--------|-------|
| TBD | Claude Fable | DEMO_WALKTHROUGH.md | PENDING | |
| TBD | Claude Fable | SUBMISSION.md | PENDING | |
| TBD | Claude Fable | INSTALL.md | PENDING | |
| TBD | Claude Fable | architecture_diagram.png | PENDING | |

---

## Final Submission Checklist

| Check | Status | Date |
|-------|--------|------|
| All files ≤ 250 lines | PENDING | — |
| No hardcoded secrets | PENDING | — |
| Slack signature verification active | PENDING | — |
| Test coverage ≥ 70% | PENDING | — |
| App installs in fresh sandbox | PENDING | — |
| All 4 /sync commands work | PENDING | — |
| App Home renders | PENDING | — |
| CI webhook triggers Watchdog | PENDING | — |
| Judge sandbox access granted | PENDING | — |
| Demo video uploaded (YouTube unlisted) | PENDING | — |
| Devpost submission complete | PENDING | — |

**Claude Fable Final Sign-Off: PENDING**

---

## How to Request Claude Fable Review

When your phase is complete:
1. Update this log with your files and date
2. Tag the PR with label `needs-claude-fable-review`
3. Claude Fable reviews, fills Status column (APPROVED / CHANGES NEEDED)
4. Only APPROVED files merge to `main`
