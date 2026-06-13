# AGENT_BRIEF_HERMES.md - Imported Reference Summary

Hermes was intended to own the Scribe agent, Watchdog agent, and submission documentation. The useful parts of the original brief are retained below as implementation guidance.

## Ownership

- `services/api/app/agents/scribe/`
- `services/api/app/agents/watchdog/`
- `docs/05-delivery/`
- `docs/06-demo-submission/`

## Scribe Expectations

- Read existing documentation context before proposing updates.
- Return concise section-level diffs or documentation recommendations.
- Avoid claiming unimplemented integrations in user-facing docs.
- Include deterministic test coverage for public behavior.

## Watchdog Expectations

- Focus on warning and failure signals, not noisy success notifications.
- Produce a short risk summary and concrete next actions.
- Keep output schema stable for the router and UI.
- Include deterministic test coverage for status and recommendation behavior.

## Documentation Expectations

- Keep every public file compact and judge-friendly.
- Maintain a demo script, install guide, architecture proof, and submission checklist.
- Clearly separate implemented functionality from planned stretch goals.

## Guardrails

- No hardcoded secrets or token-shaped placeholders.
- No dependency on paid services for the core local demo.
- Favor deterministic demo data when real external APIs are unavailable.

