---
name: "LangGraph Multi-Agent PRP Base"
description: "Base template for creating sophisticated LangGraph multi-agent workflows with stateful coordination and production deployment"
---

## Purpose

Build a sophisticated LangGraph multi-agent system that leverages stateful workflows, parallel coordination, and production-ready deployment patterns for **[SPECIFIC_USE_CASE]**.

## Core Principles

1. **Graph-First Architecture**: State schema design drives multi-agent coordination
2. **Multi-Agent Coordination**: Supervisor patterns with specialized agent roles  
3. **Async-by-Default**: All implementations use async/await for optimal performance
4. **Human-in-the-Loop**: Interrupt points for approval and intervention workflows when applicable

---

## Goal

Create a complete LangGraph multi-agent system for **[SPECIFIC_GOAL]** that includes:

- State-driven multi-agent coordination with proper reducers
- Specialized agents with clear responsibilities and tool integration
- The right multi-agent pattern for the use case
- Comprehensive testing with pytest-asyncio for async workflows

## Why

- **Stateful Intelligence**: LangGraph's cyclical execution enables sophisticated reasoning loops
- **Multi-Agent Coordination**: Specialized agents working in parallel produce better results
- **Production Scale**: Built-in support for streaming, persistence, and monitoring
- **Human Integration**: Approval workflows and intervention points for critical decisions
- **Framework Power**: Leverage LangGraph's strengths in complex, stateful workflows

## What

### LangGraph Multi-Agent System Architecture

**State Schema Design (EXAMPLE):**
```python
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
import operator

class MultiAgentState(TypedDict):
    # Core message history with proper reducer
    messages: Annotated[list[BaseMessage], operator.add]
    
    # Agent coordination fields
    agent_results: Annotated[list[dict], operator.add]
    
    # User context and preferences
    user_context: dict
    
    # Domain-specific data fields
    [DOMAIN_SPECIFIC_FIELDS]: dict
```

**Multi-Agent Coordination Strategy:**
- **Supervisor Agent**: Central coordinator making routing decisions
- **Specialized Agents**: Domain-specific agents with focused responsibilities
- **Parallel Execution**: Fan-out to multiple agents, fan-in for synthesis

**Proper Architecture:**
```python
# Graph compilation with StateGraph
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(MultiAgentState)

# Add agent nodes
workflow.add_node("supervisor", supervisor_agent)
workflow.add_node("agent_1", specialized_agent_1)
workflow.add_node("agent_2", specialized_agent_2)

# Add routing logic
workflow.add_conditional_edges(
    "supervisor", 
    route_to_agent,
    {"agent_1": "agent_1", "agent_2": "agent_2", END: END}
)

graph = workflow.compile()
```

### Success Criteria (example, not all will always be applicable)

- [ ] Multi-agent coordination working
- [ ] State schema with proper reducers (operator.add) implemented
- [ ] All node functions async with proper error handling
- [ ] Human-in-the-loop interrupt points where needed
- [ ] Comprehensive pytest-asyncio testing suite
- [ ] Performance optimized for concurrent execution

## All Needed Context

### LangGraph Documentation & Architecture

```yaml
# LANGGRAPH CORE CONCEPTS - Official documentation patterns
- url: https://langchain-ai.github.io/langgraph/concepts/multi_agent/
  why: Multi-agent system patterns and coordination approaches
  key_patterns: ["Supervisor pattern", "Hierarchical systems", "Tool handoffs"]

- url: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
  why: Human-in-the-loop implementation with interrupt mechanisms
  key_patterns: ["Dynamic interrupts", "Approval workflows", "State modification"]

- url: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/
  why: Official supervisor pattern implementation tutorial
  key_patterns: ["Central coordination", "Agent specialization", "Routing logic"]

# STATE MANAGEMENT PATTERNS - Critical for multi-agent coordination
- research_finding: "TypedDict with operator.add reducers for state merging"
  why: "Core state management pattern for multi-agent coordination"
  implementation: |
    class AgentState(TypedDict):
        messages: Annotated[list[BaseMessage], operator.add]
        research_data: Annotated[list[dict], operator.add]

- research_finding: "MessagesState for conversation management"
  why: "Built-in message handling with proper reducers"
  implementation: |
    from langgraph.graph import MessagesState
    class CustomState(MessagesState):
        additional_field: str

# PRODUCTION DEPLOYMENT - FastAPI integration patterns  
- research_finding: "FastAPI with streaming responses using astream"
  why: "Production-ready API deployment with real-time responses"
  implementation: |
    @app.post("/agent")
    async def agent_endpoint(request: AgentRequest):
        async def generate():
            async for chunk in graph.astream(request.dict()):
                yield f"data: {json.dumps(chunk)}\n\n"
        return StreamingResponse(generate())

- research_finding: "JWT authentication with user context propagation"
  why: "Production security patterns for multi-agent systems"
  implementation: |
    async def agent_with_auth(request: AuthenticatedRequest):
        user_context = validate_token(request.token)
        initial_state = {"user": user_context, "messages": request.messages}
        return await graph.ainvoke(initial_state)
```

