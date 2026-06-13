# AGENT_CONTRACTS.md — SlackSync Agent Contracts

> Owner: Claude Fable | All agents MUST conform to these schemas exactly.
> Pydantic validation runs at runtime — schema violations raise HTTP 422.

---

## Contract Rules (All Agents)

1. Every sub-agent has a single `run(input) -> output` async method
2. All inputs/outputs are Pydantic models defined in each agent's `schemas.py`
3. Agents never import from each other — only from `backend/mcp/`, `backend/ai/`, `backend/rts/`
4. Every `run()` must complete within 25 seconds (Slack async timeout buffer)
5. Agents always return a result even on partial failure — never raise unhandled exceptions
6. All Slack message payloads are built by `maestro/formatter.py` — agents return data, not Slack JSON

---

## Shared Types (backend/maestro/schemas.py)

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class AgentName(str, Enum):
    REVIEWER = "reviewer"
    TESTER = "tester"
    SCRIBE = "scribe"
    WATCHDOG = "watchdog"

class AgentStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"      # completed with warnings
    ERROR = "error"

class SlackContext(BaseModel):
    """Passed to every agent — identifies the originating Slack event."""
    team_id: str
    channel_id: str
    user_id: str
    thread_ts: Optional[str] = None   # Reply in thread if set
    message_ts: Optional[str] = None
    session_id: str                   # UUID for this request lifecycle
```

---

## Agent: Reviewer — Schemas

```python
# backend/agents/reviewer/schemas.py

class ReviewInput(BaseModel):
    slack_context: SlackContext
    repo: str                          # e.g. "org/project"
    pr_number: int
    focus_areas: List[str] = []        # e.g. ["security", "performance"]

class Severity(str, Enum):
    ERROR = "error"                    # Must fix before merge
    WARNING = "warning"                # Should fix
    SUGGESTION = "suggestion"          # Nice to have
    INFO = "info"                      # Informational

class ReviewComment(BaseModel):
    file_path: str
    line_number: Optional[int] = None
    severity: Severity
    category: str                      # "security" | "logic" | "naming" | "perf" | "test"
    message: str                       # What the issue is
    suggested_fix: Optional[str] = None

class ReviewResult(BaseModel):
    status: AgentStatus
    pr_title: str
    pr_url: str
    overall_score: int                 # 0–100
    comments: List[ReviewComment]
    summary: str                       # 2–3 sentence overall assessment
    error_message: Optional[str] = None
    execution_ms: int
```

**Maestro formatter will:**
- Convert `overall_score` → 🟢 (80+) / 🟡 (50–79) / 🔴 (<50) badge
- Group `comments` by `file_path` into Block Kit sections
- Create action buttons: [View PR] and [Create JIRA Ticket] (if errors found)

---

## Agent: Tester — Schemas

```python
# backend/agents/tester/schemas.py

class TesterInput(BaseModel):
    slack_context: SlackContext
    repo: str
    file_path: str                     # File to generate tests for
    branch: str = "main"
    test_framework: str = "pytest"     # "pytest" | "jest" | "unittest"
    coverage_target: int = 80          # Target % coverage

class TestFile(BaseModel):
    file_path: str                     # Where the test file should live
    content: str                       # Full test file source code
    test_count: int                    # Number of test functions
    is_syntax_valid: bool              # Passed compile/parse check

class TestResult(BaseModel):
    status: AgentStatus
    source_file: str
    test_files: List[TestFile]
    coverage_estimate: int             # Estimated % coverage if tests pass
    summary: str                       # "Generated 12 tests covering X, Y, Z"
    error_message: Optional[str] = None
    execution_ms: int
```

**Maestro formatter will:**
- Post summary as threaded reply
- Attach test file content as Slack file snippet (expandable)
- Add [Create PR with tests] action button

---

## Agent: Scribe — Schemas

```python
# backend/agents/scribe/schemas.py

class DocType(str, Enum):
    README = "readme"
    CHANGELOG = "changelog"
    INLINE = "inline"

