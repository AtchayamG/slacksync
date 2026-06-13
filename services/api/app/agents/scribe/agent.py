from __future__ import annotations

from typing import Dict, Optional

from .schemas import DocResult, DocSection, DocType, ScribeInput


def _section(text: str, changed: bool = False) -> DocSection:
    return DocSection(section_name=text.splitlines()[0][:80], after=text, changed=changed)


def run(input: ScribeInput) -> DocResult:
    if input.doc_type == DocType.README:
        sections = [
            _section("# README", changed=False),
            _section(
                "## Installation\n\n"
                "See `docs/05-delivery/installation.md`.\n",
                changed=True,
            ),
            _section(
                "## Demo Commands\n\n"
                "Run `/sync review PR #42`, `/sync tests`, `/sync docs`.\n",
                changed=True,
            ),
            _section("## License\n\nMIT\n", changed=False),
        ]
        full_content = "\n".join(s.after for s in sections)
        summary = "Refreshed README install and demo sections."
    else:
        sections = [
            _section(
                "# Changelog\n\n"
                "## [Unreleased]\n"
                "- Deterministic scribe output enabled.\n",
                changed=True,
            )
        ]
        full_content = "\n".join(s.after for s in sections)
        summary = "Updated changelog for doc generation support."

    return DocResult(
        status="success",
        doc_type=input.doc_type,
        sections=sections,
        full_content=full_content,
        word_count=len(full_content.split()),
        summary=summary,
    )
