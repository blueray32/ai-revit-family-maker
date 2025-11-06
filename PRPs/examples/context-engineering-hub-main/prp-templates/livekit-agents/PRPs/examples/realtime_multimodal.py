"""
Realtime Multimodal Agent Example
==================================
Uses OpenAI's Realtime API for speech-to-speech with lower latency.
Also demonstrates Gemini Live for vision capabilities.
"""

from dotenv import load_dotenv
from livekit import rtc
from livekit import agents
from livekit.agents import (
    NOT_GIVEN,
    Agent,
    AgentFalseInterruptionEvent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    ModelSettings,
    RoomInputOptions,
    RoomOutputOptions,
    RunContext,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from livekit.agents.llm import function_tool
from livekit.plugins import openai, google, silero
import json
from typing import Dict, Any
import logging

# uncomment to enable Krisp background voice/noise cancellation
# from livekit.plugins import noise_cancellation

# Load environment variables
load_dotenv(".env")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


class RealtimeAssistant(Agent):
    """OpenAI Realtime API voice assistant with ultra-low latency."""
    
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a highly responsive voice assistant using the Realtime API.
            You can respond instantly with natural speech, including filler words and thinking sounds.
            Be conversational and engaging, as if having a real phone conversation."""
        )
    
    @function_tool
    async def search_information(self, context: RunContext, query: str) -> str:
        """
        Search for information on any topic.
        
        Args:
            query: What to search for
        """
        # Mock implementation - integrate with actual search API
        results = {
            "found": True,
            "summary": f"Here's what I found about {query}...",
            "details": ["Fact 1", "Fact 2", "Fact 3"]
        }
        return json.dumps(results)
    
    @function_tool
    async def set_reminder(self, context: RunContext, reminder: str, time: str) -> str:
        """
        Set a reminder for the user.
        
        Args:
            reminder: What to be reminded about
            time: When to be reminded (e.g., "in 5 minutes", "tomorrow at 3pm")
        """
        return f"I've set a reminder to {reminder} {time}"
    
    async def on_enter(self) -> None:
        """Greet user with natural speech."""
        await self.session.generate_reply(
            instructions="Greet the user naturally, as if answering a phone call. Be warm and ask how you can help today."
        )


class MultimodalVideoAssistant(Agent):
    """Gemini Live assistant with vision capabilities."""
    
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a helpful assistant with vision capabilities.
            You can see the user's video feed and help them with visual tasks.
            Be descriptive about what you see and provide helpful guidance.""",
            # Use Gemini Live for multimodal capabilities
            llm=google.beta.realtime.RealtimeModel(
                voice="Puck",
                temperature=0.8,
                model="gemini-2.0-flash-exp"
            ),
        )
    
    @function_tool
    async def analyze_image(self, context: RunContext) -> str:
        """Analyze what's currently visible in the video feed."""
        return "I can see your video feed. What would you like to know about what I'm seeing?"
    
    @function_tool
    async def provide_instructions(self, context: RunContext, task: str) -> str:
        """
        Provide step-by-step visual instructions.
        
        Args:
            task: What the user is trying to do
        """
        return f"I'll guide you through {task} based on what I can see..."
    
    async def on_enter(self) -> None:
        """Acknowledge video capabilities."""
        await self.session.generate_reply(
            instructions="Let the user know you can see their video and are ready to help with visual tasks."
        )


