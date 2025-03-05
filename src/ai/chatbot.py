from langchain_ollama import OllamaLLM
from typing import Dict, List, Optional
import json
import logging
from .rag_pipeline import RAGPipeline
from .knowledge_retriever import KnowledgeRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TeacherTrainingChatbot:
    def __init__(self):
        """Initialize the teacher training chatbot with Llama model and educational components"""
        try:
            self.llm = OllamaLLM(model="llama3.1")
            logger.info("Successfully initialized Llama model")
        except Exception as e:
            logger.error(f"Failed to initialize Llama model: {str(e)}")
            raise

        # Initialize RAG pipeline with knowledge base integration
        self.rag_pipeline = RAGPipeline()
        
        # Initialize knowledge retriever for direct knowledge access
        self.knowledge_retriever = KnowledgeRetriever()
        
        # Educational scenario categories
        self.categories = {
            "classroom_management": {
                "description": "Handling classroom behavior and organization",
                "skills": ["behavior management", "time management", "classroom organization"]
            },
            "learning_difficulties": {
                "description": "Supporting students with learning challenges",
                "skills": ["differentiated instruction", "learning assessment", "intervention strategies"]
            },
            "behavioral_issues": {
                "description": "Addressing student behavioral concerns",
                "skills": ["conflict resolution", "positive reinforcement", "behavioral intervention"]
            },
            "special_needs": {
                "description": "Supporting students with special educational needs",
                "skills": ["IEP implementation", "accommodation strategies", "inclusive practices"]
            }
        }

        # Student personas with detailed characteristics
        self.student_personas = {
            "active": {
                "personality": "Energetic and enthusiastic",
                "challenges": "Struggles with focus and following instructions",
                "strengths": "High participation and creativity",
                "learning_style": "Kinesthetic learner"
            },
            "shy": {
                "personality": "Quiet and reserved",
                "challenges": "Hesitant to participate or ask questions",
                "strengths": "Good listener and written work",
                "learning_style": "Reflective learner"
            },
            "struggling": {
                "personality": "Determined but frustrated",
                "challenges": "Difficulty grasping core concepts",
                "strengths": "Persistent and hardworking",
                "learning_style": "Needs multi-modal approach"
            },
            "disruptive": {
                "personality": "Attention-seeking and restless",
                "challenges": "Interrupts class and distracts others",
                "strengths": "Natural leadership qualities",
                "learning_style": "Active learner"
            },
            "gifted": {
                "personality": "Intellectually curious",
                "challenges": "Gets bored with regular pace",
                "strengths": "Quick comprehension and deep thinking",
                "learning_style": "Abstract learner"
            }
        }

        # Conversation history for context
        self.conversation_history = []

    async def initialize(self):
        """Initialize the chatbot components"""
        await self.rag_pipeline.initialize()
        logger.info("Chatbot initialization complete")
        
        # Log knowledge base status
        categories = self.knowledge_retriever.get_categories()
        if categories:
            logger.info(f"Knowledge base available with categories: {', '.join(categories)}")
        else:
            logger.warning("Knowledge base not available or empty")
            
    async def generate_response(self, query: str, context: Dict = None) -> Dict:
        """
        Generate a response to a user query using the RAG pipeline with knowledge enhancement.
        
        Args:
            query (str): The user's query
            context (Dict, optional): Additional context for the query
            
        Returns:
            Dict: Response with generated text and sources
        """
        try:
            # Process query through RAG pipeline with knowledge base
            response = await self.rag_pipeline.process_query(query, context, use_knowledge_base=True)
            logger.info(f"Generated response for query: {query[:50]}...")
            return response
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": "I'm sorry, I encountered an error while processing your request.",
                "error": str(e)
            }
            
    async def generate_knowledge_scenario(self, parameters: Dict) -> Dict:
        """
        Generate a teaching scenario based on parameters using the knowledge base.
        
        Args:
            parameters (Dict): Parameters for scenario generation
                (grade_level, subject, challenge_type, etc.)
                
        Returns:
            Dict: Generated scenario with context and sources
        """
        try:
            # Generate scenario through RAG pipeline with knowledge base
            scenario = await self.rag_pipeline.generate_scenario(parameters)
            logger.info(f"Generated scenario with parameters: {json.dumps(parameters)}")
            return scenario
        except Exception as e:
            logger.error(f"Error generating scenario: {str(e)}")
            return {
                "scenario": "I'm sorry, I encountered an error while generating the scenario.",
                "error": str(e)
            }
            
    async def evaluate_response(self, scenario_id: str, teacher_response: str) -> Dict:
        """
        Evaluate a teacher's response to a scenario.
        
        Args:
            scenario_id (str): The ID of the scenario
            teacher_response (str): The teacher's response to evaluate
            
        Returns:
            Dict: Evaluation results with feedback and score
        """
        try:
            # Evaluate response through RAG pipeline with knowledge base
            evaluation = await self.rag_pipeline.evaluate_response(scenario_id, teacher_response)
            logger.info(f"Evaluated response for scenario {scenario_id}")
            return evaluation
        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            return {
                "evaluation": "I'm sorry, I encountered an error while evaluating the response.",
                "error": str(e)
            }
            
    def get_knowledge_categories(self) -> List[str]:
        """
        Get all available knowledge categories.
        
        Returns:
            List[str]: List of unique category names
        """
        return self.knowledge_retriever.get_categories()
        
    def search_knowledge(self, query: str, category: Optional[str] = None, top_k: int = 5) -> List[Dict]:
        """
        Search the knowledge base for relevant information.
        
        Args:
            query (str): The search query
            category (str, optional): Filter by knowledge category
            top_k (int): Number of results to return
            
        Returns:
            List[Dict]: List of knowledge chunks with metadata and similarity scores
        """
        return self.knowledge_retriever.search(query, category, top_k)
        
    def get_most_effective_knowledge(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Get the most effective knowledge chunks based on usage and effectiveness scores.
        
        Args:
            category (str, optional): Filter by knowledge category
            limit (int): Maximum number of results to return
            
        Returns:
            List[Dict]: List of knowledge chunks with metadata and effectiveness scores
        """
        return self.knowledge_retriever.get_most_effective_knowledge(category, limit)

    def generate_scenario(self, category: str, persona: str) -> Dict:
        """Generate a detailed educational scenario"""
        if category not in self.categories or persona not in self.student_personas:
            raise ValueError("Invalid category or persona")

        prompt = f"""
        Create a detailed elementary classroom scenario with the following context:
        
        Category: {category}
        Category Description: {self.categories[category]['description']}
        Required Skills: {', '.join(self.categories[category]['skills'])}
        
        Student Profile:
        - Personality: {self.student_personas[persona]['personality']}
        - Challenges: {self.student_personas[persona]['challenges']}
        - Strengths: {self.student_personas[persona]['strengths']}
        - Learning Style: {self.student_personas[persona]['learning_style']}
        
        Provide:
        1. Detailed situation description
        2. Specific student behaviors and triggers
        3. Classroom context and environment
        4. Immediate challenges for the teacher
        5. Learning objectives affected
        6. Other students' potential reactions
        7. Key considerations for resolution
        
        Format the response as a structured scenario that requires teacher intervention.
        """

        try:
            response = self.llm.invoke(prompt)
            scenario = {
                "category": category,
                "persona": persona,
                "description": response,
                "context": {
                    "category_info": self.categories[category],
                    "student_info": self.student_personas[persona]
                }
            }
            return scenario
        except Exception as e:
            logger.error(f"Error generating scenario: {str(e)}")
            raise

    def evaluate_response(self, scenario: Dict, teacher_response: str) -> Dict:
        """Evaluate teacher's response to a scenario"""
        evaluation_prompt = f"""
        As an educational expert, evaluate this teacher's response to the following scenario:
        
        Scenario Category: {scenario['category']}
        Required Skills: {', '.join(self.categories[scenario['category']]['skills'])}
        
        Student Profile:
        {json.dumps(scenario['context']['student_info'], indent=2)}
        
        Scenario:
        {scenario['description']}
        
        Teacher's Response:
        {teacher_response}
        
        Provide a detailed evaluation addressing:
        1. Professional Appropriateness (1-10):
           - Alignment with educational best practices
           - Professional tone and approach
           
        2. Educational Effectiveness (1-10):
           - Impact on student learning
           - Alignment with learning objectives
           
        3. Student Well-being (1-10):
           - Consideration of student's needs
           - Emotional support and understanding
           
        4. Classroom Management (1-10):
           - Immediate situation handling
           - Long-term behavioral impact
           
        5. Specific Strengths:
           - List key effective elements
           
        6. Areas for Improvement:
           - Provide actionable suggestions
           
        7. Alternative Approaches:
           - Suggest other effective strategies
        
        Format the response as a structured evaluation with clear sections and numerical scores.
        """

        try:
            response = self.llm.invoke(evaluation_prompt)
            return {
                "scenario": scenario,
                "teacher_response": teacher_response,
                "evaluation": response
            }
        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            raise

    def get_improvement_suggestions(self, evaluation_result: Dict) -> str:
        """Generate specific improvement suggestions based on evaluation"""
        prompt = f"""
        Based on the following evaluation of a teacher's response:
        
        {evaluation_result['evaluation']}
        
        Provide specific, actionable suggestions for improvement focusing on:
        1. Practical classroom strategies
        2. Communication techniques
        3. Student engagement methods
        4. Behavioral management approaches
        5. Professional development areas
        
        Format suggestions as clear, implementable steps.
        """

        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            raise

    def save_interaction(self, scenario: Dict, response: str, evaluation: Dict) -> None:
        """Save the interaction for learning and analysis"""
        interaction = {
            "timestamp": "timestamp_here",  # Add actual timestamp
            "scenario": scenario,
            "teacher_response": response,
            "evaluation": evaluation
        }
        self.conversation_history.append(interaction)
        # TODO: Implement database storage

def main():
    """Test the chatbot functionality"""
    try:
        # Initialize chatbot
        chatbot = TeacherTrainingChatbot()
        
        # Generate test scenario
        scenario = chatbot.generate_scenario("classroom_management", "active")
        print("\nGenerated Scenario:")
        print(json.dumps(scenario, indent=2))
        
        # Test teacher response
        test_response = """
        I would first observe the student's behavior to understand the triggers. 
        Then, I would quietly approach them and provide clear, specific feedback about the behavior.
        I would redirect their energy to productive tasks and use positive reinforcement when they display appropriate behavior.
        If needed, I would implement a simple behavior management plan with clear expectations and consequences.
        """
        
        # Evaluate response
        evaluation = chatbot.evaluate_response(scenario, test_response)
        print("\nResponse Evaluation:")
        print(json.dumps(evaluation, indent=2))
        
        # Get improvement suggestions
        suggestions = chatbot.get_improvement_suggestions(evaluation)
        print("\nImprovement Suggestions:")
        print(suggestions)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 