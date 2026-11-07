"""Offline demo backend.

When no API key is configured (or the provider call fails), this engine
answers directly from data/syllabus.md using simple keyword matching, so
the chatbot always works - even with zero setup and no internet.

It is intentionally simple: it is a fallback, not the main pipeline.
"""

from __future__ import annotations

import re

from faq.syllabus_kb import SECTIONS, SECTION_TITLES

DEMO_NOTICE = (
    "\n\n(Demo mode: this answer came directly from data/syllabus.md without an LLM. "
    "Add an API key in .env to get full LLM-generated answers.)"
)

FALLBACK = (
    "I could not find that in the course syllabus. Try asking about:\n"
    "- Topics covered, or a specific module (e.g. \"What is in Module 3?\")\n"
    "- Marks and assessment\n"
    "- Textbooks and references\n"
    "- Prerequisites\n"
    "- Lab experiments and tools\n"
    "- Attendance policy\n\n"
    "For anything beyond the syllabus, please contact the Department of CSE, "
    "Vivekananda College of Engineering & Technology."
)

# Intent keyword table: checked in order after the specific-unit rule.
INTENTS: list[tuple[str, tuple[str, ...]]] = [
    ("attendance", ("attendance", "attend", "leave", "policy")),
    ("topics", ("topic", "cover", "syllabus", "chapter", "portion", "unit", "module", "learn")),
    ("prerequisites", ("prerequisit", "background", "know before", "before taking")),
    ("books", ("textbook", "book", "reference", "author", "read")),
    ("lab", ("lab", "practical", "experiment", "software", "tools")),
    ("assessment", ("mark", "exam", "assess", "grade", "evaluat", "internal",
                    "midterm", "pass", "weight", "distribut")),
    ("overview", ("credit", "hour", "contact", "coordinator")),
    ("outcomes", ("outcome", "objective", "skill")),
]

STOPWORDS = {
    "what", "which", "who", "whom", "how", "when", "where", "why", "are", "is",
    "the", "this", "that", "for", "and", "with", "from", "will", "can", "does",
    "did", "about", "tell", "give", "list", "explain", "course", "subject",
    "class", "college", "please", "should", "would", "could", "have", "has",
    "there", "here", "all", "any", "some", "more", "also", "into", "many",
    "much", "take", "need",
}


def _last_user_text(messages: list[dict]) -> str:
    for msg in reversed(messages):
        if msg.get("role") == "user":
            return msg.get("content", "")
    return ""


def _format_section(title: str, body: str) -> str:
    return f"**{title}**\n\n{body.strip()}" if body else f"**{title}**"


def _section_for_title_pattern(pattern: str) -> str | None:
    for title, body in SECTIONS:
        if re.search(pattern, title, flags=re.IGNORECASE):
            return _format_section(title, body)
    return None


def _short_title(title: str) -> str:
    return re.sub(r"^Syllabus\s*[-\u2013]\s*", "", title)


def _topics_answer() -> str:
    lines = [
        f"- {_short_title(t)}"
        for t in SECTION_TITLES
        if t.lower().startswith("syllabus")
    ]
    lab = next((t for t in SECTION_TITLES if "laboratory" in t.lower()), None)
    if lab:
        lines.append(f"- {lab}")
    module_count = len(lines) - (1 if lab else 0)
    return (
        f"The course has **{module_count} modules plus an integrated laboratory component**:\n\n"
        + "\n".join(lines)
        + "\n\nAsk about a specific module (e.g. \"What is in Module 3?\") for the detailed topics."
    )


def _intent_answer(name: str) -> str | None:
    if name == "topics":
        return _topics_answer()
    mapping = {
        "attendance": "Attendance",
        "prerequisites": "Prerequisites",
        "books": "Textbooks",
        "lab": "Laboratory",
        "assessment": "Assessment",
        "overview": "Course Overview",
        "outcomes": "Course Outcomes",
    }
    found = None
    for fragment in mapping[name].split():
        for title, body in SECTIONS:
            if fragment.lower() in title.lower():
                found = (title, body)
                break
        if found:
            break
    return _format_section(*found) if found else None


def _best_section(question: str) -> tuple[str, str] | None:
    tokens = [t for t in re.findall(r"[a-z]{3,}", question.lower()) if t not in STOPWORDS]
    if not tokens:
        return None
    best, best_score = None, 0
    for title, body in SECTIONS:
        title_l, body_l = title.lower(), body.lower()
        score = sum(3 if t in title_l else (1 if t in body_l else 0) for t in set(tokens))
        if score > best_score:
            best, best_score = (title, body), score
    return best if best_score >= 1 else None


def answer_from_syllabus(question: str) -> str:
    """Produce the best possible offline answer for a syllabus question."""
    q = question.lower()

    # 1) A specific module/unit? e.g. "What is in Module 3?"
    m = re.search(r"(?:module|unit)\s*([1-5])", q)
    if m:
        section = _section_for_title_pattern(rf"(?:Module|Unit)\s*{m.group(1)}\b")
        if section:
            return section

    # 2) Known intent (topics / marks / books / ...)?
    for name, keywords in INTENTS:
        if any(k in q for k in keywords):
            answer = _intent_answer(name)
            if answer:
                return answer

    # 3) Otherwise: keyword scoring across all sections.
    best = _best_section(question)
    if best:
        return _format_section(*best)

    return FALLBACK


class DemoBackend:
    """Drop-in backend with the same `chat(messages)` interface as the LLMs."""

    name = "demo"

    def chat(self, messages: list[dict], notice: str = DEMO_NOTICE) -> str:
        return answer_from_syllabus(_last_user_text(messages)) + notice
