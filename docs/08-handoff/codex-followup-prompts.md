# Codex Follow-Up Prompts (post Claude review)

Claude upgraded the project on 2026-06-14. Below are copy-paste prompts for Codex
to finish the remaining external/human steps, in order. Run them from
`D:\Work\Codex\Hackathon Projects\Slack Agent`.

## What Claude changed (context for Codex)

- New: `services/api/app/slack/blockkit.py` (Block Kit formatter) + `tests/unit/slack/test_blockkit.py`.
- New: `.github/workflows/ci.yml` (pytest + frontend build/test + secret scan) and `.github/workflows/pages.yml` (Pages deploy).
- Edited: `services/api/app/maestro/router.py`, `services/api/app/main.py` (attach + return Block Kit blocks), `services/api/app/demo_data.py` (truthful proof state).
- Edited: `apps/web/src/api.ts`, `apps/web/src/App.tsx`, `apps/web/vite.config.ts` (standalone-on-Pages, relative base).
- Rewrote: `README.md`, `docs/06-demo-submission/devpost-submission-draft.md`.
- Updated: evidence checklist + CTO log.
- New video: `assets/demo-video/slacksync-demo-v2.mp4` (75s, 720p, captions).
- Backend: `15 passed`. Frontend build verified on a clean checkout.

## Prompt 1 — Clean up temp files, verify, commit

```
In the SlackSync repo: delete the temporary verification frames
assets/demo-video/_check_frame_3.png, _check_frame_22.png, _check_frame_50.png,
_check_frame_72.png, _check2_3.png, and _check2_72.png (do NOT commit them).
Then run: npm install && npm run build && npm run test, and
python -m pytest -q. All must pass. Then stage everything EXCEPT the _check
frames and commit with message:
"Add Block Kit formatter, CI + Pages workflows, standalone console, upgraded demo video, refreshed docs".
Do not commit any secrets.
```

## Prompt 2 — Push and confirm CI

```
Push main to https://github.com/AtchayamG/slacksync and report back the status of
the CI and Pages GitHub Actions runs. If CI fails, show me the failing job log and
fix it.
```

## Prompt 3 — Enable the public judge console (GitHub Pages)

```
In the GitHub repo settings for AtchayamG/slacksync, enable GitHub Pages with
Source = GitHub Actions. Confirm the Pages workflow deploys and give me the live
URL (expected https://atchayamg.github.io/slacksync/). Verify the console loads
and the /sync tabs (Review, Tests, Docs, Status) all render.
```

## Prompt 4 — Publish the demo video to YouTube (human upload)

The Devpost video field only accepts YouTube/Vimeo/Facebook/Youku, and the Chrome
file picker was blocked for automation, so the upload is manual:

```
Upload this file to YouTube as an UNLISTED-or-PUBLIC video, title
"SlackSync - Slack-native engineering agent operations center":
D:\Work\Codex\Hackathon Projects\Slack Agent\assets\demo-video\slacksync-demo-v2.mp4
Devpost requires the video to be public. Once it is public, give me the watch URL.
```

(After the user provides the URL, run Prompt 5.)

## Prompt 5 — Record the YouTube URL in the repo

```
Set the demo video URL to <PASTE_YOUTUBE_URL>. Update:
- docs/06-demo-submission/devpost-submission-draft.md (the "Demo video (YouTube)" line)
- docs/06-demo-submission/submission-evidence-checklist.md (flip the YouTube row to PASS with the URL)
Then commit and push.
```

## Prompt 6 — Devpost final assembly (human submit)

```
On the Devpost SlackSync project draft (1049880-slacksync): paste the description
from docs/06-demo-submission/devpost-submission-draft.md, set the video URL to the
YouTube link, upload assets/diagrams/architecture.png, set track = New Slack Agent,
add the repo URL and the GitHub Pages URL, and the Slack sandbox URL with judge
test note. Save as draft and show me the preview. DO NOT click final submit; leave
that to the user after review.
```

## Guardrails (unchanged)

- Do not final-submit Devpost without explicit user approval.
- Do not claim Slack Marketplace approval / Organizations eligibility.
- Do not commit secrets or the _check verification frames.
