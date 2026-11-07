# Connect this project to your GitHub account + Streamlit Cloud

This project folder is already a **git repository with an initial commit**,
so connecting it to your GitHub account takes about two minutes. (The build
environment has no access to your GitHub login, so the final push is yours
to make - everything is prepared for it.)

## Part 1 - Push to your GitHub account

### Option A: from the terminal (recommended)

1. Create an empty repo on GitHub:
   - Go to <https://github.com/new>
   - Repository name: `smart-faq-chatbot`
   - Visibility: Public (needed for free Streamlit Cloud deployment)
   - **Do NOT** tick "Add a README" (we already have one)
   - Click **Create repository**

2. In a terminal, inside the `smart-faq-chatbot` folder, run:

   ```bash
   git remote add origin https://github.com/<your-username>/smart-faq-chatbot.git
   git branch -M main
   git push -u origin main
   ```

   Replace `<your-username>` with your GitHub username. The first push opens
   a browser window (or asks for a Personal Access Token) to log you in.

3. Refresh the GitHub page - your project is online.

> Optional: set your own commit identity first (the initial commit currently
> uses a placeholder author):
> `git config --global user.name "Your Name"` and
> `git config --global user.email "you@example.com"`, then optionally run
> `git commit --amend --reset-author --no-edit`.

### Option B: GitHub Desktop (no terminal)

GitHub Desktop -> File -> Add local repository -> select this folder ->
Publish repository.

### Option C: GitHub CLI

```bash
gh repo create smart-faq-chatbot --public --source=. --push
```

## Part 2 - Deploy on Streamlit Community Cloud (free)

This is what "connect the project to Streamlit" means: the app is hosted from
your GitHub repo.

1. Go to <https://share.streamlit.io> and click **Sign in with GitHub**
   (authorize Streamlit).
2. Click **Create app** -> **Deploy a public app from GitHub**.
3. Pick your repository `smart-faq-chatbot`, branch `main`,
   main file path: `app.py`. Click **Deploy**.
4. Add your API key: app menu (three dots) -> **Settings** -> **Secrets**,
   and paste (then Save):

   ```toml
   LLM_PROVIDER = "openai"
   OPENAI_API_KEY = "sk-..."
   OPENAI_MODEL = "gpt-4o-mini"
   COLLEGE_NAME = "Vivekananda College of Engineering & Technology"
   ```

   (Use `HF_TOKEN = "hf_..."` instead if you prefer the free HuggingFace
   route. With no key the app still works in offline demo mode.)
5. Your chatbot is live at `https://<your-app-name>.streamlit.app` - share
   that link in your submission.

## Updating the app later

```bash
git add -A
git commit -m "Describe your change"
git push
```

Streamlit Cloud redeploys automatically on every push to `main`.
