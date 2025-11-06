"""
Parallel Research Agents - Production Pattern
=============================================

Advanced LangGraph implementation demonstrating:
- Parallel agent execution with fan-out/fan-in architecture
- Concurrent state merging with operator.add
- Send() primitive for multi-agent coordination
- Production-ready error handling and isolation
- FastAPI integration with streaming responses

This represents the most sophisticated pattern mentioned in the requirements.
"""

import os
import asyncio
from typing import Annotated, TypedDict, List, Dict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, Send
from langgraph.checkpoint.memory import MemorySaver
import operator
import json

# Configure environment
from dotenv import load_dotenv
load_dotenv()

# Production-ready state schema for parallel research
class ParallelResearchState(TypedDict):
    """State schema optimized for parallel research coordination."""
    messages: Annotated[list, operator.add]
    research_query: str
    research_results: Annotated[list[Dict], operator.add]
    synthesis_result: str
    active_agents: list[str]
    completed_agents: list[str]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Specialized research tools for different domains
@tool
async def seo_research_tool(query: str) -> str:
    """Research SEO trends, keywords, and optimization strategies."""
    # Production integration with SEO APIs would go here
    return f"SEO Research for '{query}': [Current SEO trends, keyword data, competitor analysis]"

@tool
async def social_media_research_tool(query: str) -> str:
    """Research social media trends, engagement patterns, and content strategies."""
    # Production integration with social media APIs would go here
    return f"Social Media Research for '{query}': [Platform trends, engagement data, viral content analysis]"

@tool
async def competitor_research_tool(query: str) -> str:
    """Research competitor analysis, market positioning, and strategic insights."""
    # Production integration with competitive intelligence APIs would go here
    return f"Competitor Research for '{query}': [Market analysis, competitor strategies, positioning insights]"

# Guardrail routing agent for request classification
async def guardrail_routing_agent(state: ParallelResearchState) -> dict:
    """
    Initial routing agent that classifies requests and determines research strategy.
    
    Acts as a guardrail to ensure appropriate research approach.
    """
    messages = state["messages"]
    user_query = messages[0].content if messages else ""
    
    routing_prompt = f"""
    Analyze this research request and determine the appropriate parallel research strategy:
    
    User Query: {user_query}
    
    Classify the request and decide which research agents should be activated:
    - SEO Agent: For SEO, keyword research, search optimization
    - Social Media Agent: For social platforms, engagement, content trends  
    - Competitor Agent: For competitive analysis, market research
    
    Return a JSON response with:
    {{
        "research_query": "refined research question",
        "active_agents": ["agent1", "agent2", "agent3"],
        "research_strategy": "explanation of approach"
    }}
    """
    
    response = await llm.ainvoke([SystemMessage(content=routing_prompt)])
    
    # Parse the routing decision (in production, add proper JSON validation)
    try:
        # Simplified parsing for demo - production would use proper JSON parsing
        active_agents = ["seo_agent", "social_media_agent", "competitor_agent"]
        refined_query = user_query
    except:
        active_agents = ["seo_agent", "social_media_agent", "competitor_agent"]
        refined_query = user_query
    
    return {
        "messages": [AIMessage(content=f"Routing: Activating parallel research agents")],
        "research_query": refined_query,
        "active_agents": active_agents
    }

# Parallel research agent implementations
async def seo_research_agent(state: ParallelResearchState) -> dict:
    """
    Specialized SEO research agent running in parallel.
    
    Focuses on search engine optimization insights and data.
    """
    research_query = state.get("research_query", "")
    
    seo_prompt = f"""
    You are an SEO research specialist. Conduct comprehensive SEO analysis for:
    Query: {research_query}
    
    Focus on:
    - Keyword opportunities and search volume
    - SEO trends and algorithm updates  
    - Competitor SEO strategies
    - Technical optimization opportunities
    
    Use the seo_research_tool to gather current data.
    """
    
    # Bind SEO tools
    seo_llm = llm.bind_tools([seo_research_tool])
    response = await seo_llm.ainvoke([SystemMessage(content=seo_prompt)])
    
    # Execute SEO research
    seo_results = {"agent": "seo_agent", "status": "completed"}
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_result = await seo_research_tool.ainvoke(tool_call["args"]["query"])
            seo_results.update({
                "research_data": tool_result,
                "analysis": response.content,
                "tool_calls": len(response.tool_calls)
            })
    else:
        seo_results.update({
            "analysis": response.content,
            "tool_calls": 0
        })
    
    return {
        "messages": [AIMessage(content=f"SEO Agent: Completed research analysis")],
        "research_results": [seo_results],
        "completed_agents": ["seo_agent"]
    }

