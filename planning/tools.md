# Tool Specifications
## AI Revit Family Maker Assistant

**Generated**: 2025-11-05
**Philosophy**: Minimal tools (5 essential functions), simple parameters (1-4 per tool), single-purpose

---

## Tool 1: generate_family_from_prompt

### Purpose
Generate Revit family from natural language text description using parametric templates and Revit API.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `description` | `str` | Yes | Natural language description of desired component |
| `category` | `str` | Yes | Revit category (e.g., "Furniture", "Doors", "Windows") |
| `revit_version` | `Literal["2024", "2025"]` | Yes | Target Revit version |
| `company_prefix` | `str` | No | Company prefix for naming (default: "Generic") |

### Return Value Structure

```python
{
  "family_name": "Generic_Furniture_Chair_v0.1.0",
  "file_path": "/path/to/output/Generic_Furniture_Chair_v0.1.0.rfa",
  "manifest_path": "/path/to/output/Generic_Furniture_Chair_v0.1.0.json",
  "category": "Furniture",
  "revit_version": "2025",
  "parameters": [
    {
      "name": "DIM_Height",
      "type": "Length",
      "value": "3.0",
      "unit": "feet",
      "instance": false
    }
  ],
  "flex_test_passed": true,
  "warnings": []
}
```

### Error Handling

- **Missing dimensions**: Extract from description or use defaults
- **Invalid category**: Raise ValueError with list of supported categories
- **APS failure**: Attempt local Revit fallback, log fallback usage
- **Flex test failure**: Raise error, include failed test details
- **Template not found**: Raise error with available templates for category/version

### Responsibilities

1. Parse dimensions from description (e.g., "4ft by 3ft", "2400mm x 900mm")
2. Convert all dimensions to feet (Revit internal unit)
3. Select appropriate family template by category + Revit version
4. Pin template by SHA256 hash (template immutability)
5. Configure APS Design Automation workitem
6. Set parameters with prefixes (DIM_, MTRL_, ID_, CTRL_)
7. Execute Revit API operations via AppBundle
8. Run flex test (min/nominal/max parameter sets)
9. Generate .rfa + JSON manifest
10. Return FamilyGenerationResult dict

### Integration Notes

- Use `@agent.tool` decorator with `RunContext[RevitAgentDependencies]`
- Async function for APS API calls
- Retry logic: 3 attempts with exponential backoff
- Timeout: 60 seconds per APS workitem
- Log all APS job IDs and durations

---

## Tool 2: generate_family_from_image

### Purpose
Generate Revit family from reference image using AI 3D reconstruction and mesh import.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `image_path` | `str` | Yes | Path to reference image (JPG, PNG, WebP) |
| `category` | `str` | Yes | Revit category for the generated family |
| `revit_version` | `Literal["2024", "2025"]` | Yes | Target Revit version |
| `scale_reference` | `float` | No | Known dimension for scaling (in user units) |
| `company_prefix` | `str` | No | Company prefix for naming (default: "Generic") |

### Return Value Structure

Same as `generate_family_from_prompt` with additional fields:

```python
{
  ...
  "geometry_source": "mesh",
  "mesh_license_url": "https://promeai.com/licenses/cc-by-4.0",
  "mesh_confidence": 0.87,
  "image_sanitized": true
}
```

### Error Handling

- **Image not found**: Raise FileNotFoundError with clear path
- **EXIF stripping failure**: Log warning, proceed anyway
- **3D service failure**: Fall back to parametric template + prompt
- **Low confidence (<0.5)**: Warn user, offer parametric fallback
- **Mesh too large**: Simplify mesh or reject if > 3 MB budget
- **License check failure**: Reject generation, require manual approval

### Responsibilities

1. Validate image file exists and is readable
2. Strip EXIF metadata and PII (security requirement)
3. Call image-to-3D service (PromeAI, Tripo3D, or FurniMesh)
4. Check mesh license and store license URL in manifest
5. Convert mesh to Revit-compatible format (SAT or OBJ)
6. Import mesh to appropriate family template
7. Add mandatory DIM_Scale parameter for adjustability
8. Validate real-world size after import (warn if extreme)
9. Run flex test with scale variations
10. Return FamilyGenerationResult dict

### Integration Notes

- Use `@agent.tool` decorator with `RunContext[RevitAgentDependencies]`
- Async for image-to-3D API calls
- Security: Never send confidential images without approval
- Log all external API calls (job ID, duration, endpoint)
- Fallback confidence threshold: 0.5 (configurable)

---

## Tool 3: perform_family_creation

### Purpose
Master orchestration function combining text and image inputs for hybrid family creation.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `description` | `str` | No | Natural language description |
| `image_path` | `str` | No | Path to reference image |
| `category` | `str` | No | Revit category (required but can be inferred) |
| `revit_version` | `Literal["2024", "2025"]` | No | Target Revit version (default: "2025") |
| `use_prompt` | `bool` | No | Use text prompt (default: True) |
| `use_image` | `bool` | No | Use image input (default: True) |
| `company_prefix` | `str` | No | Company prefix for naming (default: "Generic") |

### Return Value Structure

Same as `generate_family_from_prompt` with:

```python
{
  ...
  "geometry_source": "hybrid",  # or "parametric" or "mesh"
  "sources_used": ["text", "image"]
}
```

### Error Handling

- **No inputs**: Raise ValueError "Must provide description or image"
- **Category ambiguous**: Raise ValueError asking user for category
- **Both modes fail**: Return error with both failure reasons
- **Conflicting dimensions**: Text dimensions take precedence, log warning

