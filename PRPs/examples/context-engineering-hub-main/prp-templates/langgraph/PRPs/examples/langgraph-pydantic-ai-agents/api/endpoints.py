"""
Main API endpoints for the LangGraph LLM Routing Agent System.

This provides a FastAPI endpoint that integrates with LangGraph workflows,
conversation history, file attachments, and streaming responses.
"""
from typing import Optional, Dict, Any, AsyncIterator
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager, nullcontext
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import json
import os

from clients import get_agent_clients, get_model, get_langfuse_client
from pydantic_ai import Agent
from langfuse import observe

# Import our models and utilities
from api.models import (
    AgentRequest, HealthCheckResponse
)
from api.streaming import create_error_stream
from graph.workflow import create_api_initial_state
from .db_utils import (
    fetch_conversation_history,
    create_conversation,
    update_conversation_title,
    generate_session_id,
    generate_conversation_title,
    store_message,
    convert_history_to_pydantic_format,
    check_rate_limit,
    store_request
)

# Check if we're in production
is_production = os.getenv("ENVIRONMENT") == "production"

if not is_production:
    # Development: prioritize .env file
    project_root = Path(__file__).resolve().parent
    dotenv_path = project_root / '.env'
    load_dotenv(dotenv_path, override=True)
else:
    # Production: use cloud platform env vars only
    load_dotenv()

# Global clients (initialized in lifespan)
embedding_client = None
supabase = None
http_client = None
title_agent = None
langfuse = None

