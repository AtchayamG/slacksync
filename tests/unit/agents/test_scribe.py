from services.api.app.agents.scribe.agent import run
from services.api.app.agents.scribe.schemas import DocType, ScribeInput


def test_scribe_generates_changelog():
    result = run(ScribeInput(repo="atchayamg/slacksync", doc_type=DocType.CHANGELOG))
    assert result.status == "success"
    assert result.doc_type == DocType.CHANGELOG
    assert result.word_count > 0
    assert any(section.changed for section in result.sections)

