
# Ethical-RAG-Scraper

A locally-hosted, citation-enabled Retrieval-Augmented Generation (RAG) system for extracting and answering questions from subreddit knowledge bases, with full source traceability.

## Project Structure
- `data_acquisition/`: Reddit scraping scripts and output corpus
- `vector_db/`: ChromaDB setup and ingestion scripts
- `rag_engine/`: LlamaIndex integration and query engine
- `llm_server/`: Ollama setup and model management
- `api/`: FastAPI backend
- `ui/`: Streamlit frontend
- `docs/`: Project plan, setup guides, architecture
- `tests/`: Unit tests for all major modules

## Quick Start
1. Copy `.env.example` to `.env` and fill in your Reddit API credentials.
2. Install Python dependencies:
	```powershell
	pip install -r requirements.txt
	```
3. Run the pipeline:
	- Scrape subreddit: `python data_acquisition/reddit_scraper.py`
	- Ingest data: `python vector_db/chroma_ingest.py`
	- Run tests: `$env:PYTHONPATH="."; pytest tests/`
	- Start API: `uvicorn api.main:app --reload`
	- Launch UI: `streamlit run ui/app.py`

## Core Technologies
- PRAW, sentence-transformers, ChromaDB, LlamaIndex, Ollama, FastAPI, Streamlit

---
See `docs/Project_Plan.md` for the full architecture and implementation details.
