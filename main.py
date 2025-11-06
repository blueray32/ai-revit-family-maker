#!/usr/bin/env python3
"""Main entry point for Revit Family Maker Agent CLI."""

import asyncio
import sys
from pathlib import Path

from revit_family_maker import create_agent, create_dependencies


async def main():
    """Run the Revit Family Maker Agent CLI."""
    print("🏗️  Revit Family Maker Agent")
    print("=" * 60)
    print("AI-powered Revit family generation from text and images")
    print("=" * 60)
    print()

    # Check for command line arguments
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        # Interactive mode
        user_prompt = input("💬 Describe the family you want to create: ").strip()

    if not user_prompt:
        print("❌ No input provided. Please provide a description.")
        sys.exit(1)

    print(f"\n📝 Request: {user_prompt}\n")

    try:
        # Create agent and dependencies
        agent = create_agent()
        deps = create_dependencies()

        # Run agent
        print("🔧 Generating family...\n")
        result = await agent.run(user_prompt, deps=deps)

        # Display result
        print("✅ Family generation complete!")
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result.data if hasattr(result, 'data') else str(result))
        print("=" * 60)

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Copied .env.example to .env")
        print("  2. Filled in all required API keys")
        print("  3. Configured APS credentials")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
