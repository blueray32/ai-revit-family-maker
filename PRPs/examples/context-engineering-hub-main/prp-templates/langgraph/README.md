# LangGraph Multi-Agent Template

A comprehensive context engineering template for building sophisticated LangGraph multi-agent systems with stateful workflows, parallel coordination, and production-ready deployment patterns.

## 🚀 Quick Start - Copy Template First

**Deploy this template to your project directory:**

```bash
# Copy template to your target directory
python copy_template.py /path/to/your/project

# Example usage
python copy_template.py ../my-langgraph-app
python copy_template.py /home/user/content-strategy-platform
python copy_template.py ./langgraph-multi-agent-system
```

**After copying, navigate to your new project and set up:**

```bash
cd /path/to/your/project

# Fill out PRPs/INITIAL.md with the requirements for the LangGraph workflow you want to create

# Start building your multi-agent system
/generate-langgraph-prp PRPs/INITIAL.md

# Validate the PRP then:
/execute-langgraph-prp PRPs/your-prp.md
```

## 📋 PRP Framework Workflow

This template implements the specialized LangGraph PRP (Product Requirement Prompt) workflow:

### 1. Define Requirements → `PRPs/INITIAL.md`
Create detailed feature specifications for your multi-agent system:
```markdown
# Your Multi-Agent System Requirements
## Core Features
- Research coordination with parallel agents
- Human-in-the-loop approval workflows  
- Production FastAPI deployment
## Multi-Agent Architecture
- Supervisor pattern with intelligent routing
- Specialized agents (SEO, Social Media, Analysis)
- State management with operator.add reducers
```

### 2. Generate PRP → `/generate-langgraph-prp`
Transform requirements into comprehensive implementation guide:
```bash
# Generate specialized LangGraph PRP
/generate-langgraph-prp PRPs/INITIAL.md

# This creates: PRPs/langgraph-{feature-name}.md
# Contains: Multi-agent architecture, state schemas, coordination patterns
```

### 3. Execute Implementation → `/execute-langgraph-prp`  
Build complete multi-agent system from PRP:
```bash
# Execute PRP to build full implementation
/execute-langgraph-prp PRPs/langgraph-{feature-name}.md

# Creates: Complete project structure with graph/, agents/, api/
# Includes: State management, parallel coordination, production deployment
```

## 📁 Template Structure

```
langgraph-template/
├── 🔧 CLAUDE.md                          # LangGraph global rules & patterns
├── 📋 .claude/commands/                   # Specialized PRP commands
│   ├── generate-langgraph-prp.md         # Multi-agent PRP generation
│   └── execute-langgraph-prp.md          # Graph implementation execution
├── 🎯 PRPs/                               # Product Requirement Prompts
│   ├── templates/
│   │   └── prp_langgraph_base.md          # LangGraph-specialized base template
│   ├── ai_docs/                           # Comprehensive documentation
│   │   ├── langgraph_concepts.md          # Core architecture & patterns
│   │   ├── state_management.md            # TypedDict, reducers, persistence  
│   │   └── multi_agent_patterns.md        # Supervisor, parallel, hierarchical
│   └── INITIAL.md                         # Example multi-agent project
├── 🎨 examples/                           # Progressive complexity examples
│   ├── basic_react_agent/                 # Simple agent with tools
│   ├── multi_agent_supervisor/            # Central coordination pattern
│   ├── parallel_research_agents/          # Production parallel execution
│   ├── human_in_loop_agent/              # Approval workflows & interrupts
│   └── langgraph-pydantic-ai-agents/     # LangGraph + Pydantic AI integration
├── 🚀 copy_template.py                    # Template deployment script
├── 📖 README.md                           # This comprehensive guide
└── 📦 requirements.txt                    # LangGraph dependencies
```

## 🎯 What You Can Build

### Multi-Agent Coordination Systems
- **Content Strategy Platforms**: Research agents → Analysis → Strategy synthesis
- **Customer Support Systems**: Routing → Specialized experts → Human escalation
- **Research Intelligence**: Parallel data gathering → Insight generation → Report creation
- **E-commerce Optimization**: Market research → Competitor analysis → Pricing strategies

