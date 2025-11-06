"""
Synthesis Agent for parallel research workflow.

This agent synthesizes findings from all 3 parallel research agents (SEO, Social, Competitor)
and creates a comprehensive email draft based on the combined research data.
"""

import logging
from typing import Dict, Any
from pydantic_ai import Agent, RunContext

from clients import get_model
from .deps import ResearchAgentDependencies
from .prompts import SYNTHESIS_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# Initialize the synthesis agent
synthesis_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=ResearchAgentDependencies,
    system_prompt=SYNTHESIS_SYSTEM_PROMPT,
    instrument=True
)


@synthesis_agent.tool
async def synthesize_research_data(
    ctx: RunContext[ResearchAgentDependencies],
    seo_research: str,
    social_research: str,
    competitor_research: str,
    original_query: str
) -> Dict[str, Any]:
    """
    Synthesize research data from all three parallel agents.
    
    Args:
        seo_research: SEO-focused research findings
        social_research: Social media research findings
        competitor_research: Competitor analysis findings
        original_query: Original user request for context
    
    Returns:
        Dictionary with synthesis results and insights
    """
    try:
        # Create comprehensive synthesis summary
        synthesis_data = {
            "seo_insights": seo_research,
            "social_insights": social_research,
            "competitive_insights": competitor_research,
            "original_context": original_query,
            "synthesis_timestamp": "research_synthesis_completed"
        }
        
        logger.info("Research synthesis completed successfully")
        return synthesis_data
        
    except Exception as e:
        logger.error(f"Research synthesis failed: {e}")
        return {
            "error": f"Synthesis failed: {str(e)}",
            "seo_insights": seo_research,
            "social_insights": social_research,
            "competitive_insights": competitor_research
        }