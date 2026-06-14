# TASK_LIST.md — SlackSync End-to-End Task List

> Owner: Claude Fable | Deadline: July 13, 2026 @ 5:00 PM PDT
> Rule: Every file produced must be ≤ 250 lines. Split if needed.
> Status: [ ] todo | [~] in progress | [x] done | [R] review by Claude Fable

---

## PHASE 0 — Project Bootstrap (Claude Fable + Atchayam)

- [ ] P0-01  Create GitHub repo `slacksync` with MIT license (public, open source)
- [ ] P0-02  Create Slack App at api.slack.com → note Client ID, Secret, Signing Secret
- [ ] P0-03  Join Slack Developer Program → get sandbox workspace
- [ ] P0-04  Enable required Slack OAuth scopes (see ENVIRONMENT_SETUP.md)
- [ ] P0-05  Set up ngrok (local dev) or deploy to Render for public HTTPS URL
- [ ] P0-06  Copy `.env.example` → `.env` and fill all values
- [ ] P0-07  Set up GitHub Actions CI (lint + test on every PR)
- [ ] P0-08  Register on Devpost for the hackathon
- [ ] P0-09  Add the required Devpost judge accounts to sandbox
- [ ] P0-10  Configure Slack App manifest (slash commands, event subscriptions, scopes)

---

## PHASE 1 — Core Infrastructure (Codex)

### 1A — FastAPI Backend

- [ ] P1-01  `backend/api/main.py` — FastAPI app init, startup, CORS middleware (≤250 lines)
- [ ] P1-02  `backend/api/routes/slack.py` — /slack/events + /slack/commands routes (≤250 lines)
- [ ] P1-03  `backend/api/routes/webhook.py` — /webhook/ci route for CI/CD events (≤250 lines)
- [ ] P1-04  `backend/api/middleware/signature.py` — Slack request signature verification (≤250 lines)
- [ ] P1-05  `tests/unit/api/test_slack_routes.py` — unit tests
- [ ] P1-06  `tests/unit/api/test_signature.py` — signature verification tests
- [R] P1-07  Claude Fable reviews all API files

### 1B — Slack Event + Command Handling

- [ ] P1-08  `backend/slack/event_handler.py` — parse Events API payloads (≤250 lines)
- [ ] P1-09  `backend/slack/command_parser.py` — parse /sync slash commands (≤250 lines)
- [ ] P1-10  `backend/slack/message_builder.py` — Block Kit payload builder helpers (≤250 lines)
- [ ] P1-11  `backend/slack/oauth.py` — Slack OAuth 2.0 token management (≤250 lines)
- [ ] P1-12  `tests/unit/slack/test_command_parser.py`
- [ ] P1-13  `tests/unit/slack/test_message_builder.py`
- [R] P1-14  Claude Fable reviews all Slack layer files

### 1C — LLM Client

- [ ] P1-15  `backend/ai/llm_client.py` — Anthropic client with retry + timeout (≤250 lines)
- [ ] P1-16  `backend/ai/prompts.py` — all system prompts, one function per agent (≤250 lines)
- [ ] P1-17  `tests/unit/ai/test_llm_client.py` — mock Anthropic API, test retry logic
- [R] P1-18  Claude Fable reviews LLM client files

### 1D — MCP Wrappers

- [ ] P1-19  `backend/mcp/github_mcp.py` — GitHub MCP client (≤250 lines)
- [ ] P1-20  `backend/mcp/jira_mcp.py` — JIRA MCP client (≤250 lines)
- [ ] P1-21  `tests/unit/mcp/test_github_mcp.py` — mock MCP, test all methods
- [ ] P1-22  `tests/unit/mcp/test_jira_mcp.py`
- [R] P1-23  Claude Fable reviews all MCP files

### 1E — Real-Time Search Client

