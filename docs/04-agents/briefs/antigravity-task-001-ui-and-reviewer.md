# Antigravity Task 001 - UI Shell, Reviewer, Tester

## Model Preference

Use Antigravity 3.5 Flash High first if available.

## Ownership

You own only:

- `apps/web/`
- `services/api/app/agents/reviewer/`
- `services/api/app/agents/tester/`
- tests directly covering those files.

Do not modify Scribe, Watchdog, deployment, or submission docs.

## Objective

Build the polished SlackSync demo console and the Reviewer/Tester agent flows. The app must feel like a professional Slack-native engineering command center.

## Requirements

- Use the reference direction from `docs/02-product/blueprint.md`.
- Demo mode must run without secrets.
- Reviewer flow must return a typed review result with score, severity comments, Slack context sources, and suggested actions.
- Tester flow must return generated test files with syntax validation status.
- UI must include command simulator, agent status cards, Slack thread preview, and workflow timeline.
- Keep source files under 250 lines.
- Add tests for parsers/validators and UI data transforms where practical.

## Done Criteria

- `npm run build` succeeds.
- Relevant backend tests pass.
- Demo UI shows all states without overlapping text at desktop and mobile widths.
- Final response lists changed paths and any known gaps.

