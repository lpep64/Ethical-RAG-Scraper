# Ollama Setup Guide

Ollama is used to run the local LLM inference server for the RAG pipeline.

## Installation
- Download Ollama for Windows from https://ollama.com/download
- Install and run the application. It will start a server at http://localhost:11434

## Model Management
- To download the recommended model, open a terminal and run:

```
ollama pull nous-hermes-2-mistral-7b-dpo
```

- For other models, see https://ollama.com/library

## API Verification
- Test the server with:
```
curl http://localhost:11434/api/tags
```

## Notes
- Ollama automatically loads/unloads models as needed.
- Ensure the server is running before using the RAG pipeline.
- For custom models or LoRA adapters, see Ollama documentation.
