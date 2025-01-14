"""
Base Agent Class
Defines the core functionality and interface that all agents must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class AgentPersonality(BaseModel):
    """Defines the personality traits of an agent."""
    name: str
    traits: Dict[str, float]  # e.g., {'analytical': 0.8, 'creative': 0.4}
    expertise: List[str]
    description: str

class AgentState(BaseModel):
    """Represents the current state of an agent."""
    current_task: Optional[str] = None
    memory: Dict[str, Any] = {}
    confidence: float = 1.0
    context: Dict[str, Any] = {}

class BaseAgent(ABC):
    """Abstract base class for all agents in the think tank."""
    
    def __init__(self, personality: AgentPersonality):
        self.personality = personality
        self.state = AgentState()
        self.knowledge_base = None
        
    @abstractmethod
    async def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process input data according to the agent's specialty.
        
        Args:
            input_data: The data to be processed
            
        Returns:
            Dict containing the processing results
        """
        pass
        
    @abstractmethod
    async def collaborate(self, other_agent: 'BaseAgent', context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collaborate with another agent on a task.
        
        Args:
            other_agent: The agent to collaborate with
            context: Shared context for the collaboration
            
        Returns:
            Dict containing the collaboration results
        """
        pass
        
    async def update_state(self, new_state: Dict[str, Any]):
        """Update the agent's current state."""
        for key, value in new_state.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
                
    async def access_knowledge_base(self, query: str) -> Any:
        """
        Access the agent's knowledge base.
        
        Args:
            query: The query to search for in the knowledge base
            
        Returns:
            Retrieved information from the knowledge base
        """
        if self.knowledge_base is None:
            raise ValueError("Knowledge base not initialized")
        return await self.knowledge_base.query(query)
        
    async def reflect(self) -> Dict[str, Any]:
        """
        Perform self-reflection on current state and recent actions.
        
        Returns:
            Dict containing insights from reflection
        """
        # TODO: Implement reflection logic
        return {
            "state": self.state.dict(),
            "confidence": self.state.confidence,
            "current_focus": self.state.current_task
        }
        
    def __str__(self) -> str:
        return f"{self.personality.name} ({', '.join(self.personality.expertise)})"
