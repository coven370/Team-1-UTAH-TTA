import json
import sqlite3

import numpy as np
from sentence_transformers import SentenceTransformer


class KnowledgeRetriever:
    def __init__(self):
        self.db_path = "/home/team1/UTTA-Knowledge-Base-Demo/knowledge_base/vector_db.sqlite"
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query, top_k, category):
        # Convert query to embedding
        query_embedding = self.model.encode([query])[0]

        # Connect to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build query conditions
        conditions = ""
        if category:
            conditions = f" WHERE c.category = '{category}'"

        # Retrieve all vectors and compute similarities
        cursor.execute(
            f"SELECT c.id, c.text, c.metadata, c.category, e.vector FROM chunks c JOIN embeddings e ON c.id = e.chunk_id{conditions}")
        results = cursor.fetchall()

        # Compute similarities
        similarities = []
        for chunk_id, text, metadata, category, vector_blob in results:
            vector = np.frombuffer(vector_blob, dtype=np.float32)
            similarity = np.dot(query_embedding, vector)
            similarities.append(
                (chunk_id, text, metadata, category, similarity))

        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[4], reverse=True)
        top_results = similarities[:top_k]

        # Format results
        formatted_results = []
        for chunk_id, text, metadata_json, category, similarity in top_results:
            formatted_results.append({
                "id": chunk_id,
                "text": text,
                "metadata": json.loads(metadata_json),
                "category": category,
                "similarity": float(similarity)
            })

        conn.close()
        return formatted_results


retriever = KnowledgeRetriever()


def perform_search(prompt: str, top_k: int = 3, category: str | None = None) -> list[dict[str, int | str | dict[str, str] | float]]:
    return retriever.search(prompt, top_k, category)
