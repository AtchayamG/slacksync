from services.api.app.agents.watchdog.agent import run
from services.api.app.agents.watchdog.schemas import CIRun, CIStatus, EventType, WatchdogInput


def test_watchdog_triages_failed_run():
    ci_run = CIRun(
        run_id="run-42",
        status=CIStatus.FAILURE,
        branch="feature/auth",
        commit_message="tests: focus login edge cases",
        author="atchayam",
    )
    result = run(WatchdogInput(repo="atchayamg/slacksync", event_type=EventType.PUSH_WEBHOOK, ci_run=ci_run))
    assert result.status == "error"
    assert result.linked_pr_number == 42
    assert "tests failed" in result.root_cause

