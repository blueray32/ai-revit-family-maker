"""
Parallel Agent Workflow for Research and Synthesis System.

This module implements a LangGraph workflow that routes requests through a guardrail agent,
then executes 3 parallel research agents (SEO, Social, Competitor) simultaneously,
followed by a synthesis agent that combines all findings into an email draft.
"""

from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

from graph.state import ParallelAgentState
from agents.guardrail_agent import guardrail_agent
from agents.seo_research_agent import seo_research_agent
from agents.social_research_agent import social_research_agent
from agents.competitor_research_agent import competitor_research_agent
from agents.synthesis_agent import synthesis_agent
from agents.fallback_agent import fallback_agent
from agents.deps import (
    create_guardrail_deps,
    create_research_deps
)
from pydantic_ai.messages import ModelMessage
from pydantic_ai import Agent
from pydantic_ai.messages import PartDeltaEvent, PartStartEvent, TextPartDelta

load_dotenv()


async def guardrail_node(state: ParallelAgentState, writer) -> dict:
    """Guardrail node that determines if request is for research/outreach or conversation"""
    try:
        deps = create_guardrail_deps(session_id=state.get("session_id"))
        
        # Get structured routing decision with message history
        message_history = state.get("pydantic_message_history", [])
        result = await guardrail_agent.run(state["query"], deps=deps, message_history=message_history)
        decision = result.data.is_research_request
        reasoning = result.data.reasoning
        
        # Stream routing feedback to user
        if decision:
            writer("🔬 Detected research request. Starting parallel research workflow...\n\n")
        else:
            writer("💬 Routing to conversation mode...\n\n")
        
        return {
            "is_research_request": decision,
            "routing_reason": reasoning
        }
        
    except Exception as e:
        print(f"Error in guardrail: {e}")
        writer("⚠️ Guardrail failed, defaulting to conversation mode\n\n")
        return {
            "is_research_request": False,
            "routing_reason": f"Guardrail error: {str(e)}"
        }


async def seo_research_node(state: ParallelAgentState, writer) -> dict:
    """SEO research agent with streaming using .iter() pattern"""
    try:
        # Agent separator with hardcoded start message
        writer("\n\n### 🔍 SEO Research Agent Starting...\n")
        
        deps = create_research_deps(session_id=state.get("session_id"))
        agent_input = state["query"]
        message_history = state.get("pydantic_message_history", [])

        run = await seo_research_agent.run(agent_input, deps=deps, message_history=message_history)
        full_response = str(run.data) if run.data else "No response generated"

        return {
            "seo_research": [full_response],
            "research_completed": ["seo"]
        }
        
    except Exception as e:
        error_msg = f"SEO Research error: {str(e)}"
        writer(error_msg)
        return {
            "seo_research": [error_msg],
            "research_completed": ["seo_error"]
        }


async def social_research_node(state: ParallelAgentState, writer) -> dict:
    """Social Media research agent with streaming using .iter() pattern"""
    try:
        # Agent separator with hardcoded start message
        writer("\n\n### 📱 Social Media Research Agent Starting...\n")
        
        deps = create_research_deps(session_id=state.get("session_id"))
        agent_input = state["query"]
        message_history = state.get("pydantic_message_history", [])
        
        run = await social_research_agent.run(agent_input, deps=deps, message_history=message_history)
        full_response = str(run.data) if run.data else "No response generated"
            
        return {
            "social_research": [full_response],
            "research_completed": ["social"]
        }
        
    except Exception as e:
        error_msg = f"Social Research error: {str(e)}"
        writer(error_msg)
        return {
            "social_research": [error_msg],
            "research_completed": ["social_error"]
        }


async def competitor_research_node(state: ParallelAgentState, writer) -> dict:
    """Competitor research agent with streaming using .iter() pattern"""
    try:
        # Agent separator with hardcoded start message
        writer("\n\n### 🏢 Competitor Research Agent Starting...\n")
        
        deps = create_research_deps(session_id=state.get("session_id"))
        agent_input = state["query"]
        message_history = state.get("pydantic_message_history", [])
            
        run = await competitor_research_agent.run(agent_input, deps=deps, message_history=message_history)
        full_response = str(run.data) if run.data else "No response generated"
        
        return {
            "competitor_research": [full_response],
            "research_completed": ["competitor"]
        }
        
    except Exception as e:
        error_msg = f"Competitor Research error: {str(e)}"
        writer(error_msg)
        return {
            "competitor_research": [error_msg],
            "research_completed": ["competitor_error"]
        }


