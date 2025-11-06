# Multi-Agent Coordination Patterns in LangGraph

## Overview

LangGraph excels at orchestrating complex multi-agent systems where specialized agents collaborate to solve sophisticated problems. This document outlines proven patterns for agent coordination, communication, and workflow management.

## Core Multi-Agent Architectures

### 1. Supervisor Pattern

Central coordinator managing specialized worker agents:

```python
from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, START, END
import operator

class SupervisorState(TypedDict):
    messages: Annotated[list, operator.add]
    current_agent: str
    agent_results: Annotated[list[dict], operator.add]
    task_analysis: str

async def supervisor_agent(state: SupervisorState) -> dict:
    """Central supervisor that analyzes tasks and routes to appropriate agents."""
    messages = state["messages"]
    current_request = messages[-1].content if messages else ""
    
    # Analyze task and decide routing
    routing_decision = await analyze_task_requirements(current_request)
    
    return {
        "messages": [AIMessage(content=f"Routing to {routing_decision}")],
        "current_agent": routing_decision,
        "task_analysis": f"Analysis: {routing_decision} needed"
    }

def route_to_agent(state: SupervisorState) -> Literal["research", "analysis", "synthesis", END]:
    """Route based on supervisor decision."""
    current_agent = state.get("current_agent", "").lower()
    
    if "research" in current_agent:
        return "research"
    elif "analysis" in current_agent:
        return "analysis"
    elif "synthesis" in current_agent:
        return "synthesis"
    else:
        return END

# Build supervisor graph
workflow = StateGraph(SupervisorState)
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("research", research_agent)
workflow.add_node("analysis", analysis_agent)
workflow.add_node("synthesis", synthesis_agent)

workflow.add_edge(START, "supervisor")
workflow.add_conditional_edges("supervisor", route_to_agent)

# All agents return to supervisor
workflow.add_edge("research", "supervisor")
workflow.add_edge("analysis", "supervisor")
workflow.add_edge("synthesis", "supervisor")
```

### 2. Parallel Execution Pattern

Fan-out to multiple agents, fan-in for synthesis:

```python
from langgraph.graph import Send

class ParallelState(TypedDict):
    messages: Annotated[list, operator.add]
    research_results: Annotated[list[dict], operator.add]
    active_researchers: list[str]

async def parallel_coordinator(state: ParallelState) -> list[Send]:
    """Coordinate parallel agent execution using Send primitive."""
    research_query = state["messages"][-1].content
    
    # Fan out to multiple specialized research agents
    return [
        Send("seo_researcher", {"query": research_query, "domain": "SEO"}),
        Send("social_researcher", {"query": research_query, "domain": "Social Media"}),
        Send("competitor_researcher", {"query": research_query, "domain": "Competitive Intel"})
    ]

async def seo_researcher(state: dict) -> dict:
    """Specialized SEO research agent."""
    query = state["query"]
    domain = state["domain"]
    
    # Perform SEO-specific research
    seo_data = await conduct_seo_research(query)
    
    return {
        "research_results": [{"agent": "seo", "domain": domain, "data": seo_data}],
        "messages": [AIMessage(content=f"SEO research completed for: {query}")]
    }

async def synthesis_agent(state: ParallelState) -> dict:
    """Synthesize results from all parallel agents."""
    all_results = state["research_results"]
    
    # Combine and analyze all research streams
    synthesis = await synthesize_research_results(all_results)
    
    return {
        "messages": [AIMessage(content=f"Synthesis complete: {synthesis}")],
        "final_analysis": synthesis
    }

# Build parallel execution graph
workflow = StateGraph(ParallelState)
workflow.add_node("coordinator", parallel_coordinator)
workflow.add_node("seo_researcher", seo_researcher)
workflow.add_node("social_researcher", social_researcher)
workflow.add_node("competitor_researcher", competitor_researcher)
workflow.add_node("synthesis", synthesis_agent)

workflow.add_edge(START, "coordinator")
# All researchers flow to synthesis
workflow.add_edge("seo_researcher", "synthesis")
workflow.add_edge("social_researcher", "synthesis")
workflow.add_edge("competitor_researcher", "synthesis")
workflow.add_edge("synthesis", END)
```

### 3. Hierarchical Agent System

Nested supervision with team-based organization:

