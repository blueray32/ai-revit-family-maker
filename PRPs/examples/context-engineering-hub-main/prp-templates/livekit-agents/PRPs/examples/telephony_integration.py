"""
Telephony Integration Example
=============================
Demonstrates SIP/telephony integration for phone call handling,
voicemail detection, and call management.
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
from livekit.plugins import openai, deepgram, cartesia, silero
import asyncio
import json
from typing import Optional, Dict, Any
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


class TelephonyAgent(Agent):
    """Agent optimized for phone call interactions."""
    
    def __init__(self):
        super().__init__(
            instructions="""You are a professional phone assistant.
            Speak clearly and concisely as if on a phone call.
            Be aware that audio quality may vary and repeat important information.
            Always confirm details like numbers, names, and addresses."""
        )
        
        self.call_metadata: Dict[str, Any] = {}
        self.is_voicemail_detected = False
    
    @function_tool
    async def detect_answering_machine(self, context: RunContext) -> str:
        """
        Detect if we've reached a voicemail/answering machine.
        Call this AFTER hearing the voicemail greeting.
        """
        self.is_voicemail_detected = True
        
        # Leave a voicemail message
        await self.session.generate_reply(
            instructions="""Leave a professional voicemail message that includes:
            - Your name and company
            - Brief reason for calling
            - Callback number
            - Best time to reach you
            Keep it under 30 seconds."""
        )
        
        # Wait for message to complete
        await asyncio.sleep(1)
        
        # Hang up after leaving message
        await self.hangup_call()
        
        return "Voicemail message left"
    
    @function_tool
    async def hangup_call(self, context: RunContext) -> str:
        """End the current phone call."""
        # Signal to end the call
        await self.session.disconnect()
        return "Call ended"
    
    @function_tool
    async def transfer_call(self, context: RunContext, extension: str) -> str:
        """
        Transfer the call to another extension.
        
        Args:
            extension: The extension number to transfer to
        """
        # In production, integrate with SIP transfer mechanism
        await self.session.say(f"Transferring your call to extension {extension}. Please hold.")
        
        # Simulate transfer
        await asyncio.sleep(2)
        
        # Here you would initiate actual SIP transfer
        # For demo, we just notify
        return f"Call transferred to {extension}"
    
    @function_tool
    async def send_sms(
        self,
        context: RunContext,
        phone_number: str,
        message: str
    ) -> str:
        """
        Send an SMS message to the caller.
        
        Args:
            phone_number: Phone number to send to
            message: SMS message content
        """
        # Integration with SMS gateway would go here
        # Example: Twilio, MessageBird, etc.
        
        return f"SMS sent to {phone_number}: {message[:50]}..."
    
    @function_tool
    async def lookup_caller_info(self, context: RunContext) -> str:
        """Look up information about the caller."""
        # In production, integrate with CRM or caller ID service
        caller_info = self.call_metadata.get("caller_info", {})
        
        if caller_info:
            return json.dumps(caller_info, indent=2)
        else:
            return "No caller information available"
    
    @function_tool
    async def record_call_note(
        self,
        context: RunContext,
        note: str,
        category: str = "general"
    ) -> str:
        """
        Record a note about this call.
        
        Args:
            note: The note content
            category: Category (general, complaint, request, feedback)
        """
        timestamp = datetime.now().isoformat()
        call_note = {
            "timestamp": timestamp,
            "category": category,
            "note": note,
            "call_id": self.call_metadata.get("call_id", "unknown")
        }
        
        # Store in database/CRM
        return f"Note recorded: {category} - {note[:100]}"
    
    async def on_enter(self) -> None:
        """Handle call start."""
        # Extract call metadata if available
        room = self.session.room
        
        # Get SIP metadata from room attributes
        self.call_metadata = {
            "call_id": room.name,
            "caller_number": room.metadata.get("caller_number", "Unknown"),
            "called_number": room.metadata.get("called_number", "Unknown"),
            "call_start": datetime.now().isoformat()
        }
        
        # Initial greeting - professional phone greeting
        await self.session.generate_reply(
            instructions="""Answer the phone professionally:
            - State the company name
            - Your name
            - Ask how you can help
            Example: 'Thank you for calling [Company]. This is [Name]. How may I assist you today?'"""
        )
        
        # Start voicemail detection timer
        asyncio.create_task(self._voicemail_detection_timeout())
    
    async def _voicemail_detection_timeout(self):
        """Timeout for voicemail detection."""
        await asyncio.sleep(4)  # Wait 4 seconds for response
        
        if not self.session.user_speaking and not self.is_voicemail_detected:
            # Might be voicemail, prompt for detection
            print("Possible voicemail detected - no user response")
    
    async def on_exit(self) -> None:
        """Handle call end."""
        call_duration = self.session.duration_seconds
        
        # Log call details
        call_log = {
            **self.call_metadata,
            "call_end": datetime.now().isoformat(),
            "duration_seconds": call_duration,
            "voicemail": self.is_voicemail_detected
        }
        
        print(f"Call ended. Log: {json.dumps(call_log, indent=2)}")


class OutboundCallerAgent(Agent):
    """Agent for making outbound calls."""
    
    def __init__(self, call_purpose: str, target_number: str):
        self.call_purpose = call_purpose
        self.target_number = target_number
        
        super().__init__(
            instructions=f"""You are making an outbound call for: {call_purpose}.
            Be professional and respectful of the recipient's time.
            If they're busy, offer to call back at a better time."""
        )
    
    @function_tool
    async def schedule_callback(
        self,
        context: RunContext,
        preferred_time: str
    ) -> str:
        """
        Schedule a callback at the recipient's preferred time.
        
        Args:
            preferred_time: When to call back
        """
        # Schedule in system
        callback_info = {
            "number": self.target_number,
            "time": preferred_time,
            "purpose": self.call_purpose
        }
        
        await self.session.say(f"Perfect! I'll call you back {preferred_time}. Thank you for your time.")
        
        return json.dumps(callback_info)
    
    async def on_enter(self) -> None:
        """Start outbound call."""
        await self.session.generate_reply(
            instructions=f"""Introduce yourself and state the purpose of the call:
            - Your name and company
            - Briefly state: {self.call_purpose}
            - Confirm it's a good time to talk"""
        )


