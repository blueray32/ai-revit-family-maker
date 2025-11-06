#!/usr/bin/env python3
"""
LiveKit Agents Template Copy Script
====================================
Copies the complete LiveKit Agents context engineering template to a target directory.
"""

import os
import sys
import shutil
from pathlib import Path
import argparse


def copy_template(target_dir: str):
    """
    Copy the LiveKit Agents template to the target directory.
    
    Args:
        target_dir: Path to the target directory
    """
    # Get the template source directory (where this script lives)
    source_dir = Path(__file__).parent
    target_path = Path(target_dir).resolve()
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Files and directories to copy
    items_to_copy = [
        ("CLAUDE.md", "CLAUDE.md"),                    # LiveKit-specific rules
        (".claude", ".claude"),                        # Slash commands
        ("PRPs", "PRPs"),                              # PRP templates and examples
        ("agent.py", "agent.py"),                      # Main agent file (if exists)
        ("pyproject.toml", "pyproject.toml"),         # UV project config (if exists)
        ("Dockerfile", "Dockerfile"),                  # Deployment config (if exists)
        ("livekit.toml", "livekit.toml"),            # LiveKit config (if exists)
        (".env.example", ".env.example"),             # Environment template (if exists)
        ("README.md", "README-template.md"),          # Documentation (renamed)
    ]
    
    copied_items = []
    skipped_items = []
    
    print(f"📦 Copying LiveKit Agents template to: {target_path}")
    print("-" * 50)
    
    for source_name, target_name in items_to_copy:
        source_item = source_dir / source_name
        target_item = target_path / target_name
        
        if source_item.exists():
            try:
                if source_item.is_dir():
                    # Copy directory
                    if target_item.exists():
                        shutil.rmtree(target_item)
                    shutil.copytree(source_item, target_item)
                    copied_items.append(f"📁 {target_name}/")
                else:
                    # Copy file
                    shutil.copy2(source_item, target_item)
                    copied_items.append(f"📄 {target_name}")
            except Exception as e:
                skipped_items.append(f"❌ {target_name}: {str(e)}")
        else:
            # Item doesn't exist in template, skip silently unless critical
            if source_name in ["CLAUDE.md", ".claude", "PRPs", "README.md"]:
                skipped_items.append(f"⚠️  {source_name} (not found - critical file)")
    
    # Print results
    print("\n✅ Successfully copied:")
    for item in copied_items:
        print(f"  {item}")
    
    if skipped_items:
        print("\n⚠️  Skipped items:")
        for item in skipped_items:
            print(f"  {item}")
    
    # Create initial project structure if needed
    create_initial_structure(target_path)
    
    print("\n" + "=" * 50)
    print("🎉 LiveKit Agents template copied successfully!")
    print("\n📋 Next steps:")
    print("  1. cd " + str(target_path))
    print("  2. cp .env.example .env.local (and add your API keys)")
    print("  3. uv init (if starting fresh)")
    print("  4. uv add livekit-agents livekit-plugins-openai livekit-plugins-deepgram")
    print("  5. Create PRPs/INITIAL.md with your feature requirements")
    print("  6. /generate-livekit-prp PRPs/INITIAL.md")
    print("  7. /execute-livekit-prp PRPs/your-feature.md")
    print("\n💡 Quick test:")
    print("  uv run python agent.py console")
    print("\n📚 Documentation:")
    print("  - See README-template.md for complete PRP workflow")
    print("  - See CLAUDE.md for LiveKit-specific patterns")
    print("  - Check PRPs/examples/ for working code examples")
    print("\n🚀 Deploy to LiveKit Cloud:")
    print("  lk agent deploy")
    

def create_initial_structure(target_path: Path):
    """
    Create initial project structure if files don't exist.
    
    Args:
        target_path: Path to the target directory
    """
    # Create basic agent.py if it doesn't exist
    agent_file = target_path / "agent.py"
    if not agent_file.exists():
        agent_content = '''"""
LiveKit Voice Agent
==================
Basic agent implementation. Replace with your actual agent code.
"""

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, deepgram, silero, noise_cancellation

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice AI assistant."
        )
    
    async def on_enter(self):
        await self.session.generate_reply(
            instructions="Greet the user and offer assistance."
        )


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="echo"),
        vad=silero.VAD.load(),
        turn_detection="semantic"
    )
    
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
'''
        agent_file.write_text(agent_content)
        print("  ✨ Created agent.py starter file")
    
    # Create .env.example if it doesn't exist
    env_file = target_path / ".env.example"
    if not env_file.exists():
        env_content = """# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# AI Provider Keys
OPENAI_API_KEY=your-openai-key
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key  # Optional
ELEVENLABS_API_KEY=your-elevenlabs-key  # Optional

# Optional: Archon MCP Server
ARCHON_MCP_URL=ws://localhost:8080
"""
        env_file.write_text(env_content)
        print("  ✨ Created .env.example file")
    
    # Create pyproject.toml if it doesn't exist
    pyproject_file = target_path / "pyproject.toml"
    if not pyproject_file.exists():
        pyproject_content = '''[project]
name = "livekit-voice-agent"
version = "0.1.0"
description = "Voice AI agent built with LiveKit"
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
    "livekit-agents>=1.0.0",
    "livekit-plugins-openai>=1.0.0",
    "livekit-plugins-deepgram>=1.0.0",
    "livekit-plugins-silero>=1.0.0",
    "livekit-plugins-turn-detector>=1.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
'''
        pyproject_file.write_text(pyproject_content)
        print("  ✨ Created pyproject.toml")
    
    # Create Dockerfile if it doesn't exist
    dockerfile = target_path / "Dockerfile"
    if not dockerfile.exists():
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies
RUN uv sync --frozen || uv sync