- [ ] P1-24  `backend/rts/search_client.py` — Slack RTS API client (≤250 lines)
- [ ] P1-25  `tests/unit/rts/test_search_client.py`
- [R] P1-26  Claude Fable reviews RTS client

---

## PHASE 2 — Maestro Orchestrator (Codex)

- [ ] P2-01  `backend/maestro/schemas.py` — shared Pydantic models for routing (≤250 lines)
- [ ] P2-02  `backend/maestro/router.py` — command → sub-agent routing logic (≤250 lines)
- [ ] P2-03  `backend/maestro/formatter.py` — agent output → Block Kit payload (≤250 lines)
- [ ] P2-04  `backend/maestro/orchestrator.py` — multi-step workflow coordination (≤250 lines)
- [ ] P2-05  `tests/unit/maestro/test_router.py`
- [ ] P2-06  `tests/unit/maestro/test_formatter.py`
- [ ] P2-07  `tests/integration/test_full_review_flow.py` — end-to-end review workflow
- [R] P2-08  Claude Fable reviews all Maestro files

---

## PHASE 3 — Agent: Reviewer (Antigravity)

- [ ] P3-01  `backend/agents/reviewer/schemas.py` — ReviewInput, ReviewComment, ReviewResult (≤250 lines)
- [ ] P3-02  `backend/agents/reviewer/prompts.py` — code review system prompt + builder (≤250 lines)
- [ ] P3-03  `backend/agents/reviewer/parser.py` — parse LLM JSON → ReviewResult (≤250 lines)
- [ ] P3-04  `backend/agents/reviewer/agent.py` — main reviewer class + run() method (≤250 lines)
- [ ] P3-05  `tests/unit/agents/reviewer/test_parser.py`
- [ ] P3-06  `tests/unit/agents/reviewer/test_agent.py` — mock GitHub MCP + LLM
- [R] P3-07  Claude Fable reviews all Reviewer files

---

## PHASE 4 — Agent: Tester (Antigravity)

- [ ] P4-01  `backend/agents/tester/schemas.py` — TesterInput, TestFile, TestResult (≤250 lines)
- [ ] P4-02  `backend/agents/tester/prompts.py` — test generation system prompt (≤250 lines)
- [ ] P4-03  `backend/agents/tester/validator.py` — Python/JS syntax validation (≤250 lines)
- [ ] P4-04  `backend/agents/tester/agent.py` — main tester class + run() method (≤250 lines)
- [ ] P4-05  `tests/unit/agents/tester/test_validator.py`
- [ ] P4-06  `tests/unit/agents/tester/test_agent.py` — mock GitHub MCP + LLM
- [R] P4-07  Claude Fable reviews all Tester files

---

## PHASE 5 — Agent: Scribe (Hermes)

- [ ] P5-01  `backend/agents/scribe/schemas.py` — ScribeInput, DocDiff, DocResult (≤250 lines)
- [ ] P5-02  `backend/agents/scribe/prompts.py` — doc generation system prompt (≤250 lines)
- [ ] P5-03  `backend/agents/scribe/diff_builder.py` — before/after doc diff builder (≤250 lines)
- [ ] P5-04  `backend/agents/scribe/agent.py` — main scribe class + run() method (≤250 lines)
- [ ] P5-05  `tests/unit/agents/scribe/test_diff_builder.py`
- [ ] P5-06  `tests/unit/agents/scribe/test_agent.py` — mock GitHub MCP + Slack AI + LLM
- [R] P5-07  Claude Fable reviews all Scribe files

---

## PHASE 6 — Agent: Watchdog (Hermes)

