## FEATURE:

[REPLACE EVERYTHING IN BRACKETS WITH YOUR OWN CONTEXT]
[Provide an overview of the voice AI agent you want to build. The more detail the better!]
[Example: Build a customer service voice agent that can handle product inquiries, check order status, schedule appointments, and escalate to human agents when needed. The agent should have a professional yet friendly tone and support both English and Spanish.]

## TOOLS:

[Describe the tools you want for your agent(s) - functionality, arguments, what they return, etc. Be as specific as you like - the more specific the better.]
[Example tools:
- check_order_status(order_id: str) -> dict: Returns order details including status, tracking, delivery date
- search_products(query: str, max_results: int = 5) -> list: Returns matching products with name, price, description
- schedule_appointment(date: str, time: str, duration_minutes: int) -> dict: Books calendar slot and returns confirmation
- escalate_to_human(reason: str, urgency: str) -> str: Transfers to human agent with context]

## SYSTEM PROMPT(S)

[Describe the instructions for the agent(s) here - you can create the entire system prompt here or give a general description to guide the coding assistant]
[Example: "You are a professional customer service representative for [Company]. You are helpful, patient, and empathetic. Always acknowledge customer emotions, use their name when known, and provide clear, concise responses. If you don't know something, be honest and offer to find out or escalate to a specialist."]

## EXAMPLES:

[Add any additional example agents/tool implementations from past projects or online resources to the examples/ folder and reference them here.]
[The template contains the following already for LiveKit Agents:]

- **examples/basic_voice_assistant.py** - Simple conversational agent with weather, time, and calculation tools
- **examples/realtime_multimodal.py** - OpenAI Realtime API for ultra-low latency and Gemini Live for vision
- **examples/custom_tools.py** - Database access, API integration, dynamic tool creation, MCP servers
- **examples/agent_handoffs.py** - Multi-agent system with routing, escalation, and context preservation
- **examples/telephony_integration.py** - SIP/phone calls, voicemail detection, IVR, call transfers
- **examples/mcp_server_integration.py** - MCP tool discovery, multi-server orchestration, Archon integration

## DOCUMENTATION:

[Add any additional documentation you want it to reference - this can be curated docs you put in PRPs/ai_docs, URLs, etc.]

### LiveKit Official Documentation:
- **LiveKit Agents Overview**: https://docs.livekit.io/agents/
- **Voice AI Quickstart**: https://docs.livekit.io/agents/start/voice-ai/
- **Building Voice Agents**: https://docs.livekit.io/agents/build/
- **Turn Detection**: https://docs.livekit.io/agents/build/turns/
- **Tool Integration**: https://docs.livekit.io/agents/build/tools/

## VOICE PIPELINE CONFIGURATION:

### Speech-to-Text (STT)
**Recommended: Deepgram Nova-3 for best balance of speed, accuracy, and cost**

- [ ] **Deepgram** (Recommended)
  - [ ] nova-2 (General purpose, fast)
  - [ ] nova-2-phonecall (Optimized for telephony)
  - [ ] nova-3 (Latest, highest accuracy)
- [ ] **AssemblyAI**
  - [ ] universal-streaming (Best for voice agents)
  - [ ] slam-1 (Superior context understanding)
- [ ] **OpenAI Whisper**
  - [ ] whisper-large (High accuracy, higher latency)
  - [ ] whisper-medium (Balanced)
- [ ] **Azure Speech Services**
  - [ ] Standard (Real-time transcription)
- [ ] **Google Speech-to-Text**
  - [ ] Chirp 2 (Latest model)

### Large Language Model (LLM)
**Recommended: OpenAI gpt-4.1-mini for best balance of capability and cost**

- [ ] **OpenAI**
  - [ ] gpt-4.1-mini (Recommended - fast, capable, cost-effective)
  - [ ] gpt-4.1 (More capable, higher cost)
- [ ] **Anthropic**
  - [ ] claude-3.5-haiku (Fast, efficient)
  - [ ] claude-4-sonnet (Balanced)
  - [ ] claude-4-opus (Most capable)
- [ ] **Google**
  - [ ] gemini-2.5-flash (Fast, efficient)
  - [ ] gemini-2.5-pro (More capable)
- [ ] **Groq** (Ultra-fast inference)
  - [ ] llama-3.3-70b (Open source, fast)
  - [ ] mixtral-8x7b (Efficient MoE)
- [ ] **Together AI**
  - [ ] meta-llama/Llama-3.3-70B (Open source)
  - [ ] mistralai/Mixtral-8x7B (MoE architecture)

### Text-to-Speech (TTS)
**Recommended: OpenAI TTS for best balance of quality and latency**

- [ ] **OpenAI** (Recommended)
  - [ ] echo (Natural, versatile)
  - [ ] alloy (Neutral, clear)
  - [ ] shimmer (Warm, friendly)
  - [ ] onyx (Deep, authoritative)
  - [ ] nova (Energetic)
  - [ ] fable (Expressive, British)
  - [ ] ash (Warm, versatile)
- [ ] **Cartesia**
  - [ ] sonic-english (90ms latency, very fast)
  - [ ] Custom voices (Voice cloning available)
- [ ] **ElevenLabs**
  - [ ] eleven_flash_v2 (75ms latency, recommended for agents)
  - [ ] eleven_multilingual_v2 (Maximum realism)
  - [ ] Custom voices (Professional voice cloning)
- [ ] **Azure Speech Services**
  - [ ] Neural voices (Multiple languages)
  - [ ] Custom neural voice (Enterprise)

### Additional Options:

**Voice Activity Detection (VAD):**
- [x] Silero VAD (Default, recommended)

**Turn Detection:**
- [x] Multilingual Model (Recommended for natural conversation)
- [ ] Semantic Model (English only, context-aware)
- [ ] VAD-based (Faster, less contextual)
- [ ] STT Endpoint (Uses STT provider's detection)

**Noise Cancellation (keep off if you want simple):**
- [ ] Enable Krisp noise cancellation
- [ ] Use telephony-optimized (for phone calls)

## OTHER CONSIDERATIONS:

- Python 3.9+ required - all methods must be `async`
- .env file will always be .env, not .env.local
- Default recommendation: Deepgram + gpt-4.1-mini + OpenAI TTS for best balance
- Use multilingual detection for natural conversation
- Test locally first with `uv run python agent.py console`
- Keep agents simple - add complexity gradually
- Run the agent like: cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm)), just the entrypoint_fnc and prewarm_fnc parameters unless specified otherwise. Be sure to create the prewarm function like in basic_voice_assistant.py and have the necessary imports
- Always import function_tool from LiveKit when adding tools
- Prefer MultilingualModel for turn detection unless specified otherwise, import with: from livekit.plugins.turn_detector.multilingual import MultilingualModel
- Leave out @session.on("error") unless specified otherwise


[Add any additional considerations specific to your use case - latency requirements, language support, compliance needs, etc.]