# OpenAI Realtime API Configuration
async def openai_realtime_entrypoint(ctx: agents.JobContext):
    """Entry point for OpenAI Realtime API agent."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Realtime API handles STT-LLM-TTS in a single model
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="echo",  # Available voices: echo, alloy, shimmer
            temperature=0.8,
            # Optional: Configure specific behaviors
            modalities=["text", "audio"],
            instructions="Be natural and conversational, use filler words like 'um' and 'uh' when thinking.",
        )
    )
    
    await session.start(
        room=ctx.room,
        agent=RealtimeAssistant(),
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Realtime agent started in room: {ctx.room.name}")
    
    # Handle session events
    @session.on("agent_state_changed")
    def on_state_changed(ev):
        """Log agent state changes."""
        logger.info(f"State: {ev.old_state} -> {ev.new_state}")
    
    @session.on("user_started_speaking")
    def on_user_speaking():
        """Track when user starts speaking."""
        logger.debug("User started speaking")
    
    @session.on("user_stopped_speaking")
    def on_user_stopped():
        """Track when user stops speaking."""
        logger.debug("User stopped speaking")


# Gemini Live Vision Configuration
async def gemini_vision_entrypoint(ctx: agents.JobContext):
    """Entry point for Gemini Live vision agent."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    session = AgentSession()  # LLM configured in Agent class
    
    await session.start(
        room=ctx.room,
        agent=MultimodalVideoAssistant(),
        room_input_options=RoomInputOptions(
            # Enable video input for vision capabilities
            video_enabled=True,
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Vision agent started in room: {ctx.room.name}")
    
    # Handle session events
    @session.on("agent_state_changed")
    def on_state_changed(ev):
        """Log agent state changes."""
        logger.info(f"State: {ev.old_state} -> {ev.new_state}")
    
    @session.on("user_started_speaking")
    def on_user_speaking():
        """Track when user starts speaking."""
        logger.debug("User started speaking")
    
    @session.on("user_stopped_speaking")
    def on_user_stopped():
        """Track when user stops speaking."""
        logger.debug("User stopped speaking")


# Combined Multimodal Agent
class CombinedMultimodalAssistant(Agent):
    """Advanced assistant combining multiple realtime models."""
    
    def __init__(self, use_vision: bool = False) -> None:
        # Choose model based on capabilities needed
        if use_vision:
            llm = google.beta.realtime.RealtimeModel(
                voice="Puck",
                model="gemini-2.0-flash-exp"
            )
        else:
            llm = openai.realtime.RealtimeModel(
                voice="echo"
            )
        
        super().__init__(
            instructions="You are an advanced multimodal assistant.",
            llm=llm
        )
    
    @function_tool
    async def switch_mode(self, context: RunContext, mode: str) -> str:
        """
        Switch between different interaction modes.
        
        Args:
            mode: "voice", "vision", or "both"
        """
        if mode == "vision" and not context.room_input_options.video_enabled:
            return "Vision mode requires video to be enabled"
        return f"Switched to {mode} mode"


async def combined_entrypoint(ctx: agents.JobContext):
    """Entry point for combined multimodal agent."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Detect if video is available
    has_video = False  # Set based on room configuration
    
    session = AgentSession()
    
    await session.start(
        room=ctx.room,
        agent=CombinedMultimodalAssistant(use_vision=has_video),
        room_input_options=RoomInputOptions(
            video_enabled=has_video,
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Multimodal agent started with video={'enabled' if has_video else 'disabled'}")
    
    # Handle session events
    @session.on("agent_state_changed")
    def on_state_changed(ev):
        """Log agent state changes."""
        logger.info(f"State: {ev.old_state} -> {ev.new_state}")


# Performance comparison example
def compare_latencies():
    """
    Latency comparison between different configurations:
    
    Traditional Pipeline (STT -> LLM -> TTS):
    - First token: ~1.5-2.5 seconds
    - Full response: ~3-5 seconds
    - Interruption handling: ~500ms delay
    
    OpenAI Realtime API:
    - First token: ~300-500ms
    - Full response: ~1-2 seconds
    - Interruption handling: ~100ms
    
    Gemini Live:
    - First token: ~400-600ms
    - Full response: ~1.5-2.5 seconds
    - Interruption handling: ~150ms
    - Adds vision capabilities
    """
    pass


if __name__ == "__main__":
    # Choose which agent to run
    import sys
    
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "realtime":
            entrypoint_fnc = openai_realtime_entrypoint
        elif mode == "vision":
            entrypoint_fnc = gemini_vision_entrypoint
        elif mode == "combined":
            entrypoint_fnc = combined_entrypoint
        else:
            print("Usage: python realtime_multimodal.py [realtime|vision|combined]")
            sys.exit(1)
    else:
        # Default to OpenAI Realtime
        entrypoint_fnc = openai_realtime_entrypoint
    
    # Run the agent using LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint_fnc, prewarm_fnc=prewarm))