# Copy application code
COPY . .

# Run the agent
CMD ["uv", "run", "python", "agent.py"]
'''
        dockerfile.write_text(dockerfile_content)
        print("  ✨ Created Dockerfile")
    
    # Create livekit.toml if it doesn't exist
    livekit_toml = target_path / "livekit.toml"
    if not livekit_toml.exists():
        livekit_content = '''[agent]
job_type = "room"
worker_type = "agent"

[agent.prewarm]
count = 1  # Number of warm instances to maintain

[agent.scaling]
min_workers = 1
max_workers = 10
'''
        livekit_toml.write_text(livekit_content)
        print("  ✨ Created livekit.toml")
    
    # Create INITIAL.md example if PRPs directory exists
    prps_dir = target_path / "PRPs"
    if prps_dir.exists():
        initial_file = prps_dir / "INITIAL.md"
        if not initial_file.exists():
            initial_content = '''# Initial Feature Request

## Goal
Build a customer service voice agent that can:
- Answer product questions
- Check order status
- Schedule appointments
- Escalate to human agents when needed

## Requirements

### Functional Requirements
- Natural conversation flow with interruption handling
- Access to product database
- Integration with calendar system
- Multi-agent handoff capability

### Voice Configuration
- Professional, friendly tone
- Clear speech optimized for phone calls
- Support for English and Spanish

### Tools Needed
- `check_order_status`: Look up order by ID
- `search_products`: Find products by query
- `schedule_appointment`: Book calendar slots
- `escalate_to_human`: Transfer to live agent

## Success Criteria
- Response time < 1 second
- Successful tool execution > 95%
- Natural conversation flow
- Smooth agent handoffs

## Additional Context
- Existing database API at https://api.example.com
- Calendar system uses Google Calendar API
- Human agents available 9am-5pm EST
'''
            initial_file.write_text(initial_content)
            print("  ✨ Created PRPs/INITIAL.md example")


def main():
    parser = argparse.ArgumentParser(
        description="Copy LiveKit Agents context engineering template to a target directory"
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="Target directory path (required)"
    )
    parser.add_argument(
        "--help-extended",
        action="store_true",
        help="Show extended help with examples"
    )
    
    args = parser.parse_args()
    
    if args.help_extended:
        print("""
LiveKit Agents Template Copy Script - Extended Help
===================================================

This script copies the complete LiveKit Agents context engineering template
to your project directory, including:

✅ What gets copied:
  - CLAUDE.md: LiveKit-specific AI assistant rules
  - .claude/commands/: Custom slash commands for PRP generation
  - PRPs/: Templates, examples, and AI documentation
  - Configuration files: Dockerfile, livekit.toml, etc.
  - Example agent implementations
  - README.md → README-template.md (renamed to avoid conflicts)

📋 Usage Examples:

  # Copy to current directory
  python copy_template.py .
  
  # Copy to new project
  python copy_template.py ~/projects/my-voice-agent
  
  # Copy to relative path
  python copy_template.py ../voice-assistant

🔄 PRP Framework Workflow:

  Step 1: Create your requirements
    Create PRPs/INITIAL.md with your feature description
  
  Step 2: Generate PRP
    /generate-livekit-prp PRPs/INITIAL.md
  
  Step 3: Execute PRP
    /execute-livekit-prp PRPs/generated-feature.md

🚀 Quick Start After Copying:

  1. Set up environment:
     cd <target-directory>
     cp .env.example .env.local
     # Add your API keys to .env.local
  
  2. Install dependencies:
     uv init (if new project)
     uv add livekit-agents livekit-plugins-openai livekit-plugins-deepgram
  
  3. Test your agent:
     uv run python agent.py console
  
  4. Deploy to LiveKit Cloud:
     lk agent deploy

📚 Resources:
  - LiveKit Docs: https://docs.livekit.io/agents/
  - GitHub Examples: https://github.com/livekit/agents
  - Template Updates: Check the source repository
        """)
        sys.exit(0)
    
    if not args.target:
        print("Error: Target directory is required")
        print("\nUsage: python copy_template.py <target-directory>")
        print("\nExamples:")
        print("  python copy_template.py .")
        print("  python copy_template.py ~/projects/my-agent")
        print("\nFor extended help: python copy_template.py --help-extended")
        sys.exit(1)
    
    try:
        copy_template(args.target)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()