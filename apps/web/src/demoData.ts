import type { AgentResult, SyncCommand } from "@slacksync/contracts";

const context = {
  mcp: [
    { source: "github", title: "PR diff, touched files, and reviewer history", relevance: 94 },
    { source: "jira", title: "Linked delivery ticket and acceptance criteria", relevance: 86 }
  ],
  rts: [
    { channel: "#dev-agent-ops", snippet: "Security focus requested for PR review before merge.", score: 95 },
    { channel: "#backend", snippet: "Replay protection tests passed on the latest branch.", score: 90 }
  ]
};

export const commands: Array<{ id: SyncCommand; label: string; prompt: string }> = [
  { id: "review", label: "Review", prompt: "/sync review PR #42 focus:security" },
  { id: "tests", label: "Tests", prompt: "/sync tests services/auth.py framework:pytest" },
  { id: "docs", label: "Docs", prompt: "/sync docs changelog" },
  { id: "status", label: "Status", prompt: "/sync status" }
];

export const results: Record<SyncCommand, AgentResult> = {
  review: {
    kind: "review",
    status: "partial",
    prTitle: "PR #42 - Add Slack OAuth handoff",
    prUrl: "https://github.com/slacksync/demo/pull/42",
    overallScore: 78,
    comments: [
      {
        filePath: "services/api/app/slack/oauth.py",
        lineNumber: 61,
        severity: "warning",
        category: "security",
        message: "State validation should expire redeemed nonces before token exchange.",
        suggestedFix: "Move nonce invalidation before the OAuth client call."
      },
      {
        filePath: "apps/web/src/session.ts",
        lineNumber: 18,
        severity: "suggestion",
        category: "test",
        message: "Add a replay test for stale Slack install sessions."
      }
    ],
    summary: "Reviewer found a solid implementation with one pre-merge OAuth hardening item and one test follow-up.",
    executionMs: 1840,
    context
  },
  tests: {
    kind: "tests",
    status: "success",
    sourceFile: "services/auth.py",
    coverageEstimate: 86,
    testFiles: [
      {
        filePath: "tests/test_auth_tokens.py",
        content: "def test_rejects_expired_token(): ...",
        testCount: 8,
        isSyntaxValid: true
      }
    ],
    summary: "Generated 8 pytest cases covering token expiry, missing claims, and malformed headers.",
    executionMs: 1210,
    context
  },
  docs: {
    kind: "docs",
    status: "success",
    docType: "changelog",
    sections: [
      {
        sectionName: "Unreleased",
        before: "No Slack workflow notes.",
        after: "Added Slack App Home pulse, /sync command routing, and CI failure triage notes."
      }
    ],
    wordCount: 214,
    summary: "Scribe prepared a changelog section from commits and #dev launch notes.",
    executionMs: 970,
    context
  },
  status: {
    kind: "status",
    status: "partial",
    summary: "Watchdog found one failed run on feature/auth and four healthy mainline runs.",
    rootCause: "The auth smoke test is still calling the previous token refresh path.",
    fixSuggestion: "Update the fixture to seed the new refresh grant before CI smoke tests.",
    linkedPrNumber: 42,
    executionMs: 640,
    context,
    ciRuns: [
      {
        runId: "6248",
        status: "failure",
        branch: "feature/auth",
        commitSha: "a13c9d2",
        commitMessage: "Wire Slack OAuth handoff",
        author: "@atchayam",
        startedAt: "2026-06-13T16:50:00Z",
        failedStep: "auth smoke"
      },
      {
        runId: "6247",
        status: "success",
        branch: "main",
        commitSha: "c91b0ee",
        commitMessage: "Add deterministic demo fixtures",
        author: "@codex",
        startedAt: "2026-06-13T15:42:00Z"
      }
    ]
  }
};

export const timeline = [
  "Slash command acknowledged in 180 ms",
  "Maestro routed command to deterministic agent",
  "MCP and Slack RTS context attached in demo mode",
  "Block Kit response posted back to the source thread"
];