```python
class HierarchicalState(TypedDict):
    messages: Annotated[list, operator.add]
    team_assignments: dict
    team_results: Annotated[list[dict], operator.add]
    project_phase: str

async def executive_supervisor(state: HierarchicalState) -> dict:
    """Top-level supervisor managing team supervisors."""
    messages = state["messages"]
    project_request = messages[-1].content
    
    # Assign work to specialized teams
    team_assignments = await analyze_project_requirements(project_request)
    
    return {
        "team_assignments": team_assignments,
        "project_phase": "team_coordination",
        "messages": [AIMessage(content="Project assigned to specialized teams")]
    }

async def research_team_supervisor(state: HierarchicalState) -> dict:
    """Supervisor managing research team agents."""
    team_task = state["team_assignments"].get("research_team", {})
    
    # Coordinate research team members
    research_plan = await create_research_plan(team_task)
    
    return {
        "team_results": [{"team": "research", "plan": research_plan}],
        "messages": [AIMessage(content="Research team coordination complete")]
    }

async def development_team_supervisor(state: HierarchicalState) -> dict:
    """Supervisor managing development team agents."""
    team_task = state["team_assignments"].get("development_team", {})
    
    # Coordinate development team members
    dev_plan = await create_development_plan(team_task)
    
    return {
        "team_results": [{"team": "development", "plan": dev_plan}],
        "messages": [AIMessage(content="Development team coordination complete")]
    }
```

### 4. Swarm Pattern with Dynamic Handoffs

Agents dynamically hand control to one another:

```python
from langchain_core.tools import tool

class SwarmState(TypedDict):
    messages: Annotated[list, operator.add]
    active_agent: str
    agent_context: dict
    handoff_reason: str

@tool
def handoff_to_research(context: str) -> str:
    """Hand off control to research specialist."""
    return Send("research_agent", {"context": context, "handoff_reason": "research_needed"})

@tool
def handoff_to_analysis(context: str) -> str:
    """Hand off control to analysis specialist."""
    return Send("analysis_agent", {"context": context, "handoff_reason": "analysis_needed"})

async def general_agent(state: SwarmState) -> dict:
    """General agent that can hand off to specialists."""
    messages = state["messages"]
    
    # Agent with handoff tools
    agent_with_handoffs = llm.bind_tools([handoff_to_research, handoff_to_analysis])
    response = await agent_with_handoffs.ainvoke(messages)
    
    # Process any handoff tool calls
    if response.tool_calls:
        # Hand off to specialist
        for tool_call in response.tool_calls:
            handoff_context = tool_call["args"]["context"]
            return {"agent_context": {"handoff": handoff_context}}
    
    # Continue processing
    return {"messages": [response]}

async def specialist_agent(state: SwarmState, specialty: str) -> dict:
    """Specialist agent that can hand back to general or other specialists."""
    context = state.get("agent_context", {})
    
    # Process specialized task
    result = await perform_specialized_work(context, specialty)
    
    # Decide whether to hand off further or complete
    if needs_further_processing(result):
        return {"agent_context": {"needs_handoff": True}}
    else:
        return {"messages": [AIMessage(content=result)]}
```

## Communication Patterns

### Message-Based Communication

Agents communicate through shared message history:

```python
async def agent_a(state: CommunicationState) -> dict:
    """Agent A processes request and communicates via messages."""
    messages = state["messages"]
    
    # Process and respond
    response = await process_request(messages)
    
    return {
        "messages": [
            AIMessage(
                content=response,
                name="agent_a"  # Identify message source
            )
        ]
    }

async def agent_b(state: CommunicationState) -> dict:
    """Agent B responds to Agent A's message."""
    messages = state["messages"]
    
    # Find messages from agent_a
    agent_a_messages = [msg for msg in messages if getattr(msg, 'name', '') == 'agent_a']
    
    # Process and respond
    response = await respond_to_agent_a(agent_a_messages)
    
    return {
        "messages": [AIMessage(content=response, name="agent_b")]
    }
```

### State-Based Communication

Agents communicate through structured state updates:

```python
class StructuredCommunicationState(TypedDict):
    messages: Annotated[list, operator.add]
    agent_communications: Annotated[list[dict], operator.add]
    shared_workspace: dict

async def communicating_agent(state: StructuredCommunicationState) -> dict:
    """Agent that uses structured communication patterns."""
    
    # Read communications from other agents
    communications = state.get("agent_communications", [])
    latest_comm = communications[-1] if communications else None
    
    # Process and create response
    if latest_comm and latest_comm.get("target_agent") == "current_agent":
        response_data = await process_communication(latest_comm)
    else:
        response_data = await general_processing(state)
    
    # Communicate with specific agent
    return {
        "agent_communications": [{
            "from_agent": "current_agent",
            "to_agent": "target_agent", 
            "message_type": "response",
            "data": response_data,
            "timestamp": datetime.now().isoformat()
        }],
        "shared_workspace": {"last_update": "current_agent"}
    }
```

