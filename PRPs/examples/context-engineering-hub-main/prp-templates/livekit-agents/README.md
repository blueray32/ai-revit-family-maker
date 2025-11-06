# 🎤 LiveKit Agents Context Engineering Template

A comprehensive context engineering template for building realtime voice AI agents with LiveKit. This template provides everything you need to rapidly develop simple but powerful voice assistants with multimodal capabilities, turn detection, and tool integration.

> [See an example of a full RAG voice agent built with this PRP template (Dynamous Workshop).](https://github.com/dynamous-community/workshops/tree/main/livekit-rag-voice-agent)

## 🚀 Quick Start - Copy Template

Copy this template to your project directory:

```bash
# Copy to current directory
python copy_template.py .

# Copy to new project
python copy_template.py ~/projects/my-voice-agent

# Copy with extended help
python copy_template.py --help-extended
```

After copying, follow these steps:

1. **Set up environment:**
   ```bash
   cd <your-project>
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Optional: Test the out of the box agent (OpenAI and Deepgram API keys necessary in .env):**
   ```bash
   uv run python agent.py console
   ```

## 📋 PRP Framework Workflow

The Product Requirement Prompt (PRP) framework helps you build voice AI features systematically:

### Step 1: Create Your Requirements
Edit `PRPs/INITIAL.md` with your feature requirements (template included):

```markdown
## FEATURE:
Build a customer service voice agent that handles product inquiries and appointments

## TOOLS:
- check_order_status(order_id: str) -> dict
- search_products(query: str) -> list
- schedule_appointment(date: str, time: str) -> dict

## SYSTEM PROMPT(S):
Professional customer service rep - friendly, patient, and helpful

## EXAMPLES:
Using examples/basic_voice_assistant.py as starting point

## DOCUMENTATION:
See included LiveKit docs links for voice AI patterns
```

### Step 2: Generate PRP
Use the specialized command to generate a comprehensive PRP:

```bash
/generate-livekit-prp PRPs/INITIAL.md
```

Be sure to validate the PRP after generating!

This will:
- Research LiveKit patterns using Archon MCP
- Design voice pipeline architecture
- Plan tool integrations
- Create testing strategies
- Define deployment configuration

### Step 3: Execute PRP
Implement the feature using the generated PRP:

```bash
/execute-livekit-prp PRPs/customer-service-agent.md
```

This will:
- Set up UV project with dependencies
- Implement Agent class with tools
- Configure voice pipeline
- Create tests with behavioral validation
- Iterate until the tests (validation gates) are passing

## 🎯 What Is LiveKit Agents?

LiveKit Agents is a framework for building realtime AI participants that can:
- **Process voice, video, and text** in realtime
- **Use any AI provider** (OpenAI, Anthropic, Google, etc.)
- **Execute tools** with function calling
- **Handle interruptions** naturally
- **Support multiple languages**
- **Deploy anywhere** (LiveKit Cloud, Kubernetes, etc.)

## 📁 Template Structure

```
livekit-agents/
├── CLAUDE.md                          # LiveKit-specific AI rules
├── .claude/
│   └── commands/
│       ├── generate-livekit-prp.md   # PRP generation command
│       └── execute-livekit-prp.md    # PRP execution command
├── PRPs/
│   ├── templates/
│   │   └── prp_livekit_base.md       # Base PRP template
│   ├── examples/
│   │   ├── basic_voice_assistant.py  # Simple agent example
│   │   ├── realtime_multimodal.py    # Realtime API example
│   │   ├── custom_tools.py           # Tool integration
│   │   ├── agent_handoffs.py         # Multi-agent system
│   │   ├── telephony_integration.py  # Phone calls
│   │   └── mcp_server_integration.py # MCP tools
│   ├── ai_docs/
│   │   ├── livekit_architecture.md   # Architecture guide
│   │   ├── turn_detection_guide.md   # Turn detection patterns
│   │   ├── deployment_patterns.md    # Deployment strategies
│   │   └── provider_matrix.md        # AI provider comparison
│   └── INITIAL.md                    # Example feature request
├── agent.py                          # Main agent implementation
├── pyproject.toml                    # UV dependencies
├── Dockerfile                        # Container configuration
├── livekit.toml                     # LiveKit configuration
├── .env.example                     # Environment template
└── copy_template.py                 # Template deployment script
```

## 🔧 Development Setup

### Prerequisites

- **Python 3.9+** (required by LiveKit Agents)
- **UV package manager** (recommended)
- **LiveKit Cloud account** or self-hosted LiveKit server (if going to production)
- **API keys** for AI providers (OpenAI, Deepgram, etc.)

### Environment Configuration

Create `.env` with your credentials:

```bash
# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# AI Provider Keys
OPENAI_API_KEY=your-openai-key
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key  # Optional
ELEVENLABS_API_KEY=your-elevenlabs-key  # Optional
```

### Basic Agent Implementation

```python
from livekit.agents import AgentSession, Agent, function_tool
from livekit.plugins import openai, deepgram

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant."
        )
    
    @function_tool
    async def get_weather(self, context, location: str) -> str:
        """Get weather for a location."""
        return f"Weather in {location}: Sunny, 72°F"
    
    async def on_enter(self):
        await self.session.generate_reply(
            instructions="Greet the user warmly"
        )

