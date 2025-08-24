import os
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../vector_db/chroma_db')

# Configure LLM and embedding model
Settings.llm = Ollama(model="mistral", request_timeout=120.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path=DB_DIR)
collection = chroma_client.get_collection(name="subreddit_knowledge_base")
vector_store = ChromaVectorStore(chroma_collection=collection)

# Load index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store)

# Query engine
query_engine = index.as_query_engine(similarity_top_k=5)

def answer_with_citations(question):
    response = query_engine.query(question)
    answer_text = response.response
    citations = set()
    for source_node in response.source_nodes:
        if 'source' in source_node.metadata:
            citations.add(source_node.metadata['source'])
    return answer_text, sorted(list(citations))

if __name__ == "__main__":
    question = input("Enter your question: ")
    answer, sources = answer_with_citations(question)
    print("\nAnswer:\n", answer)
    print("\nSources:")
    for url in sources:
        print(f"- {url}")