async def synthesis_node(state: ParallelAgentState, writer) -> dict:
    """Synthesis agent that combines all research and creates comprehensive summary"""
    try:
        # Agent separator with hardcoded start message
        writer("\n\n### 📝 Synthesis Agent Starting...\n")
        
        deps = create_research_deps(session_id=state.get("session_id"))
        
        # Combine all research data
        seo_data = ' '.join(state.get("seo_research", []))
        social_data = ' '.join(state.get("social_research", []))
        competitor_data = ' '.join(state.get("competitor_research", []))
        
        # Construct comprehensive synthesis prompt
        synthesis_prompt = f"""
        Create a comprehensive research synthesis based on parallel research findings:
        
        Original Request: {state["query"]}
        
        SEO Research Findings:
        {seo_data}
        
        Social Media Research Findings:
        {social_data}
        
        Competitor Research Findings:
        {competitor_data}
        
        Please synthesize all research findings and create a comprehensive analysis that:
        1. Integrates insights from all three research streams into a coherent narrative
        2. Highlights key patterns and connections across different data sources
        3. Provides strategic insights and actionable intelligence
        4. Identifies strengths, weaknesses, opportunities, and threats
        5. Delivers clear, data-backed conclusions
        
        Structure your synthesis with clear sections and actionable insights.
        """
        
        message_history = state.get("pydantic_message_history", [])
        full_response = ""
        
        try:
            # Use .iter() for streaming with message history
            async with synthesis_agent.iter(synthesis_prompt, deps=deps, message_history=message_history) as run:
                async for node in run:
                    if Agent.is_model_request_node(node):
                        # Stream tokens from the model's request
                        async with node.stream(run.ctx) as request_stream:
                            async for event in request_stream:
                                if isinstance(event, PartStartEvent) and event.part.part_kind == 'text':
                                    writer(event.part.content)
                                    full_response += event.part.content
                                elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, TextPartDelta):
                                    delta = event.delta.content_delta
                                    writer(delta)
                                    full_response += delta
            
            # Capture new messages for conversation history
            new_messages = run.result.new_messages_json()
                
        except Exception as stream_error:
            print(f"Synthesis streaming failed, using fallback: {stream_error}")
            writer("\n[Streaming unavailable, generating response...]\n")
            
            run = await synthesis_agent.run(synthesis_prompt, deps=deps, message_history=message_history)
            full_response = str(run.data) if run.data else "No response generated"
            writer(full_response)
            
            # Capture new messages from fallback run
            new_messages = run.new_messages_json()
        
        # Notify user about synthesis completion
        writer("\n\n### ✅ Research synthesis completed.")
        
        return {
            "final_response": full_response,
            "synthesis_complete": True,
            "message_history": [new_messages]  # THIS agent updates history
        }
        
    except Exception as e:
        error_msg = f"Synthesis error: {str(e)}"
        writer(error_msg)
        return {
            "final_response": error_msg,
            "synthesis_complete": False,
            "message_history": []
        }


