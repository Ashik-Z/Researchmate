# ResearchMate 🔍

An autonomous AI research agent that takes a topic, searches the web, 
reflects on whether it has enough information, and writes a structured report — 
all without human intervention.

Built to explore **agentic AI development** with LangGraph, FastAPI, and Google Gemini.

---

## How it works

The agent follows a multi-step reasoning loop:

1. **Planner** — breaks the topic into 3 focused sub-questions
2. **Search** — queries the web for each sub-question via Tavily
3. **Reader** — extracts content from the top results
4. **Reflect** — decides if research is sufficient or needs another loop
5. **Writer** — synthesizes everything into a structured report

The entire process streams live to the UI so you can watch the agent think in real time.

---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Agent framework | LangGraph + LangChain |
| LLM | Google Gemini 2.5 Flash |
| Search | Tavily API |
| Backend | FastAPI + Server-Sent Events |
| Frontend | Vanilla HTML/CSS/JS |

---

## Setup

### 1. Clone and create virtual environment
```bash
git clone https://github.com/Ashik-Z/ResearchMate.git
cd ResearchMate
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add API keys
Create a `.env` file:
```
GOOGLE_API_KEY=your_gemini_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Get your keys:
- Gemini → https://aistudio.google.com
- Tavily → https://tavily.com

### 4. Run
```bash
uvicorn backend.main:app --reload
```

Visit `http://127.0.0.1:8000`

---

## Project structure
```
researchmate/
├── agent/
│   ├── state.py       # Shared state across nodes
│   ├── tools.py       # Tavily search + page reader
│   ├── nodes.py       # Planner, searcher, reader, reflect, writer
│   └── graph.py       # LangGraph flow definition
├── backend/
│   └── main.py        # FastAPI + SSE streaming endpoint
├── frontend/
│   └── index.html     # Single page UI
├── .env               # API keys (never commit this)
└── requirements.txt
```

---

## Why I built this

Agentic AI is one of the most significant shifts in how software is being built today.
Rather than a model that simply responds, an agent plans, uses tools, evaluates its own
output, and iterates — closer to how a human researcher actually works.

This project was my hands-on exploration of those concepts using production-grade tools:
LangGraph for stateful multi-step workflows, Tavily for real-time web access, and Gemini
for reasoning. The goal was to go beyond tutorials and build something that actually runs
end to end.