### Advanced LangGraph Patterns
- **Supervisor Orchestration**: Central coordinator managing specialized workers
- **Parallel Fan-out/Fan-in**: Simultaneous agent execution with result synthesis  
- **Human-in-the-Loop**: Approval gates and intervention points
- **Hierarchical Teams**: Multi-level agent organization with team supervisors
- **Dynamic Handoffs**: Agents intelligently transferring control to specialists
- **Pydantic AI Integration**: Structured agent outputs with validation and type safety

### Production-Ready Features
- **FastAPI Integration**: Streaming responses and async endpoints
- **Authentication Systems**: JWT-based multi-user access control
- **State Persistence**: PostgreSQL checkpointing for long-running workflows
- **Monitoring & Observability**: LangSmith tracing and custom metrics
- **Error Recovery**: Isolated agent failures with graceful degradation

## 📚 Key Features

### Graph-First Architecture
- **StateGraph Compilation**: Define multi-agent workflows as executable graphs
- **Cyclical Execution**: Support for loops and recurring patterns (unlike DAG-only frameworks)
- **Conditional Routing**: Dynamic agent selection based on state conditions

### Advanced State Management  
- **TypedDict Performance**: Optimized state schemas with proper reducer functions
- **operator.add Patterns**: List concatenation and state merging for parallel agents
- **Persistent Memory**: Checkpointing for conversation continuity and fault tolerance
- **State Isolation**: Prevent agent interference through careful schema design

### Multi-Agent Orchestration
- **Supervisor Pattern**: Central coordinator with intelligent task routing
- **Parallel Execution**: Simultaneous agent processing with fan-out/fan-in architecture
- **Tool Integration**: LangChain tool binding with error handling and async patterns
- **Agent Specialization**: Domain-specific agents with focused responsibilities
- **Pydantic AI Agents**: Structured outputs with validation, dependency injection, and instrumentation

## 🔍 Examples Included

### 1. Basic ReAct Agent (`examples/basic_react_agent/`)
**Foundation pattern demonstrating:**
- StateGraph with MessagesState
- Tool integration (Brave Search, Calculator)  
- Conditional routing (tool use vs direct response)
- Async agent patterns with proper error handling

```python
# Simple but complete LangGraph agent
async def agent_node(state: MessagesState) -> dict:
    response = await llm_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState) -> Literal["tools", END]:
    return "tools" if state["messages"][-1].tool_calls else END
```

### 2. Multi-Agent Supervisor (`examples/multi_agent_supervisor/`)
**Advanced coordination demonstrating:**
- Supervisor pattern with specialized worker agents
- Custom state schema with operator.add reducers
- Dynamic agent routing based on task analysis
- Agent isolation and result aggregation

```python
class SupervisorState(TypedDict):
    messages: Annotated[list, operator.add]
    current_agent: str
    agent_results: Annotated[list[dict], operator.add]

async def supervisor_agent(state: SupervisorState) -> dict:
    routing_decision = await analyze_task_requirements(state["messages"])
    return {"current_agent": routing_decision}
```

### 3. Parallel Research Agents (`examples/parallel_research_agents/`)
**Production pattern demonstrating:**
- Fan-out to multiple specialized research agents  
- Send() primitive for parallel coordination
- Concurrent state merging with proper reducers
- Synthesis agent combining all research streams
- FastAPI integration with streaming responses

```python
async def parallel_coordinator(state) -> list[Send]:
    return [
        Send("seo_agent", state),
        Send("social_agent", state), 
        Send("competitor_agent", state)
    ]
```

### 4. Human-in-the-Loop Agent (`examples/human_in_loop_agent/`)
**Approval workflow demonstrating:**
- interrupt() mechanisms for human intervention
- Risk assessment with dynamic approval requirements
- State modification and workflow resume capabilities  
- Production approval patterns for high-risk actions

```python
async def approval_gate_agent(state) -> dict:
    if state["approval_required"]:
        human_input = interrupt("Approval needed for high-risk action")
        return {"human_feedback": human_input}
    return {"pending_action": "auto_approve"}
```

### 5. LangGraph + Pydantic AI Integration (`examples/langgraph-pydantic-ai-agents/`)
**Production-ready hybrid demonstrating:**
- Pydantic AI agents integrated with LangGraph workflows  
- Specialized research agents with structured outputs and validation
- Complete FastAPI deployment with JWT authentication and streaming
- Comprehensive monitoring with LangFuse integration and observability
- Advanced parallel research system with guardrail routing

