"""
API models for the LangGraph RAG Guardrail Agent System.

These models match the patterns from examples/agent_api.py to ensure
compatibility with existing client applications.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class FileAttachment(BaseModel):
    """File attachment model for uploads"""
    fileName: str
    content: str  # Base64 encoded content
    mimeType: str


class AgentRequest(BaseModel):
    """Request model for the RAG guardrail agent endpoint"""
    query: str
    user_id: str
    request_id: str
    session_id: str
    files: Optional[List[FileAttachment]] = None


class AgentResponse(BaseModel):
    """Response model for non-streaming responses"""
    response: str
    session_id: str
    conversation_title: Optional[str] = None
    request_id: str
    # Router-specific fields
    agent_type: str = "unknown"
    routing_decision: str = "unknown"
    streaming_success: bool = True
    # Legacy fields for backward compatibility
    citations: List[str] = []
    validation_passed: bool = True
    iterations: int = 0


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    message: str
    dependencies: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    session_id: str = ""
    request_id: str = ""
    complete: bool = True


# Streaming response chunk models (for documentation)
class TextChunk(BaseModel):
    """Text streaming chunk"""
    text: str


class ValidationChunk(BaseModel):
    """Validation streaming chunk"""
    validation: str


class ErrorChunk(BaseModel):
    """Error streaming chunk"""
    error: str


class FinalSummaryChunk(BaseModel):
    """Final summary streaming chunk"""
    final_summary: Dict[str, Any]


class CompleteChunk(BaseModel):
    """Final completion chunk"""
    text: str
    session_id: str
    conversation_title: Optional[str] = None
    complete: bool = True
    request_id: str = ""