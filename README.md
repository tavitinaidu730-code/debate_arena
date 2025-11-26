# Debate Arena — Multi-Agent Debate Prototype (Streamlit)

This is a ready-to-run prototype of **The Debate Arena**. It's a minimal, local-first implementation intended to let you run and test a multi-agent debate flow using **Streamlit**.
It includes a simple LLM client abstraction that can be wired to a Google/other API using `.env` (see `.env.example`). If you don't provide an API key, the app uses a deterministic local fallback responder to simulate agent behavior so you can test the UX immediately.

## What's included
- `app.py` — Streamlit frontend to enter a topic and watch agents debate.
- `orchestrator.py` — Orchestrates multi-agent turns and debate rounds.
- `agents.py` — Agent definitions and personality templates.
- `llm.py` — LLM client abstraction (stub for Google / external API). Fallback local responder included.
- `rag.py` — Small RAG stub for evidence retrieval (simulated).
- `.env.example` — Example environment variable file for `GOOGLE_API_KEY`.
- `requirements.txt` — Python dependencies.
- `README.md` — This file.

## Run locally (Python 3.11 / 3.14 compatible)
1. Create a virtual environment and activate it:
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your `GOOGLE_API_KEY` if you plan to wire a Google/other LLM. If you don't provide one, the app will use a local fallback.
```bash
cp .env.example .env
# edit .env to add key if available
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

## How it works (short)
- Enter a debate topic, choose number of agents (2–4), pick optional round count.
- Click **Start Debate** — Orchestrator runs rounds; each agent produces responses either by calling the LLM client (if configured) or using a local fallback responder.
- After rounds complete, a summary is produced (via the orchestrator + simple summarizer).

## Where to extend
- Swap `llm.LocalLLMClient` with a real Google/OpenAI wrapper (see `llm.py` hooks).
- Replace `rag.simple_retrieve` with a FAISS or external retriever for evidence-backed debates.
- Add audio (TTS) playback and user voting in `app.py`.
