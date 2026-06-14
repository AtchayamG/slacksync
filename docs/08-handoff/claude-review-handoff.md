# Claude Review Handoff

Last updated: 2026-06-14.

## Project

SlackSync is a Slack-native agent operations center for the Slack Agent Builder Challenge. It routes `/sync` commands into specialized engineering agents for PR review, tests, docs, and CI triage, with deterministic demo mode plus Slack-ready endpoints.

## Current State

- Working directory: `D:\Work\Codex\Hackathon Projects\Slack Agent`
- Public repository: `https://github.com/AtchayamG/slacksync`
- Review instruction: pull latest `main` before reviewing. Product baseline commit: `7001d8a Add Block Kit formatter, CI + Pages workflows, dashboard charts, standalone console, upgraded demo video, refreshed docs + YouTube URL`
- License: MIT
- Devpost draft: `SlackSync`, draft ID `1049880-slacksync`
- Slack sandbox: `https://slacksync-atchayam.enterprise.slack.com`
- Slack app ID: `A0BABHV4D8E`
- Required judge accounts: invited to Slack sandbox
- Current public tunnel: `https://slacksync-atchayam.loca.lt`
- GitHub Pages console: `https://atchayamg.github.io/slacksync/`
- YouTube demo: `https://youtu.be/rHMgZBfL3PI`

## Verified Commands

Run from the project root:

```powershell
npm run build
npm run test
C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest -q
```

Latest results:

- `npm install` completed. npm reported 3 high severity audit findings; build and tests still pass.
- Frontend production build passed.
- Contract and web view-model tests passed.
- Backend tests: `15 passed in 0.58s`.
- Latest checked GitHub Actions CI run `27496753288`: success.
- Latest checked GitHub Pages workflow run `27496753268`: success.
- Secret-pattern scan returned no matches for Slack/OpenAI/GitHub token patterns or the sandbox password.

## Demo And Submission Artifacts

- Local video: `assets/demo-video/slacksync-demo-v2.mp4`
- Video duration: `75.8` seconds
- Voice: Edge TTS `en-US-AndrewNeural`
- Video renderer: `scripts/render_demo_video.py`
- Backup public video asset: `https://github.com/AtchayamG/slacksync/releases/download/demo-v1/slacksync-demo.mp4`
- Architecture diagram: `assets/diagrams/architecture.png`
- Live judge console: `https://atchayamg.github.io/slacksync/`
- YouTube video: `https://youtu.be/rHMgZBfL3PI`
- Devpost copy: `docs/06-demo-submission/devpost-submission-draft.md`
- Evidence checklist: `docs/06-demo-submission/submission-evidence-checklist.md`

## Current Submission State

1. Devpost project overview, project details, and Additional Info have been saved.
2. User manually uploaded `assets/diagrams/architecture.png` and saved Additional Info.
3. Codex verified the Devpost finalization page is visible with the terms checkbox and `Submit project` button.
4. Final Devpost submit remains human-controlled. Codex did not click submit.

## Review Priorities For Claude

1. Audit README and docs for truthful claims only.
2. Review UI/UX for judge impact and fix any obvious alignment or copy issues.
3. Check that demo video `https://youtu.be/rHMgZBfL3PI` is public/playable and matches the actual app.
4. Verify Devpost text clearly maps to New Slack Agent, MCP, and Real-Time Search without overclaiming Marketplace readiness or Organizations eligibility.
5. Confirm no secrets are committed.
6. Confirm local quickstart instructions work from a clean shell.

## Browser And Tooling Notes

- Chrome and in-app Browser are available for logged-in browser work.
- A separate installable `Computer Use` plugin was requested, but no exact install candidate appeared in the available plugin list.
- Chrome file upload was previously blocked, but the user has now manually completed the architecture upload.

## Do Not Do

- Do not final-submit Devpost until the user has reviewed the video URL, architecture upload, and final details.
- Do not claim Slack Marketplace approval or Organizations track eligibility unless a real Marketplace submission exists.
- Do not expose Slack secrets, tunnel tokens, passwords, or private account details in public docs.
