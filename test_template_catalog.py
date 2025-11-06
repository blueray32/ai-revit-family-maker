#!/usr/bin/env python3
"""
Test the Template Catalog System
Demonstrates template listing, filtering, and category normalization
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from revit_family_maker.templates import (
    get_catalog,
    normalize_category,
    CATEGORY_MAPPINGS,
)
from revit_family_maker.settings import load_settings


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def test_category_normalization():
    """Test category name normalization"""
    print_header("Category Normalization Tests")

    test_cases = [
        "chair",
        "furniture",
        "Cabinet",
        "LIGHTING",
        "sink",
        "hvac",
        "random_category",
    ]

    for category in test_cases:
        normalized = normalize_category(category)
        print(f"  {category:20} → {normalized}")


def test_template_listing():
    """Test template catalog listing"""
    print_header("Template Catalog Listing")

    # Load settings
    try:
        settings = load_settings()
        base_url = settings.aps_template_url
    except Exception:
        base_url = "https://example.com/templates/"
        print(f"⚠️  Using default URL: {base_url}")
        print("   (Set APS_TEMPLATE_URL in .env for production)\n")

    # Get catalog
    catalog = get_catalog(base_url)

    # List all templates
    all_templates = catalog.list_templates()
    print(f"Total templates: {len(all_templates)}\n")

    for template in all_templates:
        print(f"  📄 {template.id}")
        print(f"     Category: {template.category}")
        if template.subcategory:
            print(f"     Subcategory: {template.subcategory}")
        print(f"     Version: {template.revit_version}")
        print(f"     URL: {template.url}")
        print(f"     Dimensions: {template.default_width}×{template.default_depth}×{template.default_height} mm")
        print()


def test_filtered_listing():
    """Test filtered template listing"""
    print_header("Filtered Template Listing")

    base_url = "https://example.com/templates/"
    catalog = get_catalog(base_url)

    # Test category filter
    print("Furniture templates (2024):")
    furniture_templates = catalog.list_templates(category="Furniture", revit_version="2024")

    for template in furniture_templates:
        print(f"  • {template.id} - {template.description}")

    print(f"\nFound {len(furniture_templates)} furniture template(s)")

    # Test category lookup
    print("\n" + "-" * 60)
    print("Get template by category:")

    template = catalog.get_template_by_category("Furniture", "2024")
    if template:
        print(f"  Found: {template.id}")
        print(f"  Description: {template.description}")
        print(f"  Default dimensions: {template.default_width}×{template.default_depth}×{template.default_height} mm")


def test_category_mappings():
    """Test all category mappings"""
    print_header("Category Mapping Reference")

    print("All supported category keywords:\n")

    # Group by target category
    mappings_by_target = {}
    for keyword, target in CATEGORY_MAPPINGS.items():
        if target not in mappings_by_target:
            mappings_by_target[target] = []
        mappings_by_target[target].append(keyword)

    for target, keywords in sorted(mappings_by_target.items()):
        print(f"  {target}:")
        for keyword in sorted(keywords):
            print(f"    - {keyword}")
        print()


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("  Template Catalog System Test")
    print("=" * 60)

    test_category_normalization()
    test_template_listing()
    test_filtered_listing()
    test_category_mappings()

    print("\n" + "=" * 60)
    print("  All Tests Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Upload actual templates to cloud storage")
    print("  2. Update template URLs in the catalog")
    print("  3. Generate template hashes: catalog.update_hashes('templates/')")
    print("  4. Test with the agent: python main.py 'create a chair'")
    print()


if __name__ == "__main__":
    main()
