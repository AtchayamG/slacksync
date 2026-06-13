# AGENT_BRIEF_CODEX.md — Briefing for Codex (SlackSync)

> You are Codex. Read this entire document before writing a single line of code.
> Owner/Reviewer: Claude Fable. All output reviewed before merge.

---

## Your Ownership

You own the **infrastructure and orchestration** of SlackSync:
- FastAPI backend (webhook receiver)
- Slack event + command parsing layer
- LLM client (Anthropic)
- MCP wrappers (GitHub + JIRA)
- Real-Time Search client
- Maestro orchestrator
- All cloud infra (Docker, Render, GitHub Actions)

Your phases: **1A, 1B, 1C, 1D, 1E, 2, 8**

---

## Non-Negotiable Rules

1. **Every file ≤ 250 lines.** Split at logical boundaries.
2. **Verify Slack signature on EVERY incoming request** before any processing. This is a security requirement and a hackathon judging criterion.
3. **Every slash command must respond within 3 seconds** with an ack, then post the real result asynchronously. Use `asyncio.create_task()` for the actual agent work.
4. **No hardcoded tokens.** All from `os.getenv()`.
5. **All agent inputs/outputs use Pydantic schemas** from `AGENT_CONTRACTS.md`.
6. **Write unit tests alongside every file.**

---

## Key Architecture Patterns

### Slash Command 3-Second Rule

Slack times out slash commands after 3 seconds. Pattern to follow:

```python
# backend/api/routes/slack.py
@router.post("/slack/commands")
async def handle_command(request: Request, background_tasks: BackgroundTasks):
    # 1. Verify signature immediately
    await verify_slack_signature(request)

    # 2. Parse form data
    form = await request.form()
    command_text = form.get("text", "")
    response_url = form.get("response_url")

    # 3. ACK immediately (within 3 seconds)
    ack_response = {"response_type": "ephemeral",
                    "text": "⏳ Processing... I'll reply in a moment."}

    # 4. Do the real work in background
    background_tasks.add_task(
        process_command_async, command_text, response_url, form
    )

    return JSONResponse(ack_response)

async def process_command_async(text: str, response_url: str, form: dict):
    # This runs after the 200 OK is sent — no Slack timeout pressure
    route = router.route(text)
    result = await route.agent.run(route.input)
    payload = formatter.format(result)
    await post_to_response_url(response_url, payload)
```

### Signature Verification

```python
# backend/api/middleware/signature.py
import hmac, hashlib, time, os

async def verify_slack_signature(request: Request) -> None:
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    body = await request.body()

    # Reject stale requests (replay attack protection)
    if abs(time.time() - int(timestamp)) > 300:
        raise HTTPException(status_code=403, detail="Stale request")

    sig_basestring = f"v0:{timestamp}:{body.decode()}"
    my_sig = "v0=" + hmac.new(
        os.getenv("SLACK_SIGNING_SECRET").encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(my_sig, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
```

### Command Parser

```python
# backend/slack/command_parser.py
# Parse: /sync review PR #42 focus:security
# Into:  ParsedCommand(action="review", args={"pr": 42, "focus": ["security"]})

import re
from pydantic import BaseModel
from typing import Optional, List

class ParsedCommand(BaseModel):
    action: str              # "review" | "tests" | "docs" | "status" | "help"
    pr_number: Optional[int] = None
    file_path: Optional[str] = None
    focus_areas: List[str] = []
    doc_type: Optional[str] = None
    raw_text: str

def parse_command(text: str) -> ParsedCommand:
    text = text.strip()
    parts = text.split()
    action = parts[0].lower() if parts else "help"

    pr_number = None
    if "pr" in text.lower():
        match = re.search(r"#?(\d+)", text)
        if match:
            pr_number = int(match.group(1))

    file_path = None
    if action == "tests" and len(parts) > 1:
        file_path = parts[1]

    focus_areas = []
    for part in parts:
        if part.startswith("focus:"):
            focus_areas = part.replace("focus:", "").split(",")

    return ParsedCommand(
        action=action,
        pr_number=pr_number,
        file_path=file_path,
        focus_areas=focus_areas,
        raw_text=text
    )
```

### Maestro Router

```python
# backend/maestro/router.py
# DETERMINISTIC routing — no LLM needed here

from backend.maestro.schemas import AgentName, RouteDecision
from backend.slack.command_parser import ParsedCommand

COMMAND_ROUTES = {
    "review":  AgentName.REVIEWER,
    "tests":   AgentName.TESTER,
    "docs":    AgentName.SCRIBE,
    "status":  AgentName.WATCHDOG,
}

def route(command: ParsedCommand, slack_context: dict) -> RouteDecision:
    agent = COMMAND_ROUTES.get(command.action)
    if not agent:
        raise ValueError(f"Unknown command: {command.action}")
    return RouteDecision(agent=agent, slack_context=slack_context,
                         parsed_command=command)
```

---

## LLM Client Pattern

```python
# backend/ai/llm_client.py
import anthropic, asyncio, os

class LLMClient:
    def __init__(self):
        self._client = anthropic.AsyncAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    async def complete(self, system: str, user: str,
                       max_tokens: int = 1500) -> str:
        try:
            msg = await asyncio.wait_for(
                self._client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}]
                ),
                timeout=20.0   # Leave buffer under 25s agent limit
            )
            return msg.content[0].text
        except asyncio.TimeoutError:
            raise RuntimeError("LLM timeout after 20s")
        except anthropic.APIError as e:
            raise RuntimeError(f"Anthropic API error: {e}")
```

---

## Deliverable Checklist

- [ ] All Phase 1A files: api/main.py, routes/slack.py, routes/webhook.py, middleware/signature.py
- [ ] All Phase 1B files: slack/event_handler.py, command_parser.py, message_builder.py, oauth.py
- [ ] All Phase 1C files: ai/llm_client.py, ai/prompts.py
- [ ] All Phase 1D files: mcp/github_mcp.py, mcp/jira_mcp.py
- [ ] All Phase 1E files: rts/search_client.py
- [ ] All Phase 2 files: maestro/schemas.py, router.py, formatter.py, orchestrator.py
- [ ] All Phase 8 files: Dockerfile, docker-compose.yml, render.yaml, ci.yml, manifest.json
- [ ] Corresponding unit test for every file
- [ ] No file exceeds 250 lines
- [ ] Slack signature verified on `/slack/events`, `/slack/commands`, `/slack/interactions`
- [ ] Updated REVIEW_LOG.md with completed tasks
