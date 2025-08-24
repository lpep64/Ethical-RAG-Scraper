# Test Instructions for Ethical-RAG-Scraper

## How to Run Tests

1. Ensure all dependencies are installed:
   ```powershell
   pip install -r requirements.txt
   pip install pytest
   ```

2. Run the tests in the `tests/` folder:
   ```powershell
   pytest tests/
   ```

## Recommended Test Order

1. **Reddit Scraper Unit Tests**
   - `test_reddit_scraper.py`: Validates submission and comment processing logic.
2. **ChromaDB Ingestion Tests**
   - `test_chroma_ingest.py`: Checks embedding shapes and metadata structure.
3. **LlamaIndex Query Engine Tests**
   - `test_llamaindex_query.py`: Verifies answer and citation extraction.

## Main Command (Run After Tests)

Once all tests pass, run the main pipeline scripts in order:

1. **Scrape Subreddit Data**
   ```powershell
   python data_acquisition/reddit_scraper.py
   ```
2. **Ingest Data into ChromaDB**
   ```powershell
   python vector_db/chroma_ingest.py
   ```
3. **Start FastAPI Backend**
   ```powershell
   uvicorn api.main:app --reload
   ```
4. **Launch Streamlit UI**
   ```powershell
   streamlit run ui/app.py
   ```

---
Run tests regularly to catch issues before running the main pipeline.