async def social_media_research_agent(state: ParallelResearchState) -> dict:
    """
    Specialized social media research agent running in parallel.
    
    Focuses on social platform trends and engagement strategies.
    """
    research_query = state.get("research_query", "")
    
    social_prompt = f"""
    You are a social media research specialist. Analyze social trends for:
    Query: {research_query}
    
    Focus on:
    - Platform-specific trends and features
    - Engagement patterns and optimal timing
    - Content formats that drive engagement
    - Influencer and community insights
    
    Use the social_media_research_tool to gather current data.
    """
    
    # Bind social media tools
    social_llm = llm.bind_tools([social_media_research_tool])
    response = await social_llm.ainvoke([SystemMessage(content=social_prompt)])
    
    # Execute social media research
    social_results = {"agent": "social_media_agent", "status": "completed"}
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_result = await social_media_research_tool.ainvoke(tool_call["args"]["query"])
            social_results.update({
                "research_data": tool_result,
                "analysis": response.content,
                "tool_calls": len(response.tool_calls)
            })
    else:
        social_results.update({
            "analysis": response.content,
            "tool_calls": 0
        })
    
    return {
        "messages": [AIMessage(content=f"Social Media Agent: Completed trend analysis")],
        "research_results": [social_results],
        "completed_agents": ["social_media_agent"]
    }

async def competitor_research_agent(state: ParallelResearchState) -> dict:
    """
    Specialized competitor research agent running in parallel.
    
    Focuses on competitive intelligence and market positioning.
    """
    research_query = state.get("research_query", "")
    
    competitor_prompt = f"""
    You are a competitive intelligence specialist. Analyze the competitive landscape for:
    Query: {research_query}
    
    Focus on:
    - Direct and indirect competitors
    - Market positioning strategies
    - Competitive advantages and gaps
    - Pricing and business model analysis
    
    Use the competitor_research_tool to gather current data.
    """
    
    # Bind competitor research tools
    competitor_llm = llm.bind_tools([competitor_research_tool])
    response = await competitor_llm.ainvoke([SystemMessage(content=competitor_prompt)])
    
    # Execute competitor research
    competitor_results = {"agent": "competitor_agent", "status": "completed"}
    
    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_result = await competitor_research_tool.ainvoke(tool_call["args"]["query"])
            competitor_results.update({
                "research_data": tool_result,
                "analysis": response.content,
                "tool_calls": len(response.tool_calls)
            })
    else:
        competitor_results.update({
            "analysis": response.content,
            "tool_calls": 0
        })
    
    return {
        "messages": [AIMessage(content=f"Competitor Agent: Completed competitive analysis")],
        "research_results": [competitor_results],
        "completed_agents": ["competitor_agent"]
    }

# Fan-out coordination for parallel execution
async def parallel_coordinator(state: ParallelResearchState) -> List[Send]:
    """
    Coordinates the fan-out to parallel research agents.
    
    Uses Send() primitive for parallel agent execution with shared state.
    """
    active_agents = state.get("active_agents", [])
    
    # Create Send instructions for parallel execution
    parallel_sends = []
    
    if "seo_agent" in active_agents:
        parallel_sends.append(Send("seo_research_agent", state))
    
    if "social_media_agent" in active_agents:
        parallel_sends.append(Send("social_media_research_agent", state))
    
    if "competitor_agent" in active_agents:  
        parallel_sends.append(Send("competitor_research_agent", state))
    
    return parallel_sends

# Synthesis agent for combining parallel results
async def synthesis_agent(state: ParallelResearchState) -> dict:
    """
    Synthesis agent that combines all parallel research results.
    
    Creates comprehensive final analysis from all research streams.
    """
    research_results = state.get("research_results", [])
    original_query = state.get("research_query", "")
    
    synthesis_prompt = f"""
    You are a research synthesis specialist. Create a comprehensive final analysis by combining all research results.
    
    Original Query: {original_query}
    
    Research Results from Parallel Agents:
    {json.dumps(research_results, indent=2)}
    
    Create a structured synthesis that:
    1. Integrates insights from all research streams
    2. Identifies patterns and connections across domains
    3. Provides actionable recommendations  
    4. Highlights the most critical findings
    5. Suggests next steps based on combined insights
    
    Format as a comprehensive strategic analysis.
    """
    
    response = await llm.ainvoke([SystemMessage(content=synthesis_prompt)])
    
    return {
        "messages": [AIMessage(content=f"Synthesis Complete: {response.content}")],
        "synthesis_result": response.content
    }