async def entrypoint(ctx):
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="echo"),
    )
    
    await session.start(
        room=ctx.room,
        agent=Assistant()
    )
```

## 🧪 Testing Your Agent

### Console Mode
Test in your terminal with audio:

```bash
uv run python agent.py console
```

### Development Mode
Connect to LiveKit Cloud:

```bash
uv run python agent.py dev
```

### Unit Tests
Run the test suite:

```bash
uv run pytest tests/ -v --asyncio-mode=auto
```

### Behavioral Tests
Test conversation quality with judges:

```python
@pytest.mark.asyncio
async def test_greeting():
    session = AgentSession(llm=openai.LLM())
    await session.start(Assistant())
    
    result = await session.run("Hello")
    await result.expect.next_event().is_message(role="assistant").judge(
        llm, intent="Provides friendly greeting"
    )
```

## 📚 Examples Included

### 1. **Basic Voice Assistant** (`basic_voice_assistant.py`)
- Simple conversational agent
- Weather, time, and calculation tools
- Professional greeting pattern

### 2. **Realtime Multimodal** (`realtime_multimodal.py`)
- OpenAI Realtime API for low latency
- Gemini Live for vision capabilities
- Performance comparison examples

### 3. **Custom Tools** (`custom_tools.py`)
- Database integration
- API calls
- Dynamic tool creation
- MCP server integration

### 4. **Agent Handoffs** (`agent_handoffs.py`)
- Multi-agent system
- Routing and escalation
- Context preservation
- Different voices per agent

### 5. **Telephony Integration** (`telephony_integration.py`)
- SIP/phone call handling
- Voicemail detection
- Call transfers
- IVR systems

### 6. **MCP Server Integration** (`mcp_server_integration.py`)
- Tool discovery
- Multi-server orchestration
- Archon MCP integration

## ☁️ Deployment

### LiveKit Cloud

1. **Install CLI:**
   ```bash
   brew install livekit-cli  # macOS
   curl -sSL https://get.livekit.io/cli | bash  # Linux
   ```

2. **Deploy:**
   ```bash
   lk agent deploy
   ```

3. **Monitor:**
   ```bash
   lk agent logs --follow
   ```

### Docker

Build and run locally:

```bash
docker build -t my-agent .
docker run --env-file .env my-agent
```

### Kubernetes

Deploy with Helm or kubectl:

```bash
kubectl apply -f deployment.yaml
```

## 🎤 Voice Pipeline Options

### Standard Pipeline (STT → LLM → TTS)
```python
session = AgentSession(
    stt=deepgram.STT(model="nova-2"),
    llm=openai.LLM(model="gpt-4o-mini"),
    tts=cartesia.TTS(voice="professional"),
    turn_detection="semantic"
)
```

### Realtime Model (Speech-to-Speech)
```python
session = AgentSession(
    llm=openai.realtime.RealtimeModel(voice="echo")
)
# 300-500ms latency vs 1.5-2.5s for standard pipeline
```

### Multi-Modal with Vision
```python
session = AgentSession(
    llm=google.beta.realtime.RealtimeModel(voice="Puck"),
    room_input_options=RoomInputOptions(video_enabled=True)
)
```

## ⚙️ Configuration Options

### Turn Detection
- **Semantic Model** (recommended): Context-aware, natural flow
- **VAD-Based**: Faster, less contextual
- **STT Endpoint**: Balance of speed and accuracy

### Provider Selection
- **Budget**: Deepgram + GPT-4o-mini + OpenAI TTS (~$0.02/min)
- **Quality**: Deepgram + Claude Sonnet + ElevenLabs (~$0.10/min)
- **Speed**: Deepgram + Groq Llama + Cartesia (<500ms latency)
- **Realtime**: OpenAI Realtime API (~$0.06/min, <300ms)

### Scaling Options
- **Prewarm instances**: Keep agents ready
- **Auto-scaling**: Based on load
- **Regional deployment**: Reduce latency
- **Load balancing**: Distribute sessions

## 📖 Documentation

### LiveKit Resources
- [Official Docs](https://docs.livekit.io/agents/)
- [GitHub Examples](https://github.com/livekit/agents)
- [Voice AI Quickstart](https://docs.livekit.io/agents/start/voice-ai/)
- [API Reference](https://docs.livekit.io/reference/python/)

### Template Documentation
- `CLAUDE.md`: Comprehensive LiveKit patterns and rules
- `PRPs/ai_docs/`: Architecture and deployment guides
- `PRPs/examples/`: Working code examples
- `.claude/commands/`: PRP command documentation

## 🤝 Contributing

This template is part of the Context Engineering Hub. To contribute:

1. Fork the repository
2. Create your feature branch
3. Add examples or improvements
4. Submit a pull request

---

Built with ❤️ using LiveKit Agents and the PRP Framework