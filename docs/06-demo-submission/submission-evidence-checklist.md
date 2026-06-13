# Submission Evidence Checklist

| Requirement | Evidence | Status | Owner | Verification |
|---|---|---|---|---|
| India eligibility and age | `docs/01-hackathon/slack-hackathon-requirements.md` | PASS | Codex/user | Official rules read; user confirmed DOB and country |
| Devpost registration | Devpost manager page shows registered project draft | PASS | Codex | Browser showed Thanks for registering |
| Devpost project draft | SlackSync draft ID `1049880-slacksync` | PASS | Codex | Project overview saved |
| Slack Developer Program | Activated Slack Developer Program dashboard | PASS | User/Codex | Confirmation email activated; dashboard visible |
| Slack developer sandbox | `https://slacksync-atchayam.enterprise.slack.com` | PASS | User/Codex | Slack Developer Program shows `SlackSync Sandbox`, active 1/2, archives in 181 days |
| Slack sandbox judge access | Invites to `slackhack@salesforce.com`, `testing@devpost.com` | PASS | Codex | Slack invite confirmation: both invited as coworkers, expires in 30 days |
| Slack app installed | App ID `A0BABHV4D8E` in SlackSync Sandbox | PASS | Codex | `/sync review PR #42` returned SlackSync ephemeral response at 2:15 AM IST |
| Slack slash command webhook | `/slack/commands` through `https://slacksync-atchayam.loca.lt` | PASS | Codex | `/sync status` returned `2 recent runs; 1 failure in feature/auth.` |
| Public repository | `https://github.com/AtchayamG/slacksync` | PASS | Codex | GitHub reports visibility `PUBLIC`, default branch `main` |
| Open-source license | `LICENSE` | PASS | Codex | GitHub detects MIT License |
| Architecture diagram | `assets/diagrams/architecture.png` and `.svg` | PASS | Codex | Matches Slack -> tunnel -> FastAPI -> Maestro -> MCP/RTS -> agents -> web console |
| Demo video under 3 minutes | `https://github.com/AtchayamG/slacksync/releases/download/demo-v1/slacksync-demo.mp4` | PASS | Codex | MP4 is 99 seconds with narration; release asset is public |
| Project uses Agent Builder | Installed Slack app plus `/sync` agent command | PASS | Codex | Working command in sandbox with app response |
| Project uses MCP | `services/api/app/integrations/mcp_context.py` | PASS | Codex | API result includes GitHub/Jira MCP evidence and tests assert it |
| Project uses RTS API | `services/api/app/integrations/rts_search.py` | PASS | Codex | API result includes `#dev-agent-ops` RTS evidence and tests assert it |
| Final Devpost submit | Confirmation page | TODO | User | Human final review |
