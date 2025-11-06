"""
Basic ReAct Agent with LangGraph
===============================

A simple LangGraph implementation demonstrating:
- StateGraph with MessagesState  
- Tool integration with Brave Search
- Conditional routing (tool use vs direct response)
- Basic async agent pattern

This is the foundation pattern for building more complex multi-agent systems.
"""

import os
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Configure environment
from dotenv import load_dotenv
load_dotenv()

@tool
async def brave_search_tool(query: str) -> str:
    """Search the web for current information using Brave Search API."""
    # In production, integrate with actual Brave Search API
    # For demo purposes, return simulated search results
    return f"Search results for '{query}': [Simulated search data would appear here]"

@tool  
async def calculator_tool(expression: str) -> str:
    """Perform mathematical calculations safely."""
    try:
        # Safe evaluation of mathematical expressions
        result = eval(expression.replace("^", "**"))
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

# Initialize LLM with tools
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [brave_search_tool, calculator_tool]
llm_with_tools = llm.bind_tools(tools)

# Create tool node for executing tools
tool_node = ToolNode(tools)

async def agent_node(state: MessagesState) -> dict:
    """
    Main agent node that decides whether to use tools or respond directly.
    
    Returns updated state with either tool calls or final response.
    """
    messages = state["messages"]
    
    # Get response from LLM
    response = await llm_with_tools.ainvoke(messages)
    
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", END]:
    """
    Conditional routing function that decides next step based on tool calls.
    
    If the last message has tool calls, route to tools.
    Otherwise, end the conversation.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If LLM makes tool calls, route to tool node
    if last_message.tool_calls:
        return "tools"
    
    # Otherwise, end the workflow
    return END

# Build the graph
def create_basic_react_graph():
    """Create and compile the basic ReAct agent graph."""
    
    workflow = StateGraph(MessagesState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.add_edge(START, "agent")
    
    # Add conditional routing
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # After tools, always go back to agent
    workflow.add_edge("tools", "agent")
    
    # Add memory for conversation persistence
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)

async def run_basic_agent_example():
    """Example usage of the basic ReAct agent."""
    
    # Create the graph
    graph = create_basic_react_graph()
    
    # Configuration for the conversation
    config = {"configurable": {"thread_id": "basic_agent_demo"}}
    
    print("🤖 Basic LangGraph ReAct Agent Example")
    print("=" * 50)
    
    # Example queries to demonstrate functionality
    example_queries = [
        "What is the current weather in San Francisco?",
        "Calculate 25 * 47 + 133", 
        "Explain what LangGraph is and how it differs from other agent frameworks"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📝 Query {i}: {query}")
        print("-" * 30)
        
        # Run the agent
        async for event in graph.astream(
            {"messages": [HumanMessage(content=query)]}, 
            config
        ):
            for node_name, node_output in event.items():
                if "messages" in node_output:
                    message = node_output["messages"][-1]
                    
                    if isinstance(message, AIMessage):
                        if message.tool_calls:
                            print(f"🔧 {node_name}: Making tool call...")
                            for tool_call in message.tool_calls:
                                print(f"   - {tool_call['name']}: {tool_call['args']}")
                        else:
                            print(f"🤖 {node_name}: {message.content}")
                    
                    elif isinstance(message, ToolMessage):
                        print(f"⚙️  {node_name}: {message.content}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_basic_agent_example())