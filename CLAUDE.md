# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python educational repository for a University course (UTN) on Large Language Models (LLMs) applied to agriculture. The repository contains three main modules of Jupyter notebooks teaching LLM APIs, agricultural data analysis, vector databases, and fine-tuning, plus additional dashboard applications.

## Repository Structure

- `module-1-llm/`: Introduction to LLMs with 11 progressive notebooks covering OpenAI, Claude, Gemini APIs, web scraping, A/B testing, and local models
- `module-2-llm-api-rag/`: Advanced topics with 8 notebooks including API integration, NLP, vector databases, web automation, and RAG systems
- `module-3-fine-tuning/`: Fine-tuning and model specialization with comprehensive tutorial on LoRA and Unsloth
- `dashboard/`: Executive agricultural dashboard with Jupyter notebook
- `dashboard_claude/`: Interactive Streamlit dashboard for commodity price analysis
- `@dashboard_kilo/`: Additional dashboard implementation
- `.env.example`: Template for API keys and environment variables

## Development Commands

### Running Notebooks
The notebooks are designed for:
1. **Google Colab** (preferred for course exercises) - Auto-detects environment and uses Colab secrets
2. **Jupyter Lab/Notebook** locally - Uses `.env` file for API keys

### Running Streamlit Dashboard
```bash
cd dashboard_claude
pip install -r requirements.txt
streamlit run main.py
```

### Key Dependencies
Notebooks auto-install dependencies, main packages include:
- `openai`, `anthropic`, `google-genai` - LLM API clients
- `python-dotenv` - Environment variable loading
- `requests`, `beautifulsoup4` - Web scraping
- `chromadb`, `sentence-transformers` - Vector databases and embeddings
- `streamlit`, `plotly`, `yfinance` - Dashboard and visualization
- `pandas`, `matplotlib`, `seaborn` - Data analysis

## Architecture Patterns

### Environment Detection Pattern
```python
# Standard pattern used across all notebooks
import os
try:
    import google.colab
    IN_COLAB = True
    from google.colab import userdata
    api_key = userdata.get('OPENAI_API_KEY')
except ImportError:
    IN_COLAB = False
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
```

### Auto-Installation Pattern
```python
# Each notebook installs its own dependencies
!pip install -q openai anthropic google-genai python-dotenv
```

### API Integration Architecture
- **Unified Error Handling**: All notebooks check for API keys before proceeding
- **Provider Abstraction**: Similar patterns for OpenAI, Claude, and Gemini clients
- **Response Standardization**: Consistent output formatting across different LLM providers

### Vector Database Workflow
1. **ChromaDB Setup**: In-memory client for educational purposes
2. **Embedding Models**: Default `all-MiniLM-L6-v2`, upgraded to `multilingual-e5-large` for Spanish
3. **Collection Management**: Structured document storage with metadata (regions, categories)
4. **Semantic Search**: Query by meaning, not just keywords

### RAG System Architecture
1. **Retrieval Phase**: Vector similarity search in ChromaDB collections
2. **Context Preparation**: Format retrieved documents for LLM consumption
3. **Generation Phase**: LLM generates responses using retrieved context
4. **Agricultural Focus**: Specialized for farming consultations and technical queries

## Module Structure and Progression

### Module 1: Foundation (11 notebooks)
Sequential curriculum from basic API usage to local model deployment:
- `00-Índice`: Course overview and learning path
- `01-02`: Web search integration with SERP API (Starter/Solution pattern)
- `03`: OpenAI API fundamentals and message structure
- `04`: Web scraping with OpenAI for data extraction
- `05`: Claude API with vision capabilities and base64 image handling
- `06`: Gemini API for NER, QA, translation tasks
- `07`: Weather APIs integration with agricultural recommendations
- `08-09`: A/B testing frameworks for OpenAI and Gemini
- `10-11`: Local model deployment with Ollama and LM Studio

### Module 2: Advanced Applications (8 notebooks)
RAG systems and agricultural AI applications:
- `01`: Basic API concepts reinforcement
- `02`: NLP processing fundamentals
- `03`: External data integration patterns
- `04`: Web automation and scraping workflows
- `05`: Vector databases with ChromaDB and multilingual embeddings
- `06`: Precision agriculture systems integration
- `09`: RAG for enterprise documents with Gemini

### Module 3: Fine-Tuning (1 notebook)
Model specialization and customization:
- `01`: Comprehensive introduction to fine-tuning with Unsloth, LoRA, and agricultural use cases

### Dashboard Applications
- **Executive Dashboard**: Jupyter-based agricultural commodity analysis
- **Interactive Dashboard**: Streamlit app with real-time commodity prices using yfinance
- **Customizable Interface**: Support for custom Yahoo Finance symbols and timeframes

## Key Implementation Patterns

### Bilingual Development
- **Spanish Content**: Educational materials and documentation in Spanish
- **Technical English**: Code comments and variable names in English
- **Localized Data**: Argentine agricultural terminology and regional examples

### Agricultural Domain Specialization
- **Commodity Analysis**: Soy, corn, wheat, cotton pricing and trends
- **Regional Focus**: Zona núcleo and pampa húmeda agricultural regions
- **Technical Consultations**: Real farmer queries about crops, nutrients, weather impact

### Error Handling Strategy
```python
# Standard error handling pattern
if not api_key:
    raise ValueError("API key required. Set in .env or Colab secrets")

try:
    response = client.chat.completions.create(...)
except Exception as e:
    print(f"Error: {e}")
    print("Check API key validity and network connection")
```

## Security and Best Practices

### API Key Management
- **Local Development**: Use `.env` file (excluded from git)
- **Colab Environment**: Use built-in secrets management
- **Never Commit**: API keys are in `.gitignore`
- **Template Available**: `.env.example` provides required variables

### Educational Context
- **Self-Contained Notebooks**: Each notebook can run independently
- **Progressive Complexity**: Builds from basic API calls to complex RAG systems
- **Real-World Applications**: Agricultural use cases throughout

## Course Context

Educational material for UTN's "Desarrollo Avanzado de Soluciones de IA" program. The curriculum focuses on practical LLM applications in agriculture, progressing from basic API integration to sophisticated RAG systems for agricultural decision support.