# Devpost Submission Draft

## Project Name

SlackSync

## Elevator Pitch

SlackSync turns Slack into an engineering agent operations center: one `/sync`
command reviews pull requests, drafts tests, updates docs, and explains CI
failures — and posts the answer back into the thread as Block Kit, with the
context evidence behind it.

## Inspiration

Engineering teams already coordinate in Slack, but the actual work — reviewing a
PR, writing tests, updating docs, figuring out why CI went red — happens in a
dozen other tabs. Every context switch is lost time and lost context. We wanted
the place where the team already talks to also be the place where the work gets
done and audited.

## What It Does

SlackSync routes `/sync` commands and App Home actions through a deterministic
Maestro router into four specialized agents:

- **Reviewer** analyzes PR risk and posts severity-ranked review notes with a
  merge-readiness score.
- **Tester** drafts syntax-valid test files for a target source file and
  estimates coverage.
- **Scribe** prepares README or changelog updates from repository activity.
- **Watchdog** triages CI failures, names the likely root cause, and suggests
  the fix path.

Every result is a typed data contract that a dedicated Block Kit formatter layer
renders into a threaded Slack message, and every result carries the MCP and
Real-Time Search context it was based on, so the answer is auditable.

## How We Built It

- **Backend:** FastAPI with a Maestro command router, four agent modules, typed
  Pydantic schemas, a Slack signature-verification layer (5-minute replay
  window), and a Block Kit formatter that keeps presentation out of agent logic.
- **Integration boundaries:** an MCP context adapter (GitHub/Jira) and a
  Real-Time Search adapter (Slack channel context). In demo mode they return
  deterministic, clearly-labeled fixtures so the whole system runs with zero
  secrets; in real mode they are the seams where live clients plug in.
- **Frontend:** a React + Vite + TypeScript judge console that mirrors the Slack
  experience, calls the FastAPI route when available, and otherwise falls back
  to the same deterministic data so it can be hosted statically on GitHub Pages.
- **Shared contracts:** a TypeScript contracts package keeps the UI and API
  payloads aligned.
- **Quality:** GitHub Actions CI runs backend pytest, the frontend build and
  tests, and a secret scan on every push.

## How It Meets the Required Technologies

- **Slack Agent / Agent Builder:** an installed Slack app answers the `/sync`
  slash command through the FastAPI webhook and returns Block Kit.
- **MCP:** `services/api/app/integrations/mcp_context.py` attaches GitHub/Jira
  MCP evidence to every routed result, asserted by tests.
- **Real-Time Search:** `services/api/app/integrations/rts_search.py` attaches
  matching Slack channel context, asserted by tests.

## Challenges We Ran Into

Keeping the project demo-able with zero secrets while still proving the real
Slack path was the central tension. We solved it by making agent outputs typed
data contracts and treating Slack signature verification, MCP, and RTS as
explicit, testable boundaries — real where it counts, deterministic where a
secret would otherwise be required, and clearly labeled either way.

## Accomplishments We're Proud Of

A working `/sync` command live in a Slack sandbox, four agents behind one
deterministic router, a Block Kit formatter layer, MCP and RTS evidence on every
answer, a public judge console, green CI, and an end-to-end demo that needs no
secrets to run.

## What We Learned

Designing agent outputs as data contracts first — and pushing all Slack
formatting into one layer — made the system far easier to test, demo, and
extend than wiring Block Kit through the agents would have.

## What's Next

Live MCP and Real-Time Search clients behind the existing adapters, App Home
dashboards and interactive approvals, and a path toward a Slack Marketplace
listing once the product is hardened.

## Built With

FastAPI, Python, Pydantic, React, Vite, TypeScript, Slack app manifests, Block
Kit, GitHub Actions, deterministic MCP context adapters, and Slack RTS-style
context retrieval.

## Tracks

Primary: **New Slack Agent**. The implemented MCP and Real-Time Search evidence
adapters also align with those category prizes. Slack Agent for Organizations
remains a stretch and is not claimed until a real Marketplace submission exists.

## Impact

Engineering teams already work in Slack. SlackSync reduces context switching
across Slack, GitHub, CI, Jira, and docs by turning Slack into the command
surface and the audit trail for agentic engineering workflows.

## Sandbox & Judge Access

- Slack sandbox: `https://slacksync-atchayam.enterprise.slack.com`
- Slack App ID: `A0BABHV4D8E`
- Required judge accounts have been invited to the Slack sandbox
- Public repository: `https://github.com/AtchayamG/slacksync` (MIT)
- Architecture diagram: `assets/diagrams/architecture.png`
- Demo video (YouTube): https://youtu.be/rHMgZBfL3PI
