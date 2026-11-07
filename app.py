"""Smart FAQ Chatbot - Streamlit web UI (optional requirement 5).

Run with:
    streamlit run app.py

Deploy on Streamlit Community Cloud: see GITHUB_SETUP.md (push this repo to
GitHub first, then create the app on share.streamlit.io and put your keys in
the app's Secrets).
"""

from __future__ import annotations

import os

import streamlit as st


def _load_secrets_into_env() -> None:
    """Merge st.secrets (Streamlit Cloud) into os.environ, without overriding .env."""
    try:
        for key, value in st.secrets.items():
            os.environ.setdefault(key, str(value))
    except Exception:
        pass  # no secrets.toml configured - fine, demo mode still works


_load_secrets_into_env()

from faq.llm_client import LLMClient  # noqa: E402  (needs secrets loaded first)
from faq.prompt_template import build_messages, build_system_prompt  # noqa: E402
from faq.syllabus_kb import COURSE_CODE, COURSE_TITLE, CREDITS, DEGREE_LABEL, SAMPLE_QUESTIONS  # noqa: E402

st.set_page_config(page_title="Smart FAQ Chatbot", page_icon="🎓", layout="centered")


@st.cache_resource
def get_client() -> LLMClient:
    """Create the LLM client once and reuse it across reruns."""
    return LLMClient()


client = get_client()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------- sidebar --------------------------------------
with st.sidebar:
    st.header("Smart FAQ Chatbot")
    st.caption(f"**{COURSE_TITLE}** ({COURSE_CODE})\n\n{DEGREE_LABEL} · {CREDITS} credits")
    st.divider()

    st.subheader("Try a sample question")
    for sample in SAMPLE_QUESTIONS:
        if st.button(sample, key=f"sample_{sample}", use_container_width=True):
            st.session_state.pending_question = sample

    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption(f"LLM backend: {client.describe()}")

    with st.expander("Prompt template used"):
        st.code(build_system_prompt(), language="markdown")

# ----------------------------- main chat ------------------------------------
st.title("Smart FAQ Chatbot")
st.caption("Ask anything about the course syllabus - topics, units, marks, books, lab, attendance.")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

typed = st.chat_input("Ask about your syllabus...")
pending = st.session_state.pop("pending_question", None)
question = typed or pending

if question:
    st.chat_message("user").markdown(question)

    history = st.session_state.messages[-6:]  # short-term memory
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = client.generate(build_messages(question, history))
        st.markdown(answer)

    st.session_state.messages += [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]
