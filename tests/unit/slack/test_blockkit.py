from services.api.app.maestro.router import run_command
from services.api.app.slack.blockkit import format_result


def _result(text: str) -> dict:
    return run_command(text)["result"]


def _block_types(blocks: list[dict]) -> list[str]:
    return [block["type"] for block in blocks]


def test_review_blocks_have_header_and_score():
    blocks = format_result(_result("/sync review PR #42"))
    types = _block_types(blocks)
    assert types[0] == "header"
    assert "header" in types and "section" in types
    flat = str(blocks)
    assert "/100" in flat
    assert "Merge ready" in flat


def test_tests_blocks_include_coverage():
    blocks = format_result(_result("/sync tests services/auth.py"))
    assert blocks[0]["text"]["text"].startswith("Tester")
    assert any("Coverage" in str(block) for block in blocks)


def test_docs_blocks_include_word_count():
    blocks = format_result(_result("/sync docs changelog"))
    assert blocks[0]["text"]["text"].startswith("Scribe")
    assert any("Word count" in str(block) for block in blocks)


def test_status_blocks_include_failures_and_cause():
    blocks = format_result(_result("/sync status"))
    assert blocks[0]["text"]["text"].startswith("Watchdog")
    flat = str(blocks)
    assert "Failures" in flat
    assert "Likely cause" in flat


def test_every_result_ends_with_demo_mode_context():
    for text in ["/sync review PR #1", "/sync tests a.py", "/sync docs", "/sync status"]:
        blocks = format_result(_result(text))
        assert blocks[-1]["type"] == "context"
        assert "SlackSync" in str(blocks[-1])
        # Header text must respect Slack's 150 char plain_text limit.
        assert len(blocks[0]["text"]["text"]) <= 150


def test_evidence_block_present_when_context_exists():
    blocks = format_result(_result("/sync review PR #42"))
    assert any(block["type"] == "divider" for block in blocks)
    assert any("MCP" in str(block) for block in blocks)
