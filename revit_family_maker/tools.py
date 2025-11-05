"""Tool implementations for Revit Family Maker Agent."""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Literal, Optional
from dataclasses import asdict

import httpx
from PIL import Image
from tenacity import retry, stop_after_attempt, wait_exponential

from pydantic_ai import Agent, RunContext
from .dependencies import RevitAgentDependencies
from .templates import get_catalog, normalize_category
from .aps_client import get_aps_client


# ============================================
# Unit Conversion Utilities
# ============================================

def to_feet(value: float, unit: str) -> float:
    """Convert user dimensions to Revit internal feet.

    Args:
        value: Numeric value to convert
        unit: Source unit (mm, cm, m, in, ft)

    Returns:
        Value in feet, rounded to ±0.5mm tolerance

    Raises:
        ValueError: If unit is unknown
    """
    conversions = {
        "mm": 0.00328084,
        "cm": 0.0328084,
        "m": 3.28084,
        "in": 0.0833333,
        "ft": 1.0,
        "feet": 1.0
    }

    unit_lower = unit.lower()
    if unit_lower not in conversions:
        raise ValueError(
            f"Unknown unit: {unit}. Supported: mm, cm, m, in, ft"
        )

    return round(value * conversions[unit_lower], 6)


def parse_dimension(text: str) -> tuple[float, str]:
    """Parse dimension from text like '2400mm', '8ft', '3.5m'.

    Args:
        text: Dimension string

    Returns:
        Tuple of (value, unit)

    Raises:
        ValueError: If dimension cannot be parsed
    """
    # Match patterns like "2400mm", "8 ft", "3.5m"
    match = re.match(r"(\d+\.?\d*)\s*(mm|cm|m|in|ft|feet)", text.lower())
    if not match:
        raise ValueError(f"Cannot parse dimension: {text}")

    value = float(match.group(1))
    unit = match.group(2)
    return value, unit


# ============================================
# Image Security Utilities
# ============================================

