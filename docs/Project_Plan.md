# Ethical-RAG-Scraper: Project Plan

A locally-hosted, citation-enabled RAG system for extracting and answering questions from subreddit knowledge bases. See the workspace context for full details.

## Phases

1. Data Acquisition: Scrape subreddit using PRAW, store as JSONL with metadata.
2. Vector DB: Embed chunks, store in ChromaDB with metadata.
3. RAG Engine: Use LlamaIndex to retrieve, synthesize, and cite answers.
4. LLM Server: Deploy Ollama, manage models.
5. API: FastAPI backend for queries.
6. UI: Streamlit frontend.

## Technology Choices
- PRAW, sentence-transformers, ChromaDB, LlamaIndex, Ollama, FastAPI, Streamlit, Unsloth

## See README.md for setup instructions.
