import pytest

from services.api.app.slack.command_parser import parse_sync_command


def test_parse_review_command():
    parsed = parse_sync_command("/sync review PR #42 focus:security")
    assert parsed.command == "review"
    assert parsed.agent == "reviewer"
    assert parsed.target == "PR #42 focus:security"


def test_rejects_unknown_command():
    with pytest.raises(ValueError, match="Unsupported"):
        parse_sync_command("/sync deploy prod")

