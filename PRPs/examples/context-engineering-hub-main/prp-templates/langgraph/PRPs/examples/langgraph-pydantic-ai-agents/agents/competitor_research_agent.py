"""
Competitor Research Agent for parallel research workflow.

This agent performs competitor-focused web searches to gather information about people and companies,
focusing on market positioning, competitive analysis, and business intelligence.
"""

import logging
from typing import Dict, Any, List
from pydantic_ai import Agent, RunContext

from clients import get_model
from .deps import ResearchAgentDependencies
from .prompts import COMPETITOR_RESEARCH_SYSTEM_PROMPT
from tools.brave_tools import search_web_tool

logger = logging.getLogger(__name__)


# Initialize the Competitor research agent
competitor_research_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=ResearchAgentDependencies,
    system_prompt=COMPETITOR_RESEARCH_SYSTEM_PROMPT,
    instrument=True
)


@competitor_research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API with competitive analysis focus.
    
    Args:
        query: Search query optimized for competitor insights
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
        
        logger.info(f"Competitor Research - Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"Competitor Research - Web search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]