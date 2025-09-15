# Copilot Instructions for UTN Agro AI - Curso de LLMs

## Overview
This repository contains Jupyter notebooks for a course on advanced AI solutions, focusing on Large Language Models (LLMs) and their practical applications in agriculture and related domains. The structure is modular, with each module covering a specific topic or API integration.

## Architecture & Structure
- **Notebooks are organized by module and class** in folders like `module-1-llm/` and `module-3-llm-api-rag/`.
- Each notebook is self-contained, often with starter and solution versions for exercises.
- Key modules cover: LLM basics, API usage (OpenAI, Claude, Gemini), web scraping, data visualization, A/B testing, and local model deployment (Ollama, LM Studio).

## Developer Workflows
- **No explicit build or test scripts**; work is performed interactively in Jupyter notebooks.
- **Dependency management:** Notebooks auto-install required Python packages at runtime. Main packages: `openai`, `anthropic`, `google-genai`, `python-dotenv`, `requests`, `beautifulsoup4`.
- **Environment setup:**
  - For local use, copy `.env.example` to `.env` and add API keys.
  - For Colab, notebooks detect the environment and use Colab secrets (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`).
- **API keys** are required for most notebooks; see the README for setup instructions.

## Project-Specific Patterns & Conventions
- **Notebook naming:** Follows `Clase XX`, `Ejemplo`, `Solution`, and `Starter` conventions for clarity.
- **API integration:** Each notebook demonstrates usage of a specific API, with code for authentication and request handling.
- **Web scraping:** Uses `requests` and `beautifulsoup4` for extracting data from web sources.
- **A/B testing:** Dedicated notebooks for experiment design and evaluation with LLMs.
- **Local models:** Integration with Ollama and LM Studio for running models locally.

## Integration Points
- **External APIs:** OpenAI, Anthropic (Claude), Google Gemini.
- **Local model tools:** Ollama, LM Studio.
- **Data sources:** Web scraping and climate data APIs.

## Key Files & Directories
- `README.md`: Main setup and usage guide.
- `.env.example`: Template for environment variables.
- `module-1-llm/`, `module-3-llm-api-rag/`: Main notebook directories.

## Example: Installing Dependencies in a Notebook
```python
!pip install openai anthropic google-genai python-dotenv requests beautifulsoup4
```

## Example: Loading API Keys
```python
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
```

## Tips for AI Agents
- Always check for required API keys before running notebook cells.
- Use notebook cell-level installation for dependencies.
- Follow the naming conventions for new notebooks and exercises.
- Reference the README for environment setup and API key instructions.

---
_Last updated: September 2025_