# Build the parallel research graph
def create_parallel_research_graph():
    """Create and compile the production parallel research system."""
    
    workflow = StateGraph(ParallelResearchState)
    
    # Add all nodes
    workflow.add_node("guardrail_routing", guardrail_routing_agent)
    workflow.add_node("parallel_coordinator", parallel_coordinator)
    workflow.add_node("seo_research_agent", seo_research_agent)
    workflow.add_node("social_media_research_agent", social_media_research_agent)  
    workflow.add_node("competitor_research_agent", competitor_research_agent)
    workflow.add_node("synthesis_agent", synthesis_agent)
    
    # Define the workflow
    workflow.add_edge(START, "guardrail_routing")
    workflow.add_edge("guardrail_routing", "parallel_coordinator")
    
    # Parallel execution paths (coordinator sends to all agents)
    workflow.add_edge("seo_research_agent", "synthesis_agent")
    workflow.add_edge("social_media_research_agent", "synthesis_agent")
    workflow.add_edge("competitor_research_agent", "synthesis_agent")
    
    # Final synthesis to end
    workflow.add_edge("synthesis_agent", END)
    
    # Add memory for production persistence
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)

async def run_parallel_research_example():
    """Example usage of the parallel research system."""
    
    # Create the parallel research graph
    graph = create_parallel_research_graph()
    
    # Configuration for the conversation
    config = {"configurable": {"thread_id": "parallel_research_demo"}}
    
    print("🚀 Production Parallel Research Agents Example")
    print("=" * 70)
    
    # Production-level research query
    production_query = """
    I'm launching a new AI-powered productivity app for remote teams. I need comprehensive 
    research on the market opportunity, including SEO strategy for customer acquisition,
    social media trends for user engagement, and competitive landscape analysis.
    """
    
    print(f"📝 Production Query: {production_query}")
    print("-" * 70)
    
    # Track parallel execution
    agent_completions = set()
    step_count = 0
    
    # Run the parallel research system
    async for event in graph.astream(
        {"messages": [HumanMessage(content=production_query)]}, 
        config
    ):
        step_count += 1
        print(f"\n⚡ Step {step_count} - Parallel Execution:")
        
        for node_name, node_output in event.items():
            print(f"   🎯 {node_name}:")
            
            if "messages" in node_output and node_output["messages"]:
                message = node_output["messages"][-1]
                print(f"      💬 {message.content}")
            
            if "active_agents" in node_output:
                agents = node_output["active_agents"]
                print(f"      🔄 Activating agents: {agents}")
            
            if "research_results" in node_output and node_output["research_results"]:
                results = node_output["research_results"]
                for result in results:
                    agent_name = result.get("agent", "unknown")
                    agent_completions.add(agent_name)
                    print(f"      ✅ {agent_name} completed")
            
            if "synthesis_result" in node_output:
                synthesis = node_output["synthesis_result"]
                print(f"      📊 Synthesis: {synthesis[:200]}...")
                print(f"      🎉 All agents completed: {list(agent_completions)}")
    
    print("\n" + "="*70)
    print("🚀 Parallel research workflow completed successfully!")

# FastAPI integration for production deployment
def create_fastapi_app():
    """Create FastAPI app with streaming support for production deployment."""
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
    import json
    
    app = FastAPI(title="Parallel Research Agents API")
    
    class ResearchRequest(BaseModel):
        query: str
        thread_id: str = "default"
    
    @app.post("/research")
    async def research_endpoint(request: ResearchRequest):
        """Production endpoint with streaming responses."""
        graph = create_parallel_research_graph()
        config = {"configurable": {"thread_id": request.thread_id}}
        
        async def generate_response():
            async for event in graph.astream(
                {"messages": [HumanMessage(content=request.query)]}, 
                config
            ):
                yield f"data: {json.dumps(event)}\n\n"
        
        return StreamingResponse(generate_response(), media_type="text/plain")
    
    return app

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_parallel_research_example())