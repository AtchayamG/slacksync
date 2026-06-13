# Devpost Submission Draft

## Project Name

SlackSync

## Elevator Pitch

SlackSync is a Slack-native agent operations center that reviews pull requests, drafts tests, updates docs, and explains CI failures directly inside Slack.

## What It Does

SlackSync routes `/sync` commands and App Home actions through a deterministic Maestro router into four specialized agents:

- Reviewer analyzes PR risk and posts severity-ranked review notes.
- Tester drafts syntax-valid test files for target source files.
- Scribe prepares README or changelog updates from repository activity.
- Watchdog triages CI failures and suggests the likely fix path.

The local demo console mirrors the Slack experience for judging and video capture while the backend exposes Slack-ready endpoints, signature verification, MCP context evidence, and RTS context evidence.

## Built With

FastAPI, React, Vite, TypeScript, Pydantic, Slack app manifests, Block Kit-ready payload design, deterministic MCP context adapters, and Slack RTS-style context retrieval.

## Tracks

Primary: New Slack Agent.

Stretch: MCP and Real-Time Search categories through the implemented evidence adapters. Slack Agent for Organizations remains stretch until Marketplace submission is real.

## Impact

Engineering teams already work in Slack. SlackSync reduces context switching across Slack, GitHub, CI, Jira, and docs by turning Slack into the command surface and audit trail for agentic engineering workflows.

## Current Sandbox Note

Slack Developer Program activation is complete. Sandbox URL: `https://slacksync-atchayam.enterprise.slack.com`. App ID: `A0BABHV4D8E`. Judge invites were sent to `slackhack@salesforce.com` and `testing@devpost.com`.
