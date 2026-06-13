import assert from "node:assert/strict";
import { parseSyncCommand, scoreLabel } from "./index";

assert.deepEqual(
  { ...parseSyncCommand("/sync review PR #42"), tokens: ["PR", "#42"] },
  { command: "review", agent: "reviewer", target: "PR #42", tokens: ["PR", "#42"] }
);

assert.equal(parseSyncCommand("/sync tests services/auth.py").agent, "tester");
assert.equal(parseSyncCommand("/sync docs changelog").agent, "scribe");
assert.equal(parseSyncCommand("/sync status").agent, "watchdog");
assert.throws(() => parseSyncCommand("/deploy prod"), /\/sync/);
assert.throws(() => parseSyncCommand("/sync shipit"), /Unsupported/);

assert.equal(scoreLabel(91), "Merge ready");
assert.equal(scoreLabel(78), "Needs changes");
assert.equal(scoreLabel(42), "High risk");

console.log("contracts tests passed");
