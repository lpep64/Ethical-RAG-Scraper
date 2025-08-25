import os
import json
import time
from sentence_transformers import SentenceTransformer
import chromadb
import warnings



# Suppress CUDA warning if not using GPU
warnings.filterwarnings("ignore", message="Failed to find CUDA.")

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_acquisition')
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chroma_db')

# Load model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# ChromaDB client
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="subreddit_knowledge_base")



chunk_texts = []
chunk_embeddings = []
chunk_metadatas = []
chunk_ids = []
unique_ids = set()

# Read all .jsonl files in the data_acquisition directory
for filename in os.listdir(DATA_DIR):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(DATA_DIR, filename)
        print(f"Processing {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line)
                text = entry.get('content', '')
                entry_id = entry.get('id')
                if not text.strip() or not entry_id:
                    continue
                if entry_id in unique_ids:
                    continue  # Skip duplicate IDs
                unique_ids.add(entry_id)
                chunk_texts.append(text)
                chunk_metadatas.append({
                    'source': entry.get('permalink'),
                    'author': entry.get('author'),
                    'id': entry_id,
                    'type': entry.get('type'),
                    'score': entry.get('score'),
                    'created_utc': entry.get('created_utc'),
                    'title': entry.get('title', '')
                })
                chunk_ids.append(entry_id)



# Embed in batches with error handling and progress reporting
batch_size = 64
total_batches = (len(chunk_texts) + batch_size - 1) // batch_size
success_count = 0
fail_count = 0
max_retries = 3

for i in range(0, len(chunk_texts), batch_size):
    batch = chunk_texts[i:i+batch_size]
    batch_ids = chunk_ids[i:i+batch_size]
    batch_metadatas = chunk_metadatas[i:i+batch_size]
    for attempt in range(1, max_retries + 1):
        try:
            embeddings = model.encode(batch, show_progress_bar=True)
            collection.add(
                embeddings=embeddings,
                documents=batch,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            success_count += len(batch)
            print(f"Batch {i//batch_size+1}/{total_batches}: Ingested {len(batch)} chunks (Attempt {attempt})")
            break
        except Exception as e:
            print(f"Batch {i//batch_size+1}/{total_batches}: Error on attempt {attempt}: {e}")
            time.sleep(2 * attempt)  # Exponential backoff
            if attempt == max_retries:
                fail_count += len(batch)
                print(f"Batch {i//batch_size+1}/{total_batches}: Failed after {max_retries} attempts. Skipping batch.")

print(f"Ingestion complete: {success_count} chunks succeeded, {fail_count} chunks failed.")
print(f"Ingested {len(chunk_texts)} unique chunks into ChromaDB at {DB_DIR}")
