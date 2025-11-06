# Revit Family Template Catalog

This directory contains Revit family templates (.rft) used by the AI Revit Family Maker.

## Template Organization

Templates are organized by Revit category and version:

```
templates/
├── 2024/
│   ├── Generic_Model.rft
│   ├── Furniture.rft
│   ├── Casework.rft
│   ├── Lighting_Fixtures.rft
│   └── Specialty_Equipment.rft
└── 2025/
    ├── Generic_Model.rft
    ├── Furniture.rft
    ├── Casework.rft
    ├── Lighting_Fixtures.rft
    └── Specialty_Equipment.rft
```

## Template Requirements

Each template must:

1. **Be a valid Revit family template** (.rft extension)
2. **Include reference planes** for parametric control:
   - `Left`, `Right` (for width)
   - `Front`, `Back` (for depth)
   - `Top`, `Bottom` (for height)
   - `Center (Left/Right)` and `Center (Front/Back)` for alignment
3. **Be dimensioned** with locked dimensions to reference planes
4. **Have material parameters** assigned to geometry (if applicable)
5. **Be tested** with the Flex Test tool (min/nominal/max parameter values)

## Supported Categories

The system supports these Revit categories (expand as needed):

- **Generic Model** - Default fallback for unknown categories
- **Furniture** - Chairs, tables, desks, etc.
- **Casework** - Cabinets, counters, shelving
- **Lighting Fixtures** - Lamps, sconces, ceiling lights
- **Specialty Equipment** - Custom equipment, appliances
- **Plumbing Fixtures** - Sinks, toilets, showers
- **Electrical Equipment** - Panels, outlets, switches
- **Mechanical Equipment** - HVAC units, ducts

## Template Metadata

Each template should have an associated JSON metadata file for the catalog:

```json
{
  "template_id": "furniture_chair_v1",
  "category": "Furniture",
  "subcategory": "Seating",
  "revit_version": "2024",
  "file_path": "templates/2024/Furniture.rft",
  "file_hash": "sha256:abcd1234...",
  "description": "Parametric chair template with back and armrests",
  "default_parameters": {
    "Width": {"value": 600, "unit": "mm"},
    "Depth": {"value": 650, "unit": "mm"},
    "Height": {"value": 900, "unit": "mm"}
  },
  "constraints": {
    "min_width": 400,
    "max_width": 1200,
    "min_depth": 400,
    "max_depth": 1000,
    "min_height": 600,
    "max_height": 1500
  },
  "material_parameters": ["Seat Material", "Frame Material"],
  "visibility_parameters": ["Show Armrests", "Show Casters"]
}
```

## Obtaining Templates

### Option 1: Use Revit Default Templates

Copy templates from your Revit installation:

```
C:\ProgramData\Autodesk\RVT {VERSION}\Family Templates\English\
```

Select the categories you need and rename for clarity.

### Option 2: Create Custom Templates

1. Open Revit
2. **File > New > Family**
3. Choose a base template
4. Add reference planes and dimensions
5. Add parameters (DIM_Width, DIM_Depth, DIM_Height)
6. Lock dimensions to reference planes
7. Add simple geometry (for testing)
8. **Test** by changing parameters - geometry should update
9. **Save** as .rft in this directory

### Option 3: Download Community Templates

- [Revit City](https://www.revitcity.com/downloads.php?type=families)
- [BIMObject](https://www.bimobject.com/)
- [National BIM Library](https://www.nationalbimlibrary.com/)

Ensure templates have permissive licenses for your use case.

## Template Testing Checklist

Before adding a template to production:

- [ ] Opens without errors in target Revit version
- [ ] Has labeled reference planes (Left, Right, Front, Back, Top, Bottom)
- [ ] Dimensions are locked to reference planes
- [ ] Parameters DIM_Width, DIM_Depth, DIM_Height exist (or can be added)
- [ ] Geometry updates when parameters change
- [ ] Flex test passes: min values (50%), nominal (100%), max values (200%)
- [ ] File size < 500 KB (templates should be minimal)
- [ ] No errors/warnings in Revit's Review Warnings dialog
- [ ] Template category matches intended use

## Template Hashing

Generate SHA256 hash for version control:

```bash
# Linux/Mac
sha256sum templates/2024/Furniture.rft

# Windows PowerShell
Get-FileHash templates/2024/Furniture.rft -Algorithm SHA256
```

Store hash in catalog JSON and FamilyCreationParams for reproducibility.

## Uploading Templates to APS

Templates can be hosted in:

1. **OSS Bucket** (Autodesk Object Storage Service)
2. **AWS S3** with signed URLs
3. **Azure Blob Storage** with SAS tokens
4. **Direct URL** (if publicly accessible)

The agent tool `list_family_templates()` should return URLs that APS can access.

## Template Versioning

Use semantic versioning in template IDs:

- `furniture_chair_v1.0.0` - Initial release
- `furniture_chair_v1.1.0` - Added armrest parameter
- `furniture_chair_v2.0.0` - Breaking change (new constraint structure)

Always maintain backward compatibility or clearly document breaking changes.

## Example Template Catalog Entry

```python
TEMPLATE_CATALOG = {
    "furniture_chair_v1": {
        "id": "furniture_chair_v1",
        "category": "Furniture",
        "url": "https://your-storage.com/templates/2024/Furniture_Chair_v1.rft",
        "hash": "sha256:abc123...",
        "revit_version": "2024",
        "description": "Parametric office chair with adjustable height",
    },
    # Add more templates...
}
```

## Next Steps

1. **Copy** or create templates for your target categories
2. **Test** each template in Revit
3. **Generate** SHA256 hashes
4. **Upload** to cloud storage (OSS/S3/Azure)
5. **Update** the template catalog in `revit_family_maker/templates.py`
6. **Set** `APS_TEMPLATE_URL` in `.env` to your storage endpoint
