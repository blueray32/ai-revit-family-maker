"""
Multi-Agent Handoffs Example
============================
Demonstrates how to build a multi-agent system with smooth handoffs,
escalation paths, and specialized agents for different domains.
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
from typing import Optional, Dict, Any, List
from enum import Enum
import json
import asyncio
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


class AgentRole(Enum):
    """Define agent roles in the system."""
    GREETER = "greeter"
    SALES = "sales"
    SUPPORT = "support"
    TECHNICAL = "technical"
    MANAGER = "manager"


class BaseAgent(Agent):
    """Base class for all specialized agents."""
    
    def __init__(
        self,
        role: AgentRole,
        instructions: str,
        voice: Optional[str] = None,
        **kwargs
    ):
        self.role = role
        self.handoff_history: List[str] = []
        
        # Each agent can have a different voice
        if voice:
            kwargs["tts"] = cartesia.TTS(voice=voice)
        
        super().__init__(instructions=instructions, **kwargs)
    
    async def analyze_intent(self, user_message: str) -> Optional[AgentRole]:
        """Analyze user intent to determine if handoff is needed."""
        # Override in subclasses for specific routing logic
        return None
    
    async def prepare_handoff(self, target_role: AgentRole) -> Dict[str, Any]:
        """Prepare context for handoff to another agent."""
        return {
            "from_agent": self.role.value,
            "conversation_summary": await self.get_conversation_summary(),
            "user_context": await self.get_user_context(),
            "handoff_reason": f"User needs {target_role.value} assistance"
        }
    
    async def get_conversation_summary(self) -> str:
        """Get a summary of the conversation so far."""
        # Access conversation history from session
        history = self.session.history
        if len(history) > 0:
            # Summarize last few exchanges
            recent = history[-5:]  # Last 5 messages
            return f"Recent discussion about: {', '.join([msg.content[:50] for msg in recent])}"
        return "New conversation"
    
    async def get_user_context(self) -> Dict[str, Any]:
        """Get current user context."""
        return {
            "session_duration": self.session.duration_seconds,
            "previous_agents": self.handoff_history,
            "current_state": self.session.state
        }


class GreeterAgent(BaseAgent):
    """Initial agent that greets users and routes them."""
    
    def __init__(self):
        super().__init__(
            role=AgentRole.GREETER,
            instructions="""You are a friendly greeter who welcomes users and determines their needs.
            Ask clarifying questions to understand if they need:
            - Sales information (pricing, features, demos)
            - Support help (issues, problems, bugs)
            - Technical assistance (integration, API, development)
            Keep the interaction brief and route them to the right specialist.""",
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"  # Friendly voice
        )
    
    @function_tool
    async def route_to_specialist(self, context: RunContext, department: str) -> str:
        """
        Route the user to a specialist.
        
        Args:
            department: sales, support, or technical
        """
        dept_map = {
            "sales": AgentRole.SALES,
            "support": AgentRole.SUPPORT,
            "technical": AgentRole.TECHNICAL
        }
        
        if department in dept_map:
            target_role = dept_map[department]
            handoff_context = await self.prepare_handoff(target_role)
            
            # Perform the handoff
            await self.session.set_agent(
                self.create_specialist(target_role, handoff_context)
            )
            return f"Transferring to {department}"
        else:
            return "Invalid department"
    
    async def on_enter(self) -> None:
        """Greet the user."""
        await self.session.generate_reply(
            instructions="Warmly greet the user and ask how you can direct their call today."
        )
    
    async def analyze_intent(self, user_message: str) -> Optional[AgentRole]:
        """Analyze message to auto-route if clear intent."""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["buy", "price", "demo", "trial"]):
            return AgentRole.SALES
        elif any(word in message_lower for word in ["problem", "issue", "broken", "help"]):
            return AgentRole.SUPPORT
        elif any(word in message_lower for word in ["api", "integrate", "developer", "code"]):
            return AgentRole.TECHNICAL
        
        return None
    
    def create_specialist(self, role: AgentRole, context: Dict[str, Any]) -> Agent:
        """Create the appropriate specialist agent."""
        if role == AgentRole.SALES:
            return SalesAgent(context)
        elif role == AgentRole.SUPPORT:
            return SupportAgent(context)
        elif role == AgentRole.TECHNICAL:
            return TechnicalAgent(context)
        else:
            return self


class SalesAgent(BaseAgent):
    """Sales specialist for product information and demos."""
    
    def __init__(self, handoff_context: Optional[Dict] = None):
        self.handoff_context = handoff_context or {}
        
        super().__init__(
            role=AgentRole.SALES,
            instructions="""You are a knowledgeable sales specialist.
            You can discuss pricing, features, demos, and help close deals.
            Be enthusiastic but not pushy. Focus on value and solving problems.""",
            voice="6f84f4b8-58a2-430c-8c79-688dad597532"  # Professional voice
        )
    
    @function_tool
    async def show_pricing(self, context: RunContext, plan: str = "all") -> str:
        """
        Show pricing information.
        
        Args:
            plan: Which plan to show (starter, pro, enterprise, all)
        """
        pricing = {
            "starter": "$29/month - Up to 5 users",
            "pro": "$99/month - Up to 50 users", 
            "enterprise": "Custom pricing - Unlimited users"
        }
        
        if plan == "all":
            return json.dumps(pricing, indent=2)
        else:
            return pricing.get(plan, "Plan not found")
    
    @function_tool
    async def schedule_demo(
        self,
        context: RunContext,
        preferred_date: str,
        email: str
    ) -> str:
        """
        Schedule a product demo.
        
        Args:
            preferred_date: When they'd like the demo
            email: Contact email
        """
        # Integration with calendar system would go here
        return f"Demo scheduled for {preferred_date}. Confirmation sent to {email}"
    
    @function_tool
    async def escalate_to_manager(self, context: RunContext, reason: str) -> str:
        """
        Escalate to sales manager for special requests.
        
        Args:
            reason: Why escalation is needed
        """
        handoff_context = await self.prepare_handoff(AgentRole.MANAGER)
        handoff_context["escalation_reason"] = reason
        
        await self.session.set_agent(
            ManagerAgent(handoff_context, original_role=self.role)
        )
        return "Connecting you with a manager"
    
    async def on_enter(self) -> None:
        """Handle entry after handoff."""
        if self.handoff_context:
            summary = self.handoff_context.get("conversation_summary", "")
            await self.session.say(
                f"Hi! I'm from sales. I understand you're interested in our products. {summary}"
            )
        else:
            await self.session.generate_reply(
                instructions="Introduce yourself as a sales specialist and ask about their needs."
            )


class SupportAgent(BaseAgent):
    """Support specialist for handling issues and problems."""
    
    def __init__(self, handoff_context: Optional[Dict] = None):
        self.handoff_context = handoff_context or {}
        
        super().__init__(
            role=AgentRole.SUPPORT,
            instructions="""You are a helpful support specialist.
            You troubleshoot issues, provide solutions, and ensure customer satisfaction.
            Be patient, empathetic, and thorough in your assistance.""",
            voice="b7d7c7a6-4819-4d13-9237-5dfa68223c12"  # Calm, supportive voice
        )
    
    @function_tool
    async def lookup_ticket(self, context: RunContext, ticket_id: str) -> str:
        """
        Look up a support ticket.
        
        Args:
            ticket_id: The ticket ID to look up
        """
        # Mock ticket lookup
        return f"Ticket {ticket_id}: Status - In Progress, Last updated - 2 hours ago"
    
    @function_tool
    async def create_ticket(
        self,
        context: RunContext,
        issue_description: str,
        priority: str = "normal"
    ) -> str:
        """
        Create a new support ticket.
        
        Args:
            issue_description: Description of the issue
            priority: low, normal, high, urgent
        """
        ticket_id = f"TKT-{hash(issue_description) % 10000:04d}"
        return f"Created ticket {ticket_id} with {priority} priority"
    
    @function_tool
    async def escalate_technical(self, context: RunContext) -> str:
        """Escalate to technical team for complex issues."""
        handoff_context = await self.prepare_handoff(AgentRole.TECHNICAL)
        await self.session.set_agent(TechnicalAgent(handoff_context))
        return "Transferring to technical team"
    
    async def on_enter(self) -> None:
        """Handle entry after handoff."""
        await self.session.generate_reply(
            instructions="Acknowledge the user's issue and start gathering information to help."
        )


class TechnicalAgent(BaseAgent):
    """Technical specialist for API and integration support."""
    
    def __init__(self, handoff_context: Optional[Dict] = None):
        self.handoff_context = handoff_context or {}
        
        super().__init__(
            role=AgentRole.TECHNICAL,
            instructions="""You are a technical specialist with deep knowledge of APIs and integrations.
            You can help with code examples, debugging, and technical architecture.
            Be precise and provide actionable technical guidance.""",
            voice="8e95c6d4-7943-4831-ae29-c7d8fe234bd3"  # Clear, technical voice
        )
    
    @function_tool
    async def provide_code_example(
        self,
        context: RunContext,
        language: str,
        feature: str
    ) -> str:
        """
        Provide a code example.
        
        Args:
            language: Programming language (python, javascript, etc.)
            feature: What feature to demonstrate
        """
        examples = {
            "python": {
                "api_call": "import requests\nresponse = requests.get('https://api.example.com')",
                "webhook": "from flask import Flask\napp = Flask(__name__)"
            },
            "javascript": {
                "api_call": "fetch('https://api.example.com').then(r => r.json())",
                "webhook": "app.post('/webhook', (req, res) => {...})"
            }
        }
        
        if language in examples and feature in examples[language]:
            return examples[language][feature]
        else:
            return "Example not available for that combination"
    
    @function_tool
    async def check_api_status(self, context: RunContext) -> str:
        """Check the current API status."""
        # Mock API status check
        return "API Status: All systems operational. Uptime: 99.95%"
    
    async def on_enter(self) -> None:
        """Handle entry after handoff."""
        await self.session.generate_reply(
            instructions="Let the user know you're from technical support and can help with API/integration issues."
        )


class ManagerAgent(BaseAgent):
    """Manager for handling escalations and special requests."""
    
    def __init__(
        self,
        handoff_context: Optional[Dict] = None,
        original_role: Optional[AgentRole] = None
    ):
        self.handoff_context = handoff_context or {}
        self.original_role = original_role
        
        super().__init__(
            role=AgentRole.MANAGER,
            instructions="""You are a manager with authority to make special arrangements.
            You handle escalations, approve discounts, and resolve complex situations.
            Be professional, decisive, and solution-oriented.""",
            voice="1f8f5e2d-9a3b-4c7e-ae28-b7c9d3e4f5a6"  # Authoritative voice
        )
    
    @function_tool
    async def approve_discount(
        self,
        context: RunContext,
        percentage: int,
        reason: str
    ) -> str:
        """
        Approve a discount.
        
        Args:
            percentage: Discount percentage
            reason: Justification for discount
        """
        if percentage <= 20:
            return f"Approved {percentage}% discount. Reason: {reason}"
        else:
            return f"Cannot approve {percentage}% discount. Maximum is 20%"
    
    @function_tool
    async def return_to_specialist(self, context: RunContext) -> str:
        """Return to the previous specialist."""
        if self.original_role:
            # Return to the original agent
            if self.original_role == AgentRole.SALES:
                await self.session.set_agent(SalesAgent())
            elif self.original_role == AgentRole.SUPPORT:
                await self.session.set_agent(SupportAgent())
            elif self.original_role == AgentRole.TECHNICAL:
                await self.session.set_agent(TechnicalAgent())
            
            return f"Returning to {self.original_role.value}"
        else:
            return "No previous agent to return to"
    
    async def on_enter(self) -> None:
        """Handle entry as manager."""
        reason = self.handoff_context.get("escalation_reason", "your situation")
        await self.session.say(
            f"Hello, I'm a manager. I understand you need assistance with {reason}. "
            "I have the authority to help resolve this. What specific outcome are you looking for?"
        )


async def entrypoint(ctx: agents.JobContext):
    """Main entry point for multi-agent system."""
    
    # Configure session with base settings
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model="gpt-4o-mini", temperature=0.7),  # More capable model for complex routing
        # TTS configured per agent for different voices
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel()
    )
    
    # Start with greeter agent
    await session.start(
        room=ctx.room,
        agent=GreeterAgent(),
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Multi-agent system started in room: {ctx.room.name}")
    
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