```python
# Pydantic AI agent with LangGraph integration
from pydantic_ai import Agent, RunContext

seo_research_agent = Agent(
    get_model(use_smaller_model=False),
    deps_type=ResearchAgentDependencies,
    system_prompt=SEO_RESEARCH_SYSTEM_PROMPT,
    instrument=True
)

@seo_research_agent.tool
async def search_web(ctx: RunContext[ResearchAgentDependencies], query: str) -> List[Dict]:
    return await search_web_tool(api_key=ctx.deps.brave_api_key, query=query)
```

## 📖 Documentation References

### Official LangGraph Resources
- [LangGraph Multi-Agent Documentation](https://langchain-ai.github.io/langgraph/concepts/multi_agent/) - Official multi-agent patterns
- [Human-in-the-Loop Guide](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) - Interrupt mechanisms and approval workflows  
- [LangGraph Supervisor Tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/) - Supervisor pattern implementation

### Template-Specific Documentation
- `PRPs/ai_docs/langgraph_concepts.md` - Core architecture and design patterns
- `PRPs/ai_docs/state_management.md` - TypedDict, Pydantic, reducers, persistence
- `PRPs/ai_docs/multi_agent_patterns.md` - Supervisor, parallel, hierarchical coordination
- `PRPs/ai_docs/production_deployment.md` - FastAPI, authentication, monitoring, scaling

### State Management Patterns
- **TypedDict with operator.add**: Performance-optimized state with proper reducers
- **Pydantic BaseModel**: Runtime validation for complex state schemas
- **MessagesState**: Built-in conversation management with message deduplication
- **Custom Reducers**: Domain-specific state merging logic for parallel agents

## 🚫 Common Gotchas

### Multi-Agent Coordination
- **Infinite Loops**: Design conditional edges with proper termination conditions
- **State Conflicts**: Use operator.add reducers to prevent parallel agent interference  
- **Memory Leaks**: Implement state cleanup for long-running workflows
- **Race Conditions**: Design state schemas to handle concurrent agent updates

### Performance Issues
- **Tool Bottlenecks**: Use async tool calls to prevent blocking parallel execution
- **State Bloat**: Keep state lean and implement compression for large datasets
- **Connection Limits**: Use connection pooling for database and external API integrations
- **Serialization**: Ensure all state objects are JSON-serializable for checkpointing

### Production Deployment
- **Authentication**: Implement proper JWT validation and user context propagation
- **Error Isolation**: Prevent agent failures from crashing entire workflows
- **Resource Limits**: Set appropriate concurrency limits and request timeouts
- **Monitoring**: Include comprehensive logging and metrics for debugging complex workflows

### Development Workflow
- **Graph Compilation**: Always test graph.compile() during development
- **Async Testing**: Use pytest-asyncio for testing async agent workflows
- **State Schema Changes**: Update all agents when modifying state structure
- **Tool Integration**: Mock external APIs during development and testing

## 💡 Usage Examples

### Quick Development Workflow
```bash
# 1. Copy template to your project
python copy_template.py ./my-agent-system

# 2. Set up environment
cd my-agent-system
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
# Edit .env with your OpenAI, LangSmith keys

# 4. Create your requirements
# Edit PRPs/INITIAL.md with your multi-agent system requirements

# 5. Generate implementation PRP
/generate-langgraph-prp PRPs/INITIAL.md

# 6. Build your system  
/execute-langgraph-prp PRPs/langgraph-{your-feature}.md

# 7. Run and iterate
python -m pytest tests/ --asyncio-mode=auto
python api/main.py  # Start development server
```

### Customization Patterns
```bash
# Modify existing examples
cd examples/parallel_research_agents/
# Edit main.py to add your specialized research agents

# Try the Pydantic AI integration example
cd examples/langgraph-pydantic-ai-agents/
# Complete production system with structured agents, FastAPI, and monitoring

# Extend base PRP template  
# Edit PRPs/templates/prp_langgraph_base.md
# Add your domain-specific patterns and requirements

# Create custom agents
# Add new agents in agents/ directory
# Update graph compilation in graph/graph.py

# Add specialized tools
# Implement in tools/ directory  
# Bind to appropriate agents in your workflow
```

This template provides everything needed to build sophisticated, production-ready multi-agent systems with LangGraph. The progressive examples and comprehensive documentation enable rapid development from basic concepts to complex, coordinated agent workflows.