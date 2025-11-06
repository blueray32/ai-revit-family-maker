# LangGraph Template - Global Rules for Multi-Agent Context Engineering

This file contains LangGraph-specific global rules and principles that apply to ALL LangGraph multi-agent development work. These rules are based on extensive research of LangGraph architecture, patterns, and production deployments.

## 🌊 LangGraph Core Principles

**IMPORTANT: These principles apply to ALL LangGraph development work:**

### Graph-First Architecture
- **Always start with state schema design** - Define TypedDict/Pydantic models before graph implementation
- **Use StateGraph for complex workflows** - MessageGraph only for simple conversation flows  
- **Design for cyclical execution** - LangGraph excels at loops and recurring patterns (unlike DAG-only frameworks)
- **Plan node dependencies carefully** - Avoid circular dependencies and missing state keys

### Multi-Agent Coordination Patterns
- **Supervisor pattern is king** - Use central coordination for complex multi-agent systems
- **Parallel execution with fan-out/fan-in** - Design for concurrent agent processing where possible
- **Tool-based handoffs** - Use Send() primitive for structured agent communication
- **State isolation** - Prevent agent pollution through proper state management

### Async-by-Default Development
- **All node functions must be async** - `async def node_function(state)` is the standard pattern
- **Use async tool calls** - Prefer `tool.ainvoke()` over synchronous calls
- **Stream responses** - Implement `graph.astream()` for real-time user feedback
- **Handle async errors gracefully** - Proper exception handling in async workflows

## 🏗️ LangGraph Project Structure & Modularity

### Recommended Directory Organization
```
project_root/
├── graph/
│   ├── __init__.py
│   ├── state.py              # State schemas (TypedDict/Pydantic)
│   ├── nodes.py              # Node function implementations  
│   ├── graph.py              # Graph compilation and setup
│   └── routing.py            # Conditional edge logic
├── agents/
│   ├── __init__.py
│   ├── supervisor.py         # Supervisor agent coordination
│   ├── research_agent.py     # Specialized research agents
│   └── synthesis_agent.py    # Result synthesis agents
├── tools/
│   ├── __init__.py
│   ├── search_tools.py       # Web search integrations
│   ├── data_tools.py         # Data processing tools
│   └── custom_tools.py       # Domain-specific tools
├── api/
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── auth.py               # Authentication middleware
│   └── streaming.py          # Streaming response handlers
├── tests/
│   ├── __init__.py
│   ├── test_graph.py         # Graph compilation tests
│   ├── test_nodes.py         # Node isolation tests
│   └── test_agents.py        # Agent behavior tests
├── .env.example              # Environment variable template
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

### State Management Best Practices
- **Use TypedDict with operator.add for performance** - Preferred over Pydantic for most use cases
- **Implement proper state reducers** - Use `operator.add` for list concatenation, custom reducers for complex merging
- **Design for concurrent updates** - State merging must handle parallel agent execution
- **Include conversation history** - Use MessagesState or custom message management

### Code Organization Standards
- **Never create files longer than 500 lines** - Split into logical modules when approaching limit
- **Group related functionality** - Agents, tools, and graph logic in separate modules
- **Use clear, descriptive naming** - `research_agent_node`, `supervisor_routing_logic`

## 🧪 LangGraph Testing & Validation Standards

### Testing Framework Integration
- **Use pytest-asyncio** - Essential for testing async LangGraph workflows
- **Mock external dependencies** - Use `unittest.mock` for API calls and external services
- **Test node functions in isolation** - Individual node testing with synthetic state
- **Graph compilation testing** - Verify graph compiles correctly with `graph.compile()`

### Validation Approaches
```python
# Graph Compilation Testing
def test_graph_compilation():
    graph = create_research_graph()
    compiled_graph = graph.compile()
    assert compiled_graph is not None

# Node Isolation Testing
@pytest.mark.asyncio
async def test_research_node():
    mock_state = {"messages": [HumanMessage(content="test query")]}
    result = await research_agent_node(mock_state)
    assert "research_data" in result
    assert len(result["research_data"]) > 0

# Parallel Execution Testing
@pytest.mark.asyncio
async def test_parallel_agent_coordination():
    initial_state = {"messages": [HumanMessage(content="research request")]}
    results = []
    async for chunk in graph.astream(initial_state):
        results.append(chunk)
    assert len(results) > 0
```

### Common Validation Commands
```bash
# LangGraph-specific validation
python -m pytest tests/ -v --asyncio-mode=auto
python -c "from graph.graph import create_graph; create_graph().compile()"
black --check --diff .
mypy graph/ agents/ tools/
```

## 🚀 LangGraph Development Workflow & Patterns

### Development Process
1. **State Schema First** - Design TypedDict/Pydantic models before implementation
2. **Node Development** - Implement individual node functions with clear contracts
3. **Graph Assembly** - Connect nodes with edges and conditional routing
4. **Testing Integration** - Test each component and full graph execution

### LangGraph-Specific Commands
```bash
# Development workflow
pip install langgraph langgraph-cli[inmem]
langgraph dev                    # Start development server with LangGraph Studio
pytest tests/ --asyncio-mode=auto   # Run async tests
black . && mypy . && flake8 .   # Code quality checks
```

### State Management Implementation
```python
# Preferred TypedDict pattern
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    research_data: Annotated[list[dict], operator.add]
    user_context: str
    current_agent: str
```

## 🚫 LangGraph Anti-Patterns to Always Avoid

- ❌ Don't ignore state management - Proper state schema is critical for complex workflows
- ❌ Don't skip async patterns - Synchronous code limits LangGraph performance
- ❌ Don't forget error handling - Agent failures must be isolated and recoverable
- ❌ Don't skip graph compilation testing - Broken graphs fail at runtime
