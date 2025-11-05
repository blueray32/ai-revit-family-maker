"""Main agent module for Revit Family Maker.

Initializes the agent with tools, prompts, and dependencies.
"""

from pydantic_ai import Agent
from .settings import load_settings, get_llm_model
from .dependencies import RevitAgentDependencies
from .prompts import SYSTEM_PROMPT
from .tools import create_tools


def create_agent() -> Agent:
    """Create and configure the Revit Family Maker agent.

    Returns:
        Configured Agent instance with all tools registered
    """
    # Get LLM model from settings
    model = get_llm_model()

    # Create agent with system prompt and dependency type
    agent = Agent(
        model,
        deps_type=RevitAgentDependencies,
        system_prompt=SYSTEM_PROMPT
    )

    # Register all tools
    create_tools(agent)

    return agent


def create_dependencies() -> RevitAgentDependencies:
    """Create dependencies instance from settings.

    Returns:
        RevitAgentDependencies instance with all config loaded
    """
    settings = load_settings()

    return RevitAgentDependencies(
        aps_client_id=settings.aps_client_id,
        aps_client_secret=settings.aps_client_secret,
        aps_activity_name=settings.aps_da_activity,
        aps_bundle_alias=settings.aps_da_bundle_alias,
        template_catalog_url=settings.aps_template_url,
        output_bucket=settings.output_bucket_or_path,
        image_to_3d_api_key=settings.image_to_3d_api_key,
        image_to_3d_provider=settings.image_to_3d_provider,
        session_id=None
    )


async def run_agent(user_prompt: str, image_path: str | None = None) -> str:
    """Run the agent with a user prompt.

    Args:
        user_prompt: User's natural language request
        image_path: Optional path to reference image

    Returns:
        Agent's response as string
    """
    agent = create_agent()
    deps = create_dependencies()

    # Run agent with user prompt
    result = await agent.run(user_prompt, deps=deps)

    return result.data


if __name__ == "__main__":
    import asyncio

    async def main():
        # Example usage
        print("🚀 Revit Family Maker Agent")
        print("=" * 50)

        prompt = "Create a door 2100mm high by 900mm wide"
        print(f"\nUser: {prompt}\n")

        try:
            response = await run_agent(prompt)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
