import os
import json
from sentence_transformers import SentenceTransformer
import chromadb

# Paths
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data_acquisition/UnethicalLifeProTips_corpus.jsonl')
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

# Simple chunking: treat each line as a chunk (can be improved later)
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        entry = json.loads(line)
        text = entry.get('content', '')
        if not text.strip():
            continue
        chunk_texts.append(text)
        chunk_metadatas.append({
            'source': entry.get('permalink'),
            'author': entry.get('author'),
            'id': entry.get('id'),
            'type': entry.get('type'),
            'score': entry.get('score'),
            'created_utc': entry.get('created_utc'),
            'title': entry.get('title', '')
        })
        chunk_ids.append(entry.get('id'))

# Embed in batches
batch_size = 64
for i in range(0, len(chunk_texts), batch_size):
    batch = chunk_texts[i:i+batch_size]
    embeddings = model.encode(batch, show_progress_bar=True)
    chunk_embeddings.extend(embeddings)

# Ingest into ChromaDB
collection.add(
    embeddings=chunk_embeddings,
    documents=chunk_texts,
    metadatas=chunk_metadatas,
    ids=chunk_ids
)

print(f"Ingested {len(chunk_texts)} chunks into ChromaDB at {DB_DIR}")
