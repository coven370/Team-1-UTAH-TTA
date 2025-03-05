"""
RAG (Retrieval-Augmented Generation) Pipeline Module for Teacher Training Chatbot

This module implements the RAG pipeline that combines retrieval of relevant teaching
scenarios with LLM-based response generation. It handles document processing,
similarity search, and context-aware response generation.

Classes:
    RAGPipeline: Main class implementing the RAG pipeline functionality.

Example:
    pipeline = RAGPipeline()
    await pipeline.initialize()
    result = await pipeline.process_query("How to handle student disruption?")
"""

import asyncio
from typing import Dict, List, Optional
from .embedding import EmbeddingGenerator
from ..database.vector_ops import VectorOperations
from .llm_config import LLMConfig
from .knowledge_retriever import KnowledgeRetriever
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    A class implementing the RAG pipeline for the teacher training chatbot.
    
    This class combines document retrieval and response generation to provide
    context-aware responses to teaching scenarios. It uses vector similarity
    search for retrieval and an LLM for response generation.
    
    Attributes:
        embedder (EmbeddingGenerator): Instance for generating embeddings
        vector_ops (VectorOperations): Instance for vector storage operations
        llm (LLMConfig): Instance for LLM configuration and generation
        knowledge_retriever (KnowledgeRetriever): Instance for knowledge base retrieval
    """

    def __init__(self):
        """Initialize the RAG pipeline with required components."""
        self.embedder = EmbeddingGenerator()
        self.vector_ops = VectorOperations()
        self.llm = LLMConfig()
        self.knowledge_retriever = KnowledgeRetriever()
        self._performance_metrics = {}

    async def initialize(self):
        """
        Initialize pipeline components asynchronously.
        
        This method must be called before using the pipeline to ensure
        all components are properly initialized.
        """
        # Initialize existing components
        await self.vector_ops.initialize()
        
        # Log knowledge base categories if available
        categories = self.knowledge_retriever.get_categories()
        if categories:
            logger.info(f"Knowledge base categories: {', '.join(categories)}")
        else:
            logger.warning("No knowledge base categories found or knowledge base not available")

    async def process_query(self, query: str, context: Dict = None, use_knowledge_base: bool = True) -> Dict:
        """
        Process a user query through the RAG pipeline.
        
        This method retrieves relevant scenarios and knowledge, then generates
        a response using the LLM.
        
        Args:
            query (str): The user's query
            context (Dict, optional): Additional context for the query
            use_knowledge_base (bool): Whether to use the knowledge base
            
        Returns:
            Dict: Response containing generated text and sources
        """
        # Generate embedding for the query
        query_embedding = self.embedder.generate_embedding(query)
        
        # Retrieve relevant scenarios from vector database
        scenarios = await self.vector_ops.search_scenarios(query_embedding)
        
        # Retrieve relevant knowledge from knowledge base if enabled
        knowledge_chunks = []
        if use_knowledge_base:
            knowledge_chunks = self.knowledge_retriever.search(query, top_k=3)
            logger.info(f"Retrieved {len(knowledge_chunks)} knowledge chunks for query")
        
        # Combine scenarios and knowledge for context
        combined_context = self._build_context(query, scenarios, knowledge_chunks, context)
        
        # Generate response using LLM
        response = await self.llm.generate_response(query, combined_context)
        
        # Track knowledge usage
        if knowledge_chunks:
            for chunk in knowledge_chunks:
                self.knowledge_retriever.update_usage_statistics(chunk["id"])
        
        # Return response with sources
        return {
            "response": response,
            "sources": self._format_sources(scenarios, knowledge_chunks)
        }
    
    def _build_context(self, query: str, scenarios: List[Dict], knowledge_chunks: List[Dict], additional_context: Dict = None) -> str:
        """
        Build a context string from retrieved scenarios and knowledge.
        
        Args:
            query (str): The original query
            scenarios (List[Dict]): Retrieved teaching scenarios
            knowledge_chunks (List[Dict]): Retrieved knowledge chunks
            additional_context (Dict, optional): Additional context information
            
        Returns:
            str: Formatted context for the LLM
        """
        context_parts = []
        
        # Add scenarios if available
        if scenarios:
            scenarios_text = "\n\n".join([
                f"SCENARIO {i+1}: {scenario['description']}\n"
                f"Expected Response: {scenario['expected_response']}"
                for i, scenario in enumerate(scenarios[:2])  # Limit to top 2 scenarios
            ])
            context_parts.append(f"RELEVANT TEACHING SCENARIOS:\n{scenarios_text}")
        
        # Add knowledge chunks if available
        if knowledge_chunks:
            knowledge_text = "\n\n".join([
                f"KNOWLEDGE {i+1} [{chunk['category'].upper()}]: {chunk['text']}\n"
                f"Source: {chunk['metadata'].get('source', 'Educational Knowledge Base')}"
                for i, chunk in enumerate(knowledge_chunks)
            ])
            context_parts.append(f"EDUCATIONAL KNOWLEDGE:\n{knowledge_text}")
        
        # Add additional context if provided
        if additional_context:
            additional_text = "\n".join([f"{k.upper()}: {v}" for k, v in additional_context.items()])
            context_parts.append(f"ADDITIONAL CONTEXT:\n{additional_text}")
        
        # Combine all context parts
        return "\n\n".join(context_parts)
    
    def _format_sources(self, scenarios: List[Dict], knowledge_chunks: List[Dict]) -> Dict:
        """
        Format source information for the response.
        
        Args:
            scenarios (List[Dict]): Retrieved teaching scenarios
            knowledge_chunks (List[Dict]): Retrieved knowledge chunks
            
        Returns:
            Dict: Formatted source information
        """
        sources = {
            "scenarios": [
                {
                    "id": scenario.get("id"),
                    "name": scenario.get("name", "Teaching Scenario"),
                    "similarity": scenario.get("similarity", 0)
                }
                for scenario in scenarios[:2]  # Limit to top 2 scenarios
            ],
            "knowledge": [
                {
                    "id": chunk.get("id"),
                    "category": chunk.get("category", "General"),
                    "source": chunk.get("metadata", {}).get("source", "Educational Knowledge Base"),
                    "similarity": chunk.get("similarity", 0)
                }
                for chunk in knowledge_chunks
            ]
        }
        return sources
    
    async def evaluate_response(self, scenario_id: str, teacher_response: str) -> Dict:
        """
        Evaluate a teacher's response to a scenario.
        
        This method compares the teacher's response to the expected response
        and provides feedback using the knowledge base.
        
        Args:
            scenario_id (str): The ID of the scenario
            teacher_response (str): The teacher's response to evaluate
            
        Returns:
            Dict: Evaluation results with feedback and score
        """
        # Retrieve the scenario
        scenario = await self.vector_ops.get_scenario(scenario_id)
        if not scenario:
            return {"error": "Scenario not found"}
        
        # Get relevant knowledge for evaluation
        knowledge_chunks = self.knowledge_retriever.search(
            f"evaluate teaching response for {scenario['name']}", 
            top_k=3
        )
        
        # Build evaluation context
        eval_context = {
            "scenario": scenario['description'],
            "expected_response": scenario['expected_response'],
            "teacher_response": teacher_response,
            "knowledge": "\n\n".join([chunk['text'] for chunk in knowledge_chunks])
        }
        
        # Generate evaluation using LLM
        evaluation = await self.llm.generate_evaluation(eval_context)
        
        # Track knowledge usage
        if knowledge_chunks:
            for chunk in knowledge_chunks:
                self.knowledge_retriever.update_usage_statistics(chunk["id"])
        
        return {
            "evaluation": evaluation,
            "sources": self._format_sources([], knowledge_chunks)
        }
    
    async def generate_scenario(self, parameters: Dict) -> Dict:
        """
        Generate a teaching scenario based on parameters.
        
        This method creates a realistic classroom scenario using the knowledge base.
        
        Args:
            parameters (Dict): Parameters for scenario generation
                (grade_level, subject, challenge_type, etc.)
            
        Returns:
            Dict: Generated scenario with context
        """
        # Build search query from parameters
        grade_level = parameters.get("grade_level", "elementary")
        subject = parameters.get("subject", "general")
        challenge_type = parameters.get("challenge_type", "classroom_management")
        
        search_query = f"{grade_level} {subject} {challenge_type} scenario"
        
        # Retrieve relevant knowledge
        knowledge_chunks = self.knowledge_retriever.search(
            search_query,
            category=challenge_type if challenge_type in self.knowledge_retriever.get_categories() else None,
            top_k=5
        )
        
        # Build generation context
        gen_context = {
            "parameters": parameters,
            "knowledge": "\n\n".join([chunk['text'] for chunk in knowledge_chunks])
        }
        
        # Generate scenario using LLM
        scenario = await self.llm.generate_scenario(gen_context)
        
        # Track knowledge usage
        if knowledge_chunks:
            for chunk in knowledge_chunks:
                self.knowledge_retriever.update_usage_statistics(chunk["id"])
        
        return {
            "scenario": scenario,
            "sources": self._format_sources([], knowledge_chunks)
        }

    async def add_documents(self, documents: List[Dict]):
        """
        Add new documents to the RAG pipeline.

        Args:
            documents (List[Dict]): List of documents to add, each containing
                                  'content' and 'metadata' fields

        Raises:
            ValueError: If documents are invalid
            RuntimeError: If storage fails
        """
        processed_docs = self._process_documents(documents)
        await self.vector_ops.store_documents(processed_docs)

    def get_performance_metrics(self) -> Dict:
        """
        Get performance metrics for the pipeline.

        Returns:
            Dict: Performance metrics including query time, embedding time,
                 and response generation time
        """
        return self._performance_metrics.copy()

    def _process_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Process documents for storage.

        Args:
            documents (List[Dict]): Raw documents to process

        Returns:
            List[Dict]: Processed documents with embeddings
        """
        for doc in documents:
            doc['embedding'] = self.embedder.generate_embedding(doc['content'])
        return documents

    def _format_context(self, results: List[Dict]) -> str:
        """
        Format retrieved results into context string.

        Args:
            results (List[Dict]): Retrieved similar documents

        Returns:
            str: Formatted context string
        """
        context_parts = []
        for result in results:
            context_parts.append(f"{result['content']}\n")
        return "\n".join(context_parts)

    def _prepare_result(self, response: str, context: str) -> Dict:
        """
        Prepare the final result dictionary.

        Args:
            response (str): Generated response
            context (str): Used context

        Returns:
            Dict: Final result with response and metadata
        """
        return {
            'response': response,
            'sources': self._extract_sources(context),
            'confidence': self._calculate_confidence(response)
        }

# ... existing code ... 