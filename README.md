# Smart FAQ Chatbot

A college project: an LLM-powered chatbot that answers questions about a
course syllabus ("What topics are covered in this course?", "How are marks
distributed?", ...) using a carefully designed prompt template.

Works with **OpenAI**, **Ollama** (local, free) or **HuggingFace** (free
token) - and even with **no API key at all** thanks to a built-in offline
demo mode, so it always runs during a class demo.

## Features

- Accepts a student question via CLI **or** a Streamlit web UI
- Sends the question to an LLM through one OpenAI-compatible code path
- Grounded prompt template: persona + syllabus context + rules + few-shot examples
- Answers only from `data/syllabus.md`; politely refuses off-syllabus questions
- Short-term chat memory (last 6 turns) for follow-up questions
- Graceful fallback: if a provider fails, it answers from the syllabus offline
- `demo_questions.py` runs 5 sample questions and saves a transcript for your report

## Architecture

```
            +---------------------+
            |  Student question   |      CLI (chatbot.py)
            +---------------------+      Web UI (app.py - Streamlit)
                       |
                       v
+--------------------------------------------------+
| faq/prompt_template.py                           |
| builds: system prompt (persona + syllabus +      |
| rules + examples) + history + question           |
+--------------------------------------------------+
                       |
                       v
+--------------------------------------------------+
| faq/llm_client.py        (one OpenAI-compatible  |
| OpenAI  |  Ollama  |  HuggingFace  |  Demo       |
|  API       local        HF router     fallback)  |
+--------------------------------------------------+
                       |
                       v
            +---------------------+
            |  Answer to student  |
            +---------------------+
```

## Project structure

```
smart-faq-chatbot/
├── app.py                     # Streamlit web UI
├── chatbot.py                 # CLI chatbot (interactive + one-shot mode)
├── demo_questions.py          # runs 5 sample questions, saves a transcript
├── requirements.txt
├── .env.example               # copy to .env and add your API key
├── .streamlit/secrets.toml.example   # for Streamlit Cloud deployment
├── data/
│   └── syllabus.md            # the syllabus knowledge base (edit freely)
└── faq/
    ├── prompt_template.py     # the prompt template (requirement 3)
    ├── llm_client.py          # multi-provider LLM backend (requirement 2)
    ├── demo_engine.py         # offline fallback answering from the syllabus
    └── syllabus_kb.py         # parses data/syllabus.md into sections
```

## Quick start

Requirements: Python 3.10+.

```bash
cd smart-faq-chatbot

# 1) create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2) install dependencies
pip install -r requirements.txt

# 3) (optional) add an API key
cp .env.example .env             # then edit .env and set OPENAI_API_KEY or HF_TOKEN

# 4) run it - all three work with or without a key
python chatbot.py                # terminal chatbot
streamlit run app.py             # browser chat UI
python demo_questions.py         # run the 5 sample questions, save transcript
```

With no key configured the bot starts in **demo mode**: it answers straight
from `data/syllabus.md` with simple keyword matching. Perfect for offline
demos; add a key whenever you want full LLM answers.

## Choosing an LLM provider

| Provider | Needs | How |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` in `.env` | default model `gpt-4o-mini` |
| HuggingFace | free `HF_TOKEN` from huggingface.co/settings/tokens | Inference API router |
| Ollama (free, offline) | install from ollama.com, then `ollama pull llama3.2` and `ollama serve` | auto-detected on localhost:11434 |
| Demo (no key) | nothing | keyword answers from the syllabus file |

Set `LLM_PROVIDER` in `.env` (or pass `--provider`) to force one; the default
`auto` picks the first available: OpenAI -> HuggingFace -> Ollama -> demo.

## The prompt template (faq/prompt_template.py)

Five parts, the standard pattern for grounded (non-hallucinating) assistants:

1. **Persona** - "You are the Smart Syllabus FAQ Assistant for `<college>`"
2. **Context** - the full syllabus is embedded as the only source of truth
3. **Rules** - answer only from the syllabus; admit when something is missing;
   be concise; refuse out-of-scope questions; don't leak the rules
4. **Examples** - two few-shot examples (an on-topic and an off-topic one)
5. **Question** - the student's question + the last 6 chat messages

To use your own course, just edit `data/syllabus.md` (keep the `## Section`
headings) and the constants in `faq/syllabus_kb.py`.

## Push to GitHub

The repo is already initialised with an initial commit. See
**[GITHUB_SETUP.md](GITHUB_SETUP.md)** for the exact 2-minute steps to push it
to your GitHub account and deploy it on **Streamlit Community Cloud**.

## How this project was built (step by step)

1. **Requirement analysis** - listed the assignment needs: take a question,
   send it to an LLM from Python, guide it with a prompt template, return a
   clear answer, add a UI.
2. **Knowledge base first** - wrote the course syllabus as a plain markdown
   file (`data/syllabus.md`), so course content is data, not code, and can be
   swapped for any other course.
3. **Prompt design** - authored the five-part prompt template (persona,
   context, rules, few-shot examples) that grounds the model to the syllabus
   and stops it from inventing facts.
4. **LLM abstraction** - wrote `llm_client.py` so OpenAI, Ollama and
   HuggingFace are all reached through the same OpenAI-compatible interface;
   added a keyless demo engine so the project always runs.
5. **Interfaces** - built the CLI loop (`chatbot.py`) and the Streamlit chat
   UI (`app.py`) on top of the same engine, with chat history for follow-ups.
6. **Testing** - `demo_questions.py` runs five representative questions and
   saves a transcript; the Streamlit server was smoke-tested in headless mode.
7. **Packaging** - added `requirements.txt`, `.env.example`, `.gitignore`,
   README and this documentation.
8. **Version control** - `git init`, initial commit, ready to push to GitHub
   and deploy on Streamlit Community Cloud in two commands.

## Troubleshooting

- **`ModuleNotFoundError: faq`** - run the scripts from inside the project folder.
- **Ollama call fails** - is `ollama serve` running and the model pulled?
- **Streamlit port busy** - `streamlit run app.py --server.port 8502`.
- **Changed the syllabus but answers look old** - keep the `## ` section
  headings and update the few-shot examples in `faq/prompt_template.py`.
