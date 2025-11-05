"""Settings module for Revit Family Maker Agent.

Loads and validates environment variables using pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from dotenv import load_dotenv
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider")
    llm_api_key: str = Field(..., description="API key for LLM")
    llm_model: str = Field(default="gpt-4", description="Model name")
    llm_base_url: str = Field(default="https://api.openai.com/v1")

    # APS/Forge Configuration
    aps_client_id: str = Field(..., description="Autodesk Platform Services client ID")
    aps_client_secret: str = Field(..., description="APS client secret")
    aps_region: str = Field(default="us-east", description="APS region (us-east or eu-west)")
    aps_da_nickname: str = Field(..., description="Design Automation nickname")
    aps_da_activity: str = Field(..., description="DA activity name")
    aps_da_bundle_alias: str = Field(default="prod", description="AppBundle alias")
    aps_template_url: str = Field(..., description="Family template catalog URL")

    # Storage Configuration
    output_bucket_or_path: str = Field(..., description="Output location for .rfa files")

    # Image-to-3D Service
    image_to_3d_provider: str = Field(default="promeai", description="PromeAI|Tripo3D|FurniMesh")
    image_to_3d_api_key: str = Field(..., description="API key for 3D generation")

    # Optional: Vector Search
    vector_db_url: str | None = Field(default=None, description="PostgreSQL + pgvector URL")

    # Performance & Limits
    max_parallel_jobs: int = Field(default=5, description="Max concurrent APS jobs")
    file_size_budget_mb: int = Field(default=3, description="Max .rfa file size")

    # Company Defaults
    company_prefix: str = Field(default="Generic", description="Default company prefix")
    default_revit_version: str = Field(default="2025", description="2024|2025")

    # Telemetry (opt-in)
    telemetry_enabled: bool = Field(default=False, description="Enable telemetry")
    telemetry_endpoint: str | None = Field(default=None, description="Telemetry endpoint")


def load_settings() -> Settings:
    """Load and validate settings from environment."""
    load_dotenv()
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "api_key" in str(e).lower():
            error_msg += "\n\n🔍 Check your .env file:"
            error_msg += "\n  - LLM_API_KEY is required"
            error_msg += "\n  - APS_CLIENT_ID and APS_CLIENT_SECRET are required"
            error_msg += "\n  - IMAGE_TO_3D_API_KEY is required"
            error_msg += "\n\nCopy .env.example to .env and fill in your credentials."
        raise ValueError(error_msg) from e


def get_llm_model():
    """Get configured LLM model for agent."""
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)


if __name__ == "__main__":
    # Test settings loading
    try:
        settings = load_settings()
        print("✅ All settings loaded successfully")
        print(f"  LLM Model: {settings.llm_model}")
        print(f"  APS Activity: {settings.aps_da_activity}")
        print(f"  Output Path: {settings.output_bucket_or_path}")
        print(f"  Company Prefix: {settings.company_prefix}")
    except ValueError as e:
        print(f"❌ Configuration Error:\n{e}")
