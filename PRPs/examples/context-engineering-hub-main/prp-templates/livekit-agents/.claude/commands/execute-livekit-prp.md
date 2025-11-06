# Execute LiveKit Agents PRP

Execute a LiveKit Agents Product Requirement Prompt to implement a complete voice AI feature with proper testing and deployment setup.

## Usage
```
/execute-livekit-prp <path-to-prp.md>
```

## Execution Process

1. **Load and Parse PRP**
   - Read the LiveKit Agents PRP file
   - Extract voice pipeline configuration
   - Identify required providers and tools
   - Parse validation requirements

2. **ULTRATHINK - Implementation Planning**
   - Design complete agent architecture
   - Plan tool implementations
   - Map conversation flows
   - Design test scenarios
   - Plan deployment strategy

3. **Phase 1: Project Setup**
   ```bash
   # Initialize UV project
   uv init [project-name]
   cd [project-name]
   
   # Add LiveKit dependencies
   uv add livekit-agents
   uv add livekit-plugins-openai
   uv add livekit-plugins-deepgram
   uv add livekit-plugins-cartesia
   uv add livekit-plugins-silero
   uv add pytest pytest-asyncio
   
   # Sync dependencies
   uv sync
   ```

4. **Phase 2: Core Implementation**
   
   **Create agent.py:**
   - Import required plugins
   - Define Agent class with instructions
   - Implement @function_tool methods
   - Set up AgentSession configuration
   - Implement lifecycle methods
   - Add event handlers

   **Example structure:**
   ```python
   from livekit import agents
   from livekit.agents import AgentSession, Agent, function_tool
   from livekit.plugins import openai, deepgram, cartesia
   
   class Assistant(Agent):
       def __init__(self):
           super().__init__(instructions="...")
       
       @function_tool
       async def tool_name(self, context, param: str) -> str:
           """Tool description"""
           # Implementation
       
       async def on_enter(self):
           # Greeting logic
   
   async def entrypoint(ctx: agents.JobContext):
       session = AgentSession(...)
       await session.start(room=ctx.room, agent=Assistant())
   ```

5. **Phase 3: Voice Pipeline Configuration**
   
   **Configure providers based on PRP:**
   - STT provider and model
   - LLM provider and model
   - TTS provider and voice
   - VAD configuration
   - Turn detection strategy
   - Noise cancellation

6. **Phase 4: Tool Implementation**
   
   **For each tool in PRP:**
   - Create @function_tool method
   - Add type annotations
   - Implement tool logic
   - Handle errors gracefully
   - Add logging

7. **Phase 5: Testing Implementation**
   
   **Create tests/test_agent.py:**
   ```python
   import pytest
   from livekit.agents.testing import AgentTestSuite, Judge
   
   @pytest.mark.asyncio
   async def test_greeting():
       suite = AgentTestSuite()
       judge = Judge(criteria="...")
       result = await suite.test_agent(...)
       assert result.passed
   ```
   
   **Create tests for:**
   - Agent greeting behavior
   - Tool invocations
   - Interruption handling
   - Multi-agent handoffs
   - Error scenarios

8. **Phase 6: Deployment Setup**
   
   **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY pyproject.toml uv.lock ./
   RUN pip install uv && uv sync --frozen
   COPY . .
   CMD ["uv", "run", "python", "agent.py"]
   ```
   
   **Create livekit.toml:**
   ```toml
   [agent]
   job_type = "room"
   worker_type = "agent"
   
   [agent.prewarm]
   count = 1
   ```
   
   **Create .env.example:**
   ```bash
   LIVEKIT_URL=
   LIVEKIT_API_KEY=
   LIVEKIT_API_SECRET=
   OPENAI_API_KEY=
   DEEPGRAM_API_KEY=
   ```

9. **Phase 7: Validation**
   
   **Run all validation commands from PRP:**
   ```bash
   # Test in console
   uv run python agent.py console
   
   # Run unit tests
   uv run pytest tests/ -v --asyncio-mode=auto
   
   # Test specific scenarios
   uv run python agent.py test --scenario "greeting"
   ```

10. **Phase 8: Documentation**
    
    **Create README.md with:**
    - Project description
    - Setup instructions
    - Environment variables
    - Testing guide
    - Deployment instructions
    - Troubleshooting

## Success Criteria

### Required Outcomes
- [ ] Agent responds to voice input
- [ ] Turn detection works smoothly
- [ ] Tools execute correctly
- [ ] Interruptions handled gracefully
- [ ] All tests pass
- [ ] Console mode works
- [ ] Docker image builds
- [ ] Deployment validates

## Output Structure

After execution, the project should have:
```
project-name/
├── agent.py                # Main agent implementation
├── tests/
│   ├── test_agent.py      # Unit tests
│   └── test_behaviors.py  # Behavioral tests
├── Dockerfile             # Container configuration
├── livekit.toml          # LiveKit configuration
├── pyproject.toml        # UV dependencies
├── uv.lock              # Locked dependencies
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

The implementation is complete when all validation criteria pass and the agent provides natural, responsive voice interactions!