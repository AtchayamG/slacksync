# Claude Review Handoff

Last updated: 2026-06-14.

## Project

SlackSync is a Slack-native agent operations center for the Slack Agent Builder Challenge. It routes `/sync` commands into specialized engineering agents for PR review, tests, docs, and CI triage, with deterministic demo mode plus Slack-ready endpoints.

## Current State

- Working directory: `D:\Work\Codex\Hackathon Projects\Slack Agent`
- Public repository: `https://github.com/AtchayamG/slacksync`
- Latest pushed commit: `bbd23b5 Polish UI and demo video proof`
- License: MIT
- Devpost draft: `SlackSync`, draft ID `1049880-slacksync`
- Slack sandbox: `https://slacksync-atchayam.enterprise.slack.com`
- Slack app ID: `A0BABHV4D8E`
- Judge invites sent: `slackhack@salesforce.com`, `testing@devpost.com`
- Current public tunnel: `https://slacksync-atchayam.loca.lt`

## Verified Commands

Run from the project root:

```powershell
npm run build
npm run test
C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest -q
```

Latest results:

- Frontend production build passed.
- Contract and web view-model tests passed.
- Backend tests: `9 passed`.

## Demo And Submission Artifacts

- Local video: `assets/demo-video/slacksync-demo.mp4`
- Video duration: `75.288` seconds
- Voice: Edge TTS `en-US-AndrewNeural`
- Video renderer: `scripts/render_demo_video.py`
- Backup public video asset: `https://github.com/AtchayamG/slacksync/releases/download/demo-v1/slacksync-demo.mp4`
- Architecture diagram: `assets/diagrams/architecture.png`
- Devpost copy: `docs/06-demo-submission/devpost-submission-draft.md`
- Evidence checklist: `docs/06-demo-submission/submission-evidence-checklist.md`

## Known Blockers

1. Devpost video field requires YouTube, Vimeo, Facebook Video, or Youku. The GitHub release URL is a backup only.
2. YouTube Studio upload dialog opened, but Chrome automation file attachment returned `Not allowed`. Manual upload path:

```text
D:\Work\Codex\Hackathon Projects\Slack Agent\assets\demo-video\slacksync-demo.mp4
```

3. Devpost architecture upload still needs `assets/diagrams/architecture.png`.
4. Final Devpost submit should remain human-controlled after the video URL and architecture upload are confirmed.

## Review Priorities For Claude

1. Audit README and docs for truthful claims only.
2. Review UI/UX for judge impact and fix any obvious alignment or copy issues.
3. Check that demo video slides are readable and match the actual app.
4. Verify Devpost text clearly maps to New Slack Agent, MCP, and Real-Time Search without overclaiming Marketplace readiness.
5. Confirm no secrets are committed.
6. Confirm local quickstart instructions work from a clean shell.

## Browser And Tooling Notes

- Chrome and in-app Browser are available for logged-in browser work.
- A separate installable `Computer Use` plugin was requested, but no exact install candidate appeared in the available plugin list.
- Chrome file upload may still be blocked despite extension file URL access being enabled; use manual selection if needed.

## Do Not Do

- Do not final-submit Devpost until the user has reviewed the video URL, architecture upload, and final details.
- Do not claim Slack Marketplace approval or Organizations track eligibility unless a real Marketplace submission exists.
- Do not expose Slack secrets, tunnel tokens, passwords, or private account details in public docs.
