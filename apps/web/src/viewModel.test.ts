import assert from "node:assert/strict";
import { results } from "./demoData";
import { commandSummary, resultHeadline, statusTone } from "./viewModel";

assert.equal(commandSummary("/sync review PR #42"), "reviewer handles PR #42");
assert.match(resultHeadline(results.review), /78\/100/);
assert.match(resultHeadline(results.tests), /86% coverage/);
assert.equal(statusTone("success"), "good");
assert.equal(statusTone("partial"), "warn");
assert.equal(statusTone("error"), "bad");

console.log("web view-model tests passed");