class IVRAgent(Agent):
    """Interactive Voice Response (IVR) agent for call routing."""
    
    def __init__(self):
        super().__init__(
            instructions="""You are an IVR system that helps route calls.
            Listen for department names or numbers.
            Be clear about options and repeat if needed."""
        )
        
        self.menu_options = {
            "1": "sales",
            "2": "support",
            "3": "billing",
            "4": "operator",
            "sales": "sales",
            "support": "support",
            "billing": "billing",
            "operator": "operator"
        }
    
    @function_tool
    async def route_call(self, context: RunContext, option: str) -> str:
        """
        Route the call based on menu selection.
        
        Args:
            option: Menu option (1-4) or department name
        """
        department = self.menu_options.get(option.lower())
        
        if department:
            await self.session.say(f"Transferring you to {department}. Please hold.")
            
            # Here you would route to appropriate agent/queue
            # For demo, we just confirm
            return f"Call routed to {department}"
        else:
            await self.session.say("Invalid option. Please try again.")
            await self.present_menu()
            return "Invalid option"
    
    async def present_menu(self):
        """Present the IVR menu options."""
        await self.session.say(
            "Press 1 or say 'sales' for sales. "
            "Press 2 or say 'support' for technical support. "
            "Press 3 or say 'billing' for billing inquiries. "
            "Press 4 or say 'operator' for an operator."
        )
    
    async def on_enter(self) -> None:
        """Start IVR flow."""
        await self.session.say("Thank you for calling. Please listen to the following options.")
        await self.present_menu()


async def telephony_entrypoint(ctx: agents.JobContext):
    """Entry point for telephony agents."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Determine call type from room metadata
    room_metadata = ctx.room.metadata
    call_type = room_metadata.get("call_type", "inbound")
    
    # Configure for telephony
    session = AgentSession(
        # Optimized for phone audio
        stt=deepgram.STT(
            model="nova-2-phonecall",  # Optimized for phone calls
            language="en"
        ),
        llm=openai.LLM(
            model="gpt-4o-mini",
            temperature=0.5  # More consistent for phone calls
        ),
        tts=cartesia.TTS(
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
            speed=0.95  # Slightly slower for phone clarity
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel()
    )
    
    # Choose agent based on call type
    if call_type == "outbound":
        purpose = room_metadata.get("purpose", "follow-up")
        number = room_metadata.get("target_number", "unknown")
        agent = OutboundCallerAgent(purpose, number)
    elif call_type == "ivr":
        agent = IVRAgent()
    else:
        agent = TelephonyAgent()
    
    await session.start(
        room=ctx.room,
        agent=agent,
        # room_input_options=RoomInputOptions(
            # Optimized noise cancellation for telephony
            # noise_cancellation=noise_cancellation.BVCTelephony(),
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Telephony agent started: {call_type}")
    
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


async def sip_configuration_example():
    """
    Example SIP configuration for LiveKit.
    This would typically be configured via LiveKit Cloud dashboard or API.
    """
    
    config = {
        "sip_trunk": {
            "name": "Main Trunk",
            "numbers": ["+1234567890"],
            "allowed_addresses": ["sip.provider.com"],
            "username": "your_sip_username",
            "password": "your_sip_password"
        },
        "dispatch_rules": [
            {
                "name": "Support Line",
                "trunk": "Main Trunk",
                "rule": {
                    "phone_number": "+1234567890",
                    "room_prefix": "support-",
                    "agent": "telephony-agent"
                }
            }
        ],
        "outbound_settings": {
            "caller_id": "+1234567890",
            "max_concurrent": 10,
            "retry_policy": {
                "max_attempts": 3,
                "retry_delay": 300  # 5 minutes
            }
        }
    }
    
    return config


if __name__ == "__main__":
    # Run the agent using LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=telephony_entrypoint, prewarm_fnc=prewarm))