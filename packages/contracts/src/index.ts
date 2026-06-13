export type AgentName = "reviewer" | "tester" | "scribe" | "watchdog";
export type AgentStatus = "ready" | "running" | "blocked" | "complete";
export type ResultStatus = "success" | "partial" | "error";
export type Severity = "error" | "warning" | "suggestion" | "info";
export type SyncCommand = "review" | "tests" | "docs" | "status";

export interface IntegrationEvidence {
  mcp: Array<{ source: string; title: string; relevance: number }>;
  rts: Array<{ channel: string; snippet: string; score: number }>;
}

export interface SlackContext {
  teamId: string;
  channelId: string;
  userId: string;
  threadTs?: string;
  messageTs?: string;
  sessionId: string;
}

export interface ReviewComment {
  filePath: string;
  lineNumber?: number;
  severity: Severity;
  category: string;
  message: string;
  suggestedFix?: string;
}

export interface ReviewResult {
  kind: "review";
  status: ResultStatus;
  prTitle: string;
  prUrl: string;
  overallScore: number;
  comments: ReviewComment[];
  summary: string;
  executionMs: number;
  context?: IntegrationEvidence;
}

export interface TestFile {
  filePath: string;
  content: string;
  testCount: number;
  isSyntaxValid: boolean;
}

export interface TestResult {
  kind: "tests";
  status: ResultStatus;
  sourceFile: string;
  testFiles: TestFile[];
  coverageEstimate: number;
  summary: string;
  executionMs: number;
  context?: IntegrationEvidence;
}

export interface DocResult {
  kind: "docs";
  status: ResultStatus;
  docType: "readme" | "changelog" | "inline";
  sections: Array<{ sectionName: string; before?: string; after: string }>;
  wordCount: number;
  summary: string;
  executionMs: number;
  context?: IntegrationEvidence;
}

export interface CiRun {
  runId: string;
  status: "success" | "failure" | "cancelled" | "in_progress";
  branch: string;
  commitSha: string;
  commitMessage: string;
  author: string;
  startedAt: string;
  finishedAt?: string;
  failedStep?: string;
}

export interface CiResult {
  kind: "status";
  status: ResultStatus;
  ciRuns: CiRun[];
  rootCause?: string;
  fixSuggestion?: string;
  linkedPrNumber?: number;
  summary: string;
  executionMs: number;
  context?: IntegrationEvidence;
}

export type AgentResult = ReviewResult | TestResult | DocResult | CiResult;

export interface CommandParseResult {
  command: SyncCommand;
  agent: AgentName;
  target: string;
  tokens: string[];
}

const routes: Record<SyncCommand, AgentName> = {
  review: "reviewer",
  tests: "tester",
  docs: "scribe",
  status: "watchdog"
};

export function parseSyncCommand(input: string): CommandParseResult {
  const parts = input.trim().split(/\s+/).filter(Boolean);
  if (parts[0] !== "/sync") {
    throw new Error("Command must start with /sync");
  }
  const command = parts[1] as SyncCommand | undefined;
  if (!command || !(command in routes)) {
    throw new Error("Unsupported /sync command");
  }
  const tokens = parts.slice(2);
  return {
    command,
    agent: routes[command],
    target: tokens.join(" ") || "workspace",
    tokens
  };
}

export function scoreLabel(score: number): "Merge ready" | "Needs changes" | "High risk" {
  if (score >= 80) return "Merge ready";
  if (score >= 50) return "Needs changes";
  return "High risk";
}
