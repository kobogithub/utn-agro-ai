# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python educational repository for a University course (UTN) on Large Language Models (LLMs) applied to agriculture. The repository contains two main modules of Jupyter notebooks teaching LLM APIs, agricultural data analysis, and vector databases.

## Repository Structure

- `module-1-llm/`: Introduction to LLMs with practical notebooks covering OpenAI, Claude, Gemini APIs, web scraping, and A/B testing
- `module-3-llm-api-rag/`: Advanced topics including API integration, NLP, vector databases, web automation, and precision agriculture systems
- `.env.example`: Template for API keys and environment variables
- `.venv/`: Python virtual environment (excluded from git)

## Environment Setup

### Python Environment
The project uses Python with a virtual environment:
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows
```

### Environment Variables
Copy and configure API keys:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

Required API keys:
- `OPENAI_API_KEY` - OpenAI GPT models
- `ANTHROPIC_API_KEY` - Claude models
- `GOOGLE_API_KEY` - Gemini models
- `SERPER_API_KEY` - Web search functionality (optional)
- `WEATHER_API_KEY` - Weather data APIs (optional)

## Development Commands

### Running Notebooks
The notebooks can be run in:
1. **Jupyter Lab/Notebook** locally
2. **Google Colab** (preferred for course exercises)

### Key Dependencies
Notebooks auto-install required packages, but main dependencies include:
- `openai` - OpenAI API client
- `anthropic` - Claude API client
- `google-genai` - Gemini API client
- `python-dotenv` - Environment variable loading
- `requests` - HTTP requests
- `beautifulsoup4` - Web scraping
- `chromadb` - Vector database
- `sentence-transformers` - Text embeddings

### Testing
No formal test suite - notebooks are educational and self-contained.

## Architecture

### Module 1: LLM Fundamentals
- API integration patterns for major LLM providers
- Web scraping and data extraction workflows
- A/B testing frameworks for LLM evaluation
- Local model deployment with Ollama/LM Studio

### Module 3: Advanced Applications
- Vector database implementations using ChromaDB
- RAG (Retrieval Augmented Generation) systems
- Agricultural precision systems integration
- Web automation and data pipeline examples

### Key Patterns
- **Environment Detection**: Notebooks automatically detect Colab vs local environments
- **API Key Management**: Secure loading from .env files or Colab secrets
- **Error Handling**: Clear messages for missing API keys and dependencies
- **Bilingual Support**: Spanish educational content with English code comments

## Security Notes

- API keys are automatically excluded via `.gitignore`
- Use `.env.example` as template, never commit actual `.env`
- Colab notebooks use Google's secrets management
- All sensitive data is properly isolated from version control

## Course Context

This is educational material for UTN's "Desarrollo Avanzado de Soluciones de IA" program focusing on agricultural AI applications. The notebooks progressively build from basic LLM API usage to advanced RAG systems for agricultural decision support.