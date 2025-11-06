"""
Custom Tools Example
====================
Demonstrates various tool patterns including database access, API calls,
dynamic tool generation, and MCP server integration.
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
import aiohttp
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import sqlite3
from contextlib import asynccontextmanager
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


class ToolsAssistant(Agent):
    """Assistant with comprehensive tool integration."""
    
    def __init__(self, db_path: str = "assistant.db") -> None:
        self.db_path = db_path
        self.api_client = APIClient()
        
        super().__init__(
            instructions="""You are a capable assistant with access to various tools.
            You can search databases, make API calls, manage schedules, and more.
            Always confirm actions before executing them when they have side effects."""
        )
    
    # Database Tools
    @function_tool
    async def search_database(
        self, 
        context: RunContext, 
        query: str,
        table: str = "products",
        limit: int = 5
    ) -> str:
        """
        Search the database for information.
        
        Args:
            query: Search query
            table: Table to search in (products, users, orders)
            limit: Maximum number of results
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Safe parameterized query
            safe_tables = ["products", "users", "orders"]
            if table not in safe_tables:
                return f"Invalid table. Choose from: {safe_tables}"
            
            # Example search implementation
            sql = f"SELECT * FROM {table} WHERE name LIKE ? LIMIT ?"
            cursor.execute(sql, (f"%{query}%", limit))
            
            results = cursor.fetchall()
            conn.close()
            
            if results:
                return json.dumps({"found": len(results), "data": results})
            else:
                return "No results found"
                
        except Exception as e:
            return f"Database error: {str(e)}"
    
    @function_tool
    async def update_record(
        self,
        context: RunContext,
        record_id: str,
        field: str,
        value: str,
        table: str = "products"
    ) -> str:
        """
        Update a record in the database.
        
        Args:
            record_id: ID of the record to update
            field: Field to update
            value: New value
            table: Table containing the record
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validate and execute update
            safe_fields = ["name", "description", "status", "notes"]
            if field not in safe_fields:
                return f"Cannot update field '{field}'"
            
            sql = f"UPDATE {table} SET {field} = ? WHERE id = ?"
            cursor.execute(sql, (value, record_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                conn.close()
                return f"Successfully updated {field} for record {record_id}"
            else:
                conn.close()
                return f"No record found with ID {record_id}"
                
        except Exception as e:
            return f"Update failed: {str(e)}"
    
    # API Integration Tools
    @function_tool
    async def call_external_api(
        self,
        context: RunContext,
        endpoint: str,
        method: str = "GET",
        data: Optional[str] = None
    ) -> str:
        """
        Make a call to an external API.
        
        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, PUT, DELETE)
            data: JSON data for POST/PUT requests
        """
        try:
            result = await self.api_client.request(
                endpoint=endpoint,
                method=method,
                data=json.loads(data) if data else None
            )
            return json.dumps(result)
        except Exception as e:
            return f"API call failed: {str(e)}"
    
    @function_tool
    async def get_stock_price(self, context: RunContext, symbol: str) -> str:
        """
        Get current stock price for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, GOOGL)
        """
        # Mock implementation - replace with actual API
        prices = {
            "AAPL": 195.89,
            "GOOGL": 141.23,
            "MSFT": 378.91,
            "AMZN": 155.33
        }
        
        if symbol.upper() in prices:
            price = prices[symbol.upper()]
            return f"{symbol.upper()} is currently trading at ${price}"
        else:
            return f"Stock symbol {symbol} not found"
    
    # Scheduling Tools
    @function_tool
    async def schedule_appointment(
        self,
        context: RunContext,
        date: str,
        time: str,
        duration_minutes: int = 30,
        description: str = ""
    ) -> str:
        """
        Schedule an appointment.
        
        Args:
            date: Date in YYYY-MM-DD format
            time: Time in HH:MM format
            duration_minutes: Duration of appointment
            description: What the appointment is for
        """
        try:
            # Parse and validate datetime
            appointment_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            
            if appointment_dt < datetime.now():
                return "Cannot schedule appointments in the past"
            
            # Mock scheduling logic
            end_time = appointment_dt + timedelta(minutes=duration_minutes)
            
            # Here you would integrate with actual calendar API
            appointment = {
                "id": f"apt_{datetime.now().timestamp()}",
                "start": appointment_dt.isoformat(),
                "end": end_time.isoformat(),
                "description": description
            }
            
            return f"Scheduled: {description} on {date} at {time} for {duration_minutes} minutes"
            
        except ValueError as e:
            return f"Invalid date/time format: {str(e)}"
    
    @function_tool
    async def check_availability(
        self,
        context: RunContext,
        date: str,
        duration_minutes: int = 30
    ) -> str:
        """
        Check availability for a given date.
        
        Args:
            date: Date to check in YYYY-MM-DD format
            duration_minutes: Required duration
        """
        # Mock availability check
        available_slots = [
            "09:00", "10:30", "14:00", "15:30", "16:00"
        ]
        
        return f"Available slots on {date}: {', '.join(available_slots)}"
    
    # File Operations
    @function_tool
    async def read_document(
        self,
        context: RunContext,
        document_name: str
    ) -> str:
        """
        Read a document from the knowledge base.
        
        Args:
            document_name: Name of the document to read
        """
        # Mock document reading
        documents = {
            "privacy_policy": "Our privacy policy ensures...",
            "user_guide": "Welcome to our user guide...",
            "faq": "Frequently asked questions..."
        }
        
        if document_name in documents:
            return documents[document_name]
        else:
            available = ", ".join(documents.keys())
            return f"Document not found. Available: {available}"
    
    # Dynamic Tool Creation
    def create_dynamic_tool(self, field_name: str):
        """Dynamically create a tool for a specific field."""
        
        async def dynamic_handler(context: RunContext, value: str) -> str:
            # Custom logic based on field_name
            return f"Set {field_name} to: {value}"
        
        # Return as a function_tool
        return function_tool(
            dynamic_handler,
            name=f"set_{field_name}",
            description=f"Set the {field_name} field"
        )
    
    async def on_enter(self) -> None:
        """Initialize and greet."""
        # Initialize database if needed
        self._init_database()
        
        await self.session.generate_reply(
            instructions="""Greet the user and briefly mention you can help with:
            - Searching information
            - Scheduling appointments
            - Making API calls
            - Managing data"""
        )
    
    def _init_database(self):
        """Initialize database with sample tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create sample tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                price REAL,
                status TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                product_id INTEGER,
                quantity INTEGER,
                status TEXT,
                created_at TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()


