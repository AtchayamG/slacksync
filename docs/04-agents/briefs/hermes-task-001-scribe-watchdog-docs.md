# Hermes Task 001 - Scribe, Watchdog, Submission Docs

## Model Preference

Use `stepfun/step-3.7-flash:free` first. If it fails repeatedly, use another free/available Hermes model such as Nemotron Ultra only for the blocked piece.

## Ownership

You own only:

- `services/api/app/agents/scribe/`
- `services/api/app/agents/watchdog/`
- `docs/05-delivery/`
- `docs/06-demo-submission/`
- tests directly covering those files.

Do not modify Reviewer, Tester, or the web app.

## Objective

Build Scribe and Watchdog demo-capable agent flows plus submission-ready documentation skeletons.

## Requirements

- Scribe must generate README/changelog style output from demo repo activity and preserve before/after sections.
- Watchdog must parse CI webhook-like payloads and produce root cause, likely PR, and fix suggestion.
- Demo mode must be deterministic and work without secrets.
- Add docs for install, demo script, sample commands, architecture proof, and Slack sandbox status.
- Keep source files under 250 lines.
- No secret leakage.

## Done Criteria

- Relevant backend tests pass.
- Docs are specific and do not claim unavailable sandbox proof.
- Final response lists changed paths and known gaps.

