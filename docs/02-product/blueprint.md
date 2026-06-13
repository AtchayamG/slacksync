# SlackSync Product Blueprint

## Product Thesis

SlackSync is a Slack-native agent operations center for engineering teams. It turns Slack into the command surface for code review, test generation, documentation updates, and CI failure triage using Slack Agent Builder, MCP integrations, and Real-Time Search.

## Winning Angle

Most hackathon entries will be simple assistants. SlackSync should feel like a real operational product:

- Slack App Home as a dashboard.
- Slash commands for daily engineering workflows.
- Threaded Block Kit outputs with action buttons.
- Real-time search for workspace context.
- MCP integrations for GitHub/Jira/tool access.
- A polished web demo console for judges and video capture.

## Primary User

A small engineering team that already lives in Slack and wants fewer context switches between Slack, GitHub, CI, Jira, and docs.

## Core Demo Workflow

1. Open SlackSync App Home and show weekly engineering pulse.
2. Run `/sync review PR #42`.
3. Show Reviewer agent collecting PR diff, Slack RTS context, and MCP data.
4. Post a structured review card with severity, score, and actions.
5. Run `/sync tests services/auth.py`.
6. Post generated test summary and syntax-valid test snippet.
7. Run `/sync docs changelog`.
8. Show Scribe diff preview from commits and Slack context.
9. Trigger CI failure webhook.
10. Watchdog posts root cause, likely PR, and fix suggestion.

## Architecture Decisions

- Backend: FastAPI with Slack signature verification and async task routing.
- Slack surface: slash commands, app mentions, App Home, modals, Block Kit messages.
- Integrations: Slack Agent Builder/AI, MCP wrappers, Slack RTS client, GitHub/Jira adapters.
- Demo mode: deterministic local sample data that runs without secrets.
- Production mode: environment-driven Slack credentials and real tool tokens.
- Web app: polished judge dashboard mirroring Slack state for video and local inspection.

## UX Direction

Professional, futuristic, Slack-native, and dense enough for operational work:

- Dark/light support.
- Activity timeline.
- Agent status cards.
- Slack-like threaded message preview.
- Command palette / slash command simulator.
- Architecture/proof panel.
- No marketing-only landing page as the main experience.

## Success Criteria

- The app runs locally without real Slack secrets in demo mode.
- At least four agent flows are executable through API/UI simulation.
- Block Kit payloads are valid, inspectable, and tested.
- Slack signature verification is implemented for real mode.
- README and docs make judge setup obvious.
- Demo video can be built from real app/CLI/browser footage.
