from typing import TypedDict, List, Optional, Annotated
from pydantic_ai.messages import ModelMessage
import operator

class ParallelAgentState(TypedDict, total=False):
    """LangGraph state for parallel research workflow"""
    # Input
    query: str
    session_id: str  
    request_id: str
    
    # Guardrail output
    is_research_request: bool
    routing_reason: str
    
    # Parallel research outputs - using operator.add for state merging
    seo_research: Annotated[List[str], operator.add]
    social_research: Annotated[List[str], operator.add]
    competitor_research: Annotated[List[str], operator.add]
    research_completed: Annotated[List[str], operator.add]
    
    # Synthesis output
    synthesis_complete: bool
    
    # Final response
    final_response: str
    
    # Message history management
    pydantic_message_history: List[ModelMessage]
    message_history: List[bytes]  # Only populated by synthesis/fallback
    
    # API context
    conversation_title: Optional[str]
    is_new_conversation: Optional[bool]

# Legacy alias for backwards compatibility
SequentialAgentState = ParallelAgentState