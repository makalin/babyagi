import os
import pinecone
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, provider, index_name, api_key=None, embedding_model_name='all-MiniLM-L6-v2'):
        self.provider = provider
        self.index_name = index_name
        self.embedding_model = SentenceTransformer(embedding_model_name)
        if provider == 'pinecone':
            pinecone.init(api_key=api_key, environment="us-east1-gcp")
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(index_name, dimension=384)
            self.index = pinecone.Index(index_name)
        else:
            self.index = {}

    def embed_text(self, text):
        return self.embedding_model.encode(text).tolist()

    def add_task(self, task_id, embedding, metadata):
        if self.provider == 'pinecone':
            self.index.upsert([(task_id, embedding, metadata)])
        else:
            self.index[task_id] = (embedding, metadata)

    def query_tasks(self, text, top_k=3):
        embedding = self.embed_text(text)
        if self.provider == 'pinecone':
            return self.index.query(embedding, top_k=top_k, include_metadata=True)
        else:
            # Simple local search by cosine similarity
            from numpy import dot
            from numpy.linalg import norm
            import numpy as np
            results = []
            for tid, (emb, meta) in self.index.items():
                sim = dot(embedding, emb) / (norm(embedding) * norm(emb) + 1e-8)
                results.append((sim, tid, meta))
            results.sort(reverse=True)
            return results[:top_k] 