# FastAPI app setup
security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
    """
    Verify the JWT token from Supabase and return the user information.
    
    Args:
        credentials: The HTTP Authorization credentials containing the bearer token
        
    Returns:
        Dict[str, Any]: The user information from Supabase
        
    Raises:
        HTTPException: If the token is invalid or the user cannot be verified
    """
    try:
        # Get the token from the Authorization header
        token = credentials.credentials
        
        # Access the global HTTP client
        global http_client
        if not http_client:
            raise HTTPException(status_code=500, detail="HTTP client not initialized")
        
        # Get the Supabase URL and anon key from environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        # Make request to Supabase auth API to get user info
        response = await http_client.get(
            f"{supabase_url}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": supabase_key
            }
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Auth response error: {response.text}")
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        # Return the user information
        user_data = response.json()
        return user_data
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI application."""
    global embedding_client, supabase, http_client, title_agent, langfuse
    
    # Startup: Initialize all clients
    embedding_client, supabase, http_client = get_agent_clients()
    title_agent = Agent(model=get_model())
    langfuse = get_langfuse_client()
    
    yield  # This is where the app runs
    
    # Shutdown: Clean up resources
    if http_client:
        await http_client.aclose()


# Initialize FastAPI app with lifespan
def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="LangGraph Parallel Research Agents System",
        version="1.0.0",
        description="Parallel research agents system: 3 agents (SEO, Social, Competitor) run simultaneously for comprehensive research synthesis",
        lifespan=lifespan
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


app = create_app()


@app.post("/api/langgraph-parallel-agents")
async def langgraph_routing_agents_endpoint(
    request: AgentRequest, 
    user: Dict[str, Any] = Depends(verify_token)
):
    """
    LangGraph parallel agent workflow endpoint with streaming and conversation history.
    Parallel flow: 3 research agents (SEO, Social, Competitor) run simultaneously, 
    then synthesis agent combines findings into email draft.
    
    Args:
        request: Agent request with query, session info, and optional files
        user: Verified user information from JWT token
        
    Returns:
        StreamingResponse or AgentResponse
    """
    # Verify that the user ID in the request matches the user ID from the token
    if request.user_id != user.get("id"):
        error_stream = create_error_stream(
            "User ID in request does not match authenticated user", 
            request.session_id
        )
        return StreamingResponse(
                error_stream.stream_error(),
                media_type='text/plain'
            )
    
    try:
        # Check rate limit
        rate_limit_ok = await check_rate_limit(supabase, request.user_id)
        if not rate_limit_ok:
            error_msg = "Rate limit exceeded. Please try again later."
            error_stream = create_error_stream(error_msg, request.session_id)
            return StreamingResponse(
                error_stream.stream_error(),
                media_type='text/plain'
            )
        
        # Start request tracking in parallel
        request_tracking_task = asyncio.create_task(
            store_request(supabase, request.request_id, request.user_id, request.query)
        )
        
        session_id = request.session_id
        conversation_record = None
        
        # Check if session_id is empty, create a new conversation if needed
        if not session_id:
            session_id = generate_session_id(request.user_id)
            conversation_record = await create_conversation(supabase, request.user_id, session_id)
        
        # Store user's query immediately (no file support in simplified version)
        await store_message(
            supabase=supabase,
            session_id=session_id,
            message_type="human",
            content=request.query
        )
        
        # Fetch conversation history from the DB
        conversation_history = await fetch_conversation_history(supabase, session_id)
        
        # Convert conversation history to Pydantic AI format
        pydantic_messages = await convert_history_to_pydantic_format(conversation_history)
        
        # Start title generation in parallel if this is a new conversation
        title_task = None
        if conversation_record:
            title_task = asyncio.create_task(
                generate_conversation_title(title_agent, request.query)
            )
        
        # Create simplified initial state
        initial_state = create_api_initial_state(
            query=request.query,
            session_id=session_id,
            request_id=request.request_id,
            pydantic_message_history=pydantic_messages
        )
        
        # Return streaming response
        return StreamingResponse(
            stream_langgraph_response(
                initial_state=initial_state,
                session_id=session_id,
                title_task=title_task,
                request_tracking_task=request_tracking_task,
                user_id=request.user_id
            ),
            media_type="text/plain"
        )
    
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        
        # Store error message in conversation if session_id exists
        if session_id:
            await store_message(
                supabase=supabase,
                session_id=session_id,
                message_type="ai",
                content="I apologize, but I encountered an error processing your request.",
                data={"error": str(e), "request_id": request.request_id}
            )
        
        # Return error response
        error_stream = create_error_stream(f"Error: {str(e)}", session_id)
        return StreamingResponse(
            error_stream.stream_error(),
            media_type='text/plain'
        )


async def stream_langgraph_response(
    initial_state: Dict[str, Any],
    session_id: str,
    title_task: Optional[asyncio.Task] = None,
    request_tracking_task: Optional[asyncio.Task] = None,
    user_id: Optional[str] = None
) -> AsyncIterator[bytes]:
    """
    Stream LangGraph workflow response with real-time token streaming using custom stream mode.
    
    Args:
        initial_state: Initial state for LangGraph
        session_id: Session ID for database operations
        title_task: Optional title generation task
        request_tracking_task: Optional request tracking task
        
    Yields:
        Streaming response bytes with real-time tokens
    """
    try:
        # Import workflow directly
        from graph.workflow import workflow
        
        thread_id = f"llm-routing-{session_id}"
        config = {"configurable": {"thread_id": thread_id}}
        
        # Add LangFuse callback if available
        tracing_span = nullcontext()
        if langfuse:
            try:
                from langfuse.langchain import CallbackHandler
                langfuse_handler = CallbackHandler()
                config["callbacks"] = [langfuse_handler]

                # Start the Langfuse trace
                tracing_span = langfuse.start_as_current_span(name="parallel-agents", input={"user_query": initial_state["query"]})
            except Exception as e:
                print(e)
        
        full_response = ""
        final_state = None
        
        # Use astream with stream_mode="custom" to get real-time streaming
        with tracing_span as span:
            # Update Langfuse trace with user ID and session ID
            if langfuse and span:
                span.update_trace(user_id=user_id, session_id=session_id)

            async for stream_mode, chunk in workflow.astream(
                initial_state, config, stream_mode=["custom", "values"]
            ):
                if stream_mode == "custom":
                    # Custom streaming content from writer() calls in nodes
                    if isinstance(chunk, str):
                        # Direct string content from writer
                        full_response += chunk
                        chunk_data = {"text": full_response}
                        yield json.dumps(chunk_data).encode('utf-8') + b'\n'
                    elif isinstance(chunk, bytes):
                        # Bytes content, decode and yield
                        try:
                            decoded = chunk.decode('utf-8')
                            full_response += decoded
                            chunk_data = {"text": full_response}
                            yield json.dumps(chunk_data).encode('utf-8') + b'\n'
                        except Exception:
                            # If can't decode, yield as-is
                            yield chunk
                elif stream_mode == "values":
                    # State values - the last one will be our final state
                    final_state = chunk

            # Update Langfuse trace with output
            if langfuse and span:
                span.update(output={"agent_response": full_response})                
            
        # Store agent's response in database - always store even if final_state is incomplete
        # Use collected full_response as primary content, final_state for metadata
        try:
            # Handle message_history which contains bytes objects
            message_data = final_state.get("message_history", []) if final_state else []
            if message_data and len(message_data) > 0:
                # message_data contains bytes, use the first one directly
                message_data_bytes = message_data[0] if isinstance(message_data[0], bytes) else None
            else:
                message_data_bytes = None
            
            # Ensure we always store the response, even with minimal data
            await store_message(
                supabase=supabase,
                session_id=session_id,
                message_type="ai",
                content=full_response or "No response generated",  # Use collected streaming response
                message_data=message_data_bytes,
                data={
                    "request_id": initial_state["request_id"],
                    "routing_decision": final_state.get("routing_decision", "unknown") if final_state else "unknown",
                    "streaming_tokens_collected": len(full_response) if full_response else 0
                }
            )
        except Exception as db_error:
            print(f"Database storage error: {db_error}")
        
        # Handle title generation if it's running
        if title_task:
            try:
                conversation_title = await title_task
                await update_conversation_title(supabase, session_id, conversation_title)
                
                # Send final chunk with title
                final_chunk = {
                    "session_id": session_id,
                    "conversation_title": conversation_title,
                    "complete": True,
                    "request_id": initial_state["request_id"],
                    "final_response": full_response,
                    "routing_decision": final_state.get("routing_decision", "unknown") if final_state else "unknown"
                }
                yield json.dumps(final_chunk).encode('utf-8') + b'\n'
            except Exception as e:
                print(f"Error processing title: {str(e)}")
        
        # Wait for request tracking task
        if request_tracking_task:
            try:
                await request_tracking_task
            except Exception as e:
                print(f"Error tracking request: {str(e)}")
        
    except Exception as e:
        print(e)
        error_msg = f"Streaming error: {str(e)}"
        error_chunk = {"text": error_msg}
        yield json.dumps(error_chunk).encode('utf-8') + b'\n'


@app.get("/health")
async def health_check() -> HealthCheckResponse:
    """Health check endpoint for container orchestration and monitoring."""
    try:
        # Check if critical dependencies are initialized
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": "LangGraph Parallel Research Agents System is running",
            "dependencies": {
                "embedding_client": "connected" if embedding_client else "disconnected",
                "supabase": "connected" if supabase else "disconnected", 
                "http_client": "connected" if http_client else "disconnected",
                "title_agent": "connected" if title_agent else "disconnected"
            }
        }
        
        # If any critical service is not initialized, mark as unhealthy
        if not all(v == "connected" for v in health_status["dependencies"].values()):
            health_status["status"] = "unhealthy"
            raise HTTPException(status_code=503, detail=health_status)
        
        return HealthCheckResponse(**health_status)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=503, 
            detail={
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}"
            }
        )


@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "system": "LangGraph Parallel Research Agents System",
        "version": "1.0.0", 
        "description": "Parallel research agents system: 3 agents (SEO, Social, Competitor) run simultaneously for comprehensive research synthesis",
        "endpoints": {
            "POST /api/langgraph-parallel-agents": "Main LangGraph parallel research agents endpoint with streaming",
            "GET /health": "Health check endpoint",
            "GET /": "System information"
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)