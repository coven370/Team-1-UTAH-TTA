"""
Knowledge Retriever Module for Utah Teacher Training Assistant (UTTA)

This module handles the integration with the Educational Knowledge Base,
providing functionality to retrieve relevant knowledge chunks for generating
classroom management scenarios, evaluating teacher responses, and providing
evidence-based feedback.

Classes:
    KnowledgeRetriever: Main class for knowledge retrieval operations.

Example:
    retriever = KnowledgeRetriever()
    knowledge = retriever.search("classroom disruption strategies")
"""

import sqlite3
import json
import numpy as np
import os
import logging
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeRetriever:
    """
    A class to retrieve knowledge from the Educational Knowledge Base.
    
    This class handles the connection to the vector database and provides
    methods for semantic search and knowledge retrieval.
    
    Attributes:
        db_path (str): Path to the vector database
        model (SentenceTransformer): The embedding model for semantic search
    """
    
    def __init__(self, db_path="/home/team1/UTTA-Knowledge-Base-Demo/knowledge_base/vector_db.sqlite"):
        """
        Initialize the KnowledgeRetriever with the path to the vector database.
        
        Args:
            db_path (str): Path to the vector database
                          Defaults to "/home/team1/UTTA-Knowledge-Base-Demo/knowledge_base/vector_db.sqlite"
        """
        self.db_path = db_path
        self._check_database_exists()
        self._initialize_model()
        
    def _check_database_exists(self):
        """Check if the vector database exists."""
        if not os.path.exists(self.db_path):
            logger.warning(f"Vector database not found at {self.db_path}")
            logger.warning("Knowledge retrieval will not be available")
            self.database_available = False
        else:
            logger.info(f"Vector database found at {self.db_path}")
            self.database_available = True
            
    def _initialize_model(self):
        """Initialize the sentence transformer model for embeddings."""
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully")
            self.embedding_available = True
        except Exception as e:
            logger.error(f"Error loading SentenceTransformer model: {e}")
            logger.warning("Running in fallback mode without semantic search")
            self.embedding_available = False
            
    def search(self, query: str, category: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for relevant knowledge chunks using semantic similarity.
        
        Args:
            query (str): The search query
            category (str, optional): Filter by knowledge category
                                     (e.g., "classroom_management", "teaching_strategies")
            top_k (int): Number of results to return (default: 3)
            
        Returns:
            List[Dict[str, Any]]: List of knowledge chunks with metadata and similarity scores
        """
        if not self.database_available:
            logger.warning("Vector database not available. Cannot perform search.")
            return []
            
        if not self.embedding_available:
            logger.warning("Embedding model not available. Using fallback keyword search.")
            return self._fallback_keyword_search(query, category, top_k)
            
        try:
            # Convert query to embedding
            query_embedding = self.model.encode(query)
            
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query conditions
            conditions = ""
            params = []
            if category:
                conditions = " WHERE c.category = ?"
                params.append(category)
            
            # Retrieve all vectors and compute similarities
            cursor.execute(f"""
                SELECT c.id, c.text, c.metadata, c.category, e.vector 
                FROM chunks c 
                JOIN embeddings e ON c.id = e.chunk_id
                {conditions}
            """, params)
            
            results = []
            for chunk_id, text, metadata_json, category, vector_blob in cursor.fetchall():
                vector = np.frombuffer(vector_blob, dtype=np.float32)
                # Calculate cosine similarity
                similarity = np.dot(query_embedding, vector) / (np.linalg.norm(query_embedding) * np.linalg.norm(vector))
                results.append({
                    "id": chunk_id,
                    "text": text,
                    "metadata": json.loads(metadata_json),
                    "category": category,
                    "similarity": float(similarity)
                })
            
            # Sort by similarity and return top k
            results.sort(key=lambda x: x["similarity"], reverse=True)
            top_results = results[:top_k]
            
            conn.close()
            logger.info(f"Retrieved {len(top_results)} knowledge chunks for query: {query}")
            return top_results
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return self._fallback_keyword_search(query, category, top_k)
            
    def _fallback_keyword_search(self, query: str, category: Optional[str] = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Simple keyword search as fallback when semantic search is unavailable.
        
        Args:
            query (str): The search query
            category (str, optional): Filter by knowledge category
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of knowledge chunks with metadata and similarity scores
        """
        if not self.database_available:
            logger.warning("Vector database not available. Cannot perform search.")
            return []
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Split query into keywords
            keywords = [k.lower() for k in query.split()]
            
            # Get chunks matching keywords
            if category:
                cursor.execute("SELECT id, text, metadata, category FROM chunks WHERE category = ?", (category,))
            else:
                cursor.execute("SELECT id, text, metadata, category FROM chunks")
                
            results = []
            for row in cursor.fetchall():
                chunk_id, text, metadata_json, category = row
                text_lower = text.lower()
                
                # Calculate a simple score based on keyword matches
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    results.append({
                        "id": chunk_id,
                        "text": text,
                        "metadata": json.loads(metadata_json),
                        "category": category,
                        "similarity": score / len(keywords)  # Normalized score
                    })
                    
            # Sort by score and return top_k
            results.sort(key=lambda x: x["similarity"], reverse=True)
            top_results = results[:top_k]
            
            conn.close()
            logger.info(f"Retrieved {len(top_results)} knowledge chunks using keyword search for query: {query}")
            return top_results
            
        except Exception as e:
            logger.error(f"Error in keyword search: {e}")
            return []
            
    def update_usage_statistics(self, chunk_id: int, effectiveness_score: float = 0.0) -> None:
        """
        Update usage statistics for a knowledge chunk.
        
        Args:
            chunk_id (int): The ID of the knowledge chunk
            effectiveness_score (float): The effectiveness score (0.0-1.0)
        """
        if not self.database_available:
            logger.warning("Vector database not available. Cannot update usage statistics.")
            return
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current usage count and effectiveness score
            cursor.execute("SELECT usage_count, effectiveness_score FROM chunks WHERE id = ?", (chunk_id,))
            result = cursor.fetchone()
            
            if result:
                usage_count, current_score = result
                
                # Calculate new weighted average score
                new_usage_count = usage_count + 1
                if effectiveness_score > 0:
                    new_score = (current_score * usage_count + effectiveness_score) / new_usage_count
                else:
                    new_score = current_score
                    
                # Update the database
                cursor.execute(
                    "UPDATE chunks SET usage_count = ?, effectiveness_score = ? WHERE id = ?",
                    (new_usage_count, new_score, chunk_id)
                )
                conn.commit()
                logger.info(f"Updated usage statistics for chunk {chunk_id}: score={new_score:.2f}, uses={new_usage_count}")
            else:
                logger.warning(f"Chunk ID {chunk_id} not found")
                
            conn.close()
            
        except Exception as e:
            logger.error(f"Error updating usage statistics: {e}")
            
    def get_categories(self) -> List[str]:
        """
        Get all available knowledge categories.
        
        Returns:
            List[str]: List of unique category names
        """
        if not self.database_available:
            logger.warning("Vector database not available. Cannot retrieve categories.")
            return []
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT DISTINCT category FROM chunks")
            categories = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            logger.info(f"Retrieved {len(categories)} knowledge categories")
            return categories
            
        except Exception as e:
            logger.error(f"Error retrieving categories: {e}")
            return []
            
    def get_most_effective_knowledge(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most effective knowledge chunks based on usage and effectiveness scores.
        
        Args:
            category (str, optional): Filter by knowledge category
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of knowledge chunks with metadata and effectiveness scores
        """
        if not self.database_available:
            logger.warning("Vector database not available. Cannot retrieve effective knowledge.")
            return []
            
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if category:
                cursor.execute(
                    """SELECT id, text, metadata, category, effectiveness_score, usage_count 
                       FROM chunks 
                       WHERE category = ? AND usage_count > 0 
                       ORDER BY effectiveness_score DESC, usage_count DESC 
                       LIMIT ?""",
                    (category, limit)
                )
            else:
                cursor.execute(
                    """SELECT id, text, metadata, category, effectiveness_score, usage_count 
                       FROM chunks 
                       WHERE usage_count > 0 
                       ORDER BY effectiveness_score DESC, usage_count DESC 
                       LIMIT ?""",
                    (limit,)
                )
                
            results = []
            for row in cursor.fetchall():
                chunk_id, text, metadata_json, category, score, count = row
                results.append({
                    "id": chunk_id,
                    "text": text,
                    "metadata": json.loads(metadata_json),
                    "category": category,
                    "effectiveness_score": score,
                    "usage_count": count
                })
                
            conn.close()
            logger.info(f"Retrieved {len(results)} most effective knowledge chunks")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving effective knowledge: {e}")
            return [] 