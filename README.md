<div align="center">
  <h1>🚀 AgenticCV</h1>
  <p><strong>Enterprise-Grade AI Job Application Engine</strong></p>
  
  <p>
    <a href="https://github.com/Bhargav1488-max/AgenticCV/issues"><img alt="Issues" src="https://img.shields.io/github/issues/Bhargav1488-max/AgenticCV?color=0088ff" /></a>
    <a href="https://github.com/Bhargav1488-max/AgenticCV/pulls"><img alt="Pull Requests" src="https://img.shields.io/github/issues-pr/Bhargav1488-max/AgenticCV?color=0088ff" /></a>
    <a href="https://github.com/Bhargav1488-max/AgenticCV/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Bhargav1488-max/AgenticCV" /></a>
  </p>
</div>

---

**AgenticCV** is a powerful, self-hosted AI engine that dynamically tailors your Master CV and Cover Letter to any Job Description in seconds. Powered by multi-agent architectures and multiple LLM providers, it delivers high ATS matching, flawless LaTeX-compiled PDFs, and real-time semantic analysis.

## ✨ Features

- 🧠 **Multi-LLM Engine** — Native support for Google Gemini, Groq, GitHub Models, NVIDIA NIM, OpenRouter, Cohere, and Azure OpenAI.
- 📄 **LaTeX PDF Pipeline** — Generates professional, deterministic PDFs by compiling dynamic JSON outputs directly into LaTeX templates.
- 📊 **Real-Time ATS Scoring** — Built-in Applicant Tracking System simulator that scores your tailored CV, identifies missing keywords, and provides actionable recommendations.
- 🎯 **Surgical Tailoring** — UI toggles let you choose exactly which sections to modify (Title, Summary, Skills, Experience) while preserving historical accuracy.
- 🕸️ **Automated JD Scraping** — Paste a job description or provide a URL to automatically scrape and parse the role requirements.
- ✉️ **Cover Letter Generation** — Generates tailored cover letters compiled to professional PDF format.
- 🐳 **Dockerized** — One command to build and run. No local LaTeX installation needed.

## 🏗️ Architecture

```mermaid
graph TD;
    A[User UI - Streamlit] -->|Upload Master CV| B[PDF/DOCX Parser]
    A -->|Input JD URL/Text| C[Job Description Scraper]
    
    B --> D{AI Orchestrator}
    C --> D
    
    D -->|Strict JSON Schema| E[(Multi-LLM Engine)]
    E -.->|Gemini / Groq / GPT-4o / etc.| D
    
    D -->|Tailored CV JSON| F[LaTeX Generator]
    D -->|Cover Letter Text| F
    
    F -->|Raw .tex files| G[PDFLaTeX Compiler]
    G -->|Compiled PDFs| A
    
    D -->|CV + JD| H[ATS Semantic Matcher]
    H -->|Score & Keywords| A
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

The fastest way to get up and running — no Python or LaTeX installation needed.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/)

```bash
# Clone the repository
git clone https://github.com/Bhargav1488-max/AgenticCV.git
cd AgenticCV

# Build and start
docker compose up -d --build
```

Open **http://localhost:8501** in your browser.

#### Docker Commands Reference

| Command | Description |
|---|---|
| `docker compose up -d --build` | Build image and start container |
| `docker compose up -d` | Start without rebuilding |
| `docker compose down` | Stop and remove container |
| `docker compose logs -f` | Follow live logs |
| `docker compose restart` | Restart container |

### Option 2: Local Development

**Prerequisites:**
- Python 3.10+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for LaTeX PDF compilation) **or** a local LaTeX distribution ([TeX Live](https://tug.org/texlive/) / [MiKTeX](https://miktex.org/))

```bash
# Clone the repository
git clone https://github.com/Bhargav1488-max/AgenticCV.git
cd AgenticCV

# Set up virtual environment
python -m venv venv

# Activate (choose your OS)
source venv/bin/activate        # macOS / Linux
.\venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

> **Note:** When running locally without a LaTeX distribution installed, AgenticCV automatically delegates PDF compilation to the Docker container. Just make sure `docker compose up -d --build` has been run at least once.

## 📁 Project Structure

```
AgenticCV/
├── app.py                  # Streamlit entrypoint
├── config.yaml             # LLM providers & app settings
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Container orchestration
├── .env.example            # Environment variable template
├── modules/
│   ├── llm_engine.py       # Multi-LLM orchestrator
│   ├── cv_parser.py        # PDF/DOCX CV parser
│   ├── jd_scraper.py       # Job description scraper
│   ├── latex_generator.py  # LaTeX template engine
│   ├── latex_compiler.py   # PDF compilation (local + Docker fallback)
│   ├── ats_scorer.py       # ATS semantic matching
│   ├── prompts.py          # LLM prompt templates
│   ├── config_loader.py    # YAML config loader
│   ├── history_manager.py  # Session history
│   └── utils.py            # Shared utilities
├── ui/
│   ├── sidebar.py          # Settings sidebar
│   ├── tab_tailor.py       # CV tailoring tab
│   ├── tab_manual.py       # Manual CV builder
│   ├── tab_ats.py          # ATS scoring tab
│   ├── tab_cv_preview.py   # CV preview tab
│   ├── tab_cover_letter.py # Cover letter tab
│   └── tab_history.py      # History tab
├── output/                 # Generated PDFs & .tex files
└── data/                   # Uploaded CVs & scraped JDs
```

## ⚙️ Configuration

### LLM API Keys

Configure your API keys in the **UI Sidebar** at runtime, or set them as environment variables:

| Variable | Provider |
|---|---|
| `GOOGLE_API_KEY` | Google Gemini |
| `GROQ_API_KEY` | Groq |
| `GITHUB_TOKEN` | GitHub Models |
| `NVIDIA_API_KEY` | NVIDIA NIM |
| `OPENROUTER_API_KEY` | OpenRouter |
| `COHERE_API_KEY` | Cohere |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI |

You only need **one** provider configured to get started.

### Supported Models

Provider configuration is managed in [`config.yaml`](config.yaml):

| Provider | Models |
|---|---|
| **Google Gemini** | `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash-exp` |
| **Groq** | `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it` |
| **GitHub Models** | `gpt-4o`, `gpt-4o-mini`, `Mistral-large` |
| **NVIDIA NIM** | `meta/llama-3.1-70b-instruct`, `meta/llama-3.1-8b-instruct`, `mistralai/mixtral-8x22b-instruct` |
| **OpenRouter** | `openai/gpt-4o-mini`, `anthropic/claude-3.5-sonnet`, `google/gemini-1.5-flash`, `meta-llama/llama-3.1-8b-instruct:free` |
| **Cohere** | `command-r-plus`, `command-r` |
| **Azure OpenAI** | `gpt-4o`, `gpt-4o-mini`, `gpt-35-turbo` |

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ for AI Engineers and DevOps Professionals.*
