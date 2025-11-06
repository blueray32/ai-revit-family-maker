"""
Multi-Agent Supervisor System with LangGraph
===========================================

Demonstrates advanced LangGraph patterns:
- Supervisor pattern with central coordination
- Specialized agents with distinct responsibilities  
- Custom state schema with operator.add reducers
- Dynamic agent routing based on task analysis
- Hierarchical agent communication

This example shows how to build production-ready multi-agent systems.
"""

import os
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI  
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import operator

# Configure environment
from dotenv import load_dotenv
load_dotenv()

# Custom state schema for multi-agent coordination
class SupervisorState(TypedDict):
    """State schema for multi-agent supervisor system."""
    messages: Annotated[list, operator.add]
    current_agent: str
    task_analysis: str
    agent_results: Annotated[list[dict], operator.add]
    final_answer: str

# Initialize LLMs
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Research tools for specialized agents
@tool
async def web_search_tool(query: str) -> str:
    """Search the web for current information."""
    # In production, integrate with actual search API
    return f"Web search results for '{query}': [Current information would be retrieved here]"

@tool
async def data_analysis_tool(data: str) -> str:
    """Analyze data and extract insights."""
    return f"Data analysis of '{data}': [Analysis results would be computed here]"

@tool
async def report_generation_tool(content: str) -> str:
    """Generate structured reports from content."""
    return f"Generated report based on: {content[:100]}... [Full formatted report would be created here]"

# Specialized Agent Implementations

async def supervisor_agent(state: SupervisorState) -> dict:
    """
    Central supervisor that analyzes tasks and routes to appropriate agents.
    
    The supervisor decides which specialized agent should handle the current task.
    """
    messages = state["messages"]
    current_request = messages[-1].content if messages else ""
    
    # Task analysis prompt
    task_analysis_prompt = f"""
    Analyze this request and determine which agent should handle it:
    Request: {current_request}
    
    Available agents:
    - research_agent: Web research, fact-finding, information gathering
    - analysis_agent: Data analysis, calculations, pattern recognition  
    - report_agent: Document generation, summarization, formatting
    
    If the task is complete or you have enough information, respond with "COMPLETE".
    Otherwise, respond with the agent name that should handle this task.
    
    Current task analysis: {state.get('task_analysis', 'Initial analysis')}
    Previous agent results: {state.get('agent_results', [])}
    """
    
    response = await llm.ainvoke([SystemMessage(content=task_analysis_prompt)])
    
    # Extract the routing decision
    agent_decision = response.content.strip().lower()
    
    return {
        "messages": [AIMessage(content=f"Supervisor analysis: {response.content}")],
        "current_agent": agent_decision,
        "task_analysis": response.content
    }

async def research_agent(state: SupervisorState) -> dict:
    """
    Specialized research agent focused on information gathering.
    
    Uses web search and fact-finding to collect relevant information.
    """
    messages = state["messages"]
    task_context = state.get("task_analysis", "")
    
    # Research-specific prompt
    research_prompt = f"""
    You are a research specialist. Based on the supervisor's analysis, conduct thorough research.
    
    Task context: {task_context}
    Recent messages: {messages[-3:] if len(messages) >= 3 else messages}
    
    Use the web_search_tool to gather current, factual information relevant to the request.
    Focus on accuracy and comprehensive coverage of the topic.
    """
    
    # Bind research tools
    research_llm = llm.bind_tools([web_search_tool])
    response = await research_llm.ainvoke([SystemMessage(content=research_prompt)])
    
    # Execute tools if needed
    research_results = []
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "web_search_tool":
                search_result = await web_search_tool.ainvoke(tool_call["args"]["query"])
                research_results.append({
                    "agent": "research_agent",
                    "tool": "web_search",
                    "query": tool_call["args"]["query"],
                    "result": search_result
                })
    
    return {
        "messages": [AIMessage(content=f"Research Agent: {response.content}")],
        "agent_results": research_results or [{"agent": "research_agent", "result": response.content}]
    }

async def analysis_agent(state: SupervisorState) -> dict:
    """
    Specialized analysis agent focused on data processing and insights.
    
    Analyzes information and extracts meaningful patterns and insights.
    """
    messages = state["messages"]
    previous_results = state.get("agent_results", [])
    
    analysis_prompt = f"""
    You are a data analysis specialist. Analyze the available information and extract key insights.
    
    Previous research results: {previous_results}
    Context from messages: {messages[-2:] if len(messages) >= 2 else messages}
    
    Use the data_analysis_tool to process the information and identify patterns, trends, or key insights.
    Provide actionable analysis based on the available data.
    """
    
    # Bind analysis tools
    analysis_llm = llm.bind_tools([data_analysis_tool])
    response = await analysis_llm.ainvoke([SystemMessage(content=analysis_prompt)])
    
    # Execute analysis tools if needed
    analysis_results = []
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "data_analysis_tool":
                analysis_result = await data_analysis_tool.ainvoke(tool_call["args"]["data"])
                analysis_results.append({
                    "agent": "analysis_agent",
                    "tool": "data_analysis",
                    "input": tool_call["args"]["data"],
                    "result": analysis_result
                })
    
    return {
        "messages": [AIMessage(content=f"Analysis Agent: {response.content}")],
        "agent_results": analysis_results or [{"agent": "analysis_agent", "result": response.content}]
    }

