import { parseSyncCommand, scoreLabel, type AgentResult } from "@slacksync/contracts";

export function commandSummary(input: string) {
  const parsed = parseSyncCommand(input);
  return `${parsed.agent} handles ${parsed.target}`;
}

export function resultHeadline(result: AgentResult): string {
  if (result.kind === "review") {
    return `${scoreLabel(result.overallScore)} - ${result.overallScore}/100`;
  }
  if (result.kind === "tests") {
    return `${result.testFiles[0]?.testCount ?? 0} tests - ${result.coverageEstimate}% coverage`;
  }
  if (result.kind === "docs") {
    return `${result.docType} update - ${result.wordCount} words`;
  }
  return `${result.ciRuns.length} CI runs - ${result.status}`;
}

export function statusTone(status: AgentResult["status"]) {
  return status === "success" ? "good" : status === "partial" ? "warn" : "bad";
}
