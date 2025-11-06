"""Pytest configuration and fixtures for Revit Family Maker tests."""

import pytest
from pathlib import Path
from revit_family_maker.dependencies import RevitAgentDependencies


@pytest.fixture
def test_deps() -> RevitAgentDependencies:
    """Create test dependencies with mock credentials."""
    return RevitAgentDependencies(
        aps_client_id="test_client_id",
        aps_client_secret="test_client_secret",
        aps_activity_name="TestActivity",
        aps_bundle_alias="test",
        template_catalog_url="https://test.example.com/templates/",
        output_bucket="/tmp/test_output",
        image_to_3d_api_key="test_3d_api_key",
        image_to_3d_provider="promeai",
        session_id="test-session-123"
    )


@pytest.fixture
def sample_image_path(tmp_path) -> Path:
    """Create a sample test image."""
    from PIL import Image

    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    image_path = tmp_path / "test_image.jpg"
    img.save(image_path)

    return str(image_path)


@pytest.fixture
def mock_aps_token() -> str:
    """Mock APS OAuth token."""
    return "mock_aps_token_abc123"
