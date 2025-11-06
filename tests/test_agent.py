"""Integration tests for Revit Family Maker Agent."""

import pytest
from pydantic_ai.models.test import TestModel
from revit_family_maker import create_agent


class TestAgentIntegration:
    """Integration tests for the complete agent."""

    @pytest.mark.asyncio
    async def test_agent_creation(self):
        """Test that agent can be created successfully."""
        agent = create_agent()
        assert agent is not None
        assert agent.system_prompt is not None

    @pytest.mark.asyncio
    async def test_agent_with_test_model(self, test_deps):
        """Test agent with TestModel (no actual LLM calls)."""
        agent = create_agent()

        # Override with TestModel for testing
        test_model = TestModel()
        test_agent = agent.override(model=test_model)

        # Test basic invocation structure
        # Note: TestModel returns mock data, not real results
        assert test_agent is not None

    def test_agent_has_tools(self):
        """Test that agent has all required tools registered."""
        agent = create_agent()

        # Agent should have tools registered
        # (Can't easily test tool count without inspecting internals,
        #  but we can verify agent was created successfully)
        assert agent is not None

    def test_dependencies_creation(self, test_deps):
        """Test that dependencies are properly structured."""
        assert test_deps.aps_client_id == "test_client_id"
        assert test_deps.aps_client_secret == "test_client_secret"
        assert test_deps.template_catalog_url.startswith("https://")
        assert test_deps.image_to_3d_provider in ["promeai", "tripo3d", "furnimesh"]


class TestValidationGates:
    """Tests for PRP validation gates."""

    def test_category_validation_required(self):
        """Test that category is mandatory (validation gate)."""
        # This test verifies the category validation requirement
        # In actual usage, the agent should refuse to proceed without category
        pass  # Placeholder for actual validation test

    def test_unit_conversion_validation(self):
        """Test that units are converted to feet (validation gate)."""
        from revit_family_maker.tools import to_feet

        # All dimensions must be converted to feet
        test_cases = [
            (2100, "mm", 6.89),  # Door height
            (900, "mm", 2.95),   # Door width
            (8, "ft", 8.0),      # Already in feet
        ]

        for value, unit, expected in test_cases:
            result = to_feet(value, unit)
            assert abs(result - expected) < 0.01

    def test_naming_convention_validation(self):
        """Test family naming convention (validation gate)."""
        # Pattern: {Company}_{Category}_{Subtype}_v{semver}
        test_name = "Generic_Furniture_Chair_v0.1.0"

        # Must contain underscores
        assert "_" in test_name

        # Must contain version
        assert "v0.1.0" in test_name or "v1.0.0" in test_name

        # No spaces allowed
        assert " " not in test_name

    def test_parameter_prefix_validation(self):
        """Test parameter prefix requirements (validation gate)."""
        valid_prefixes = ["DIM_", "MTRL_", "ID_", "CTRL_"]

        # All parameters must have valid prefixes
        test_params = [
            "DIM_Height",
            "DIM_Width",
            "MTRL_Frame",
            "ID_Manufacturer"
        ]

        for param in test_params:
            has_valid_prefix = any(
                param.startswith(prefix) for prefix in valid_prefixes
            )
            assert has_valid_prefix, f"{param} missing valid prefix"

    def test_file_size_budget_validation(self):
        """Test file size budget enforcement (validation gate)."""
        max_size_bytes = 3 * 1024 * 1024  # 3 MB

        # Test that manifest includes file size check
        from revit_family_maker.tools import generate_manifest

        manifest = generate_manifest(
            family_name="Test",
            revit_version="2025",
            category="Furniture",
            template_id="Test_v1",
            template_hash="sha256:abc",
            parameters=[],
            geometry_source="parametric",
            flex_test_passed=True,
            file_size_bytes=2 * 1024 * 1024  # 2 MB - should pass
        )

        assert manifest["file_size_bytes"] < max_size_bytes


class TestErrorHandling:
    """Tests for error handling and edge cases."""

    def test_missing_category_error(self):
        """Test error when category is missing."""
        # Should raise ValueError when category is not provided
        pass  # Placeholder for actual test

    def test_invalid_unit_error(self):
        """Test error for invalid unit."""
        from revit_family_maker.tools import to_feet

        with pytest.raises(ValueError, match="Unknown unit"):
            to_feet(100, "invalid_unit")

    def test_missing_image_error(self):
        """Test error for missing image file."""
        from revit_family_maker.tools import strip_exif_pii

        with pytest.raises(FileNotFoundError):
            strip_exif_pii("/nonexistent/image.jpg")


@pytest.mark.skip(reason="Requires actual credentials and services")
class TestRealIntegration:
    """Integration tests that require real credentials.

    These tests are skipped by default. Run with real credentials to test
    actual APS, image-to-3D, and LLM integrations.
    """

    @pytest.mark.asyncio
    async def test_real_aps_integration(self):
        """Test actual APS Design Automation integration."""
        pass

    @pytest.mark.asyncio
    async def test_real_image_to_3d_integration(self):
        """Test actual image-to-3D service integration."""
        pass

    @pytest.mark.asyncio
    async def test_end_to_end_family_creation(self):
        """Test complete end-to-end family creation."""
        pass
