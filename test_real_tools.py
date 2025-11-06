"""Direct test of agent tools with real LLM."""

import asyncio
from revit_family_maker import create_agent, create_dependencies

async def test_with_tools():
    print("🧪 Testing Agent with Real OpenAI + Tools")
    print("=" * 70)

    agent = create_agent()
    deps = create_dependencies()

    # Very explicit prompt that should trigger tool call
    prompt = """
    I want to create a Revit door family with the following specifications:
    - Category: Doors (confirmed)
    - Height: 2100mm (convert to feet)
    - Width: 900mm (convert to feet)
    - Revit Version: 2025
    - Company: Generic

    Please use the generate_family_from_prompt tool to create this now.
    Do not ask for confirmation - proceed with generation.
    """

    print(f"📝 Prompt:\n{prompt}\n")
    print("🔧 Running agent with tool access...\n")

    result = await agent.run(prompt, deps=deps)

    print("=" * 70)
    print("✅ AGENT RESPONSE:")
    print("=" * 70)
    # Check if output has data attribute or use string representation
    if hasattr(result, 'data'):
        print(result.data)
    else:
        print(result.output if hasattr(result, 'output') else str(result))
    print("=" * 70)

    # Check for tool usage
    if hasattr(result, 'all_messages'):
        print("\n📊 MESSAGE HISTORY:")
        print("=" * 70)
        for msg in result.all_messages():
            print(f"Role: {msg.role}")
            if hasattr(msg, 'content'):
                print(f"Content: {msg.content[:200]}...")
            print("-" * 70)

if __name__ == "__main__":
    asyncio.run(test_with_tools())