def strip_exif_pii(image_path: str) -> str:
    """Strip EXIF metadata and PII from image before external calls.

    Args:
        image_path: Path to original image

    Returns:
        Path to sanitized image

    Raises:
        FileNotFoundError: If image doesn't exist
        IOError: If image cannot be processed
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        # Open image and strip EXIF
        img = Image.open(image_path)
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)

        # Save to safe path
        safe_path = f"{image_path}.safe.jpg"
        image_without_exif.save(safe_path)

        return safe_path
    except Exception as e:
        raise IOError(f"Failed to sanitize image: {e}") from e


# ============================================
# APS/Revit API Integration (Stubbed)
# ============================================

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def execute_aps_workitem(
    client_id: str,
    client_secret: str,
    template_url: str,
    parameters: dict,
    activity_id: str,
    max_wait: int = 600
) -> dict:
    """Execute Design Automation workitem with real APS API.

    Args:
        client_id: APS client ID
        client_secret: APS client secret
        template_url: URL to family template (.rft)
        parameters: Family parameters dict
        activity_id: Fully qualified activity ID (e.g., "nickname.Activity+alias")
        max_wait: Maximum wait time in seconds (default: 600)

    Returns:
        Dict with:
        - status: "success" or "failed"
        - rfa_content: Revit family file bytes
        - manifest_content: JSON manifest bytes
        - job_id: WorkItem ID
        - duration_sec: Execution time

    Raises:
        RuntimeError: If WorkItem fails
        TimeoutError: If WorkItem times out
    """
    import time

    start_time = time.time()

    print(f"🔧 Executing APS workitem:")
    print(f"  Template: {template_url}")
    print(f"  Activity: {activity_id}")

    # Get APS client
    client = get_aps_client(client_id, client_secret)

    # Prepare WorkItem arguments
    arguments = {
        "templateFile": {
            "url": template_url,
            "verb": "get",
        },
        "parametersFile": {
            "url": "data:application/json," + json.dumps(parameters),
            "verb": "get",
        },
        "outputFamily": {
            "verb": "put",
            "url": None,  # APS will provide signed URL
        },
        "outputManifest": {
            "verb": "put",
            "url": None,  # APS will provide signed URL
        },
    }

    # Create WorkItem and wait for completion
    final_status, outputs = await client.create_workitem_and_wait(
        activity_id=activity_id,
        arguments=arguments,
        max_wait=max_wait
    )

    duration = time.time() - start_time

    # Extract downloaded files
    rfa_content = outputs.get("outputFamily")
    manifest_content = outputs.get("outputManifest")

    if not rfa_content or not manifest_content:
        raise RuntimeError("Missing output files from WorkItem")

    print(f"✅ WorkItem completed in {duration:.1f}s")

    return {
        "status": "success",
        "rfa_content": rfa_content,
        "manifest_content": manifest_content,
        "job_id": final_status["id"],
        "duration_sec": duration,
        "report_url": final_status.get("reportUrl"),
    }


# ============================================
# Image-to-3D Service Integration (Stubbed)
# ============================================

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def generate_3d_from_image(
    image_path: str,
    provider: str,
    api_key: str
) -> dict:
    """Generate 3D mesh from image using AI service.

    TODO: Implement actual image-to-3D API integration.
    This is a placeholder implementation.

    Args:
        image_path: Path to sanitized image
        provider: Service provider (promeai, tripo3d, furnimesh)
        api_key: API key for service

    Returns:
        Dict with mesh_url, confidence, license_url
    """
    print(f"🎨 [STUB] Generating 3D from image:")
    print(f"  Image: {image_path}")
    print(f"  Provider: {provider}")

    # Simulate success
    return {
        "mesh_url": "https://example.com/generated_mesh.obj",
        "confidence": 0.85,
        "license_url": "https://example.com/license/cc-by-4.0",
        "job_id": "stub-3d-job-456"
    }


# ============================================
# Template Catalog (Stubbed)
# ============================================

async def get_template_catalog(
    catalog_url: str,
    revit_version: str,
    category_filter: Optional[str] = None
) -> list[dict]:
    """Get family template catalog from the template management system.

    Args:
        catalog_url: Base URL for template storage
        revit_version: Filter by Revit version (2024 or 2025)
        category_filter: Optional category filter (e.g., "Furniture")

    Returns:
        List of template metadata dicts
    """
    # Get catalog instance
    catalog = get_catalog(catalog_url)

    # Normalize category if provided
    normalized_category = None
    if category_filter:
        normalized_category = normalize_category(category_filter)

    # List templates with filters
    templates = catalog.list_templates(
        category=normalized_category,
        revit_version=revit_version
    )

    # Convert to dict format
    return [
        {
            "template_id": t.id,
            "template_url": t.url,
            "template_hash": t.hash or "pending",
            "category": t.category,
            "subcategory": t.subcategory,
            "revit_version": t.revit_version,
            "parametric_capabilities": ["DIM_Width", "DIM_Depth", "DIM_Height"],
            "description": t.description,
            "default_dimensions": {
                "width": {"value": t.default_width, "unit": "mm"},
                "depth": {"value": t.default_depth, "unit": "mm"},
                "height": {"value": t.default_height, "unit": "mm"}
            },
            "constraints": {
                "min_width": t.min_width,
                "max_width": t.max_width,
                "min_depth": t.min_depth,
                "max_depth": t.max_depth,
                "min_height": t.min_height,
                "max_height": t.max_height
            }
        }
        for t in templates
    ]


# ============================================
# Manifest Generation
# ============================================

def generate_manifest(
    family_name: str,
    revit_version: str,
    category: str,
    template_id: str,
    template_hash: str,
    parameters: list[dict],
    geometry_source: str,
    flex_test_passed: bool,
    file_size_bytes: int,
    **kwargs
) -> dict:
    """Generate JSON manifest for family.

    Args:
        family_name: Generated family name
        revit_version: Revit version (2024, 2025)
        category: Family category
        template_id: Template identifier
        template_hash: Template SHA256 hash
        parameters: List of parameter dicts
        geometry_source: Source type (parametric|mesh|hybrid)
        flex_test_passed: Flex test result
        file_size_bytes: File size in bytes
        **kwargs: Additional manifest fields

    Returns:
        Complete manifest dict
    """
    from datetime import datetime

    manifest = {
        "family_name": family_name,
        "revit_version": revit_version,
        "category": category,
        "template_id": template_id,
        "template_hash": template_hash,
        "parameters": parameters,
        "geometry_source": geometry_source,
        "flex_test_passed": flex_test_passed,
        "file_size_bytes": file_size_bytes,
        "creation_timestamp": datetime.utcnow().isoformat() + "Z",
        **kwargs
    }

    return manifest


# ============================================
# Tool Implementations
# ============================================

def create_tools(agent: Agent):
    """Register all tools with the agent.

    Args:
        agent: Pydantic AI agent instance
    """

    @agent.tool
    async def generate_family_from_prompt(
        ctx: RunContext[RevitAgentDependencies],
        description: str,
        category: str,
        revit_version: Literal["2024", "2025"],
        company_prefix: str = "Generic"
    ) -> dict:
        """Generate Revit family from text prompt using parametric templates.

        Args:
            ctx: Runtime context with dependencies
            description: Natural language description
            category: Revit category (Furniture, Doors, Windows, etc.)
            revit_version: Target Revit version
            company_prefix: Company prefix for naming

        Returns:
            Dict with family_name, file_path, manifest_path, etc.
        """
        print(f"\n📝 Generating family from prompt:")
        print(f"  Description: {description}")
        print(f"  Category: {category}")
        print(f"  Version: {revit_version}")

        # Parse dimensions from description
        # Example: "door 2100mm x 900mm" → extract dimensions
        dimensions = {}
        for keyword in ["width", "depth", "height", "tall", "wide", "deep"]:
            pattern = rf"{keyword}[\s:]*(\d+\.?\d*\s*(?:mm|cm|m|in|ft))"
            match = re.search(pattern, description.lower())
            if match:
                value, unit = parse_dimension(match.group(1))
                dimensions[keyword] = to_feet(value, unit)

        # Use defaults if not found
        if "height" not in dimensions and "tall" not in dimensions:
            dimensions["height"] = 3.0  # Default 3 feet
        if "width" not in dimensions and "wide" not in dimensions:
            dimensions["width"] = 2.0  # Default 2 feet
        if "depth" not in dimensions and "deep" not in dimensions:
            dimensions["depth"] = 2.0  # Default 2 feet

        print(f"  Parsed dimensions (feet): {dimensions}")

        # Get appropriate template
        templates = await get_template_catalog(
            ctx.deps.template_catalog_url,
            revit_version,
            category
        )

        if not templates:
            raise ValueError(
                f"No templates found for category '{category}' "
                f"and Revit version {revit_version}"
            )

        template = templates[0]  # Use first matching template
        print(f"  Using template: {template['template_id']}")

        # Prepare parameters for Revit API
        parameters = [
            {"name": "DIM_Height", "type": "Length", "value": str(dimensions.get("height", 3.0)), "unit": "feet", "instance": False},
            {"name": "DIM_Width", "type": "Length", "value": str(dimensions.get("width", 2.0)), "unit": "feet", "instance": False},
            {"name": "DIM_Depth", "type": "Length", "value": str(dimensions.get("depth", 2.0)), "unit": "feet", "instance": False},
        ]

        # Generate family name
        family_name = f"{company_prefix}_{category.replace(' ', '')}_{revit_version}_v0.1.0"

        # Execute APS workitem
        workitem_result = await execute_aps_workitem(
            client_id=ctx.deps.aps_client_id,
            client_secret=ctx.deps.aps_client_secret,
            template_url=template["template_url"],
            parameters={
                "category": category,
                "width": dimensions["width"],
                "width_unit": dimensions["width_unit"],
                "depth": dimensions["depth"],
                "depth_unit": dimensions["depth_unit"],
                "height": dimensions["height"],
                "height_unit": dimensions["height_unit"],
                "company_prefix": company_prefix,
                "version": "0.1.0",
                **parameters
            },
            activity_id=ctx.deps.aps_activity_name
        )

        # Parse manifest from returned content
        manifest_json = json.loads(workitem_result["manifest_content"].decode("utf-8"))

        # Save files locally (or upload to your storage)
        output_dir = Path(ctx.deps.output_bucket)
        output_dir.mkdir(parents=True, exist_ok=True)

        rfa_path = output_dir / f"{family_name}.rfa"
        manifest_path = output_dir / f"{family_name}.json"

        rfa_path.write_bytes(workitem_result["rfa_content"])
        manifest_path.write_text(json.dumps(manifest_json, indent=2))

        print(f"💾 Saved: {rfa_path} ({len(workitem_result['rfa_content'])} bytes)")
        print(f"💾 Saved: {manifest_path}")

        return {
            "family_name": family_name,
            "file_path": str(rfa_path),
            "manifest_path": str(manifest_path),
            "category": category,
            "revit_version": revit_version,
            "parameters": manifest_json.get("parameters", []),
            "flex_test_passed": manifest_json.get("flex_test_passed", False),
            "warnings": [],
            "job_id": workitem_result["job_id"],
            "duration_sec": workitem_result["duration_sec"]
        }

    @agent.tool
    async def generate_family_from_image(
        ctx: RunContext[RevitAgentDependencies],
        image_path: str,
        category: str,
        revit_version: Literal["2024", "2025"],
        scale_reference: Optional[float] = None,
        company_prefix: str = "Generic"
    ) -> dict:
        """Generate Revit family from reference image using AI 3D reconstruction.

        Args:
            ctx: Runtime context with dependencies
            image_path: Path to reference image
            category: Revit category
            revit_version: Target Revit version
            scale_reference: Known dimension for scaling (optional)
            company_prefix: Company prefix for naming

        Returns:
            Dict with family_name, file_path, manifest_path, etc.
        """
        print(f"\n🖼️  Generating family from image:")
        print(f"  Image: {image_path}")
        print(f"  Category: {category}")
        print(f"  Version: {revit_version}")

        # Sanitize image (strip EXIF/PII)
        safe_image_path = strip_exif_pii(image_path)
        print(f"  Sanitized image: {safe_image_path}")

        # Generate 3D mesh from image
        mesh_result = await generate_3d_from_image(
            safe_image_path,
            ctx.deps.image_to_3d_provider,
            ctx.deps.image_to_3d_api_key
        )

        print(f"  Mesh generated: {mesh_result['mesh_url']}")
        print(f"  Confidence: {mesh_result['confidence']}")

        # Check confidence threshold
        if mesh_result["confidence"] < 0.5:
            print("  ⚠️  Low confidence, consider parametric fallback")

        # Get appropriate template
        templates = await get_template_catalog(
            ctx.deps.template_catalog_url,
            revit_version,
            category
        )

        if not templates:
            raise ValueError(
                f"No templates found for category '{category}' "
                f"and Revit version {revit_version}"
            )

        template = templates[0]
        print(f"  Using template: {template['template_id']}")

        # Prepare parameters
        parameters = [
            {"name": "DIM_Scale", "type": "Number", "value": "1.0", "unit": "", "instance": False},
        ]

        if scale_reference:
            parameters[0]["value"] = str(scale_reference)

        # Generate family name
        family_name = f"{company_prefix}_{category.replace(' ', '')}_FromImage_{revit_version}_v0.1.0"

        # Execute APS workitem with mesh import
        workitem_result = await execute_aps_workitem(
            client_id=ctx.deps.aps_client_id,
            client_secret=ctx.deps.aps_client_secret,
            template_url=template["template_url"],
            parameters={
                "category": category,
                "geometry_source": "mesh",
                "mesh_url": mesh_result["mesh_url"],
                "mesh_scale": scale_reference or 1.0,
                "company_prefix": company_prefix,
                "version": "0.1.0",
                **parameters
            },
            activity_id=ctx.deps.aps_activity_name
        )

        # Parse manifest from returned content
        manifest_json = json.loads(workitem_result["manifest_content"].decode("utf-8"))

        # Add mesh metadata to manifest
        manifest_json["mesh_license_url"] = mesh_result["license_url"]
        manifest_json["mesh_confidence"] = mesh_result["confidence"]
        manifest_json["image_sanitized"] = True

        # Save files locally (or upload to your storage)
        output_dir = Path(ctx.deps.output_bucket)
        output_dir.mkdir(parents=True, exist_ok=True)

        rfa_path = output_dir / f"{family_name}.rfa"
        manifest_path = output_dir / f"{family_name}.json"

        rfa_path.write_bytes(workitem_result["rfa_content"])
        manifest_path.write_text(json.dumps(manifest_json, indent=2))

        print(f"💾 Saved: {rfa_path} ({len(workitem_result['rfa_content'])} bytes)")
        print(f"💾 Saved: {manifest_path}")

        return {
            "family_name": family_name,
            "file_path": str(rfa_path),
            "manifest_path": str(manifest_path),
            "category": category,
            "revit_version": revit_version,
            "parameters": manifest_json.get("parameters", []),
            "flex_test_passed": manifest_json.get("flex_test_passed", False),
            "warnings": [],
            "job_id": workitem_result["job_id"],
            "duration_sec": workitem_result["duration_sec"],
            "mesh_confidence": mesh_result["confidence"]
        }

    @agent.tool
    async def perform_family_creation(
        ctx: RunContext[RevitAgentDependencies],
        description: Optional[str] = None,
        image_path: Optional[str] = None,
        category: Optional[str] = None,
        revit_version: Literal["2024", "2025"] = "2025",
        use_prompt: bool = True,
        use_image: bool = True,
        company_prefix: str = "Generic"
    ) -> dict:
        """Master orchestration function combining text and image inputs.

        Args:
            ctx: Runtime context with dependencies
            description: Natural language description (optional)
            image_path: Path to reference image (optional)
            category: Revit category (required, but can be inferred)
            revit_version: Target Revit version
            use_prompt: Use text prompt
            use_image: Use image input
            company_prefix: Company prefix for naming

        Returns:
            Dict with family_name, file_path, manifest_path, etc.
        """
        print(f"\n🔧 Performing family creation:")
        print(f"  Description: {description}")
        print(f"  Image: {image_path}")
        print(f"  Category: {category}")

        # Validate inputs
        if not description and not image_path:
            raise ValueError("Must provide description or image")

        if not category:
            raise ValueError(
                "Category is required. Please specify one of: "
                "Furniture, Doors, Windows, Walls, Generic Models"
            )

        # Determine mode
        has_text = description and use_prompt
        has_image = image_path and use_image

        if has_text and has_image:
            # Hybrid mode: run both in parallel
            print("  Mode: Hybrid (text + image)")

            results = await asyncio.gather(
                generate_family_from_prompt(
                    ctx, description, category, revit_version, company_prefix
                ),
                generate_family_from_image(
                    ctx, image_path, category, revit_version, None, company_prefix
                )
            )

            prompt_result, image_result = results

            # Merge results (text drives parameters, image drives shape)
            # For now, return image result with prompt parameters
            merged_result = image_result.copy()
            merged_result["parameters"].extend(prompt_result["parameters"])
            merged_result["geometry_source"] = "hybrid"
            merged_result["sources_used"] = ["text", "image"]

            return merged_result

        elif has_text:
            # Text-only mode
            print("  Mode: Text-only (parametric)")
            return await generate_family_from_prompt(
                ctx, description, category, revit_version, company_prefix
            )

        elif has_image:
            # Image-only mode
            print("  Mode: Image-only (mesh)")
            return await generate_family_from_image(
                ctx, image_path, category, revit_version, None, company_prefix
            )

        else:
            raise ValueError("No valid input mode selected")

    @agent.tool
    async def list_family_templates(
        ctx: RunContext[RevitAgentDependencies],
        revit_version: Literal["2024", "2025"] = "2025",
        category_filter: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> list[dict]:
        """List available family templates with immutability guarantees.

        Args:
            ctx: Runtime context with dependencies
            revit_version: Filter by Revit version
            category_filter: Optional category filter
            limit: Max results
            offset: Pagination offset

        Returns:
            List of template metadata dicts
        """
        # Use template URL from settings
        catalog_url = ctx.deps.template_catalog_url

        templates = await get_template_catalog(
            catalog_url,
            revit_version,
            category_filter
        )

        # Apply pagination
        return templates[offset:offset + limit]

    @agent.tool
    async def get_family(
        ctx: RunContext[RevitAgentDependencies],
        family_id: str
    ) -> dict:
        """Retrieve previously created family for iterative refinement.

        Args:
            ctx: Runtime context with dependencies
            family_id: Family name or ID

        Returns:
            Dict with family metadata, manifest, and current parameters
        """
        print(f"\n📂 Retrieving family: {family_id}")

        # TODO: Implement actual storage retrieval
        # For now, return mock data

        mock_family = {
            "family_name": family_id,
            "file_path": f"{ctx.deps.output_bucket}/{family_id}.rfa",
            "manifest": {
                "family_name": family_id,
                "category": "Furniture",
                "revit_version": "2025",
                "parameters": [
                    {"name": "DIM_Height", "value": "3.0", "unit": "feet"}
                ],
                "flex_test_passed": True
            },
            "current_parameters": [
                {"name": "DIM_Height", "value": "3.0", "unit": "feet"}
            ]
        }

        return mock_family
