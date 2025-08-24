import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def test_embedding_shape():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    text = ["Test chunk one.", "Test chunk two."]
    embeddings = model.encode(text)
    assert isinstance(embeddings, np.ndarray) or isinstance(embeddings, list)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384

def test_metadata_structure():
    sample = {
        'source': 'https://www.reddit.com/r/test/comments/abc123/',
        'author': 'user',
        'id': 'abc123',
        'type': 'submission',
        'score': 10,
        'created_utc': 1672531200,
        'title': 'Test Title'
    }
    assert 'source' in sample and sample['source'].startswith('https://')
    assert isinstance(sample['score'], int)
    assert isinstance(sample['created_utc'], int)