async def report_agent(state: SupervisorState) -> dict:
    """
    Specialized report agent focused on synthesis and document generation.
    
    Creates final reports and summaries based on research and analysis.
    """
    messages = state["messages"]
    all_results = state.get("agent_results", [])
    
    report_prompt = f"""
    You are a report generation specialist. Create a comprehensive final response.
    
    All agent results: {all_results}
    Original request context: {messages[0].content if messages else ""}
    
    Use the report_generation_tool to create a well-structured, comprehensive response
    that synthesizes all the research and analysis into a clear final answer.
    """
    
    # Bind report tools
    report_llm = llm.bind_tools([report_generation_tool])
    response = await report_llm.ainvoke([SystemMessage(content=report_prompt)])
    
    # Generate final report
    final_report = response.content
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call["name"] == "report_generation_tool":
                report_result = await report_generation_tool.ainvoke(tool_call["args"]["content"])
                final_report = report_result
    
    return {
        "messages": [AIMessage(content=f"Report Agent: {final_report}")],
        "final_answer": final_report,
        "agent_results": [{"agent": "report_agent", "result": final_report}]
    }

# Routing logic for supervisor decisions
def route_to_agent(state: SupervisorState) -> Literal["research_agent", "analysis_agent", "report_agent", END]:
    """
    Route to the appropriate agent based on supervisor decision.
    """
    current_agent = state.get("current_agent", "").lower()
    
    if "research" in current_agent:
        return "research_agent"
    elif "analysis" in current_agent:
        return "analysis_agent"
    elif "report" in current_agent:
        return "report_agent"
    elif "complete" in current_agent:
        return END
    else:
        # Default to ending if unclear
        return END

# Build the multi-agent supervisor graph
def create_supervisor_graph():
    """Create and compile the multi-agent supervisor system."""
    
    workflow = StateGraph(SupervisorState)
    
    # Add all agent nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("research_agent", research_agent) 
    workflow.add_node("analysis_agent", analysis_agent)
    workflow.add_node("report_agent", report_agent)
    
    # Start with supervisor
    workflow.add_edge(START, "supervisor")
    
    # Supervisor routes to appropriate agents
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "research_agent": "research_agent",
            "analysis_agent": "analysis_agent", 
            "report_agent": "report_agent",
            END: END
        }
    )
    
    # All agents return to supervisor for next decision
    workflow.add_edge("research_agent", "supervisor")
    workflow.add_edge("analysis_agent", "supervisor")
    workflow.add_edge("report_agent", "supervisor")
    
    # Add memory for conversation persistence
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)

async def run_supervisor_example():
    """Example usage of the multi-agent supervisor system."""
    
    # Create the supervisor graph
    graph = create_supervisor_graph()
    
    # Configuration for the conversation
    config = {"configurable": {"thread_id": "supervisor_demo"}}
    
    print("🤖 Multi-Agent Supervisor System Example")
    print("=" * 60)
    
    # Complex query that requires multiple agents
    complex_query = """
    I need a comprehensive analysis of the current state of artificial intelligence in healthcare.
    Please research recent developments, analyze the key trends and challenges, 
    and provide a structured report with actionable insights.
    """
    
    print(f"📝 Complex Query: {complex_query}")
    print("-" * 60)
    
    # Track execution steps
    step_count = 0
    
    # Run the multi-agent system
    async for event in graph.astream(
        {"messages": [HumanMessage(content=complex_query)]}, 
        config
    ):
        step_count += 1
        print(f"\n🔄 Step {step_count}:")
        
        for node_name, node_output in event.items():
            if "messages" in node_output and node_output["messages"]:
                message = node_output["messages"][-1]
                print(f"   🎯 {node_name}: {message.content[:100]}...")
            
            if "current_agent" in node_output:
                next_agent = node_output["current_agent"]
                print(f"   ➡️  Next agent: {next_agent}")
            
            if "agent_results" in node_output and node_output["agent_results"]:
                results = node_output["agent_results"]
                print(f"   📊 Results added: {len(results)} items")
            
            if "final_answer" in node_output:
                final = node_output["final_answer"]
                print(f"   ✅ Final answer: {final[:150]}...")
    
    print("\n" + "="*60)
    print("🎉 Multi-agent workflow completed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_supervisor_example())