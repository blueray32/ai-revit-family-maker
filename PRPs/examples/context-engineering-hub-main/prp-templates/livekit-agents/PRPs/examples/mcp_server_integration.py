"""
MCP Server Integration Example
==============================
Demonstrates integration with Model Context Protocol (MCP) servers
for advanced tool capabilities and external service connections.
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
import json
import asyncio
from typing import Dict, Any, List, Optional
import aiohttp
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


class MCPIntegratedAgent(Agent):
    """Agent with MCP server integration for extended capabilities."""
    
    def __init__(self, mcp_servers: List[Dict[str, str]] = None):
        self.mcp_servers = mcp_servers or []
        self.mcp_connections = {}
        
        super().__init__(
            instructions="""You are an advanced assistant with access to MCP servers.
            You can query databases, access APIs, and use specialized tools through MCP.
            Always verify tool availability before attempting to use them."""
        )
    
    async def connect_mcp_servers(self):
        """Establish connections to configured MCP servers."""
        for server in self.mcp_servers:
            try:
                connection = await self.connect_to_mcp(
                    server["url"],
                    server["name"]
                )
                self.mcp_connections[server["name"]] = connection
                print(f"Connected to MCP server: {server['name']}")
            except Exception as e:
                print(f"Failed to connect to {server['name']}: {e}")
    
    async def connect_to_mcp(self, url: str, name: str) -> Dict:
        """Connect to a single MCP server."""
        # In production, use actual MCP client library
        # This is a mock implementation
        return {
            "url": url,
            "name": name,
            "connected": True,
            "available_tools": await self.discover_mcp_tools(url)
        }
    
    async def discover_mcp_tools(self, server_url: str) -> List[Dict]:
        """Discover available tools from MCP server."""
        # Mock tool discovery - in production, query MCP server
        return [
            {
                "name": "database_query",
                "description": "Query the database",
                "parameters": ["query", "database"]
            },
            {
                "name": "web_search",
                "description": "Search the web",
                "parameters": ["query", "max_results"]
            },
            {
                "name": "document_analysis",
                "description": "Analyze documents",
                "parameters": ["document_id", "analysis_type"]
            }
        ]
    
    @function_tool
    async def execute_mcp_tool(
        self,
        context: RunContext,
        server_name: str,
        tool_name: str,
        parameters: str
    ) -> str:
        """
        Execute a tool on an MCP server.
        
        Args:
            server_name: Name of the MCP server
            tool_name: Name of the tool to execute
            parameters: JSON string of tool parameters
        """
        if server_name not in self.mcp_connections:
            return f"MCP server '{server_name}' not connected"
        
        try:
            params = json.loads(parameters)
            
            # Mock MCP tool execution - replace with actual MCP client call
            result = await self._mock_mcp_execution(
                server_name,
                tool_name,
                params
            )
            
            return json.dumps(result)
        except json.JSONDecodeError:
            return "Invalid parameters format"
        except Exception as e:
            return f"MCP tool execution failed: {str(e)}"
    
    async def _mock_mcp_execution(
        self,
        server: str,
        tool: str,
        params: Dict
    ) -> Dict:
        """Mock MCP tool execution."""
        # Simulate different tool responses
        if tool == "database_query":
            return {
                "success": True,
                "results": [
                    {"id": 1, "name": "Item 1"},
                    {"id": 2, "name": "Item 2"}
                ],
                "count": 2
            }
        elif tool == "web_search":
            return {
                "success": True,
                "results": [
                    {"title": "Result 1", "url": "https://example.com/1"},
                    {"title": "Result 2", "url": "https://example.com/2"}
                ]
            }
        elif tool == "document_analysis":
            return {
                "success": True,
                "analysis": {
                    "summary": "Document summary here",
                    "key_points": ["Point 1", "Point 2"],
                    "sentiment": "neutral"
                }
            }
        else:
            return {"success": False, "error": "Unknown tool"}
    
    @function_tool
    async def list_mcp_tools(self, context: RunContext, server_name: str = None) -> str:
        """
        List available tools from MCP servers.
        
        Args:
            server_name: Optional server name to filter by
        """
        tools_list = []
        
        for name, connection in self.mcp_connections.items():
            if server_name and name != server_name:
                continue
            
            server_tools = {
                "server": name,
                "tools": connection.get("available_tools", [])
            }
            tools_list.append(server_tools)
        
        return json.dumps(tools_list, indent=2)
    
    @function_tool
    async def query_knowledge_base(
        self,
        context: RunContext,
        query: str,
        source: str = "all"
    ) -> str:
        """
        Query the knowledge base through MCP.
        
        Args:
            query: Search query
            source: Knowledge source to search (all, docs, code, etc.)
        """
        # Use MCP server for knowledge base queries
        if "knowledge" in self.mcp_connections:
            result = await self.execute_mcp_tool(
                context,
                "knowledge",
                "search",
                json.dumps({"query": query, "source": source})
            )
            return result
        else:
            return "Knowledge base MCP server not available"
    
    async def on_enter(self) -> None:
        """Initialize MCP connections and greet user."""
        # Connect to MCP servers
        await self.connect_mcp_servers()
        
        # List available capabilities
        tools_count = sum(
            len(conn.get("available_tools", []))
            for conn in self.mcp_connections.values()
        )
        
        await self.session.generate_reply(
            instructions=f"""Greet the user and mention you have access to {tools_count} tools
            through {len(self.mcp_connections)} MCP servers. Offer to help with:
            - Database queries
            - Web searches
            - Document analysis
            - Knowledge base access"""
        )
    
    async def on_exit(self) -> None:
        """Clean up MCP connections."""
        for name, connection in self.mcp_connections.items():
            # Close MCP connections properly
            print(f"Closing MCP connection: {name}")


class ArchonMCPAgent(Agent):
    """Agent specifically integrated with Archon MCP server."""
    
    def __init__(self):
        super().__init__(
            instructions="""You are integrated with the Archon MCP server.
            You can perform RAG queries, search code examples, and access documentation.
            Use these capabilities to provide accurate, context-aware assistance."""
        )
        
        self.archon_connected = False
    
    @function_tool
    async def archon_rag_query(
        self,
        context: RunContext,
        query: str,
        source_domain: str = None,
        match_count: int = 5
    ) -> str:
        """
        Perform a RAG query using Archon MCP.
        
        Args:
            query: Search query
            source_domain: Optional domain filter
            match_count: Number of results to return
        """
        # Simulate Archon MCP RAG query
        results = {
            "success": True,
            "results": [
                {
                    "content": f"Result 1 for: {query}",
                    "relevance": 0.95,
                    "source": source_domain or "general"
                },
                {
                    "content": f"Result 2 for: {query}",
                    "relevance": 0.87,
                    "source": source_domain or "general"
                }
            ][:match_count]
        }
        
        return json.dumps(results, indent=2)
    
    @function_tool
    async def archon_code_search(
        self,
        context: RunContext,
        query: str,
        language: str = None,
        match_count: int = 3
    ) -> str:
        """
        Search for code examples using Archon MCP.
        
        Args:
            query: Code search query
            language: Programming language filter
            match_count: Number of examples to return
        """
        # Simulate Archon code search
        examples = {
            "success": True,
            "examples": [
                {
                    "title": f"Example: {query}",
                    "language": language or "python",
                    "code": "def example():\n    pass",
                    "description": "Example implementation"
                }
            ][:match_count]
        }
        
        return json.dumps(examples, indent=2)
    
    @function_tool
    async def archon_create_task(
        self,
        context: RunContext,
        project_id: str,
        title: str,
        description: str = "",
        assignee: str = "AI IDE Agent"
    ) -> str:
        """
        Create a task in Archon project management.
        
        Args:
            project_id: Project UUID
            title: Task title
            description: Task description
            assignee: Who will work on the task
        """
        # Simulate task creation
        task = {
            "success": True,
            "task_id": f"task-{hash(title) % 10000:04d}",
            "project_id": project_id,
            "title": title,
            "status": "todo",
            "assignee": assignee
        }
        
        return json.dumps(task, indent=2)
    
    async def on_enter(self) -> None:
        """Connect to Archon and greet."""
        # Simulate Archon connection
        self.archon_connected = True
        
        await self.session.generate_reply(
            instructions="""Greet the user and mention you're connected to Archon MCP.
            You can help with:
            - Searching documentation and code
            - Creating and managing tasks
            - Performing RAG queries for accurate information"""
        )


class MultiMCPOrchestrator(Agent):
    """Agent that orchestrates multiple MCP servers for complex tasks."""
    
    def __init__(self):
        self.mcp_registry = {
            "database": "ws://localhost:8001",
            "knowledge": "ws://localhost:8002",
            "archon": "ws://localhost:8003",
            "tools": "ws://localhost:8004"
        }
        
        super().__init__(
            instructions="""You orchestrate multiple MCP servers to accomplish complex tasks.
            You can combine data from different sources and coordinate multi-step operations."""
        )
    
    @function_tool
    async def orchestrate_workflow(
        self,
        context: RunContext,
        workflow_type: str,
        parameters: str
    ) -> str:
        """
        Orchestrate a multi-step workflow across MCP servers.
        
        Args:
            workflow_type: Type of workflow (research, analysis, automation)
            parameters: JSON parameters for the workflow
        """
        try:
            params = json.loads(parameters)
            
            if workflow_type == "research":
                return await self._research_workflow(params)
            elif workflow_type == "analysis":
                return await self._analysis_workflow(params)
            elif workflow_type == "automation":
                return await self._automation_workflow(params)
            else:
                return f"Unknown workflow type: {workflow_type}"
                
        except Exception as e:
            return f"Workflow failed: {str(e)}"
    
    async def _research_workflow(self, params: Dict) -> str:
        """Execute research workflow across MCP servers."""
        results = {
            "workflow": "research",
            "steps": []
        }
        
        # Step 1: Query knowledge base
        knowledge_result = {
            "step": "knowledge_search",
            "query": params.get("query"),
            "results": ["Finding 1", "Finding 2"]
        }
        results["steps"].append(knowledge_result)
        
        # Step 2: Search code examples
        code_result = {
            "step": "code_search",
            "examples": ["Example 1", "Example 2"]
        }
        results["steps"].append(code_result)
        
        # Step 3: Analyze findings
        analysis_result = {
            "step": "analysis",
            "summary": "Research complete with key findings"
        }
        results["steps"].append(analysis_result)
        
        return json.dumps(results, indent=2)
    
    async def _analysis_workflow(self, params: Dict) -> str:
        """Execute analysis workflow."""
        return json.dumps({
            "workflow": "analysis",
            "status": "completed",
            "insights": ["Insight 1", "Insight 2"]
        })
    
    async def _automation_workflow(self, params: Dict) -> str:
        """Execute automation workflow."""
        return json.dumps({
            "workflow": "automation",
            "tasks_created": 3,
            "status": "initiated"
        })


async def mcp_entrypoint(ctx: agents.JobContext):
    """Entry point for MCP-integrated agents."""
    
    logger.info(f"Agent started in room: {ctx.room.name}")
    
    # Configure MCP servers
    mcp_servers = [
        {"name": "main", "url": "ws://localhost:8080"},
        {"name": "knowledge", "url": "ws://localhost:8081"},
        {"name": "tools", "url": "ws://localhost:8082"}
    ]
    
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="en"),
        llm=openai.LLM(model="gpt-4o-mini", temperature=0.7),
        tts=openai.TTS(voice="echo", speed=1.0),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel()
    )
    
    # Create MCP-integrated agent
    agent = MCPIntegratedAgent(mcp_servers=mcp_servers)
    
    await session.start(
        room=ctx.room,
        agent=agent,
        # room_input_options=RoomInputOptions(
            # Enable noise cancellation
            # noise_cancellation=noise_cancellation.BVC(),
            # For telephony, use: noise_cancellation.BVCTelephony()
        # ),
        room_output_options=RoomOutputOptions(transcription_enabled=True),
    )
    
    logger.info(f"MCP-integrated agent started with {len(mcp_servers)} servers")
    
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
    cli.run_app(WorkerOptions(entrypoint_fnc=mcp_entrypoint, prewarm_fnc=prewarm))