"""Smart FAQ Chatbot package.

Modules:
    syllabus_kb     - loads data/syllabus.md and exposes parsed sections
    prompt_template - builds the system prompt sent to the LLM
    llm_client      - multi-provider LLM backend (OpenAI / Ollama / HuggingFace / demo)
    demo_engine     - offline demo backend that answers straight from the syllabus
"""

__version__ = "1.0.0"
