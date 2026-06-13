# SlackSync — Slack Agent Builder Challenge 2026
### Track: New Slack Agent | AI-Powered Engineering Workflow Automation Inside Slack

---

## What Is SlackSync?

SlackSync is a production-grade **Slack agent** that brings an entire AI-powered engineering workflow directly into Slack. Engineers trigger code reviews, generate unit tests, auto-update documentation, and receive CI/CD status — all from a single Slack slash command or mention, without leaving their workspace.

It uses:
- **Slack AI capabilities** (native Slack AI summarization + AI assistant)
- **MCP server integration** (GitHub MCP for code access, JIRA MCP for ticket management)
- **Real-Time Search (RTS) API** (surface PR context, error logs, and docs in real time)

---

## Hackathon Target

| Field | Value |
|---|---|
| Hackathon | Slack Agent Builder Challenge 2026 |
| Track | New Slack Agent |
| Prize | $8,000 (1st place) + Dreamforce 2026 pass |
| Deadline | July 13, 2026 @ 5:00 PM PDT |
| Eligibility | India ✅ explicitly listed |
| Participants | ~70 active submitters |

---

## The Four Sub-Agents (All inside Slack)

| Agent | Trigger | What It Does |
|---|---|---|
| **Reviewer** | `/sync review PR #42` | AI code review posted as threaded Slack message |
| **Tester** | `/sync tests path/to/file.py` | Generates unit tests, posts as Slack file snippet |
| **Scribe** | `/sync docs` | Updates README/changelog, posts diff summary |
| **Watchdog** | Automatic (CI webhook) | Posts CI/CD failures with AI-written root cause |

All four are orchestrated by a **Maestro** layer that parses Slack events, routes to the right sub-agent, and formats responses back into Slack threads.

---

## Owner / Quality Gate

**Claude Fable** (this Claude instance) is the final owner and QA gate for all agent-produced output. No file merges to `main` without a Claude Fable review sign-off recorded in `REVIEW_LOG.md`.

---

## Repository Structure

```
slacksync/
├── README.md
├── ARCHITECTURE.md
├── TASK_LIST.md
├── AGENT_CONTRACTS.md
├── REVIEW_LOG.md
├── ENVIRONMENT_SETUP.md
│
├── backend/
│   ├── slack/
│   │   ├── event_handler.py       # Parses Slack Events API payloads
│   │   ├── command_parser.py      # Parses /sync slash commands
│   │   ├── message_builder.py     # Builds Block Kit response payloads
│   │   └── oauth.py               # Slack OAuth + token management
│   │
│   ├── maestro/
│   │   ├── router.py              # Routes commands to sub-agents
│   │   ├── formatter.py           # Formats agent output for Slack
│   │   └── orchestrator.py        # Coordinates multi-step workflows
│   │
│   ├── agents/
│   │   ├── reviewer/              # Code review sub-agent
│   │   ├── tester/                # Test generation sub-agent
│   │   ├── scribe/                # Documentation sub-agent
│   │   └── watchdog/              # CI/CD monitoring sub-agent
│   │
│   ├── mcp/
│   │   ├── github_mcp.py          # GitHub MCP client wrapper
│   │   └── jira_mcp.py            # JIRA MCP client wrapper
│   │
│   ├── rts/
│   │   └── search_client.py       # Slack Real-Time Search API client
│   │
│   ├── ai/
│   │   ├── llm_client.py          # Anthropic / OpenAI client wrapper
│   │   └── prompts.py             # All system + task prompts
│   │
│   └── api/
│       └── main.py                # FastAPI app — Slack webhook receiver
│
├── frontend/                      # Minimal App Home dashboard (Block Kit)
│   └── app_home/
│       ├── home_view.py           # App Home Block Kit view builder
│       └── modals.py              # Input modals for complex commands
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── infra/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── render.yaml                # One-click deploy to Render (or Railway)
│
└── docs/
    ├── demo_script/
    │   ├── DEMO_WALKTHROUGH.md
    │   └── SAMPLE_WORKFLOW.md
    └── SUBMISSION.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Platform | Slack Agent Builder + Slack Events API |
| AI / LLM | Anthropic Claude API (claude-sonnet-4-6) |
| Slack AI | Native Slack AI summarization (conversation summaries) |
| MCP Integrations | GitHub MCP, JIRA MCP |
| Real-Time Search | Slack RTS API |
| Backend | Python + FastAPI + Uvicorn |
| Deployment | Render / Railway (publicly accessible HTTPS for Slack) |
| Block Kit | Slack Block Kit (rich message formatting) |
| Auth | Slack OAuth 2.0 |

---

## File Limits

> **Every source file must be ≤ 250 lines.** If a file approaches 250 lines, split it. This rule is enforced by Claude Fable during review.

---

## Quickstart for Agents (Codex / Antigravity / Hermes)

1. Read `ARCHITECTURE.md` — understand the full Slack event flow
2. Read `AGENT_CONTRACTS.md` — understand each sub-agent's I/O schemas
3. Read `TASK_LIST.md` — pick your assigned phase
4. Read your agent brief in `agents/AGENT_BRIEF_*.md`
5. Build your module. Keep every file ≤ 250 lines
6. Write tests in `tests/` mirroring your module path
7. Update `REVIEW_LOG.md` with completed tasks
8. Claude Fable performs final review before merge
