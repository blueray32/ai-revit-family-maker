"""
Database utility functions for the Agent API.

This module contains functions for interacting with the database,
including conversation and message management.
"""
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from supabase import Client
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter
import random
import string


async def fetch_conversation_history(supabase: Client, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Fetch the most recent conversation history for a session."""
    try:
        response = supabase.table("messages") \
            .select("*") \
            .eq("session_id", session_id) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        # Convert to list and reverse to get chronological order
        messages = response.data[::-1]
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch conversation history: {str(e)}")


async def create_conversation(supabase: Client, user_id: str, session_id: str) -> Dict[str, Any]:
    """Create a new conversation record in the database.
    
    Args:
        user_id (str): The user ID
        session_id (str): The session ID
        
    Returns:
        Dict[str, Any]: The created conversation record
    
    """
    try:
        response = supabase.table("conversations") \
            .insert({"user_id": user_id, "session_id": session_id}) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create conversation record")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")


async def update_conversation_title(supabase: Client, session_id: str, title: str) -> Dict[str, Any]:
    """Update the title of a conversation.
    
    Args:
        session_id (int): The conversation session ID
        title (str): The new title
        
    Returns:
        Dict[str, Any]: The updated conversation record
    
    """
    try:
        response = supabase.table("conversations") \
            .update({"title": title}) \
            .eq("session_id", session_id) \
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to update conversation title")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update conversation title: {str(e)}")


def generate_session_id(user_id: str) -> str:
    """Generate a unique session ID for a new conversation.
    
    Args:
        user_id (str): The user ID
        
    Returns:
        str: The generated session ID
    
    """
    # Generate a random string of 10 characters
    random_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    return f"{user_id}~{random_str}"


async def generate_conversation_title(title_agent: Agent, query: str) -> str:
    """Generate a title for a conversation based on the first user message.
    
    Args:
        query (str): The first user message
        
    Returns:
        str: The generated title
    
    """
    try:
        prompt = f"Based on the user message below, create a 4-6 word sentence for the conversation description since this is the first message in the description.\n\n{query}"
        result = await title_agent.run(prompt)

        # Extract just the text content from the result
        title = result.data.strip()
        return title
    except Exception as e:
        print(f"Error generating conversation title: {str(e)}")
        return "New Conversation"  # Fallback title


async def store_message(
    supabase: Client,
    session_id: str, 
    message_type: str, 
    content: str, 
    message_data: Optional[bytes] = None, 
    data: Optional[Dict] = None,
    files: Optional[List[Dict[str, str]]] = None
):
    """Store a message in the Supabase messages table.
    
    Args:
        supabase: Supabase client
        session_id: The session ID for the conversation
        message_type: Type of message ('human' or 'ai')
        content: The message content
        message_data: Optional binary data associated with the message
        data: Optional additional data for the message
        files: Optional list of file attachments with fileName, content, and mimeType
    """
    message_obj = {
        "type": message_type,
        "content": content
    }
    if data:
        message_obj["data"] = data
        
    # Add files to the message object if provided
    if files:
        message_obj["files"] = files

    try:
        insert_data = {
            "session_id": session_id,
            "message": message_obj
        }
        
        # Add message_data if provided
        if message_data:
            insert_data["message_data"] = message_data.decode('utf-8')
        
        supabase.table("messages").insert(insert_data).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store message: {str(e)}")



async def convert_history_to_pydantic_format(conversation_history):
    """Convert Supabase conversation history to format expected by Pydantic AI.
    Only uses messages with message_data field.
    """
    messages: List[ModelMessage] = []
    
    for msg in conversation_history:
        # Only process messages with message_data
        if msg.get("message_data"):
            try:
                # Parse the message_data JSON and validate it as Pydantic AI messages
                message_data_json = msg["message_data"]
                # Extend our messages list with the validated messages
                messages.extend(ModelMessagesTypeAdapter.validate_json(message_data_json))
            except Exception as e:
                print(f"Error parsing message_data: {str(e)}")
                # Skip this message if there's an error parsing
                continue
    
    return messages


async def check_rate_limit(supabase: Client, user_id: str, rate_limit: int = 5) -> bool:
    """
    Check if the user has exceeded the rate limit.
    
    Args:
        supabase: Supabase client
        user_id: User ID to check
        rate_limit: Maximum number of requests allowed per minute
        
    Returns:
        bool: True if rate limit is not exceeded, False otherwise
    """
    try:
        # Get timestamp for one minute ago
        one_minute_ago = (datetime.now(timezone.utc) - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
        
        # Use count() to efficiently get just the number of requests without fetching all records
        response = supabase.table("requests") \
            .select("*", count="exact") \
            .eq("user_id", user_id) \
            .gte("timestamp", one_minute_ago) \
            .execute()
        
        # Get the count from the response
        request_count = response.count if hasattr(response, 'count') else 0
        
        # Check if the number of requests exceeds the rate limit
        return request_count < rate_limit
    except Exception as e:
        print(f"Error checking rate limit: {str(e)}")
        # In case of error, allow the request to proceed
        return True


async def store_request(supabase: Client, request_id: str, user_id: str, query: str):
    """
    Store a request in the requests table for rate limiting purposes.
    
    Args:
        supabase: Supabase client
        request_id: Unique request ID
        user_id: User ID
        query: User's query
    """
    try:
        supabase.table("requests").insert({
            "id": request_id,
            "user_id": user_id,
            "user_query": query,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }).execute()
    except Exception as e:
        print(f"Error storing request: {str(e)}")

