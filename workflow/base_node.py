"""
Base Workflow Node
Defines the core functionality for workflow nodes in the think tank system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from ..agents.base_agent import BaseAgent

class NodeState(BaseModel):
    """Represents the current state of a workflow node."""
    active: bool = False
    completed: bool = False
    iteration: int = 0
    results: Dict[str, Any] = {}
    errors: List[str] = []

class NodeConfig(BaseModel):
    """Configuration for a workflow node."""
    name: str
    description: str
    required_agents: List[str]
    max_iterations: int
    timeout_seconds: int
    auto_proceed: bool = True

class BaseWorkflowNode(ABC):
    """Abstract base class for all workflow nodes."""
    
    def __init__(self, config: NodeConfig):
        self.config = config
        self.state = NodeState()
        self.next_nodes: List['BaseWorkflowNode'] = []
        self.previous_nodes: List['BaseWorkflowNode'] = []
        self.participating_agents: Dict[str, BaseAgent] = {}
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data through this workflow node.
        
        Args:
            input_data: Data to be processed by this node
            
        Returns:
            Dict containing the processing results
        """
        pass
        
    async def connect_agent(self, agent: BaseAgent):
        """
        Connect an agent to this workflow node.
        
        Args:
            agent: The agent to connect to this node
        """
        if agent.personality.name.lower() in self.config.required_agents:
            self.participating_agents[agent.personality.name.lower()] = agent
            
    def add_next_node(self, node: 'BaseWorkflowNode'):
        """Add a node that should be processed after this one."""
        self.next_nodes.append(node)
        node.previous_nodes.append(self)
        
    async def validate_readiness(self) -> bool:
        """
        Check if the node is ready to process data.
        
        Returns:
            bool indicating if the node is ready
        """
        # Check if we have all required agents
        missing_agents = set(self.config.required_agents) - set(self.participating_agents.keys())
        if missing_agents:
            raise ValueError(f"Missing required agents: {missing_agents}")
            
        # Check if previous nodes are completed if any
        for prev_node in self.previous_nodes:
            if not prev_node.state.completed:
                return False
                
        return True
        
    async def start(self):
        """Prepare the node for processing."""
        self.state.active = True
        self.state.iteration = 0
        self.state.completed = False
        self.state.results.clear()
        self.state.errors.clear()
        
    async def complete(self, results: Dict[str, Any]):
        """
        Mark the node as completed with the given results.
        
        Args:
            results: The final results from this node's processing
        """
        self.state.active = False
        self.state.completed = True
        self.state.results = results
        
    async def handle_error(self, error: Exception):
        """
        Handle an error that occurred during processing.
        
        Args:
            error: The error that occurred
        """
        self.state.errors.append(str(error))
        if len(self.state.errors) >= self.config.max_iterations:
            raise RuntimeError(f"Max iterations ({self.config.max_iterations}) reached with errors")
            
    def __str__(self) -> str:
        return f"{self.config.name} Node (Active: {self.state.active}, Completed: {self.state.completed})"
