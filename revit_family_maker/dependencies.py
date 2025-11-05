"""Dependencies module for Revit Family Maker Agent.

Defines the dependency dataclass for dependency injection.
"""

from dataclasses import dataclass


@dataclass
class RevitAgentDependencies:
    """Dependencies for Revit family maker agent.

    Injected into tool context via RunContext[RevitAgentDependencies].
    All sensitive data loaded from environment variables.
    """

    # APS Configuration
    aps_client_id: str
    aps_client_secret: str
    aps_activity_name: str
    aps_bundle_alias: str
    template_catalog_url: str

    # Storage
    output_bucket: str

    # Image-to-3D Service
    image_to_3d_api_key: str
    image_to_3d_provider: str

    # Optional session tracking
    session_id: str | None = None
