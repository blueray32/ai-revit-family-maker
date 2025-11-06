"""
Fallback Agent for sequential research and outreach system.

This agent handles normal conversation requests that don't require the research workflow.
"""

import logging
from pydantic_ai import Agent

from clients import get_model
from .deps import GuardrailDependencies
from .prompts import FALLBACK_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# Initialize the fallback agent
fallback_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=GuardrailDependencies,
    system_prompt=FALLBACK_SYSTEM_PROMPT,
    instrument=True
)
