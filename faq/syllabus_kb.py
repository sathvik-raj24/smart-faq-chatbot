"""Syllabus knowledge base.

Loads data/syllabus.md, parses it into named sections and exposes a few
course metadata constants used by the UI and the prompt template.
"""

from __future__ import annotations

from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "syllabus.md"

# --- Course metadata (edit here or via environment variables) ---------------
COURSE_TITLE = "Computer Networks"
COURSE_CODE = "BCS502"
DEGREE_LABEL = "B.E. CSE - Semester V (VTU 2022 Scheme)"
CREDITS = 4

SAMPLE_QUESTIONS = [
    "What topics are covered in this course?",
    "How are the marks distributed for this course?",
    "Which textbooks should I refer to?",
    "What are the prerequisites for this course?",
    "What is covered in Module 3?",
]


def load_syllabus_text() -> str:
    """Return the full syllabus as a single string."""
    return DATA_FILE.read_text(encoding="utf-8")


def _parse_sections(text: str) -> list[tuple[str, str]]:
    """Split the markdown into (section_title, section_body) pairs.

    Every line starting with '## ' begins a new section; all following
    non-empty lines belong to that section's body.
    """
    raw: list[tuple[str, list[str]]] = []
    for line in text.splitlines():
        if line.startswith("## "):
            raw.append((line[3:].strip(), []))
        elif raw and line.strip():
            raw[-1][1].append(line.rstrip())
    return [(title, "\n".join(lines).strip()) for title, lines in raw]


SECTIONS: list[tuple[str, str]] = _parse_sections(load_syllabus_text())
SECTION_TITLES: list[str] = [title for title, _ in SECTIONS]


def find_section(fragment: str) -> tuple[str, str] | None:
    """Return the first (title, body) whose title contains `fragment`."""
    fragment = fragment.lower()
    for title, body in SECTIONS:
        if fragment in title.lower():
            return title, body
    return None
