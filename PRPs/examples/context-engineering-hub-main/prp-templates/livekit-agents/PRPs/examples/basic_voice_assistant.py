"""
LiveKit Voice Agent
==================
Main agent implementation file. This is a starter template - replace with your actual agent code.
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
from livekit.plugins import openai, deepgram, silero
from datetime import datetime
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


class Assistant(Agent):
    """Main voice assistant implementation."""
    
    def __init__(self):
        super().__init__(
            instructions="""You are a helpful and friendly voice AI assistant.
            You speak clearly and naturally, as if having a phone conversation.
            Be concise but warm in your responses.
            If you don't know something, be honest about it."""
        )
    
    @function_tool
    async def get_current_time(self, context: RunContext) -> str:
        """Get the current time."""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    @function_tool
    async def example_tool(self, context: RunContext, parameter: str) -> str:
        """
        Example tool function - replace with your actual tools.
        
        Args:
            parameter: Example parameter
        """
        return f"Processed: {parameter}"
    
    async def on_enter(self):
        """Called when the agent becomes active."""
        logger.info("Agent session started")
        
        # Generate initial greeting
        await self.session.generate_reply(
            instructions="Greet the user warmly and ask how you can help them today."
        )
    
    async def on_exit(self):
        """Called when the agent session ends."""
        logger.info("Agent session ended")


async def entrypoint(ctx: agents.JobContext):
    """Main entry point for the agent worker."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Configure the voice pipeline
    session = AgentSession(
        # Speech-to-Text
        stt=deepgram.STT(
            model="nova-2",
            language="en",
        ),
        
        # Large Language Model
        llm=openai.LLM(
            model="gpt-4.1-mini",
            temperature=0.7,
        ),
        
        # Text-to-Speech
        tts=openai.TTS(
            voice="echo",
            speed=1.0,
        ),
        
        # Voice Activity Detection
        vad=silero.VAD.load(),
        
        # Turn detection strategy
        turn_detection=MultilingualModel(),
    )
    
    # Start the session
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
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


if __name__ == "__main__":
    # Run the agent using LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))