### Multi-Agent Coordination Patterns

```yaml
# SUPERVISOR PATTERN - Central coordination approach
supervisor_architecture:
  pattern: "Central supervisor making routing decisions based on task analysis"
  implementation: |
    async def supervisor_agent(state: MultiAgentState):
        # Analyze current state and decide next agent
        routing_decision = analyze_task_requirements(state)
        return {"current_agent": routing_decision}
  
  routing_logic: |
    def route_to_agent(state: MultiAgentState) -> str:
        current_agent = state.get("current_agent", "END")
        if current_agent == "research":
            return "research_agent"
        elif current_agent == "synthesis":
            return "synthesis_agent"
        return END

# PARALLEL EXECUTION - Fan-out/fan-in patterns
parallel_coordination:
  pattern: "Multiple agents processing simultaneously, results merged"
  implementation: |
    # Fan-out to parallel agents
    workflow.add_node("parallel_coordinator", parallel_coordinator)
    workflow.add_node("agent_a", research_agent_a)
    workflow.add_node("agent_b", research_agent_b)  
    workflow.add_node("agent_c", research_agent_c)
    workflow.add_node("synthesizer", synthesis_agent)
    
    # Parallel execution with Send primitive
    def fan_out_to_agents(state):
        return [
            Send("agent_a", {"messages": state["messages"]}),
            Send("agent_b", {"messages": state["messages"]}),
            Send("agent_c", {"messages": state["messages"]})
        ]

# TOOL HANDOFFS - Structured agent communication
tool_handoff_pattern:
  pattern: "Agents communicate through tool-based handoffs with Send()"
  implementation: |
    class HandoffTool(BaseTool):
        name = "handoff_to_agent"
        description = "Hand off task to specialized agent"
        
        def _run(self, agent_name: str, context: str):
            return Send(agent_name, {"messages": [HumanMessage(content=context)]})
```

### Testing & Validation Framework

```yaml
# PYTEST-ASYNCIO TESTING - Async workflow testing patterns
async_testing_setup:
  graph_compilation_test: |
    def test_graph_compilation():
        """Test that multi-agent graph compiles successfully"""
        graph = create_multi_agent_graph()
        compiled_graph = graph.compile()
        assert compiled_graph is not None
  
  node_isolation_test: |
    @pytest.mark.asyncio
    async def test_supervisor_agent():
        """Test supervisor agent routing logic"""
        mock_state = {"messages": [HumanMessage(content="test")]}
        result = await supervisor_agent(mock_state)
        assert "current_agent" in result
        assert result["current_agent"] in ["research", "analysis", "synthesis"]
  
  multi_agent_integration_test: |
    @pytest.mark.asyncio  
    async def test_multi_agent_workflow():
        """Test complete multi-agent workflow execution"""
        initial_state = {"messages": [HumanMessage(content="complex task")]}
        results = []
        async for chunk in graph.astream(initial_state):
            results.append(chunk)
        assert len(results) > 0
        assert any("agent_results" in chunk for chunk in results)

# MOCK STRATEGIES - External dependency mocking
mocking_patterns:
  tool_mocking: |
    @pytest.fixture
    def mock_search_tool():
        with patch('tools.search.BraveSearchTool') as mock:
            mock.return_value.ainvoke.return_value = "mocked search results"
            yield mock
  
  api_mocking: |
    @pytest.mark.asyncio
    async def test_with_mocked_api(httpx_mock):
        httpx_mock.add_response(json={"result": "mocked response"})
        # Test agent with mocked external API
```

## Implementation Blueprint

### Phase 1: State Schema & Graph Architecture

```python
# 1. Define comprehensive state schema
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage  
import operator

class [PROJECT_NAME]State(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    [DOMAIN_SPECIFIC_STATE]: Annotated[list[dict], operator.add]
    current_agent: str
    user_context: dict

# 2. Create graph architecture with proper compilation
from langgraph.graph import StateGraph, START, END

def create_[PROJECT_NAME]_graph():
    workflow = StateGraph([PROJECT_NAME]State)
    
    # Add specialized nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("[AGENT_1]", [agent_1]_node)
    workflow.add_node("[AGENT_2]", [agent_2]_node)
    
    # Add routing logic
    workflow.add_conditional_edges("supervisor", route_to_agent)
    workflow.add_edge(START, "supervisor")
    
    return workflow.compile()
```

