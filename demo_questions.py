#!/usr/bin/env python3
"""Run 5 sample syllabus questions through the chatbot and save a transcript.

Useful as a quick test and for screenshots in your project report.

Usage:
    python demo_questions.py                    # auto provider (demo mode without keys)
    python demo_questions.py --provider openai  # run through a real LLM

Saves the transcript to demo_transcript.txt.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from chatbot import strip_markdown
from faq.llm_client import LLMClient
from faq.prompt_template import build_messages
from faq.syllabus_kb import SAMPLE_QUESTIONS

LINE = "=" * 64


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the sample FAQ questions")
    parser.add_argument("--provider", choices=["auto", "openai", "ollama", "huggingface", "demo"],
                        help="LLM backend (default: LLM_PROVIDER env var or 'auto')")
    args = parser.parse_args()

    client = LLMClient(args.provider)
    transcript: list[str] = [
        "Smart FAQ Chatbot - demo transcript",
        f"Generated : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"LLM backend: {client.describe()}",
        "Answers to 5 sample course-syllabus questions.",
        LINE,
    ]

    for index, question in enumerate(SAMPLE_QUESTIONS, start=1):
        print(f"\n{LINE}\nQ{index}. {question}")
        answer = strip_markdown(client.generate(build_messages(question)))
        print(f"\n{answer}")
        transcript += [f"\nQ{index}. {question}\n", f"A: {answer}\n", LINE]

    out_path = "demo_transcript.txt"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(transcript))
    print(f"\nTranscript saved to {out_path}")


if __name__ == "__main__":
    main()
