# PRP: [Feature Name] - LiveKit Voice AI Agent

---
name: "[Feature Name]"
type: "voice-ai-agent"
framework: "livekit-agents"
version: "1.0"
---

## Goal

[Describe the voice AI feature you want to build. Be specific about the agent's purpose, capabilities, and user interactions.]

Example:
- Build a customer service voice agent that can handle product inquiries
- Create a voice assistant for scheduling appointments
- Develop a multi-agent system for technical support with escalation

## Why

[Explain the business value and user benefits]

- **User Experience**: How will this improve user interactions?
- **Efficiency**: What processes will be automated?
- **Scalability**: How will this handle growth?
- **Innovation**: What new capabilities does this enable?

## What

### Voice Pipeline Architecture

```yaml
Pipeline Configuration:
  STT:
    provider: deepgram  # or assemblyai, azure, whisper
    model: nova-2       # or nova-2-general, nova-2-meeting
    language: en        # or multi for multilingual
  
  LLM:
    provider: openai    # or anthropic, google, groq
    model: gpt-4o-mini  # or claude-3-sonnet, gemini-pro
    temperature: 0.7
    max_tokens: 150
  
  TTS:
    provider: openai    # or cartesia, elevenlabs, playht
    voice: echo         # or specific voice ID
    speed: 1.0
  
  VAD:
    provider: silero
    threshold: 0.5
  
  Turn Detection:
    strategy: semantic  # or vad_based, stt_endpoint
    sensitivity: 0.7
```

### Agent Design

```python
Agent Class Structure:
  - Name: [AgentClassName]
  - Base: livekit.agents.Agent
  - Instructions: |
      "You are a [role] who [capabilities].
      Your personality is [traits].
      Always [behaviors].
      Never [restrictions]."
  
  Tools:
    - tool_name_1: Description and parameters
    - tool_name_2: Description and parameters
  
  Lifecycle:
    - on_enter: Initial greeting and setup
    - on_exit: Cleanup and handoff
  
  State Management:
    - conversation_context
    - user_preferences
    - session_data
```

### Multi-Agent Workflows (if applicable)

```yaml
Agent Hierarchy:
  GreeterAgent:
    role: Initial contact and routing
    handoff_to: [SpecialistAgent, SupportAgent]
  
  SpecialistAgent:
    role: Domain-specific assistance
    tools: [technical_tools]
    escalate_to: SupervisorAgent
  
  SupervisorAgent:
    role: Handle complex cases
    capabilities: [override, manual_intervention]
```

### Tool Definitions

```python
Required Tools:
  - get_user_info:
      description: "Retrieve user information"
      parameters:
        - user_id: str
      returns: dict
  
  - search_knowledge_base:
      description: "Search internal documentation"
      parameters:
        - query: str
        - limit: int = 5
      returns: list[str]
  
  - [additional_tools]:
      description: "..."
      parameters: [...]
      returns: ...
```

## Success Criteria

### Functional Requirements
- [ ] Agent responds to voice input within 2 seconds
- [ ] Turn detection correctly identifies speaker changes
- [ ] Tools execute successfully with proper error handling
- [ ] Interruptions are handled gracefully
- [ ] Multi-agent handoffs work seamlessly (if applicable)

### Quality Metrics
- [ ] Conversation feels natural and responsive
- [ ] Average response latency < 500ms
- [ ] Turn detection accuracy > 95%
- [ ] Tool execution success rate > 99%
- [ ] User satisfaction score > 4.5/5

### Testing Coverage
- [ ] Unit tests for all tools
- [ ] Behavioral tests with judges
- [ ] Integration tests for agent handoffs
- [ ] Load testing for concurrent sessions
- [ ] Edge case handling verified

## All Needed Context (MUST READ)

### LiveKit Documentation
```yaml
Essential Resources:
  - url: https://docs.livekit.io/agents/
    why: Complete Agents framework documentation
  
  - url: https://docs.livekit.io/agents/build/
    why: Building voice agents guide
  
  - url: https://docs.livekit.io/agents/build/turns/
    why: Turn detection patterns
  
  - url: https://docs.livekit.io/agents/build/tools/
    why: Tool integration patterns
  
  - url: https://github.com/livekit/agents/tree/main/examples
    why: Working examples repository
```

### Project Context
```yaml
Existing Code:
  - file: [path/to/existing/agent.py]
    why: Current agent implementation to extend
  
  - file: [path/to/database/models.py]
    why: Data models for tool integration
  
  - file: [path/to/api/client.py]
    why: API client for external services
```

## Implementation Blueprint

### Phase 1: Project Setup

```bash
# Initialize UV project
uv init [project-name]
cd [project-name]

# Add core dependencies
uv add livekit-agents
uv add livekit-plugins-openai
uv add livekit-plugins-deepgram
uv add livekit-plugins-cartesia
uv add livekit-plugins-silero
uv add livekit-plugins-turn-detector
uv add python-dotenv aiohttp

# Add dev dependencies
uv add --dev pytest pytest-asyncio pytest-cov black ruff

# Create project structure
mkdir -p {tests,tools,agents,config}
touch agent.py .env.example livekit.toml Dockerfile
```

### Phase 2: Core Agent Implementation

```python
# agent.py structure
"""
1. Imports and configuration
2. Tool definitions with @function_tool
3. Agent class with instructions
4. AgentSession configuration
5. Entrypoint function
6. CLI runner
"""

# Implementation checklist:
- [ ] Define Agent class with instructions
- [ ] Implement @function_tool methods
- [ ] Configure AgentSession with providers
- [ ] Add lifecycle methods (on_enter, on_exit)
- [ ] Set up event handlers
- [ ] Add error handling and logging
```

### Phase 3: Tool Integration

```python
# For each tool:
- [ ] Define function signature with types
- [ ] Add @function_tool decorator
- [ ] Implement tool logic
- [ ] Add error handling
- [ ] Create unit tests
- [ ] Document usage
```

### Phase 4: Testing Suite

```bash
# Create test files
touch tests/test_agent.py
touch tests/test_tools.py
touch tests/test_behaviors.py

# Test scenarios:
- [ ] Agent initialization
- [ ] Greeting behavior
- [ ] Tool invocations
- [ ] Interruption handling
- [ ] Error recovery
- [ ] Multi-agent handoffs
```

### Phase 5: Deployment Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
CMD ["uv", "run", "python", "agent.py"]
```

```toml
# livekit.toml
[agent]
job_type = "room"
worker_type = "agent"

[agent.prewarm]
count = 1
```

### Phase 6: Validation & Optimization

```bash
# Local testing
uv run python agent.py console

# Run test suite
uv run pytest tests/ -v --asyncio-mode=auto

# Performance testing
uv run python tests/load_test.py
```

## Validation Commands

```bash
# Development
uv sync                                    # Install dependencies
uv run python agent.py console            # Test in terminal
uv run python agent.py dev               # Connect to LiveKit

# Testing
uv run pytest tests/ -v                  # Run all tests
uv run pytest tests/ --cov=.            # With coverage
uv run python -m pytest --asyncio-mode=auto  # Async tests

# Code Quality
uv run black .                           # Format code
uv run ruff check .                      # Lint code
```

## Common Implementation Patterns

### Greeting Pattern
```python
class Assistant(Agent):
    async def on_enter(self):
        await self.session.generate_reply(
            instructions="Greet the user warmly and ask how you can help"
        )
```

### Tool Usage Pattern
```python
@function_tool
async def search_products(context: RunContext, query: str, category: str = None) -> str:
    """Search product catalog"""
    try:
        results = await database.search(query, category)
        return json.dumps(results[:5])
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return "I couldn't search products at the moment"
```

### Interruption Handling
```python
await self.session.say(
    "Let me explain our return policy in detail...",
    allow_interruptions=True
)
```

### Multi-Agent Handoff
```python
if "technical" in user_intent:
    await self.session.set_agent(
        TechnicalAgent(),
        handoff_message="Transferring you to our technical specialist"
    )
```

### Error Recovery
```python
@session.on("error")
async def on_error(error: Exception):
    logger.error(f"Session error: {error}")
    await session.say("I encountered an issue. Let me try again.")
```

## Monitoring & Observability

```python
# Structured logging
import structlog
logger = structlog.get_logger()

# Log key events
logger.info("agent.started", session_id=session.id)
logger.info("tool.executed", tool=tool_name, duration=elapsed)
logger.error("tool.failed", tool=tool_name, error=str(e))

# Metrics to track
- Session duration
- Tool execution times
- Turn detection accuracy
- Error rates
- Token usage
```

## Anti-Patterns to Avoid

- ❌ Don't use synchronous code in async methods
- ❌ Don't ignore error handling
- ❌ Don't hardcode credentials
- ❌ Don't skip input validation
- ❌ Don't create long-running tools
- ❌ Don't forget to test interruptions
- ❌ Don't neglect logging
- ❌ Don't skip behavioral testing

## Confidence Score: [X/10]

Explain your confidence level and any concerns or uncertainties about the implementation.

## Next Steps

After PRP approval:
1. Execute implementation with `/execute-livekit-prp`
2. Test thoroughly in console mode
3. Run behavioral test suite
4. Deploy to staging environment
5. Conduct user testing
6. Deploy to production
7. Monitor and iterate

---

Remember: The goal is to create a simple yet powerful voice AI agent that provides natural, responsive conversations!