class APIClient:
    """Async API client for external services."""
    
    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
    
    @asynccontextmanager
    async def get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        try:
            yield self.session
        finally:
            pass  # Keep session alive for reuse
    
    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an API request."""
        async with self.get_session() as session:
            url = f"{self.base_url}/{endpoint}"
            
            async with session.request(
                method=method,
                url=url,
                json=data,
                headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()


# MCP Server Integration Example
class MCPToolsAssistant(Agent):
    """Assistant with MCP server tool integration."""
    
    def __init__(self, mcp_url: str = "ws://localhost:8080") -> None:
        super().__init__(
            instructions="I can access tools from the MCP server.",
            # MCP tools are automatically discovered and registered
            mcp_servers=[
                {
                    "url": mcp_url,
                    "name": "main_mcp",
                    "auto_discover": True
                }
            ]
        )
    
    async def on_mcp_tool_call(self, tool_name: str, params: Dict) -> Any:
        """Handle MCP tool calls with custom logic."""
        print(f"MCP tool called: {tool_name} with params: {params}")
        # Add any pre/post processing here
        return await super().on_mcp_tool_call(tool_name, params)


async def entrypoint(ctx: agents.JobContext):
    """Main entry point."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en"),
        llm=openai.LLM(model="gpt-4o-mini", temperature=0.7),
        tts=openai.TTS(voice="echo", speed=1.0),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel()
    )
    
    # Create assistant with tools
    assistant = ToolsAssistant(db_path="assistant.db")
    
    # Optionally add dynamic tools
    dynamic_fields = ["phone_number", "email", "address"]
    for field in dynamic_fields:
        tool = assistant.create_dynamic_tool(field)
        assistant.add_tool(tool)
    
    await session.start(
        room=ctx.room,
        agent=assistant,
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"Tools assistant started")
    
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