### Phase 2: Multi-Agent Implementation (need to implement the agents as well)

```python
# 3. Implement supervisor coordination
async def supervisor_agent(state: [PROJECT_NAME]State) -> dict:
    """Central coordinator making routing decisions"""
    messages = state["messages"]
    current_task = messages[-1].content
    
    # Implement task analysis and routing logic
    next_agent = analyze_task_and_route(current_task)
    
    return {
        "current_agent": next_agent,
        "messages": [AIMessage(content=f"Routing to {next_agent}")]
    }

# 4. Create specialized agent implementations
async def [agent_1]_node(state: [PROJECT_NAME]State) -> dict:
    """Specialized agent for [SPECIFIC_FUNCTION]"""
    # Implement agent-specific logic
    # Use bound tools for agent specialization
    # Return updated state with results
    pass
```

### Phase 3: Testing & Validation

```python
# 7. Implement comprehensive testing
import pytest

@pytest.mark.asyncio
async def test_[project_name]_workflow():
    """Test complete multi-agent workflow"""
    initial_state = {"messages": [HumanMessage(content="[TEST_QUERY]")]}
    
    results = []
    async for chunk in graph.astream(initial_state):
        results.append(chunk)
    
    assert len(results) > 0
    assert "[EXPECTED_RESULT_PATTERN]" in str(results)
```

## Validation Loop

### Level 1: LangGraph Architecture Validation

```bash
# Graph compilation and state schema testing
python -c "from graph.state import [PROJECT_NAME]State; print('✓ State schema valid')"
python -c "from graph.graph import create_[project_name]_graph; create_[project_name]_graph(); print('✓ Graph compiles')"

# Multi-agent structure validation
test -f agents/supervisor.py && echo "✓ Supervisor agent exists"
test -f agents/[agent_1].py && echo "✓ Specialized agents exist"
test -d tools/ && echo "✓ Tool integration directory exists"

# Async pattern verification
grep -r "async def" . | wc -l  # Should be > 5 for multi-agent system
grep -r "await.*ainvoke\|astream" . | wc -l  # Should have async LangGraph patterns
```

### Level 2: Multi-Agent Coordination Testing

```bash
# State management patterns
grep -r "operator\.add\|MessagesState" . | wc -l  # Should have proper reducers
grep -r "StateGraph\|MessageGraph" . | wc -l  # Should use proper graph types
grep -r "Send.*agent\|supervisor" . | wc -l  # Should have coordination patterns

# Tool integration verification  
python -c "from tools.[tool_module] import *; print('✓ Tools importable')"
grep -r "bind_tools\|LangChain.*tool" . | wc -l  # Should have tool bindings
```

### Level 3: Testing & Quality Validation

```bash
# Async testing implementation
pytest tests/test_graph.py -v --asyncio-mode=auto  # Must pass
python -c "import pytest; print('✓ pytest-asyncio available')"

# Code quality checks  
black --check . && echo "✓ Code formatting correct"
mypy graph/ agents/ --ignore-missing-imports && echo "✓ Type checking passed"

# Documentation and environment
test -f .env.example && echo "✓ Environment template exists"
grep -q "LangGraph.*multi.*agent" README.md && echo "✓ Documentation present"
```

## Final Success Metrics

### Technical Implementation
- [ ] **Multi-Agent Coordination**: Correct multi-agent pattern with specialized agents working correctly
- [ ] **State Management**: TypedDict/Pydantic following best practices  
- [ ] **Graph Compilation**: StateGraph compiling and executing without errors
- [ ] **Async Architecture**: All nodes async with proper await patterns
- [ ] **Tool Integration**: All agents have the necessary tools

### Quality & Testing
- [ ] **Test Coverage**: pytest-asyncio tests for graph, agents, and API
- [ ] **Error Handling**: Graceful failure and agent isolation implemented
- [ ] **Documentation**: Clear setup, usage, and architecture guides

### LangGraph-Specific Features
- [ ] **Human-in-the-Loop**: Interrupt mechanisms where specified
- [ ] **Parallel Execution**: Fan-out/fan-in patterns for concurrent processing if applicable
- [ ] **State Persistence**: Checkpointing for long-running workflows if applicable
- [ ] **Performance**: Optimized for concurrent execution and scaling if applicable

**Remember**: Focus on LangGraph's strengths - sophisticated multi-agent coordination, stateful workflows, and production-ready deployment patterns. This is not a simple chatbot but a complex, intelligent system.