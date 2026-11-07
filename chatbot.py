#!/usr/bin/env python3
"""Smart FAQ Chatbot - command line interface (requirements 1, 2 and 4).

Usage:
    python chatbot.py                          # interactive chat (auto provider)
    python chatbot.py --provider ollama        # force a provider
    python chatbot.py --question "..."         # one-shot question, then exit
"""

from __future__ import annotations

import argparse
import re

from faq.llm_client import LLMClient
from faq.prompt_template import build_messages


def strip_markdown(text: str) -> str:
    """Remove the small bit of Markdown the bot uses, for clean terminal output."""
    text = text.replace("## ", "")
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Smart FAQ Chatbot (course syllabus assistant)")
    parser.add_argument("--provider", choices=["auto", "openai", "ollama", "huggingface", "demo"],
                        help="LLM backend (default: LLM_PROVIDER env var or 'auto')")
    parser.add_argument("--question", help="ask one question and exit (non-interactive)")
    args = parser.parse_args()

    client = LLMClient(args.provider)

    print("=" * 64)
    print("Smart FAQ Chatbot - course syllabus assistant")
    print(f"LLM backend : {client.describe()}")
    print("Type a question (or 'quit' to exit).")
    print("=" * 64)

    history: list[dict] = []

    if args.question:  # one-shot mode, handy for testing
        answer = client.generate(build_messages(args.question))
        print(f"\nYou : {args.question}")
        print(f"\nBot : {strip_markdown(answer)}")
        return

    while True:
        try:
            question = input("\nYou : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in {"quit", "exit", "q", "bye"}:
            print("Good luck with the course. Goodbye!")
            break

        answer = client.generate(build_messages(question, history))
        print(f"\nBot : {strip_markdown(answer)}")

        history += [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ]
        history = history[-6:]  # keep the prompt small


if __name__ == "__main__":
    main()
