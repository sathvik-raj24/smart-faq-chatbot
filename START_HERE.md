# START HERE - Complete Beginner Guide

This file explains EVERYTHING in simple baby steps. Follow top to bottom.

## What is an API key?

An API key is like a **password** that lets your Python code talk to an AI
company's server. Your chatbot sends: (your question + your key) and the AI
sends back the answer.

- No key? The bot still works in **demo mode** (answers directly from
  `data/syllabus.md` without any AI). Good for testing, not for submission.

## STEP 1 - Install 2 free tools (one time only)

1. **Python** (3.10 or newer): https://www.python.org/downloads/
   - During install, TICK the box "Add Python to PATH". Very important.
2. **Git**: https://git-scm.com/downloads (only needed for the GitHub step)

Check both worked: open Command Prompt and type `python --version` and
`git --version`. Both should print a version number.

## STEP 2 - Get your API key (5 minutes)

Easy FREE option - HuggingFace:

1. Go to https://huggingface.co and click **Sign Up** (free).
2. After login, click your profile picture (top right) -> **Settings**.
3. Left menu -> **Access Tokens** -> **Create new token**.
4. Name: `faq-chatbot`, type: Read. Click Create.
5. Copy the token. It starts with `hf_...`. Keep it private!

(Paid alternative: OpenAI at https://platform.openai.com/api-keys - the key
starts with `sk-...` and needs a credit card. gpt-4o-mini costs only a few
paisa per question, but free HuggingFace is fine for this project.)

## STEP 3 - Put the key into the project

1. Open the `smart-faq-chatbot` folder.
2. Click the address bar in that folder, type `cmd`, press Enter.
   A black terminal opens inside the folder.
3. Type this to create your settings file:

   ```bash
   copy .env.example .env      (Windows)
   cp .env.example .env        (Mac/Linux)
   ```

4. Open the new `.env` file with Notepad and make it look like this
   (paste YOUR token after the `=`):

   ```
   LLM_PROVIDER=huggingface
   COLLEGE_NAME=Vivekananda College of Engineering & Technology
   OPENAI_API_KEY=
   OPENAI_MODEL=gpt-4o-mini
   HF_TOKEN=hf_PASTE_YOUR_TOKEN_HERE
   HUGGINGFACE_MODEL=meta-llama/Llama-3.1-8B-Instruct
   OLLAMA_MODEL=llama3.2
   ```

5. Save and close. (If you prefer OpenAI instead: set
   `LLM_PROVIDER=openai` and paste your `sk-...` key into OPENAI_API_KEY.)

Never share this file or upload it to GitHub - `.gitignore` already
protects you.

## STEP 4 - The only 2 changes you might want (both optional)

1. **College name**: already set to "Vivekananda College of Engineering &"
   "Technology" in the code and `.env.example`. If you made a `.env` earlier
   with a different name, just update its `COLLEGE_NAME=` line.
2. **Your own syllabus**: open `data/syllabus.md` in Notepad and replace
   the text with your course syllabus. Keep every line starting with `## `
   as a section heading. That's it - no code changes needed.

## STEP 5 - Run the chatbot

In the same terminal (inside the project folder):

```bash
pip install -r requirements.txt
streamlit run app.py
```

Your browser opens the chatbot automatically. Type a question like
"What topics are covered in this course?". To stop: press Ctrl+C.

Terminal-only version (no browser): `python chatbot.py`
Run the 5 sample questions + save a transcript: `python demo_questions.py`

## STEP 6 - Connect to YOUR GitHub account

1. Go to https://github.com/new while logged into your GitHub account.
2. Repository name: `smart-faq-chatbot` | Public | do NOT tick "Add a README".
3. Click **Create repository**. GitHub shows you a URL, copy it.
4. Back in your terminal (project folder):

   ```bash
   git remote add origin https://github.com/YOUR-USERNAME/smart-faq-chatbot.git
   git branch -M main
   git push -u origin main
   ```

   A login window pops up -> log in to GitHub -> done. Refresh the GitHub
   page and your code is online.
5. If git asks for your name/email first:

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

## STEP 7 - Put the chatbot online (Streamlit Cloud, free)

1. Go to https://share.streamlit.io -> **Continue with GitHub**.
2. **Create app** -> pick your `smart-faq-chatbot` repo, branch `main`,
   Main file: `app.py` -> **Deploy**.
3. App menu (three dots) -> **Settings** -> **Secrets** -> paste:

   ```toml
   LLM_PROVIDER = "huggingface"
   HF_TOKEN = "hf_PASTE_YOUR_TOKEN_HERE"
   COLLEGE_NAME = "Vivekananda College of Engineering & Technology"
   ```

4. Save. Your bot now lives at a public link like
   `https://smart-faq-chatbot.streamlit.app` - share this in your submission!

## Quick problem fixing

| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python, tick "Add to PATH" |
| `ModuleNotFoundError: faq` | Run commands from INSIDE the project folder |
| Bot says "Demo mode" | Your key is missing/wrong in `.env` |
| Ollama errors | Ignore - only if you chose Ollama |
| Streamlit port busy | `streamlit run app.py --server.port 8502` |
