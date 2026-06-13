# AGENT_BRIEF_ANTIGRAVITY.md - Imported Reference Summary

Antigravity was intended to own the Reviewer agent, Tester agent, and polished product UI. The original brief has been compacted into public-repo-safe implementation guidance.

## Ownership

- `services/api/app/agents/reviewer/`
- `services/api/app/agents/tester/`
- `apps/web/src/`
- Shared contracts in `packages/contracts/src/`

## Reviewer Expectations

- Parse PR-oriented user intent.
- Produce a risk score, concise findings, and practical next actions.
- Keep output deterministic for tests and demo reliability.

## Tester Expectations

- Translate user targets into useful test plans.
- Prefer executable and maintainable tests over generic advice.
- Validate generated code shape before presenting it as runnable.

## UI Expectations

- Professional Slack-native engineering console aesthetic.
- Clear agent status, workflow timeline, approvals, and activity feed.
- Responsive layout that works on desktop and mobile.
- No marketing-only landing page as the primary experience.

## Guardrails

- Keep files compact.
- Keep UI state predictable and testable.
- Do not claim marketplace approval or paid integrations until they exist.

