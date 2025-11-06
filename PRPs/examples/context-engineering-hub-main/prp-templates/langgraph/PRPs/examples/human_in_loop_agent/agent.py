"""
Human-in-the-Loop Agent with LangGraph
=====================================

Advanced LangGraph pattern demonstrating:
- Human-in-the-loop with interrupt() mechanisms
- Approval workflows and intervention points
- State modification and resume capabilities
- Dynamic interruption based on conditions
- Production-ready approval patterns

This example shows how to build agents that require human oversight and intervention.
"""

import os
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import interrupt
from langgraph.checkpoint.memory import MemorySaver
import operator

# Configure environment
from dotenv import load_dotenv
load_dotenv()

# State schema for human-in-the-loop workflows
class HumanInLoopState(TypedDict):
    """State schema optimized for human intervention workflows."""
    messages: Annotated[list, operator.add]
    pending_action: str
    approval_required: bool
    human_feedback: str
    risk_level: str
    execution_log: Annotated[list[dict], operator.add]

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# High-risk tools that require approval
@tool
async def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Send email to specified recipient - REQUIRES APPROVAL."""
    return f"Email sent to {recipient} with subject '{subject}'"

@tool  
async def make_purchase_tool(item: str, amount: float) -> str:
    """Make a purchase - REQUIRES APPROVAL for amounts over $100."""
    return f"Purchased {item} for ${amount}"

@tool
async def delete_data_tool(dataset: str) -> str:
    """Delete data from system - REQUIRES APPROVAL."""
    return f"Deleted dataset: {dataset}"

@tool
async def schedule_meeting_tool(participants: str, time: str, topic: str) -> str:
    """Schedule meeting with participants - Low risk, auto-approved."""
    return f"Scheduled meeting with {participants} at {time} about {topic}"

# Risk assessment for determining approval requirements
async def risk_assessment_agent(state: HumanInLoopState) -> dict:
    """
    Analyze the current request and determine risk level and approval requirements.
    
    Categorizes actions as low, medium, or high risk based on potential impact.
    """
    messages = state["messages"]
    current_request = messages[-1].content if messages else ""
    
    risk_prompt = f"""
    Analyze this request and determine the risk level and approval requirements:
    
    Request: {current_request}
    
    Risk Assessment Criteria:
    - HIGH RISK: Financial transactions >$100, data deletion, external communications
    - MEDIUM RISK: System changes, scheduling with external parties, data access
    - LOW RISK: Information retrieval, internal scheduling, basic calculations
    
    Return your assessment in this format:
    Risk Level: [HIGH/MEDIUM/LOW]
    Approval Required: [YES/NO]
    Reasoning: [Brief explanation]
    Recommended Action: [What should happen next]
    """
    
    response = await llm.ainvoke([SystemMessage(content=risk_prompt)])
    
    # Parse risk assessment (simplified for demo)
    risk_analysis = response.content
    
    # Determine risk level and approval requirement
    approval_required = "HIGH RISK" in risk_analysis or "Approval Required: YES" in risk_analysis
    risk_level = "HIGH" if "HIGH RISK" in risk_analysis else "MEDIUM" if "MEDIUM RISK" in risk_analysis else "LOW"
    
    return {
        "messages": [AIMessage(content=f"Risk Assessment: {risk_analysis}")],
        "risk_level": risk_level,
        "approval_required": approval_required,
        "execution_log": [{"stage": "risk_assessment", "risk_level": risk_level, "approval_required": approval_required}]
    }

# Approval gate with human intervention
async def approval_gate_agent(state: HumanInLoopState) -> dict:
    """
    Human-in-the-loop approval gate that interrupts for high-risk actions.
    
    Uses interrupt() to pause execution and wait for human input.
    """
    approval_required = state.get("approval_required", False)
    risk_level = state.get("risk_level", "LOW")
    messages = state["messages"]
    
    if approval_required:
        # Create approval prompt for human
        approval_prompt = f"""
        🚨 APPROVAL REQUIRED 🚨
        
        Risk Level: {risk_level}
        Action requested: {messages[-1].content if messages else 'Unknown'}
        
        Please review and decide:
        1. APPROVE - Allow the action to proceed
        2. MODIFY - Provide modifications to the request  
        3. REJECT - Block the action completely
        
        Additional context or modifications:
        """
        
        # Interrupt execution for human approval
        human_input = interrupt(approval_prompt)
        
        # Process human decision
        if human_input:
            decision = human_input.get("decision", "REJECT").upper()
            feedback = human_input.get("feedback", "")
            
            return {
                "messages": [AIMessage(content=f"Human Decision: {decision} - {feedback}")],
                "human_feedback": feedback,
                "pending_action": decision,
                "execution_log": [{"stage": "human_approval", "decision": decision, "feedback": feedback}]
            }
        else:
            # No human input received, default to rejection
            return {
                "messages": [AIMessage(content="No human approval received - Action rejected")],
                "human_feedback": "No response",
                "pending_action": "REJECT",
                "execution_log": [{"stage": "human_approval", "decision": "REJECT", "reason": "no_response"}]
            }
    else:
        # Low risk - auto-approve
        return {
            "messages": [AIMessage(content=f"Auto-approved (Risk Level: {risk_level})")],
            "pending_action": "APPROVE",
            "execution_log": [{"stage": "auto_approval", "risk_level": risk_level}]
        }

# Tool execution with approval enforcement
async def tool_execution_agent(state: HumanInLoopState) -> dict:
    """
    Execute tools based on approval status and human feedback.
    
    Respects human decisions and modifies actions based on feedback.
    """
    pending_action = state.get("pending_action", "REJECT")
    human_feedback = state.get("human_feedback", "")
    messages = state["messages"]
    
    if pending_action == "REJECT":
        return {
            "messages": [AIMessage(content="Action rejected. No tools executed.")],
            "execution_log": [{"stage": "execution", "status": "rejected"}]
        }
    
    elif pending_action == "MODIFY":
        # Handle modifications based on human feedback
        modified_request = f"Modified request based on feedback: {human_feedback}"
        
        return {
            "messages": [AIMessage(content=f"Executing modified action: {modified_request}")],
            "execution_log": [{"stage": "execution", "status": "modified", "action": modified_request}]
        }
    
    elif pending_action == "APPROVE":
        # Execute the approved action
        original_request = messages[0].content if messages else ""
        
        # Determine which tool to use (simplified logic for demo)
        execution_result = "Action executed successfully"
        
        if "email" in original_request.lower():
            # Would execute email tool with proper parameters
            execution_result = "Email sent with approval"
        elif "purchase" in original_request.lower():
            # Would execute purchase tool with proper parameters  
            execution_result = "Purchase completed with approval"
        elif "delete" in original_request.lower():
            # Would execute delete tool with proper parameters
            execution_result = "Data deletion completed with approval"
        elif "meeting" in original_request.lower():
            # Would execute meeting tool (low risk)
            execution_result = "Meeting scheduled"
        
        return {
            "messages": [AIMessage(content=f"✅ {execution_result}")],
            "execution_log": [{"stage": "execution", "status": "completed", "result": execution_result}]
        }
    
    else:
        return {
            "messages": [AIMessage(content="Unknown action status")],
            "execution_log": [{"stage": "execution", "status": "error", "reason": "unknown_action"}]
        }

# Routing logic for approval workflow
def route_after_assessment(state: HumanInLoopState) -> Literal["approval_gate", "tool_execution"]:
    """Route based on risk assessment results."""
    approval_required = state.get("approval_required", False)
    
    if approval_required:
        return "approval_gate"
    else:
        return "tool_execution"

def route_after_approval(state: HumanInLoopState) -> Literal["tool_execution", END]:
    """Route after human approval decision."""
    pending_action = state.get("pending_action", "REJECT")
    
    if pending_action in ["APPROVE", "MODIFY"]:
        return "tool_execution"
    else:
        return END

# Build the human-in-the-loop graph
def create_human_in_loop_graph():
    """Create and compile the human-in-the-loop agent system."""
    
    workflow = StateGraph(HumanInLoopState)
    
    # Add all nodes
    workflow.add_node("risk_assessment", risk_assessment_agent)
    workflow.add_node("approval_gate", approval_gate_agent)
    workflow.add_node("tool_execution", tool_execution_agent)
    
    # Define the workflow
    workflow.add_edge(START, "risk_assessment")
    
    # Conditional routing based on risk assessment
    workflow.add_conditional_edges(
        "risk_assessment",
        route_after_assessment,
        {
            "approval_gate": "approval_gate",
            "tool_execution": "tool_execution"
        }
    )
    
    # Routing after human approval
    workflow.add_conditional_edges(
        "approval_gate", 
        route_after_approval,
        {
            "tool_execution": "tool_execution",
            END: END
        }
    )
    
    # Tool execution always ends the workflow
    workflow.add_edge("tool_execution", END)
    
    # Add memory for conversation persistence
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory, interrupt_before=["approval_gate"])

async def run_human_in_loop_examples():
    """Example usage of the human-in-the-loop system."""
    
    # Create the human-in-the-loop graph
    graph = create_human_in_loop_graph()
    
    print("🤖 Human-in-the-Loop Agent Examples")
    print("=" * 60)
    
    # Example scenarios with different risk levels
    scenarios = [
        {
            "name": "Low Risk - Meeting Scheduling",
            "query": "Please schedule a team meeting for next Tuesday at 2 PM to discuss project updates",
            "expected_risk": "LOW"
        },
        {
            "name": "High Risk - Email Campaign", 
            "query": "Send a marketing email to all customers announcing our new product launch",
            "expected_risk": "HIGH"
        },
        {
            "name": "High Risk - Data Deletion",
            "query": "Delete the old customer database from last year to free up storage space", 
            "expected_risk": "HIGH"
        },
        {
            "name": "Medium Risk - Purchase Request",
            "query": "Purchase 5 software licenses for the development team at $150 each",
            "expected_risk": "HIGH"  # Over $100 total
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"Query: {scenario['query']}")
        print(f"Expected Risk: {scenario['expected_risk']}")
        print("-" * 60)
        
        # Configuration for each scenario
        config = {"configurable": {"thread_id": f"human_loop_scenario_{i}"}}
        
        try:
            # Run the human-in-the-loop workflow
            step_count = 0
            async for event in graph.astream(
                {"messages": [HumanMessage(content=scenario["query"])]}, 
                config
            ):
                step_count += 1
                print(f"   🔄 Step {step_count}:")
                
                for node_name, node_output in event.items():
                    if "messages" in node_output and node_output["messages"]:
                        message = node_output["messages"][-1]
                        print(f"      🎯 {node_name}: {message.content}")
                    
                    if "risk_level" in node_output:
                        risk = node_output["risk_level"]
                        print(f"      ⚠️  Risk Level: {risk}")
                    
                    if "approval_required" in node_output:
                        approval = node_output["approval_required"]
                        print(f"      🚨 Approval Required: {approval}")
                    
                    if "execution_log" in node_output and node_output["execution_log"]:
                        log_entries = node_output["execution_log"]
                        for entry in log_entries:
                            print(f"      📝 Log: {entry}")
            
        except Exception as e:
            if "interrupt" in str(e).lower():
                print(f"      ⏸️  INTERRUPTED: Waiting for human approval")
                print(f"      👤 Human intervention required for: {scenario['name']}")
                
                # In a real application, this would wait for actual human input
                # For demo purposes, we simulate different approval decisions
                if "meeting" in scenario["query"].lower():
                    print(f"      ✅ Auto-approved (low risk)")
                else:
                    print(f"      🛑 Requires manual approval (high risk)")
            else:
                print(f"      ❌ Error: {e}")
        
        print("\n" + "="*60)
    
    print("🎉 Human-in-the-loop examples completed!")
    print("\nNote: In production, high-risk actions would pause execution")
    print("and wait for actual human approval through a web interface.")

# Web interface simulation for human approvals  
def create_approval_interface():
    """
    Simulate web interface for human approvals.
    
    In production, this would be a proper web UI.
    """
    approval_interface = {
        "pending_approvals": [],
        "completed_approvals": []
    }
    
    def add_pending_approval(request_id: str, details: dict):
        approval_interface["pending_approvals"].append({
            "id": request_id,
            "details": details,
            "timestamp": "2024-01-01T00:00:00Z"
        })
    
    def process_approval(request_id: str, decision: str, feedback: str = ""):
        # Move from pending to completed
        pending = approval_interface["pending_approvals"]
        for approval in pending:
            if approval["id"] == request_id:
                approval["decision"] = decision
                approval["feedback"] = feedback
                approval_interface["completed_approvals"].append(approval)
                approval_interface["pending_approvals"].remove(approval)
                break
    
    return approval_interface

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_human_in_loop_examples())