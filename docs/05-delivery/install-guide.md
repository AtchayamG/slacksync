# Install Guide

## Local Demo

```powershell
cd "D:\Work\Codex\Hackathon Projects\Slack Agent"
copy .env.example .env
npm.cmd install
npm.cmd run build
npm.cmd run test
C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pip install -r services\api\requirements.txt
C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pytest -q
```

Run the backend:

```powershell
C:\Users\Atchayam\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m uvicorn services.api.app.main:app --reload --port 8000
```

Run the web console:

```powershell
npm.cmd run dev
```

Open `http://127.0.0.1:5174/`.

## Slack Setup

1. Create a Slack app from `ops/slack-app-manifest.json`.
2. Set request URLs after deployment:
   - Slash command: `<APP_BASE_URL>/slack/commands`
   - Interactivity: `<APP_BASE_URL>/slack/interactions`
   - Events: `<APP_BASE_URL>/slack/events`
3. Copy Slack credentials into `.env`.
4. Keep `APP_ENV=demo` until real Slack credentials are available.

## Sandbox Status

Slack Developer Program is active. Sandbox URL: `https://slacksync-atchayam.enterprise.slack.com`.
