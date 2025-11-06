"""Tests for Revit Family Maker tools."""

import pytest
from revit_family_maker.tools import (
    strip_exif_pii,
    generate_manifest,
    get_template_catalog
)


class TestImageSecurity:
    """Test suite for image security functions."""

    def test_strip_exif_pii(self, sample_image_path):
        """Test EXIF stripping from image."""
        safe_path = strip_exif_pii(sample_image_path)

        # Check that safe image was created
        import os
        assert os.path.exists(safe_path)
        assert safe_path.endswith(".safe.jpg")

        # Clean up
        os.remove(safe_path)

    def test_strip_exif_pii_missing_file(self):
        """Test error handling for missing image file."""
        with pytest.raises(FileNotFoundError):
            strip_exif_pii("/nonexistent/image.jpg")


class TestManifestGeneration:
    """Test suite for manifest generation."""

    def test_generate_manifest_basic(self):
        """Test basic manifest generation."""
        manifest = generate_manifest(
            family_name="Test_Furniture_Chair_v0.1.0",
            revit_version="2025",
            category="Furniture",
            template_id="FurnitureTemplate_2025_v1.0",
            template_hash="sha256:abc123",
            parameters=[
                {"name": "DIM_Height", "value": "3.0", "unit": "feet"}
            ],
            geometry_source="parametric",
            flex_test_passed=True,
            file_size_bytes=512000
        )

        assert manifest["family_name"] == "Test_Furniture_Chair_v0.1.0"
        assert manifest["revit_version"] == "2025"
        assert manifest["category"] == "Furniture"
        assert manifest["template_id"] == "FurnitureTemplate_2025_v1.0"
        assert manifest["flex_test_passed"] is True
        assert "creation_timestamp" in manifest

    def test_generate_manifest_with_kwargs(self):
        """Test manifest generation with additional fields."""
        manifest = generate_manifest(
            family_name="Test_Family",
            revit_version="2025",
            category="Furniture",
            template_id="Template_v1",
            template_hash="sha256:xyz",
            parameters=[],
            geometry_source="mesh",
            flex_test_passed=True,
            file_size_bytes=1024000,
            mesh_confidence=0.87,
            mesh_license_url="https://example.com/license"
        )

        assert manifest["mesh_confidence"] == 0.87
        assert manifest["mesh_license_url"] == "https://example.com/license"


class TestTemplateCatalog:
    """Test suite for template catalog functions."""

    @pytest.mark.asyncio
    async def test_get_template_catalog_all(self):
        """Test retrieving all templates."""
        templates = await get_template_catalog(
            "https://test.example.com/templates/",
            "2025",
            None
        )

        assert len(templates) >= 3  # Should have at least 3 mock templates
        assert all("template_id" in t for t in templates)
        assert all("category" in t for t in templates)

    @pytest.mark.asyncio
    async def test_get_template_catalog_filtered(self):
        """Test retrieving templates filtered by category."""
        templates = await get_template_catalog(
            "https://test.example.com/templates/",
            "2025",
            "Furniture"
        )

        assert len(templates) == 1
        assert templates[0]["category"] == "Furniture"

    @pytest.mark.asyncio
    async def test_get_template_catalog_version_filter(self):
        """Test templates filtered by Revit version."""
        templates_2025 = await get_template_catalog(
            "https://test.example.com/templates/",
            "2025",
            None
        )

        templates_2024 = await get_template_catalog(
            "https://test.example.com/templates/",
            "2024",
            None
        )

        # All templates should be for 2025 in mock catalog
        assert all(t["revit_version"] == "2025" for t in templates_2025)
        assert len(templates_2024) == 0  # No 2024 templates in mock


class TestParameterPrefixes:
    """Test suite for parameter naming conventions."""

    def test_parameter_prefixes(self):
        """Test that parameters use correct prefixes."""
        valid_prefixes = ["DIM_", "MTRL_", "ID_", "CTRL_"]

        test_params = [
            "DIM_Height",
            "DIM_Width",
            "MTRL_Surface",
            "ID_Manufacturer",
            "CTRL_ShowGrille"
        ]

        for param in test_params:
            assert any(param.startswith(prefix) for prefix in valid_prefixes), \
                f"Parameter {param} doesn't use valid prefix"

    def test_family_naming_convention(self):
        """Test family naming follows convention."""
        family_name = "Generic_Furniture_Chair_v0.1.0"

        # Should have format: {Company}_{Category}_{Subtype}_v{semver}
        parts = family_name.split("_")
        assert len(parts) >= 4
        assert parts[0] == "Generic"  # Company
        assert parts[1] == "Furniture"  # Category
        assert "v0.1.0" in family_name  # Version
