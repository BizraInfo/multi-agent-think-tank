"""
Configuration management for the Multi-Agent Think Tank system.
"""

from typing import Dict, Any, List
from pathlib import Path
from pydantic import BaseModel, BaseSettings
from decouple import config

class AgentConfig(BaseModel):
    """Configuration for individual agents."""
    name: str
    role: str
    traits: Dict[str, float]
    expertise: List[str]
    llm_model: str
    temperature: float
    max_tokens: int

class WorkflowConfig(BaseModel):
    """Configuration for workflow nodes."""
    enabled_nodes: List[str]
    max_iterations: int
    timeout_seconds: int
    auto_loop: bool

class SystemConfig(BaseSettings):
    """Main system configuration."""
    # API Configuration
    openai_api_key: str = config('OPENAI_API_KEY', default='')
    
    # Agent Settings
    agents: Dict[str, AgentConfig] = {
        "strategist": AgentConfig(
            name="Strategist",
            role="Long-term planning and direction",
            traits={"analytical": 0.8, "strategic": 0.9, "creative": 0.6},
            expertise=["strategic planning", "goal setting", "risk assessment"],
            llm_model="gpt-4",
            temperature=0.7,
            max_tokens=1000
        ),
        "analyst": AgentConfig(
            name="Analyst",
            role="Data-driven pattern recognition",
            traits={"analytical": 0.95, "detail_oriented": 0.9, "systematic": 0.85},
            expertise=["data analysis", "pattern recognition", "statistical inference"],
            llm_model="gpt-4",
            temperature=0.3,
            max_tokens=1000
        ),
        "creative": AgentConfig(
            name="Creative Thinker",
            role="Novel idea generation",
            traits={"creative": 0.95, "intuitive": 0.8, "open_minded": 0.9},
            expertise=["brainstorming", "innovation", "lateral thinking"],
            llm_model="gpt-4",
            temperature=0.9,
            max_tokens=1000
        ),
        "synthesizer": AgentConfig(
            name="Synthesizer",
            role="Concept connection and integration",
            traits={"analytical": 0.7, "creative": 0.7, "systematic": 0.8},
            expertise=["concept integration", "pattern synthesis", "knowledge mapping"],
            llm_model="gpt-4",
            temperature=0.6,
            max_tokens=1000
        ),
        "implementer": AgentConfig(
            name="Implementer",
            role="Practical execution planning",
            traits={"practical": 0.9, "detail_oriented": 0.85, "systematic": 0.8},
            expertise=["execution planning", "resource allocation", "task management"],
            llm_model="gpt-4",
            temperature=0.4,
            max_tokens=1000
        ),
        "researcher": AgentConfig(
            name="Researcher",
            role="Deep knowledge exploration",
            traits={"analytical": 0.85, "thorough": 0.9, "curious": 0.8},
            expertise=["research methodology", "information synthesis", "knowledge discovery"],
            llm_model="gpt-4",
            temperature=0.5,
            max_tokens=1000
        ),
        "challenger": AgentConfig(
            name="Challenger",
            role="Critical evaluation",
            traits={"critical": 0.9, "analytical": 0.8, "objective": 0.85},
            expertise=["critical analysis", "risk assessment", "assumption testing"],
            llm_model="gpt-4",
            temperature=0.6,
            max_tokens=1000
        )
    }
    
    # Workflow Settings
    workflow: WorkflowConfig = WorkflowConfig(
        enabled_nodes=["problem_definition", "brainstorming", "analysis", 
                      "synthesis", "evaluation", "decision", "action"],
        max_iterations=5,
        timeout_seconds=300,
        auto_loop=True
    )
    
    # System Settings
    debug_mode: bool = config('DEBUG_MODE', default=False, cast=bool)
    log_level: str = config('LOG_LEVEL', default='INFO')
    max_concurrent_tasks: int = config('MAX_CONCURRENT_TASKS', default=3, cast=int)
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

def load_config() -> SystemConfig:
    """Load and return the system configuration."""
    return SystemConfig()
