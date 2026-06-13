# Three-Minute Demo Script

## 0:00-0:20 - Hook

Show SlackSync dashboard and say: "SlackSync turns Slack into an engineering agent operations center. Review, tests, docs, and CI triage happen from one `/sync` command."

## 0:20-0:55 - Command Router

Click Review, Tests, Docs, and Status in the command simulator. Show the deterministic route line and Slack thread preview updating.

## 0:55-1:35 - Agent Workflows

Show Reviewer comments, Tester generated test file, Scribe changelog section, and Watchdog root cause analysis.

## 1:35-2:10 - Architecture

Show architecture proof: Slack surfaces -> FastAPI -> Maestro -> specialized agents -> Block Kit. Mention MCP and RTS are explicit adapter boundaries.

## 2:10-2:40 - Slack Readiness

Show `ops/slack-app-manifest.json`, Slack request signature tests, and `/slack/commands` route. State demo mode avoids secrets while real mode validates Slack signatures.

## 2:40-3:00 - Impact

Close with impact: fewer context switches, faster PR review, faster CI recovery, and auditable human-in-the-loop Slack threads.