### Tool-Based Handoffs

Use tools to facilitate agent coordination:

```python
@tool
async def delegate_to_specialist(task_description: str, specialist_type: str) -> str:
    """Delegate specific tasks to specialist agents."""
    return Send(f"{specialist_type}_agent", {
        "task": task_description,
        "delegated_by": "coordinator",
        "priority": "high"
    })

@tool
async def request_consultation(question: str, expert_domain: str) -> str:
    """Request expert consultation from domain specialist."""
    return Send(f"{expert_domain}_expert", {
        "consultation_request": question,
        "requesting_agent": "current_agent"
    })

async def coordinating_agent(state: CoordinationState) -> dict:
    """Agent with coordination tools."""
    
    # Agent with delegation tools
    coordinator = llm.bind_tools([delegate_to_specialist, request_consultation])
    response = await coordinator.ainvoke(state["messages"])
    
    return {"messages": [response]}
```

## Error Handling and Recovery

### Agent Isolation

Prevent failures in one agent from affecting others:

```python
async def isolated_agent(state: IsolatedState) -> dict:
    """Agent with proper error isolation."""
    try:
        # Perform agent work
        result = await risky_agent_operation(state)
        return {"agent_results": [{"agent": "isolated", "status": "success", "result": result}]}
    
    except Exception as e:
        # Handle error without crashing workflow
        logger.error(f"Agent failed: {e}")
        return {
            "agent_results": [{
                "agent": "isolated", 
                "status": "failed", 
                "error": str(e)
            }],
            "messages": [AIMessage(content="Agent encountered an error but workflow continues")]
        }
```

### Fallback Agents

Backup agents for critical functionality:

```python
async def primary_agent(state: FallbackState) -> dict:
    """Primary agent with fallback capability."""
    try:
        result = await primary_operation(state)
        return {"primary_result": result, "used_fallback": False}
    
    except Exception as e:
        # Trigger fallback
        return {"primary_failed": True, "error": str(e)}

async def fallback_agent(state: FallbackState) -> dict:
    """Fallback agent for when primary fails."""
    
    if state.get("primary_failed"):
        # Use alternative approach
        result = await fallback_operation(state)
        return {"fallback_result": result, "used_fallback": True}
    
    # Primary succeeded, no fallback needed
    return {}

def route_with_fallback(state: FallbackState) -> Literal["primary", "fallback", END]:
    """Route to fallback if primary failed."""
    if state.get("primary_failed"):
        return "fallback"
    elif "primary_result" in state:
        return END
    else:
        return "primary"
```

## Performance Optimization

### Concurrent Agent Execution

Optimize parallel agent performance:

```python
import asyncio

async def optimized_parallel_agents(state: ParallelState) -> list[Send]:
    """Optimized parallel execution with proper resource management."""
    
    # Limit concurrent agents to prevent resource exhaustion
    semaphore = asyncio.Semaphore(3)  # Max 3 concurrent agents
    
    async def rate_limited_agent(agent_name: str, agent_state: dict):
        async with semaphore:
            return Send(agent_name, agent_state)
    
    # Create rate-limited agent invocations
    agent_tasks = [
        rate_limited_agent("agent_1", state),
        rate_limited_agent("agent_2", state),
        rate_limited_agent("agent_3", state),
        rate_limited_agent("agent_4", state),
        rate_limited_agent("agent_5", state)
    ]
    
    return await asyncio.gather(*agent_tasks)
```

### Memory-Efficient State Design

Optimize state for multi-agent workflows:

```python
class OptimizedMultiAgentState(TypedDict):
    # Core communication (keep minimal)
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Agent results with size limits
    agent_results: Annotated[list[dict], lambda x, y: (x + y)[-100:]]  # Keep last 100
    
    # Current state only (not accumulated)
    current_agent: str
    processing_stage: str
    
    # Metadata (not accumulated)
    workflow_metadata: dict
```

This comprehensive approach to multi-agent coordination enables building sophisticated, scalable agent systems that can handle complex workflows with proper error handling, communication, and performance optimization.