"""
SEO Research Agent for parallel research workflow.

This agent performs SEO-focused web searches to gather information about people and companies,
focusing on search engine visibility, online presence, and digital footprint.
"""

import logging
from typing import Dict, Any, List
from pydantic_ai import Agent, RunContext

from clients import get_model
from .deps import ResearchAgentDependencies
from .prompts import SEO_RESEARCH_SYSTEM_PROMPT
from tools.brave_tools import search_web_tool

logger = logging.getLogger(__name__)


# Initialize the SEO research agent
seo_research_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=ResearchAgentDependencies,
    system_prompt=SEO_RESEARCH_SYSTEM_PROMPT,
    instrument=True
)


@seo_research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API with SEO focus.
    
    Args:
        query: Search query optimized for SEO insights
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
        
        logger.info(f"SEO Research - Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"SEO Research - Web search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]