### Responsibilities

1. Validate inputs (at least one of description or image required)
2. Validate category is provided (mandatory)
3. Determine mode: text-only, image-only, or hybrid
4. If hybrid: run `generate_family_from_prompt` and `generate_family_from_image` in parallel
5. Merge results intelligently (text drives parameters, image drives shape)
6. Generate unified .rfa with hybrid geometry
7. Create manifest documenting both sources
8. Run comprehensive flex test
9. Return FamilyGenerationResult dict

### Integration Notes

- Use `@agent.tool` decorator with `RunContext[RevitAgentDependencies]`
- Parallel execution using `asyncio.gather()` for hybrid mode
- Primary entry point for agent (most users will call this)
- Handles mode selection logic automatically

---

## Tool 4: list_family_templates

### Purpose
List available family templates with immutability guarantees for template selection.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `revit_version` | `Literal["2024", "2025"]` | No | Filter by Revit version (default: "2025") |
| `category_filter` | `str` | No | Filter by category (e.g., "Furniture") |
| `limit` | `int` | No | Max results (default: 20) |
| `offset` | `int` | No | Pagination offset (default: 0) |

### Return Value Structure

```python
[
  {
    "template_id": "WindowTemplate_2025_v2.3",
    "template_url": "https://s3.amazonaws.com/templates/WindowTemplate_2025_v2.3.rft",
    "template_hash": "sha256:def456abc...",
    "category": "Windows",
    "revit_version": "2025",
    "parametric_capabilities": ["DIM_Width", "DIM_Height", "CTRL_GrillePattern"],
    "description": "Parametric window with adjustable grilles and muntins"
  },
  ...
]
```

### Error Handling

- **Template catalog unavailable**: Return cached list or raise error
- **Invalid category**: Return empty list with warning
- **No templates for version**: Raise error with supported versions

### Responsibilities

1. Query template catalog (URL or database)
2. Filter by Revit version and category
3. Verify each template hash matches catalog (immutability check)
4. Return paginated results
5. Include parametric capabilities for each template

### Integration Notes

- Use `@agent.tool_plain` decorator (no context dependency)
- Async function for catalog API calls
- Cache template list for 1 hour (configurable)
- Template immutability: never mutate templates in-place

---

## Tool 5: get_family

### Purpose
Retrieve previously created family for iterative refinement and multi-turn conversations.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `family_id` | `str` | Yes | Family name or ID (e.g., "Generic_Furniture_Chair_v0.1.0") |

### Return Value Structure

```python
{
  "family_name": "Generic_Furniture_Chair_v0.1.0",
  "file_path": "/path/to/Generic_Furniture_Chair_v0.1.0.rfa",
  "manifest": {
    "family_name": "Generic_Furniture_Chair_v0.1.0",
    "category": "Furniture",
    "parameters": [...],
    "flex_test_passed": true,
    ...
  },
  "current_parameters": [
    {"name": "DIM_Height", "value": "3.0", "unit": "feet"}
  ]
}
```

### Error Handling

- **Family not found**: Raise ValueError with similar family suggestions
- **Manifest missing**: Warn and return partial data
- **File corrupted**: Raise error with last known good version

### Responsibilities

1. Search for family by ID/name in output storage
2. Load manifest JSON
3. Extract current parameter values
4. Return full metadata for agent context
5. Enable iterative modifications without regenerating from scratch

### Integration Notes

- Use `@agent.tool` decorator with `RunContext[RevitAgentDependencies]`
- Async function for storage API calls
- Conversation memory: store family_id for "make it taller" requests
- Used for multi-turn refinement workflows

---

## Tool Integration Architecture

```
User Request
     ↓
   Agent
     ↓
perform_family_creation (orchestrator)
     ↓
   ┌─────┴─────┐
   ↓           ↓
generate_from_prompt   generate_from_image
   ↓                      ↓
list_family_templates   (image-to-3D service)
   ↓
   └──────┬──────┘
          ↓
    APS/Revit API
          ↓
    .rfa + manifest
          ↓
      get_family (for refinements)
```

---

## Testing Strategy

Each tool must have:
1. **Unit tests** with mocked APS/external APIs
2. **Integration tests** with real APS calls (test credentials)
3. **Error handling tests** for all failure modes
4. **Performance tests** (generation < 60 seconds)
5. **TestModel validation** for agent decision-making

---

## Common Patterns

### Unit Conversion
All tools must convert user dimensions to feet before Revit API calls:
```python
def to_feet(value: float, unit: str) -> float:
    conversions = {
        "mm": 0.00328084, "cm": 0.0328084, "m": 3.28084,
        "in": 0.0833333, "ft": 1.0
    }
    return round(value * conversions[unit], 6)
```

### Error Messages
Never leak sensitive data:
```python
# Good
raise ValueError("Category is required. Supported: Furniture, Doors, Windows")

# Bad
raise ValueError(f"Failed: {aps_client_id} invalid at {template_url}")
```

### Retry Logic
All external API calls:
```python
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def call_external_api(...): ...
```

---

## Summary

- **5 tools total**: 3 core generation, 1 listing, 1 retrieval
- **Simple parameters**: 1-4 per tool
- **Consistent structure**: All return dict with family_name, file_path, manifest
- **Error handling**: Graceful failures, actionable messages
- **Security**: EXIF stripping, no credential leaks
- **Performance**: Async, retry logic, timeouts
