"""
Template Catalog Management
Manages Revit family templates with metadata, hashing, and cloud storage URLs
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TemplateMetadata:
    """Metadata for a Revit family template"""

    id: str
    category: str
    subcategory: Optional[str] = None
    url: str = ""
    local_path: Optional[str] = None
    hash: str = ""
    revit_version: str = "2025"
    description: str = ""
    default_width: float = 1000.0  # mm
    default_depth: float = 1000.0  # mm
    default_height: float = 1000.0  # mm
    min_width: float = 100.0
    max_width: float = 10000.0
    min_depth: float = 100.0
    max_depth: float = 10000.0
    min_height: float = 100.0
    max_height: float = 10000.0


class TemplateCatalog:
    """Manages the catalog of available Revit templates"""

    def __init__(self, base_url: str = ""):
        self.base_url = base_url.rstrip("/")
        self.templates: Dict[str, TemplateMetadata] = {}
        self._initialize_default_catalog()

    def _initialize_default_catalog(self):
        """Initialize with default template mappings."""

        version_path = "2025"

        def template_url(file_name: str) -> str:
            return f"{self.base_url}/{version_path}/{file_name}"

        default_templates = [
            # Generic Model - fallback for unknown categories
            TemplateMetadata(
                id="generic_model_v1",
                category="Generic Models",
                url=template_url("Generic_Model.rft"),
                description="Generic parametric model template",
                default_width=1000.0,
                default_depth=1000.0,
                default_height=1000.0,
            ),
            # Furniture templates
            TemplateMetadata(
                id="furniture_v1",
                category="Furniture",
                url=template_url("Furniture.rft"),
                description="Furniture family template with standard dimensions",
                default_width=800.0,
                default_depth=800.0,
                default_height=900.0,
                min_width=300.0,
                max_width=3000.0,
            ),
            # Casework
            TemplateMetadata(
                id="casework_v1",
                category="Casework",
                url=template_url("Casework.rft"),
                description="Cabinet and casework template",
                default_width=900.0,
                default_depth=600.0,
                default_height=900.0,
                min_width=300.0,
                max_width=3000.0,
            ),
            # Lighting Fixtures
            TemplateMetadata(
                id="lighting_v1",
                category="Lighting Fixtures",
                url=template_url("Lighting_Fixture.rft"),
                description="Lighting fixture template",
                default_width=300.0,
                default_depth=300.0,
                default_height=400.0,
                min_width=100.0,
                max_width=2000.0,
            ),
            # Specialty Equipment
            TemplateMetadata(
                id="specialty_equipment_v1",
                category="Specialty Equipment",
                url=template_url("Specialty_Equipment.rft"),
                description="Specialty equipment template",
                default_width=1000.0,
                default_depth=1000.0,
                default_height=1500.0,
            ),
            # Plumbing Fixtures
            TemplateMetadata(
                id="plumbing_v1",
                category="Plumbing Fixtures",
                url=template_url("Plumbing_Fixture.rft"),
                description="Plumbing fixture template",
                default_width=600.0,
                default_depth=600.0,
                default_height=800.0,
                min_width=300.0,
                max_width=2000.0,
            ),
            # Electrical Equipment
            TemplateMetadata(
                id="electrical_v1",
                category="Electrical Equipment",
                url=template_url("Electrical_Equipment.rft"),
                description="Electrical equipment template",
                default_width=500.0,
                default_depth=300.0,
                default_height=600.0,
            ),
            # Mechanical Equipment
            TemplateMetadata(
                id="mechanical_v1",
                category="Mechanical Equipment",
                url=template_url("Mechanical_Equipment.rft"),
                description="Mechanical equipment template",
                default_width=1000.0,
                default_depth=800.0,
                default_height=1200.0,
            ),
        ]

        for template in default_templates:
            self.add_template(template)

    def add_template(self, template: TemplateMetadata):
        """Add a template to the catalog"""
        self.templates[template.id] = template

        # Also index by category for easy lookup
        category_key = f"category:{template.category.lower()}"
        if category_key not in self.templates:
            self.templates[category_key] = template

    def get_template(self, template_id: str) -> Optional[TemplateMetadata]:
        """Get template by ID"""
        return self.templates.get(template_id)

    def get_template_by_category(
        self, category: str, revit_version: str = "2025"
    ) -> Optional[TemplateMetadata]:
        """Get template by category name"""
        category_key = f"category:{category.lower()}"
        template = self.templates.get(category_key)

        if template and template.revit_version == revit_version:
            return template

        # Try fuzzy matching
        for tid, tmpl in self.templates.items():
            if not tid.startswith("category:") and tmpl.category.lower() == category.lower():
                if tmpl.revit_version == revit_version:
                    return tmpl

        # Fallback to generic model
        return self.get_template("generic_model_v1")

    def list_templates(
        self, category: Optional[str] = None, revit_version: Optional[str] = None
    ) -> List[TemplateMetadata]:
        """List all templates, optionally filtered"""
        results = []

        for tid, template in self.templates.items():
            # Skip category index keys
            if tid.startswith("category:"):
                continue

            # Apply filters
            if category and template.category.lower() != category.lower():
                continue

            if revit_version and template.revit_version != revit_version:
                continue

            results.append(template)

        return results

    def calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a template file"""
        sha256_hash = hashlib.sha256()
        path = Path(file_path)

        if not path.exists():
            return ""

        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return f"sha256:{sha256_hash.hexdigest()}"

    def update_hashes(self, templates_dir: str):
        """Update hashes for all local templates"""
        templates_path = Path(templates_dir)

        if not templates_path.exists():
            return

        for template in self.templates.values():
            if hasattr(template, "local_path") and template.local_path:
                local_file = templates_path / template.local_path
                if local_file.exists():
                    template.hash = self.calculate_hash(str(local_file))
                    print(f"Updated hash for {template.id}: {template.hash[:16]}...")


