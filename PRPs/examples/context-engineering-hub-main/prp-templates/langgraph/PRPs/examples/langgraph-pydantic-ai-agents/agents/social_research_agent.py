"""
Social Media Research Agent for parallel research workflow.

This agent performs social media-focused web searches to gather information about people and companies,
focusing on social presence, engagement metrics, and social media activities.
"""

import logging
from typing import Dict, Any, List
from pydantic_ai import Agent, RunContext

from clients import get_model
from .deps import ResearchAgentDependencies
from .prompts import SOCIAL_RESEARCH_SYSTEM_PROMPT
from tools.brave_tools import search_web_tool

logger = logging.getLogger(__name__)


# Initialize the Social Media research agent
social_research_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=ResearchAgentDependencies,
    system_prompt=SOCIAL_RESEARCH_SYSTEM_PROMPT,
    instrument=True
)


@social_research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API with social media focus.
    
    Args:
        query: Search query optimized for social media insights
        max_results: Maximum number of results to return (1-10)
    
    Returns:
        List of search results with title, URL, description, and score
    """
    try:        
        # Ensure max_results is within valid range
        max_results = min(max(max_results, 1), 10)
        
        results = await search_web_tool(
            api_key=ctx.deps.brave_api_key,
            query=query,
            count=max_results
        )
        
        logger.info(f"Social Research - Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"Social Research - Web search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]