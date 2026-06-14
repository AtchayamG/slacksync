# Final Review Prompt For Claude

Use this prompt for the last Claude pass before the user decides whether to submit.

```text
Finalize-review SlackSync for the Slack Agent Builder Challenge, but do not click final submit unless I explicitly authorize it in this Claude session after your review.

Work from:
D:\Work\Codex\Hackathon Projects\Slack Agent

Latest known good commit:
7001d8a Add Block Kit formatter, CI + Pages workflows, dashboard charts, standalone console, upgraded demo video, refreshed docs + YouTube URL

Public artifacts:
- Repo: https://github.com/AtchayamG/slacksync
- Pages console: https://atchayamg.github.io/slacksync/
- YouTube demo: https://youtu.be/rHMgZBfL3PI
- Slack sandbox: https://slacksync-atchayam.enterprise.slack.com
- Architecture image in repo: assets/diagrams/architecture.png
- Devpost draft: project 1049880-slacksync

Known verification:
- `npm install` completed; npm reported 3 high severity audit findings.
- `npm run build` passed.
- `npm run test` passed.
- `C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest -q` passed with 15 tests.
- GitHub Actions CI run 27494987041 succeeded.
- GitHub Pages workflow run 27495044194 succeeded.
- Devpost Additional Info architecture upload was completed manually and the finalization page is visible.

Your review checklist:
1. Pull/inspect the latest repo state and confirm there are no uncommitted secrets or temp demo frames.
2. Re-run build/tests if time permits. If anything fails, stop and show the log.
3. Open the Pages console and verify it loads, the Review/Tests/Docs/Status tabs render, and the bar + donut charts are visible.
4. Open the YouTube demo and confirm it is playable and under 3 minutes.
5. Review the Devpost draft/preview for truthful claims only. It must use Track: New Slack Agent.
6. Do not claim Slack Marketplace approval or Organizations-track eligibility.
7. Do not put judge email addresses, secrets, tokens, passwords, or private account details in any public field.
8. Confirm the architecture image is present in Additional Info.
9. Leave final submit untouched unless I explicitly say: "Claude, final-submit SlackSync now."

Report back in this format:
PASS:
RISKS:
MUST FIX BEFORE SUBMIT:
OPTIONAL POLISH:
FINAL SUBMIT READINESS:
```

## Guardrails

- Do not final-submit Devpost without explicit user approval.
- Do not claim Slack Marketplace approval or Organizations eligibility.
- Do not commit secrets or `_*.png` verification frames.
- Do not expose judge email addresses in public fields.