class ScribeInput(BaseModel):
    slack_context: SlackContext
    repo: str
    branch: str = "main"
    doc_type: DocType = DocType.README
    commit_range: Optional[str] = None  # For changelog: "v1.0..HEAD"

class DocSection(BaseModel):
    section_name: str                   # e.g. "Quick Start", "API Reference"
    before: Optional[str] = None        # Previous content (None if new section)
    after: str                          # New content

class DocResult(BaseModel):
    status: AgentStatus
    doc_type: DocType
    sections: List[DocSection]
    full_content: str                   # Complete new file content
    word_count: int
    summary: str                        # "Updated 3 sections, added API reference"
    error_message: Optional[str] = None
    execution_ms: int
```

**Maestro formatter will:**
- Show diff preview (before/after) for changed sections in Block Kit
- Collapse unchanged sections
- Add [Create PR with docs] action button

---

## Agent: Watchdog — Schemas

```python
# backend/agents/watchdog/schemas.py

class CIEventType(str, Enum):
    PUSH_WEBHOOK = "push_webhook"      # Triggered by CI/CD webhook
    MANUAL_STATUS = "manual_status"   # Triggered by /sync status command

class CIRunStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"

class CIRun(BaseModel):
    run_id: str
    status: CIRunStatus
    branch: str
    commit_sha: str
    commit_message: str
    author: str
    started_at: str                    # ISO-8601
    finished_at: Optional[str] = None
    logs_url: Optional[str] = None
    failed_step: Optional[str] = None  # Name of failing step/job

class WatchdogInput(BaseModel):
    slack_context: SlackContext
    event_type: CIEventType
    repo: str
    ci_run: Optional[CIRun] = None    # Set for PUSH_WEBHOOK
    channel_override: Optional[str] = None  # Post to specific channel

class CIResult(BaseModel):
    status: AgentStatus
    ci_runs: List[CIRun]              # 1 for webhook, 5 for /sync status
    root_cause: Optional[str] = None  # AI-written, only on FAILURE
    fix_suggestion: Optional[str] = None
    linked_pr_number: Optional[int] = None  # PR likely responsible
    linked_pr_url: Optional[str] = None
    summary: str
    error_message: Optional[str] = None
    execution_ms: int
```

**Maestro formatter will:**
- For FAILURE: post alert with ❌ header, root cause, linked PR, action buttons
- For STATUS: post compact run history table (last 5 runs with status badges)

---

## Maestro Router Contract

```python
# backend/maestro/router.py

class RouteDecision(BaseModel):
    agent: AgentName
    input_payload: dict                # Validated by the target agent's Input schema
    respond_in_thread: bool = True
    channel_id: str
    team_id: str

# Routing table (in router.py — not via LLM, deterministic):
COMMAND_ROUTES = {
    "review":  AgentName.REVIEWER,
    "tests":   AgentName.TESTER,
    "docs":    AgentName.SCRIBE,
    "status":  AgentName.WATCHDOG,
}
```

**Rule:** Routing is always deterministic from the command keyword. Never use an LLM to decide which agent runs — that adds latency and failure modes.

---

## Formatter Contract (maestro/formatter.py)

```python
# Every format_* function returns a Slack API-ready dict

def format_review_result(result: ReviewResult) -> dict:
    """Returns Slack chat.postMessage payload with blocks."""
    ...

def format_test_result(result: TestResult) -> dict:
    """Returns Slack chat.postMessage payload + files.upload call."""
    ...

def format_doc_result(result: DocResult) -> dict:
    """Returns Slack chat.postMessage payload with diff sections."""
    ...

def format_ci_result(result: CIResult, event_type: CIEventType) -> dict:
    """Returns Slack chat.postMessage payload."""
    ...

def format_error(agent: AgentName, error: str) -> dict:
    """Returns a user-friendly error Block Kit message."""
    ...
```

**All formatters must:**
- Never exceed 50 blocks per message (Slack limit)
- Include a fallback `text` field for notification previews
- Use Block Kit `actions` block for every actionable result
