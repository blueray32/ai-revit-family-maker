# Generate LangGraph PRP

## Feature file: [specified_file.md]

Generate a comprehensive PRP for building sophisticated LangGraph multi-agent applications based on the detailed requirements in the specified feature file. This follows the LangGraph-specific PRP framework workflow: INITIAL.md → generate-langgraph-prp → execute-langgraph-prp.

**CRITICAL: Web search and LangGraph documentation research is essential. Use it extensively throughout this process.**

## LangGraph Research Process

1. **Read and Understand Multi-Agent Requirements**
   - Read the specified INITIAL.md file thoroughly
   - Understand the multi-agent coordination requirements
   - Identify state management complexity and agent specializations
   - Note specific LangGraph features needed (parallel execution, human-in-the-loop, etc.)
   - Determine supervisor vs. hierarchical vs. swarm architecture needs

2. **Extensive LangGraph Web Research (CRITICAL)**
   - **Web search LangGraph multi-agent patterns extensively** - this is essential
   - Study official LangGraph documentation for state management approaches
   - Research StateGraph vs MessageGraph patterns for the use case
   - Find real-world LangGraph implementations with similar requirements
   - Look for LangGraph supervisor pattern examples and best practices
   - Research parallel execution and fan-out/fan-in coordination patterns
   - Identify human-in-the-loop implementation strategies

3. **LangGraph Architecture Analysis**
   - Examine successful multi-agent LangGraph implementations found through web research
   - Identify state schema patterns (TypedDict vs Pydantic approaches)
   - Extract agent coordination patterns and graph topology designs
   - Document tool integration approaches and LangChain bindings
   - Note production deployment patterns with FastAPI and streaming
   - Research testing approaches for async graph workflows

4. **Context Engineering Adaptation for LangGraph**
   - Map discovered LangGraph patterns to the specific requirements
   - Plan state-first development approach with proper schema design
   - Design multi-agent validation requirements specific to graph workflows
   - Plan LangGraph-specific implementation blueprints and examples

## LangGraph PRP Generation

Using PRPs/templates/prp_langgraph_base.md as the foundation:

### Critical LangGraph Context to Include from Web Research

**LangGraph Documentation (from web search)**:
- Official LangGraph multi-agent documentation URLs with specific patterns
- State management guides for TypedDict and Pydantic integration
- Graph compilation and execution tutorials
- Human-in-the-loop implementation guides with interrupt mechanisms
- Production deployment patterns with LangGraph Platform

**Multi-Agent Implementation Patterns (from research)**:
- Supervisor pattern implementations with central coordination
- Parallel execution examples with fan-out/fan-in architectures
- State merging strategies with operator.add and custom reducers
- Tool handoff patterns using Send() primitive
- Hierarchical agent coordination approaches

**Real-World LangGraph Examples**:
- Links to successful LangGraph multi-agent implementations found online
- Code snippets demonstrating state schema design and graph compilation
- Production deployment examples with FastAPI and streaming integration
- Testing patterns for async graph workflows with pytest-asyncio

### LangGraph Implementation Blueprint

Based on web research findings:
- **Multi-Agent Architecture**: Document agent specialization and coordination strategy
- **State Schema Design**: Plan TypedDict/Pydantic models with proper reducers
- **Graph Topology**: Design node connections, edges, and conditional routing
- **Tool Integration Strategy**: LangChain tool binding and custom tool development
- **Human-in-the-Loop Design**: Interrupt points and approval workflow implementation
- **Production Deployment**: FastAPI integration with authentication and streaming

### LangGraph Validation Gates (Must be Executable)

```bash
# LangGraph Project Structure Validation
ls -la graph/ agents/ tools/ api/ tests/
find . -name "*.py" | grep -E "(state|graph|agent)" | wc -l  # Should have core components

# State Schema and Graph Compilation Testing
python -c "from graph.state import AgentState; print('State schema valid')"
python -c "from graph.graph import create_graph; create_graph().compile(); print('Graph compiles')"

# Multi-Agent Workflow Testing
python -m pytest tests/test_graph.py -v --asyncio-mode=auto
python -c "from agents.supervisor import supervisor_agent; print('Agents importable')"

# Production Deployment Validation
python -c "from api.main import app; print('FastAPI app created')"
grep -r "astream\|async" . | wc -l  # Should have async patterns throughout

# LangGraph-Specific Pattern Validation
grep -r "StateGraph\|MessageGraph" . | wc -l  # Should use proper graph types
grep -r "operator\.add\|MessagesState" . | wc -l  # Should have proper state management
grep -r "Send\|supervisor" . | wc -l  # Should have multi-agent coordination
```

*** CRITICAL: Do extensive web research on LangGraph before writing the PRP ***
*** Use WebSearch tool extensively to understand multi-agent patterns deeply ***

## Output

Save as: `PRPs/langgraph-{feature-name}.md`

## LangGraph Quality Checklist

- [ ] Extensive web research completed on LangGraph multi-agent patterns
- [ ] Official LangGraph documentation thoroughly reviewed and referenced
- [ ] Real-world multi-agent examples and architectures identified
- [ ] Complete state schema design planned with proper reducers
- [ ] Multi-agent coordination strategy documented (supervisor/hierarchical/parallel)
- [ ] Tool integration approach specified with LangChain bindings
- [ ] Human-in-the-loop patterns included where appropriate
- [ ] Production deployment strategy with FastAPI and streaming
- [ ] Testing approach with pytest-asyncio and async patterns
- [ ] All web research findings documented in PRP context
- [ ] LangGraph-specific gotchas and patterns captured

Score the PRP on a scale of 1-10 (confidence level for creating comprehensive, production-ready LangGraph multi-agent systems based on thorough research).

Remember: The goal is creating sophisticated, stateful multi-agent workflows that leverage LangGraph's cyclical execution, parallel coordination, and production-ready deployment capabilities through comprehensive research and specialized context engineering.