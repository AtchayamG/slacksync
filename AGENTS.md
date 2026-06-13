# SlackSync Agent Rules

This repository is a hackathon production build. Keep edits focused, testable, and demo-ready.

## Non-negotiables

- Do not commit or print secrets. Never hardcode Slack tokens, app tokens, API keys, GitHub tokens, OAuth codes, or payment details.
- Every source file should stay under 250 lines unless there is a strong reason and the CTO reviewer approves it.
- Demo mode must work without real Slack, GitHub, Jira, or LLM secrets.
- Real mode must verify Slack request signatures before processing Slack webhooks.
- Agent outputs are data contracts first; Slack Block Kit formatting happens in a formatter layer.
- Do not claim a feature is real if it is only simulated. Label demo-mode behavior clearly in docs.

## Product Intent

SlackSync should feel like an operational Slack product, not a marketing page:

- Fast App Home dashboard.
- Dense but readable engineering metrics.
- Threaded Slack message previews.
- Command simulator for `/sync review`, `/sync tests`, `/sync docs`, and `/sync status`.
- Architecture and submission proof panels.

## Coordination

Multiple agents may work in this repository. Do not revert unrelated changes. If a file changed since you last read it, re-read it and adapt.
