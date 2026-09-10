# 🏢 Intelligent Competitor Intelligence \& Company Prospectus Generator

An automated AI-powered competitive intelligence tool that scrapes company websites, selects key sub-pages using structured JSON extraction, and streams an executive brochure or pitch report in real-time.

Built with Python, Streamlit, BeautifulSoup, and supports multiple LLM providers (**OpenAI**, **Google Gemini**, and **Ollama**).

\---

## 📌 Project Architecture

```text
├── config.py       	# API configuration, default model definitions, and system prompts
├── scraper.py      	# Resilient web scraping module (BeautifulSoup + requests) with safety guards
├── engine.py       	# Core logic: link selection (JSON mode), context assembly, and LLM streaming
├── requirements.txt 	# Project dependencies

├── Readme.md        	# Documentation

└── app.py          	# Interactive UI built with Streamlit
```

\---

## 🛠️ Setup \& Installation

### 1\. Prerequisites

* **Python 3.10+** installed.
* (Optional) `uv` package manager or standard `venv`.

### 2\. Environment Setup

Clone this repository and navigate to the project directory:

```bash
cd git-project
```

Create and activate a virtual environment:

```bash
# Using standard venv
python -m venv .venv

# Activate on Mac/Linux:
source .venv/bin/activate

# Activate on Windows (CMD/PowerShell):
.venv\\Scripts\\activate
```

Or if you are using `uv`:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

If using `uv`:

```bash
uv pip install -r requirements.txt
```

\---

## ⚙️ Environment Configuration

Create a `.env` file in the root of your project directory:

```env
OPENAI\_API\_KEY=your\_openai\_api\_key\_here
GOOGLE\_API\_KEY=your\_gemini\_api\_key\_here
OLLAMA\_BASE\_URL=http://localhost:11434/v1
```

\---

## 🚀 Running the Application

Launch the Streamlit dashboard by running:

```bash
streamlit run app.py
```

If using `uv`:

```bash
uv run streamlit run app.py
```

Open your browser at `http://localhost:8501`.

\---

## 💡 Key Features

* **Dynamic Sub-page Selection**: Automatically finds and extracts high-value links (e.g., *About Us*, *Products*, *Careers*, *Pricing*) while filtering out non-HTTP schemes, social share links, and legal fine print using LLM JSON output.
* **Multi-Provider LLM Integration**: Easily toggle between cloud LLMs (OpenAI `gpt-4.1-mini`, Gemini `gemini-2.5-flash-lite`) and local open-source models (Ollama `llama3.2`).
* **Real-Time Token Streaming**: Stream outputs character-by-character for immediate visual feedback.
* **Robust Exception Handling**: Built-in safeguards against invalid URL schemes (`mailto:`, `tel:`), missing URL attributes, and request timeouts.

