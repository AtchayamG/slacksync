import type { AgentResult } from "@slacksync/contracts";

const API_BASE = "http://127.0.0.1:8000";

// When the console is served from static hosting (e.g. GitHub Pages) there is no
// local FastAPI to reach, so callers fall back to the bundled deterministic demo
// data instead of issuing a request that is guaranteed to fail.
export function apiAvailable(): boolean {
  if (typeof window === "undefined") return true;
  const host = window.location.hostname;
  return host === "127.0.0.1" || host === "localhost";
}

export interface CommandResponse {
  parsed: {
    command: string;
    agent: string;
    target: string;
    tokens: string[];
  };
  result: AgentResult;
}

export async function runCommand(text: string): Promise<CommandResponse> {
  const response = await fetch(`${API_BASE}/api/commands`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  if (!response.ok) {
    throw new Error(`Command failed: ${response.status}`);
  }
  return response.json() as Promise<CommandResponse>;
}
