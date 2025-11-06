"""
Centralized client and model configuration for the LLM Routing Multi-Agent System.
"""
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI
from supabase import Client
from httpx import AsyncClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_langfuse_client():
    """Get LangFuse client if environment variables are set, otherwise return None"""
    try:
        from langfuse import get_client
        
        langfuse = get_client()
        if langfuse.auth_check():
            return langfuse
        return None
    except Exception:
        return None

def get_model(use_smaller_model: bool = False):
    """Get configured LLM model for agents
    
    Args:
        use_smaller_model: If True, uses LLM_CHOICE_SMALL env var for lightweight routing decisions
    """
    if use_smaller_model:
        llm = os.getenv('LLM_CHOICE_SMALL') or 'gpt-4.1-nano'
    else:
        llm = os.getenv('LLM_CHOICE') or 'gpt-4.1-mini'
    
    base_url = os.getenv('LLM_BASE_URL') or 'https://api.openai.com/v1'
    api_key = os.getenv('LLM_API_KEY') or 'no-api-key-provided'

    return OpenAIModel(llm, provider=OpenAIProvider(base_url=base_url, api_key=api_key))

def get_agent_clients():
    """Get configured clients for agent dependencies"""
    # Embedding client setup
    embedding_base_url = os.getenv('EMBEDDING_BASE_URL', 'https://api.openai.com/v1')
    embedding_api_key = os.getenv('EMBEDDING_API_KEY', os.getenv('LLM_API_KEY', 'no-api-key-provided'))
    
    embedding_client = AsyncOpenAI(base_url=embedding_base_url, api_key=embedding_api_key)

    # Supabase client setup
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment variables")
    
    supabase = Client(supabase_url, supabase_key)

    # HTTP client for general requests
    http_client = AsyncClient()

    return embedding_client, supabase, http_client