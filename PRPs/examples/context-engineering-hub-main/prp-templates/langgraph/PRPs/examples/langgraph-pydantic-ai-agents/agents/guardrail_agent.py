"""
Guardrail Agent for sequential research and outreach system.

This lightweight agent determines if a request is for research/outreach or normal conversation.
"""

import logging
from dataclasses import dataclass

from pydantic_ai import Agent

from clients import get_model
from .deps import GuardrailDependencies
from .prompts import GUARDRAIL_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


@dataclass 
class GuardrailResponse:
    """Structured guardrail decision for Pydantic AI output_type"""
    is_research_request: bool
    reasoning: str


# Initialize the guardrail agent with smaller model for fast decisions
guardrail_agent = Agent(
    get_model(use_smaller_model=True),
    output_type=GuardrailResponse,
    deps_type=GuardrailDependencies,
    system_prompt=GUARDRAIL_SYSTEM_PROMPT,
    instrument=True
)
