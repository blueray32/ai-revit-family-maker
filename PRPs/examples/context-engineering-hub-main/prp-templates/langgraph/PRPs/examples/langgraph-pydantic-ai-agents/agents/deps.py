from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class GuardrailDependencies:
    """Guardrail agent dependencies - minimal for fast decisions"""
    session_id: Optional[str] = None

@dataclass
class ResearchAgentDependencies:
    """Dependencies for the research agent"""
    brave_api_key: str
    session_id: Optional[str] = None

def create_guardrail_deps(session_id: Optional[str] = None) -> GuardrailDependencies:
    """Create GuardrailDependencies instance for fast guardrail decisions"""
    return GuardrailDependencies(session_id=session_id)

def create_research_deps(session_id: Optional[str] = None) -> ResearchAgentDependencies:
    """Create ResearchAgentDependencies instance"""
    brave_api_key = os.getenv("BRAVE_API_KEY", "")
    
    return ResearchAgentDependencies(
        brave_api_key=brave_api_key,
        session_id=session_id
    )