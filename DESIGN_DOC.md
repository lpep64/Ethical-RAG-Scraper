# Ethical-RAG-Scraper: Design Document

## Overview

Ethical-RAG-Scraper is designed to provide a local, transparent, and extensible RAG pipeline for knowledge extraction from Reddit.

## Phases

### 1. Data Acquisition

- **Design Choice:** PRAW for Reddit API due to its reliability and ease of use.
- **Why:** Reddit is a rich source of unconventional knowledge. Only public subreddits are scraped.

### 2. Vector Storage

- **Design Choice:** ChromaDB for its local-first simplicity and fast similarity search.
- **Why:** Avoids cloud lock-in and supports privacy.

### 3. RAG Orchestration

- **Design Choice:** LlamaIndex for flexible document retrieval and integration with local LLMs.
- **Why:** Enables modular, citation-enabled answers.

### 4. Backend API

- **Design Choice:** FastAPI for its speed, async support, and automatic OpenAPI docs.
- **Why:** Professional, scalable, and easy to document.

### 5. Frontend UI

- **Design Choice:** Streamlit for rapid prototyping and interactive querying.
- **Why:** Enables non-technical users to interact with the system.

## Extensibility

- New data sources (web, APIs) can be added via the `data_acquisition` module.
- Model upgrades are supported via Ollama and Unsloth.

## Ethics

- Only public data is scraped.
- Citations are always provided.