# Category mappings for validation and normalization
CATEGORY_MAPPINGS = {
    # Furniture
    "furniture": "Furniture",
    "chair": "Furniture",
    "chairs": "Furniture",
    "table": "Furniture",
    "tables": "Furniture",
    "desk": "Furniture",
    "desks": "Furniture",
    "seating": "Furniture",
    "sofa": "Furniture",
    "couch": "Furniture",
    # Casework
    "casework": "Casework",
    "cabinet": "Casework",
    "cabinets": "Casework",
    "shelving": "Casework",
    "counter": "Casework",
    "counters": "Casework",
    # Lighting
    "lighting": "Lighting Fixtures",
    "light": "Lighting Fixtures",
    "lights": "Lighting Fixtures",
    "lighting fixtures": "Lighting Fixtures",
    "lamp": "Lighting Fixtures",
    "lamps": "Lighting Fixtures",
    # Equipment
    "specialty equipment": "Specialty Equipment",
    "equipment": "Specialty Equipment",
    "appliance": "Specialty Equipment",
    "appliances": "Specialty Equipment",
    # Plumbing
    "plumbing": "Plumbing Fixtures",
    "plumbing fixtures": "Plumbing Fixtures",
    "sink": "Plumbing Fixtures",
    "sinks": "Plumbing Fixtures",
    "toilet": "Plumbing Fixtures",
    "toilets": "Plumbing Fixtures",
    # Electrical
    "electrical": "Electrical Equipment",
    "electrical equipment": "Electrical Equipment",
    # Mechanical
    "mechanical": "Mechanical Equipment",
    "mechanical equipment": "Mechanical Equipment",
    "hvac": "Mechanical Equipment",
    # Generic
    "generic": "Generic Models",
    "generic model": "Generic Models",
    "generic models": "Generic Models",
}


def normalize_category(category: str) -> str:
    """Normalize category name to standard Revit category"""
    if not category:
        return "Generic Models"

    normalized = category.strip().lower()
    return CATEGORY_MAPPINGS.get(normalized, "Generic Models")


# Global catalog instance (initialized with base_url from settings)
_catalog: Optional[TemplateCatalog] = None


def get_catalog(base_url: str = "") -> TemplateCatalog:
    """Get or create the global template catalog"""
    global _catalog
    if _catalog is None:
        _catalog = TemplateCatalog(base_url)
    return _catalog
