"""
HTTP Streaming Bridge for LangGraph to FastAPI integration.

This module provides the bridge between LangGraph's StreamWriter interface
and FastAPI's streaming response, allowing real-time streaming of agent
responses through HTTP.
"""
import asyncio
import json
from typing import AsyncIterator, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class StreamBridge:
    """Bridge between LangGraph StreamWriter and HTTP streaming"""
    
    # Internal queue for streaming chunks
    _chunks: asyncio.Queue = field(default_factory=asyncio.Queue)
    _completed: bool = field(default=False)
    _final_data: Optional[Dict[str, Any]] = field(default=None)
    
    def write(self, data: bytes) -> None:
        """
        StreamWriter interface - called by LangGraph workflow.
        
        Args:
            data: Bytes to stream (usually JSON-encoded)
        """
        print(f"🌊 StreamBridge.write called with: {data[:100]}...")  # Debug logging
        # Put data into the queue for HTTP streaming - handle both sync and async contexts
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in an async context, create a task
                asyncio.create_task(self._chunks.put(data))
            else:
                # We're in a sync context, run directly
                loop.run_until_complete(self._chunks.put(data))
        except RuntimeError:
            # No event loop, create new one
            asyncio.run(self._chunks.put(data))
    
    async def stream_http(self) -> AsyncIterator[bytes]:
        """
        HTTP streaming interface - called by FastAPI.
        
        Yields:
            Bytes to stream to HTTP client
        """
        while True:
            try:
                # Wait for next chunk with timeout
                chunk = await asyncio.wait_for(self._chunks.get(), timeout=1.0)  # Increased timeout
                
                if chunk is None:  # End signal
                    break
                    
                yield chunk
                
            except asyncio.TimeoutError:
                # Check if workflow completed
                if self._completed:
                    break
                continue
        
        # Yield final summary if available
        if self._final_data:
            final_chunk = json.dumps({
                "final_summary": self._final_data
            }).encode('utf-8') + b'\n'
            yield final_chunk
    
    def complete(self, final_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Signal completion of streaming.
        
        Args:
            final_data: Optional final data to include in stream
        """
        self._completed = True
        self._final_data = final_data
        # Send end signal
        asyncio.create_task(self._chunks.put(None))


class ErrorStreamBridge:
    """Specialized bridge for streaming errors"""
    
    def __init__(self, error_message: str, session_id: str = ""):
        self.error_message = error_message
        self.session_id = session_id
    
    async def stream_error(self) -> AsyncIterator[bytes]:
        """Stream error response"""
        # First yield the error message as text
        yield json.dumps({"text": self.error_message}).encode('utf-8') + b'\n'
        
        # Then yield final error chunk
        final_data = {
            "text": self.error_message,
            "session_id": self.session_id,
            "error": self.error_message,
            "complete": True
        }
        yield json.dumps(final_data).encode('utf-8') + b'\n'


def create_stream_bridge() -> StreamBridge:
    """Factory function to create a new stream bridge"""
    return StreamBridge()


def create_error_stream(error_message: str, session_id: str = "") -> ErrorStreamBridge:
    """Factory function to create an error stream bridge"""
    return ErrorStreamBridge(error_message, session_id)


# Utility functions for common streaming patterns

async def stream_workflow_response(
    workflow_func,
    initial_state: Dict[str, Any],
    *args,
    **kwargs
) -> AsyncIterator[bytes]:
    """
    Generic function to stream a LangGraph workflow response.
    
    Args:
        workflow_func: The LangGraph workflow function to execute
        initial_state: Initial state for the workflow
        *args, **kwargs: Additional arguments for the workflow
        
    Yields:
        Bytes to stream to HTTP client
    """
    # Create stream bridge
    bridge = create_stream_bridge()
    
    try:
        # Run workflow in background task
        workflow_task = asyncio.create_task(
            workflow_func(initial_state, bridge, *args, **kwargs)
        )
        
        # Stream responses as they come
        async for chunk in bridge.stream_http():
            yield chunk
        
        # Wait for workflow completion and get final state
        await workflow_task
        
        # The bridge will handle final summary streaming
        
    except Exception as e:
        # Stream error if workflow fails
        error_bridge = create_error_stream(f"Workflow error: {str(e)}")
        async for error_chunk in error_bridge.stream_error():
            yield error_chunk


async def stream_json_chunks(data_stream: AsyncIterator[Dict[str, Any]]) -> AsyncIterator[bytes]:
    """
    Convert an async iterator of dictionaries to JSON byte chunks.
    
    Args:
        data_stream: AsyncIterator yielding dictionaries
        
    Yields:
        JSON-encoded byte chunks
    """
    async for data in data_stream:
        chunk = json.dumps(data).encode('utf-8') + b'\n'
        yield chunk