async def fallback_node(state: ParallelAgentState, writer) -> dict:
    """Fallback node for normal conversation"""
    try:
        # Agent separator
        writer("\n\n💬 Conversation Agent Starting...\n\n")
        
        deps = create_guardrail_deps(session_id=state.get("session_id"))
        agent_input = state["query"]
        message_history = state.get("pydantic_message_history", [])
        full_response = ""
        
        try:
            # Use .iter() for streaming with message history
            async with fallback_agent.iter(agent_input, deps=deps, message_history=message_history) as run:
                async for node in run:
                    if Agent.is_model_request_node(node):
                        # Stream tokens from the model's request
                        async with node.stream(run.ctx) as request_stream:
                            async for event in request_stream:
                                if isinstance(event, PartStartEvent) and event.part.part_kind == 'text':
                                    writer(event.part.content)
                                    full_response += event.part.content
                                elif isinstance(event, PartDeltaEvent) and isinstance(event.delta, TextPartDelta):
                                    delta = event.delta.content_delta
                                    writer(delta)
                                    full_response += delta
            
            # CRITICAL: Capture new messages for conversation history
            new_messages = run.result.new_messages_json()
                
        except Exception as stream_error:
            print(f"Fallback streaming failed, using fallback: {stream_error}")
            writer("\n[Streaming unavailable, generating response...]\n")
            
            run = await fallback_agent.run(agent_input, deps=deps, message_history=message_history)
            full_response = str(run.data) if run.data else "No response generated"
            writer(full_response)
            
            # Capture new messages from fallback run
            new_messages = run.new_messages_json()
        
        return {
            "final_response": full_response,
            "message_history": [new_messages]  # THIS agent updates history
        }
        
    except Exception as e:
        error_msg = f"Fallback error: {str(e)}"
        writer(error_msg)
        return {
            "final_response": error_msg,
            "message_history": []
        }


def route_after_guardrail(state: ParallelAgentState):
    """Conditional routing based on guardrail decision"""
    if state.get("is_research_request", False):
        return ["seo_research_node", "social_research_node", "competitor_research_node"]
    else:
        return "fallback_node"


def create_workflow():
    """Create and configure the parallel agent workflow with fan-out/fan-in pattern"""
    
    # Create state graph
    builder = StateGraph(ParallelAgentState)
    
    # Add all nodes
    builder.add_node("guardrail_node", guardrail_node)
    builder.add_node("seo_research_node", seo_research_node)
    builder.add_node("social_research_node", social_research_node)
    builder.add_node("competitor_research_node", competitor_research_node)
    builder.add_node("synthesis_node", synthesis_node)
    builder.add_node("fallback_node", fallback_node)
    
    # Set entry point
    builder.add_edge(START, "guardrail_node")
    
    # Add conditional routing after guardrail for parallel execution
    builder.add_conditional_edges(
        "guardrail_node",
        route_after_guardrail,
        ["seo_research_node", "social_research_node", "competitor_research_node", "fallback_node"]
    )
    
    # Parallel research nodes all feed into synthesis (fan-in)
    builder.add_edge("seo_research_node", "synthesis_node")
    builder.add_edge("social_research_node", "synthesis_node")
    builder.add_edge("competitor_research_node", "synthesis_node")
    
    # End nodes
    builder.add_edge("synthesis_node", END)
    builder.add_edge("fallback_node", END)
    
    # Compile the graph
    return builder.compile()


# Create the workflow instance
workflow = create_workflow()


def create_api_initial_state(
    query: str,
    session_id: str,
    request_id: str,
    pydantic_message_history: Optional[List[ModelMessage]] = None
) -> ParallelAgentState:
    """Create initial state for API mode with parallel agent support"""
    return {
        "query": query,
        "session_id": session_id,
        "request_id": request_id,
        "is_research_request": False,
        "routing_reason": "",
        "seo_research": [],
        "social_research": [],
        "competitor_research": [],
        "research_completed": [],
        "synthesis_complete": False,
        "final_response": "",
        "pydantic_message_history": pydantic_message_history or [],
        "message_history": [],
        "conversation_title": None,
        "is_new_conversation": False
    }


def extract_api_response_data(state: ParallelAgentState) -> Dict[str, Any]:
    """Extract response data for API return"""
    return {
        "session_id": state.get("session_id"),
        "request_id": state.get("request_id"),
        "query": state["query"],
        "response": state.get("final_response", ""),
        "is_research_request": state.get("is_research_request", False),
        "routing_reason": state.get("routing_reason", ""),
        "seo_research": ' '.join(state.get("seo_research", [])),
        "social_research": ' '.join(state.get("social_research", [])),
        "competitor_research": ' '.join(state.get("competitor_research", [])),
        "synthesis_complete": state.get("synthesis_complete", False),
        "conversation_title": state.get("conversation_title"),
        "is_new_conversation": state.get("is_new_conversation", False)
    }