- [ ] P6-01  `backend/agents/watchdog/schemas.py` — WatchdogInput, CIRun, CIResult (≤250 lines)
- [ ] P6-02  `backend/agents/watchdog/prompts.py` — root cause analysis prompt (≤250 lines)
- [ ] P6-03  `backend/agents/watchdog/ci_parser.py` — parse GitHub Actions / webhook payloads (≤250 lines)
- [ ] P6-04  `backend/agents/watchdog/agent.py` — main watchdog class + run() method (≤250 lines)
- [ ] P6-05  `tests/unit/agents/watchdog/test_ci_parser.py`
- [ ] P6-06  `tests/unit/agents/watchdog/test_agent.py` — mock GitHub MCP + LLM
- [R] P6-07  Claude Fable reviews all Watchdog files

---

## PHASE 7 — App Home + Modals (Antigravity)

- [ ] P7-01  `frontend/app_home/home_view.py` — App Home Block Kit view builder (≤250 lines)
- [ ] P7-02  `frontend/app_home/modals.py` — Input modals for complex commands (≤250 lines)
- [ ] P7-03  `tests/unit/frontend/test_home_view.py` — assert Block Kit payload structure
- [R] P7-04  Claude Fable reviews App Home files

---

## PHASE 8 — Infra + Deployment (Codex)

- [ ] P8-01  `infra/Dockerfile` — production container (≤250 lines)
- [ ] P8-02  `infra/docker-compose.yml` — local dev stack (≤250 lines)
- [ ] P8-03  `infra/render.yaml` — one-click Render deploy config (≤250 lines)
- [ ] P8-04  `.github/workflows/ci.yml` — lint + test on every push (≤250 lines)
- [ ] P8-05  `manifest.json` — Slack App manifest for quick install (≤250 lines)
- [R] P8-06  Claude Fable reviews all infra files

---

## PHASE 9 — Demo + Documentation (Hermes)

- [ ] P9-01  `docs/demo_script/DEMO_WALKTHROUGH.md` — step-by-step 3-min demo script
- [ ] P9-02  `docs/demo_script/SAMPLE_WORKFLOW.md` — sample commands + expected Slack output
- [ ] P9-03  `docs/SUBMISSION.md` — Devpost submission text draft
- [ ] P9-04  `docs/architecture_diagram.png` — visual architecture diagram
- [ ] P9-05  Record 3-minute demo video → upload to YouTube (unlisted)
- [ ] P9-06  `docs/INSTALL.md` — how judges install + test the app in their Slack sandbox
- [R] P9-07  Claude Fable reviews all submission materials

---

## PHASE 10 — Final QA (Claude Fable)

- [R] P10-01  Line count audit — every file ≤ 250 lines (automated: `wc -l`)
- [R] P10-02  Secrets audit - no hardcoded Slack, LLM, or GitHub token values.
- [R] P10-03  Slack signature verification works on all routes
- [R] P10-04  All Pydantic schemas validated in unit tests
- [R] P10-05  Test coverage ≥ 70% overall (`pytest --cov`)
- [R] P10-06  App installs cleanly in a fresh Slack sandbox
- [R] P10-07  All 4 slash commands work end-to-end in sandbox
- [R] P10-08  App Home renders correctly
- [R] P10-09  CI webhook triggers Watchdog alert in Slack
- [R] P10-10  Sandbox URL shared with the required Devpost judge accounts
- [R] P10-11  Final `REVIEW_LOG.md` sign-off
- [R] P10-12  Submit on Devpost before July 13, 2026 @ 5:00 PM PDT

---

## Assignment Summary

| Phase | Assigned To | Focus |
|---|---|---|
| 0 | Claude Fable + Atchayam | Bootstrap + Slack App creation |
| 1A–1E | Codex | API, Slack layer, LLM, MCP, RTS clients |
| 2 | Codex | Maestro orchestrator |
| 3 | Antigravity | Reviewer agent |
| 4 | Antigravity | Tester agent |
| 5 | Hermes | Scribe agent |
| 6 | Hermes | Watchdog agent |
| 7 | Antigravity | App Home + Modals |
| 8 | Codex | Infra + deployment |
| 9 | Hermes | Demo + docs |
| 10 | Claude Fable | Final QA + submission |
