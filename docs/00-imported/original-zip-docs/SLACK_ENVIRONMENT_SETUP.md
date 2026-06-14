# ENVIRONMENT_SETUP.md — SlackSync Setup Guide

> Read this first. Every value in `.env` must be filled before running.

---

## Step 1 — Create the Slack App

1. Go to https://api.slack.com/apps → "Create New App" → "From an app manifest"
2. Paste `manifest.json` from `infra/manifest.json`
3. Select your developer sandbox workspace
4. Note: **Client ID**, **Client Secret**, **Signing Secret**, and **Bot User OAuth Token**
5. Install the app to your sandbox workspace → copy the **Bot User OAuth Token**

### Required OAuth Scopes

```
Bot Token Scopes:
  app_mentions:read       - Receive @mentions
  channels:history        - Read channel messages (for RTS + Slack AI)
  chat:write              - Post messages
  chat:write.public       - Post to channels the bot isn't in
  commands                - Register /sync slash command
  files:write             - Upload test file snippets
  im:history              - Read DMs (optional)
  search:read             - Real-Time Search API
  users:read              - Get user info for display

User Token Scopes:
  search:read             - Required for RTS API (user-level)
```

### Slash Command Configuration

In Slack App settings → Features → Slash Commands:
```
Command:      /sync
Request URL:  https://YOUR_DOMAIN/slack/commands
Description:  AI engineering workflow agent
Usage hint:   review PR #42 | tests path/to/file.py | docs | status
```

### Event Subscriptions

In Slack App settings → Features → Event Subscriptions:
```
Request URL:  https://YOUR_DOMAIN/slack/events

Subscribe to bot events:
  app_home_opened         - Render App Home dashboard
  app_mention             - Handle @SlackSync mentions
```

---

## Step 2 — Fill .env

Copy `.env.example` → `.env` and fill every value:

```bash
# ============================================================
# SLACK
# ============================================================
SLACK_BOT_TOKEN placeholder: Bot User OAuth Token
SLACK_SIGNING_SECRET placeholder: From App Credentials
SLACK_CLIENT_ID=<client-id>               # From App Credentials
SLACK_CLIENT_SECRET=<client-secret>       # From App Credentials
SLACK_APP_TOKEN=<app-level-token>         # For Socket Mode (local dev only)

# ============================================================
# ANTHROPIC (LLM backbone)
# ============================================================
ANTHROPIC_API_KEY=<anthropic-api-key>

# ============================================================
# GITHUB MCP
# ============================================================
GITHUB_TOKEN=<github-token>               # Personal access token with repo scope
GITHUB_DEFAULT_REPO=org/project           # Default repo if none specified in command

# ============================================================
# JIRA MCP
# ============================================================
JIRA_BASE_URL=https://yourorg.atlassian.net
JIRA_EMAIL=you@yourorg.com
JIRA_API_TOKEN=...
JIRA_DEFAULT_PROJECT=ENG                  # Default project key for bug creation

# ============================================================
# APP CONFIG
# ============================================================
ENVIRONMENT=development                   # development | production
PORT=8000
AGENT_TIMEOUT_SECONDS=25                  # Must be < Slack's 30s async limit
LOG_LEVEL=INFO

# ============================================================
# DEPLOYMENT (production only)
# ============================================================
PUBLIC_URL=https://your-app.onrender.com  # Your public HTTPS URL
```

---

## Step 3 — Local Development

### Prerequisites
- Python 3.11+
- Docker (for local Redis if needed)
- ngrok (for HTTPS tunnel to localhost)

### Install and run

```bash
git clone https://github.com/YOUR_ORG/slacksync.git
cd slacksync
cp .env.example .env
# Fill .env values

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn api.main:app --reload --port 8000
```

### Expose local server to Slack

```bash
ngrok http 8000
# Copy the https URL → paste into Slack App settings as Request URL
```

---

## Step 4 — Deploy to Render (Recommended for hackathon)

1. Push repo to GitHub
2. Go to https://render.com → "New Web Service" → Connect GitHub repo
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `uvicorn backend.api.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from `.env` in Render dashboard
6. Your public URL is `https://slacksync-xxx.onrender.com`
7. Update Slack App Request URLs to use this URL

---

## Python Dependencies (requirements.txt)

```txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
slack-sdk==3.31.0
httpx==0.27.0
pydantic==2.7.1
pydantic-settings==2.2.1
anthropic==0.28.0
python-dotenv==1.0.1
pytest==8.2.0
pytest-asyncio==0.23.6
pytest-mock==3.14.0
```

---

## Slack App Manifest (infra/manifest.json)

```json
{
  "display_information": {
    "name": "SlackSync",
    "description": "AI-powered engineering workflow agent",
    "background_color": "#4A154B"
  },
  "features": {
    "app_home": {
      "home_tab_enabled": true,
      "messages_tab_enabled": false
    },
    "bot_user": {
      "display_name": "SlackSync",
      "always_online": true
    },
    "slash_commands": [
      {
        "command": "/sync",
        "url": "https://YOUR_DOMAIN/slack/commands",
        "description": "AI engineering workflow agent",
        "usage_hint": "review PR #42 | tests path/file.py | docs | status",
        "should_escape": false
      }
    ]
  },
  "oauth_config": {
    "scopes": {
      "bot": [
        "app_mentions:read",
        "channels:history",
        "chat:write",
        "chat:write.public",
        "commands",
        "files:write",
        "search:read",
        "users:read"
      ]
    }
  },
  "settings": {
    "event_subscriptions": {
      "request_url": "https://YOUR_DOMAIN/slack/events",
      "bot_events": [
        "app_home_opened",
        "app_mention"
      ]
    },
    "interactivity": {
      "is_enabled": true,
      "request_url": "https://YOUR_DOMAIN/slack/interactions"
    }
  }
}
```

---

## Running Tests

```bash
cd backend

# Unit tests (no Slack or GitHub connection needed)
pytest tests/unit/ -v --tb=short

# All tests with coverage
pytest tests/ --cov=. --cov-report=term-missing --cov-fail-under=70

# Single agent tests
pytest tests/unit/agents/reviewer/ -v
```

---

## GitHub Actions CI (.github/workflows/ci.yml)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest tests/unit/ -v --tb=short
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
          SLACK_SIGNING_SECRET: ${{ secrets.SLACK_SIGNING_SECRET }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GH_TOKEN }}
          ENVIRONMENT: test
```

---

## Judge Access Setup

Before submitting, add judges to your Slack sandbox:

```
Required Devpost judge accounts  → invite to sandbox as full members
```

Then in your Devpost submission, provide:
- Sandbox workspace URL
- Instructions to use `/sync` commands
- A pre-seeded test repo so review/tests/docs commands work immediately
