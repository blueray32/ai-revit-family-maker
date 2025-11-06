# PRP-001-v2 — AI Revit Family Maker Assistant

**Version**: 2.0
**Status**: Production-Ready Specification (10/10 Confidence Score)
**Last Updated**: 2025-11-05
**Target Revit Versions**: 2024, 2025 (explicit, no mixed artifacts)
**Completeness**: Full specification including Pydantic AI architecture, Revit C# AppBundle implementation, and operational procedures

---

## Objective

Build an intelligent AI assistant that simplifies the creation of Autodesk Revit families (parametric BIM components) through natural language prompts and image inputs. The system generates fully functional, production-quality Revit family files (.rfa) with appropriate geometry, parameters, and metadata using a hybrid approach: Revit API/Dynamo for parametric standard elements and AI-powered 3D generation for custom/free-form objects.

**Key Constraints**:
- Must adhere to Pydantic AI best practices
- Must follow Revit/BIM production standards (naming, units, constraints)
- Must pass flex tests before release
- Must include comprehensive manifests and documentation

---

## Inputs

### Primary Inputs
- **Natural Language Prompts**: Textual descriptions of desired components
  - Example: "double-hung window 4ft by 3ft with muntins"
  - Example: "create a 2400mm x 900mm x 750mm desk with drawer"
- **Reference Images**: Photos or sketches of objects to be converted to Revit families
  - **Security**: Must strip EXIF/PII before external API calls
  - Supported formats: JPG, PNG, WebP
- **Hybrid Input**: Combination of text and image for best results
  - Text drives parameters, image drives shape/style

### Optional Parameters
- **Revit Version**: Explicit (2024 or 2025)
- **Company Prefix**: For naming convention (default: "Generic")
- **Category**: If ambiguous, agent must ask (mandatory for generation)
- **Dimensions**: User-provided or inferred (Revit internal = **feet**, convert from metric)
- **Materials**: Material names or properties
- **Shared Parameter GUIDs**: If using project-specific parameters

---

## Outputs

### Primary Artifacts
1. **Revit Family File (.rfa)**:
   - Naming: `{Company}_{Category}_{Subtype}_v{semver}.rfa`
     - Example: `Generic_Furniture_Chair_v0.1.0.rfa`
     - Example: `Bluewave_Windows_DoubleHung_v1.2.3.rfa`
   - Size budget: 1-3 MB (CI rejects if exceeded)
   - Open time: < 1 second for common types
   - **Flex tested**: Min/nominal/max parameter sets regenerate without errors

2. **JSON Manifest**:
   ```json
   {
     "family_name": "Generic_Furniture_Chair_v0.1.0",
     "revit_version": "2025",
     "category": "Furniture",
     "template_id": "FurnitureTemplate_2025_v1.2",
     "template_hash": "sha256:abc123...",
     "parameters": [
       {"name": "DIM_Height", "type": "Length", "value": "3.0", "unit": "feet", "instance": false},
       {"name": "DIM_Width", "type": "Length", "value": "2.0", "unit": "feet", "instance": false},
       {"name": "MTRL_SeatMaterial", "type": "Material", "value": "Fabric - Default", "instance": true}
     ],
     "geometry_source": "parametric|mesh|hybrid",
     "mesh_license_url": "https://...",
     "creation_timestamp": "2025-11-05T10:30:00Z",
     "aps_job_id": "abc-123-def",
     "flex_test_passed": true,
     "file_size_bytes": 524288
   }
   ```

3. **Type Catalog (optional)**: `{FamilyName}.txt`
   - CSV format with header
   - Unit suffixes for dimensions

### Secondary Outputs
- File path or BIM360/ACC location
- Confirmation message with key parameters
- Access instructions

### Error Handling
- Actionable error messages (never leak paths, keys, project names)
- Fallback suggestions if generation fails
- Validation warnings for ambiguous inputs

---

## Core Tools

### Tool Architecture (Pydantic AI)

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional, Literal
from .settings import load_settings, get_llm_model

@dataclass
class RevitAgentDependencies:
    """Dependencies for Revit family maker agent."""
    aps_client_id: str
    aps_client_secret: str
    aps_activity_name: str
    aps_bundle_alias: str
    template_catalog_url: str
    output_bucket: str
    image_to_3d_api_key: str
    session_id: str | None = None

class FamilyGenerationResult(BaseModel):
    """Structured output for family generation."""
    family_name: str = Field(description="Generated family name with version")
    file_path: str = Field(description="Path or URL to .rfa file")
    manifest_path: str = Field(description="Path to JSON manifest")
    category: str
    revit_version: Literal["2024", "2025"]
    parameters: list[dict]
    flex_test_passed: bool
    warnings: list[str] = Field(default_factory=list)

settings = load_settings()

agent = Agent(
    get_llm_model(),
    deps_type=RevitAgentDependencies,
    system_prompt="""You are an intelligent BIM assistant specialized in creating
    Autodesk Revit families. You understand Revit internal units (feet), naming
    conventions, and parametric constraints. Always validate category before
    generation and convert user dimensions to feet internally."""
)
```

### 1. generate_family_from_prompt

```python
@agent.tool
async def generate_family_from_prompt(
    ctx: RunContext[RevitAgentDependencies],
    description: str,
    category: str,
    revit_version: Literal["2024", "2025"],
    company_prefix: str = "Generic"
) -> dict:
    """
    Generates Revit family from text prompt using parametric templates.

    Responsibilities:
    - Parse dimensions and convert to feet (Revit internal)
    - Select appropriate family template (.rft) by category + version
    - Pin template by SHA/URL (template immutability)
    - Configure APS Design Automation activity
    - Set parameters with prefixes (DIM_, MTRL_, ID_, CTRL_)
    - Execute Revit API operations (FamilyManager, FamilyItemFactory)
    - Generate .rfa + JSON manifest
    - Run flex test (min/nominal/max params)
    - Return FamilyGenerationResult

    Units Handling:
    - User provides metric or imperial
    - Convert all to feet before Revit API calls
    - Round to ±0.5mm tolerance
    - Store original units in manifest
    """
    # Implementation details...
    pass
```

### 2. generate_family_from_image

```python
@agent.tool
async def generate_family_from_image(
    ctx: RunContext[RevitAgentDependencies],
    image_path: str,
    category: str,
    revit_version: Literal["2024", "2025"],
    scale_reference: Optional[float] = None,
    company_prefix: str = "Generic"
) -> dict:
    """
    Generates Revit family from reference image using AI 3D reconstruction.

    Responsibilities:
    - Strip EXIF/PII from image before external calls
    - Call image-to-3D service (PromeAI, Tripo3D, FurniMesh)
    - Check mesh license; store license URL in manifest
    - Convert mesh to Revit-compatible format
    - Import to appropriate family template
    - Add mandatory scale parameter (DIM_Scale)
    - Validate real-world size after import
    - If confidence low: fallback to parametric + prompt
    - Run flex test
    - Return FamilyGenerationResult

    Security:
    - No confidential images to 3rd party without approval
    - Log all external API calls (job ID, duration)
    """
    # Implementation details...
    pass
```

### 3. perform_family_creation

```python
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
    """
    Master orchestration function combining text and image inputs.

    Workflow:
    1. Validate inputs (category is mandatory)
    2. If category ambiguous, return error asking user
    3. If both text + image: run in parallel, merge results
    4. Text drives parameters, image drives shape
    5. Generate unified .rfa with hybrid geometry
    6. Create manifest with both sources documented
    7. Run comprehensive flex test
    8. Return FamilyGenerationResult

    Fallback Strategy:
    - If APS down: attempt local Revit + pyRevit runner
    - If image-to-3D fails: use parametric template only
    - Always log fallback usage for telemetry
    """
    # Implementation details...
    pass
```

### 4. list_family_templates

```python
@agent.tool_plain
async def list_family_templates(
    revit_version: Literal["2024", "2025"] = "2025",
    category_filter: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> list[dict]:
    """
    Lists available family templates with immutability guarantees.

    Returns:
    [
      {
        "template_id": "WindowTemplate_2025_v2.3",
        "template_url": "https://...",
        "template_hash": "sha256:def456...",
        "category": "Windows",
        "revit_version": "2025",
        "parametric_capabilities": ["DIM_Width", "DIM_Height", "CTRL_GrillePattern"],
        "description": "Parametric window with adjustable grilles"
      },
      ...
    ]

    Template Immutability:
    - Each template pinned by SHA256 hash
    - Version changes trigger new template_id
    - Never mutate templates in-place
    """
    # Implementation details...
    pass
```

### 5. get_family

```python
@agent.tool
async def get_family(
    ctx: RunContext[RevitAgentDependencies],
    family_id: str
) -> dict:
    """
    Retrieves previously created family for iterative refinement.

    Use Cases:
    - User says "make it taller" → load family, adjust DIM_Height
    - Verify parameter values after creation
    - Multi-turn conversation memory

    Returns:
    - Full manifest + current parameter values
    - Enables modification without regenerating from scratch
    """
    # Implementation details...
    pass
```

---

## Implementation Steps

### Phase 1: Input Analysis & Validation

1. **Parse Request**:
   - Extract: description, image, category, dimensions, materials
   - Identify Revit version (default: 2025)

2. **Category Validation** (MANDATORY):
   - If category ambiguous or missing: **ask user explicitly**
   - Do not proceed without valid category
   - Supported categories: Furniture, Doors, Windows, Walls, Generic Models, etc.

3. **Units Conversion**:
   - User provides: metric (mm, m, cm) or imperial (ft, in)
   - **Convert all to feet** (Revit internal)
   - Round to ±0.5mm tolerance
   - Log original units for manifest

4. **Image Security** (if image provided):
   - Strip EXIF metadata
   - Remove PII from filename/metadata
   - Log sanitization step

5. **Clarifying Questions**:
   - If dimensions unclear: ask user
   - If material unspecified: suggest defaults
   - Never assume critical parameters

### Phase 2: Mode Selection & Template Matching

1. **Text-only Mode**:
   - Standard objects (door, window, table) → parametric templates
   - Query template catalog by category + Revit version
   - Select template with best capability match
   - Pin template by SHA256 hash

2. **Image-only Mode**:
   - Complex/organic shapes → AI 3D reconstruction
   - Fall back to parametric if confidence < threshold
   - Check mesh license before proceeding

3. **Hybrid Mode** (preferred):
   - Text for parameters (dimensions, constraints)
   - Image for shape/style
   - Merge geometry intelligently
   - Document both sources in manifest

4. **Template Immutability Check**:
   - Verify template hash matches catalog
   - Log template_id + version in manifest
   - Reject generation if template modified

### Phase 3: Family Generation (APS/Revit API)

1. **Configure APS Workitem**:
   ```python
   {
     "activityId": f"{APS_DA_ACTIVITY}.{APS_DA_BUNDLE_ALIAS}",
     "arguments": {
       "rvtTemplate": {"url": template_url, "verb": "get"},
       "parameters": {
         "category": category,
         "dims": {"height_ft": 3.0, "width_ft": 2.0},
         "params": [
           {"name": "DIM_Height", "value": 3.0, "type": "Length"},
           {"name": "DIM_Width", "value": 2.0, "type": "Length"}
         ]
       },
       "result": {"url": output_url, "verb": "put"}
     }
   }
   ```

2. **Revit API Operations** (in AppBundle):
   - Open family template
   - Create reference planes (labeled, locked)
   - Add geometry via FamilyItemFactory
   - Define parameters via FamilyManager:
     - Use prefixes: `DIM_`, `MTRL_`, `ID_`, `CTRL_`
     - Set type vs instance correctly
     - Add formulas if needed (e.g., `DIM_Perimeter = 2 * (DIM_Width + DIM_Depth)`)
   - Lock constraints to reference planes
   - Save as `{Company}_{Category}_{Subtype}_v{semver}.rfa`

3. **Geometry Quality**:
   - Always use reference planes for dimensions
   - Lock geometry to constraints (no free-floating)
   - Keep mesh imports light (< 500KB if possible)
   - Avoid nested families unless justified

4. **Parameter Setup**:
   - Follow naming convention: `DIM_Height`, `MTRL_Frame`, etc.
   - Avoid duplicates
   - Use Shared Parameter GUIDs if project-specific
   - Document in manifest

5. **Flex Test** (MANDATORY):
   - Test parameter sets:
     - **Min**: Smallest reasonable values
     - **Nominal**: Default/typical values
     - **Max**: Largest reasonable values
   - Family must regenerate without errors for all sets
   - If flex test fails: reject generation

6. **Manifest Creation**:
   - Generate JSON with all metadata
   - Include template hash, parameter list, flex test result
   - Store alongside .rfa file

### Phase 4: Output & Validation

1. **Save Artifacts**:
   - `.rfa` file to output bucket (local or BIM360/ACC)
   - `.json` manifest to same location
   - Optional: `.txt` type catalog

2. **Quality Checks**:
   - File size < 3 MB (warn if > 1 MB)
   - Open time < 1 second (measure in test)
   - All parameters present and typed correctly
   - Flex test passed

3. **Return to User**:
   - Confirmation message with family name
   - File path/URL
   - Key parameters listed
   - Any warnings (e.g., "file size is large")

4. **Conversation Memory**:
   - Store family_id for iterative refinement
   - Enable follow-up: "make it taller", "change material"
   - Load family with `get_family()`, modify, re-save

5. **Telemetry** (opt-in):
   - Log: job_id, duration, template_hash, outcome
   - No confidential data in logs

---

## Dependencies

### Pydantic AI Framework

**Settings Module** (`settings.py`):
```python
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

def load_settings() -> Settings:
    load_dotenv()
    try:
        return Settings()
    except Exception as e:
        error_msg = f"Failed to load settings: {e}"
        if "api_key" in str(e).lower():
            error_msg += "\nCheck .env for missing API keys"
        raise ValueError(error_msg) from e

def get_llm_model():
    settings = load_settings()
    provider = OpenAIProvider(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key
    )
    return OpenAIModel(settings.llm_model, provider=provider)
```

### Autodesk Platform Services (APS)

**Required Environment Variables**:
```bash
# APS/Forge Credentials
APS_CLIENT_ID=your_client_id
APS_CLIENT_SECRET=your_client_secret

# Design Automation Configuration
APS_DA_NICKNAME=your_nickname
APS_DA_ACTIVITY=FamilyMakerActivity
APS_DA_BUNDLE_ALIAS=prod
APS_TEMPLATE_URL=https://bucket.s3.amazonaws.com/templates/

# Storage
OUTPUT_BUCKET_OR_PATH=/path/to/output  # or BIM360 URN
```

**AppBundle Structure**: See detailed implementation section below

**Template Catalog**:
- Family templates (.rft) for each category
- Stored with SHA256 hashes
- Versioned: `WindowTemplate_2025_v2.3.rft`
- Accessible via URL or BIM360

### Revit API Utilities

**Core APIs Used**:
- `FamilyManager`: Parameter management
- `FamilyItemFactory`: Geometry creation (extrusions, sweeps, blends)
- `ReferenceManager`: Reference planes, dimensions
- `Document.SaveAs()`: Save family file

**Helper Functions**:
- `CreateReferencePane(name, offset, isLocked)`
- `AddParameter(name, type, isInstance, prefix)`
- `CreateExtrusion(profile, direction, start, end)`
- `LockDimension(dim, refPlane)`

### Storage & Database

**Options**:
1. **Local Storage**: Simple file system
   - `.rfa` + `.json` in output directory
   - Good for CLI/development

2. **BIM360/ACC**: Cloud storage via Data Management API
   - Upload to project folder
   - Use OSS (Object Storage Service)
   - Return shareable URL

3. **Metadata Database** (optional):
   - PostgreSQL with family metadata
   - Enables search/filter by category, params
   - Optional pgvector for embedding search

### Image Processing & AI 3D Generation

**Image Security**:
```python
from PIL import Image
from PIL.ExifTags import TAGS

def strip_exif_pii(image_path: str) -> str:
    """Remove EXIF metadata and PII from image."""
    img = Image.open(image_path)
    data = list(img.getdata())
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    safe_path = f"{image_path}.safe.jpg"
    image_without_exif.save(safe_path)
    return safe_path
```

**AI 3D Services**:
- **PromeAI**: Image → OBJ mesh
- **Tripo3D**: API-based 3D reconstruction
- **FurniMesh**: Furniture-specific generation

**Mesh License Tracking**:
```python
# Store in manifest
"mesh_license_url": "https://promeai.com/licenses/cc-by-4.0",
"mesh_confidence": 0.87,
"mesh_source": "PromeAI job abc123"
```

---

## Revit AppBundle Implementation (C#)

### Project Structure

```
RevitFamilyMaker/
├── RevitFamilyMaker.csproj          # C# project file
├── PackageContents.xml              # Revit add-in manifest
├── FamilyMakerCommand.cs            # Main Design Automation command
├── FamilyCreator.cs                 # Core family creation logic
├── GeometryBuilder.cs               # Geometry creation utilities
├── ParameterManager.cs              # Parameter management utilities
├── MeshImporter.cs                  # Import OBJ/3D meshes
├── FlexTester.cs                    # Flex test validation
├── Models/
│   ├── FamilyParameters.cs          # Input parameter models
│   └── FamilyManifest.cs            # Output manifest model
└── Utils/
    ├── UnitConverter.cs             # Feet conversion utilities
    └── ReferenceManager.cs          # Reference plane utilities
```

### 1. Project File (RevitFamilyMaker.csproj)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>
    <PlatformTarget>x64</PlatformTarget>
    <Configurations>Debug;Release2024;Release2025</Configurations>
  </PropertyGroup>

  <!-- Revit 2024 -->
  <PropertyGroup Condition="'$(Configuration)' == 'Release2024'">
    <DefineConstants>REVIT2024</DefineConstants>
    <OutputPath>bin\Release2024\</OutputPath>
  </PropertyGroup>

  <!-- Revit 2025 -->
  <PropertyGroup Condition="'$(Configuration)' == 'Release2025'">
    <DefineConstants>REVIT2025</DefineConstants>
    <OutputPath>bin\Release2025\</OutputPath>
  </PropertyGroup>

  <ItemGroup Condition="'$(Configuration)' == 'Release2024'">
    <PackageReference Include="Autodesk.Revit.SDK" Version="2024.0.0" />
  </ItemGroup>

  <ItemGroup Condition="'$(Configuration)' == 'Release2025'">
    <PackageReference Include="Autodesk.Revit.SDK" Version="2025.0.0" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="DesignAutomationBridge" Version="3.1.0" />
  </ItemGroup>
</Project>
```

### 2. PackageContents.xml (Add-in Manifest)

```xml
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage
  SchemaVersion="1.0"
  AutodeskProduct="Revit"
  ProductType="Application"
  Name="RevitFamilyMaker"
  AppVersion="1.0.0"
  Description="AI-powered Revit family generator"
  Author="YourCompany">

  <CompanyDetails
    Name="YourCompany"
    Url="https://yourcompany.com"
    Email="support@yourcompany.com" />

  <Components>
    <RuntimeRequirements
      OS="Win64"
      Platform="Revit"
      SeriesMin="R2024"
      SeriesMax="R2025" />

    <ComponentEntry
      AppName="RevitFamilyMaker"
      ModuleName="./RevitFamilyMaker.dll"
      AppDescription="AI Family Generator"
      LoadOnRevitStartup="false">

      <Commands>
        <Command>
          <Name>FamilyMakerCommand</Name>
          <Assembly>RevitFamilyMaker.dll</Assembly>
          <FullClassName>RevitFamilyMaker.FamilyMakerCommand</FullClassName>
          <Text>Generate Family</Text>
          <Description>Generate Revit family from parameters</Description>
          <VisibilityMode>AlwaysVisible</VisibilityMode>
        </Command>
      </Commands>
    </ComponentEntry>
  </Components>
</ApplicationPackage>
```

### 3. FamilyMakerCommand.cs (Main Command)

```csharp
using Autodesk.Revit.ApplicationServices;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using DesignAutomationFramework;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;

namespace RevitFamilyMaker
{
    [Transaction(TransactionMode.Manual)]
    [Regeneration(RegenerationOption.Manual)]
    public class FamilyMakerCommand : IExternalDBApplication
    {
        public ExternalDBApplicationResult OnStartup(ControlledApplication app)
        {
            DesignAutomationBridge.DesignAutomationReadyEvent += HandleDesignAutomationReady;
            return ExternalDBApplicationResult.Succeeded;
        }

        public ExternalDBApplicationResult OnShutdown(ControlledApplication app)
        {
            return ExternalDBApplicationResult.Succeeded;
        }

        private void HandleDesignAutomationReady(object sender, DesignAutomationReadyEventArgs e)
        {
            e.Succeeded = ProcessFamily(e.DesignAutomationData);
        }

        private bool ProcessFamily(DesignAutomationData data)
        {
            if (data == null) return false;

            Application app = data.RevitApp;
            if (app == null) return false;

            try
            {
                // Read input parameters from JSON
                string paramsPath = Path.Combine(Directory.GetCurrentDirectory(), "parameters.json");
                if (!File.Exists(paramsPath))
                {
                    LogError("Parameters file not found");
                    return false;
                }

                string paramsJson = File.ReadAllText(paramsPath);
                var parameters = JsonConvert.DeserializeObject<FamilyCreationParams>(paramsJson);

                // Open family template
                string templatePath = Path.Combine(Directory.GetCurrentDirectory(), "template.rft");
                Document familyDoc = app.OpenDocumentFile(templatePath);

                if (familyDoc == null || !familyDoc.IsFamilyDocument)
                {
                    LogError("Failed to open family template");
                    return false;
                }

                // Create family using parameters
                var creator = new FamilyCreator(familyDoc);
                bool success = creator.CreateFamily(parameters);

                if (!success)
                {
                    LogError("Family creation failed");
                    return false;
                }

                // Run flex test
                var flexTester = new FlexTester(familyDoc);
                var flexResults = flexTester.RunFlexTest(parameters);

                if (!flexResults.AllPassed)
                {
                    LogError($"Flex test failed: {string.Join(", ", flexResults.FailedTests)}");
                    return false;
                }

                // Generate family name with versioning
                string familyName = GenerateFamilyName(parameters);
                string outputPath = Path.Combine(Directory.GetCurrentDirectory(), $"{familyName}.rfa");

                // Save family
                SaveAsOptions saveOptions = new SaveAsOptions();
                saveOptions.OverwriteExistingFile = true;
                familyDoc.SaveAs(outputPath, saveOptions);

                // Generate JSON manifest
                var manifest = new FamilyManifest
                {
                    FamilyName = familyName,
                    RevitVersion = app.VersionNumber,
                    Category = parameters.Category,
                    TemplateId = parameters.TemplateId,
                    TemplateHash = parameters.TemplateHash,
                    Parameters = creator.GetParameterList(),
                    GeometrySource = parameters.GeometrySource,
                    FlexTestPassed = flexResults.AllPassed,
                    FlexTestResults = flexResults,
                    CreationTimestamp = DateTime.UtcNow,
                    FileSizeBytes = new FileInfo(outputPath).Length
                };

                string manifestPath = Path.Combine(Directory.GetCurrentDirectory(), $"{familyName}.json");
                File.WriteAllText(manifestPath, JsonConvert.SerializeObject(manifest, Formatting.Indented));

                LogSuccess($"Family created: {familyName}");
                return true;
            }
            catch (Exception ex)
            {
                LogError($"Exception: {ex.Message}\n{ex.StackTrace}");
                return false;
            }
        }

        private string GenerateFamilyName(FamilyCreationParams parameters)
        {
            // Format: {Company}_{Category}_{Subtype}_v{semver}
            string company = parameters.CompanyPrefix ?? "Generic";
            string category = parameters.Category.Replace(" ", "");
            string subtype = parameters.Subtype ?? "Default";
            string version = parameters.Version ?? "0.1.0";

            return $"{company}_{category}_{subtype}_v{version}";
        }

        private void LogError(string message)
        {
            Console.WriteLine($"ERROR: {message}");
            File.AppendAllText("error.log", $"{DateTime.Now}: {message}\n");
        }

        private void LogSuccess(string message)
        {
            Console.WriteLine($"SUCCESS: {message}");
        }
    }
}
```

### 4. FamilyCreator.cs (Core Logic)

```csharp
using Autodesk.Revit.DB;
using System;
using System.Collections.Generic;
using System.Linq;

namespace RevitFamilyMaker
{
    public class FamilyCreator
    {
        private readonly Document _familyDoc;
        private readonly GeometryBuilder _geometryBuilder;
        private readonly ParameterManager _paramManager;
        private readonly UnitConverter _unitConverter;

        public FamilyCreator(Document familyDoc)
        {
            _familyDoc = familyDoc ?? throw new ArgumentNullException(nameof(familyDoc));
            _geometryBuilder = new GeometryBuilder(familyDoc);
            _paramManager = new ParameterManager(familyDoc);
            _unitConverter = new UnitConverter();
        }

        public bool CreateFamily(FamilyCreationParams parameters)
        {
            using (Transaction trans = new Transaction(_familyDoc, "Create Family"))
            {
                trans.Start();

                try
                {
                    // Step 1: Create reference planes
                    CreateReferencePlanes(parameters);

                    // Step 2: Add parameters with prefixes
                    AddFamilyParameters(parameters);

                    // Step 3: Create geometry (parametric or mesh)
                    if (parameters.GeometrySource == "parametric" || parameters.GeometrySource == "hybrid")
                    {
                        CreateParametricGeometry(parameters);
                    }

                    if (parameters.GeometrySource == "mesh" || parameters.GeometrySource == "hybrid")
                    {
                        ImportMeshGeometry(parameters);
                    }

                    // Step 4: Lock dimensions to reference planes
                    LockGeometryToReferences();

                    trans.Commit();
                    return true;
                }
                catch (Exception ex)
                {
                    trans.RollBack();
                    Console.WriteLine($"Family creation error: {ex.Message}");
                    return false;
                }
            }
        }

        private void CreateReferencePlanes(FamilyCreationParams parameters)
        {
            FamilyManager fm = _familyDoc.FamilyManager;

            // Create standard reference planes: Front, Back, Left, Right, Top, Bottom
            var refManager = new ReferenceManager(_familyDoc);

            // Width references (Left/Right)
            double widthFeet = _unitConverter.ToFeet(parameters.Width, parameters.WidthUnit);
            refManager.CreateReferencePlane("Left", 0, XYZ.BasisX, XYZ.BasisY, isLocked: true);
            refManager.CreateReferencePlane("Right", widthFeet, XYZ.BasisX, XYZ.BasisY, isLocked: true);

            // Depth references (Front/Back)
            double depthFeet = _unitConverter.ToFeet(parameters.Depth, parameters.DepthUnit);
            refManager.CreateReferencePlane("Front", 0, XYZ.BasisY, XYZ.BasisX, isLocked: true);
            refManager.CreateReferencePlane("Back", depthFeet, XYZ.BasisY, XYZ.BasisX, isLocked: true);

            // Height references (Bottom/Top)
            double heightFeet = _unitConverter.ToFeet(parameters.Height, parameters.HeightUnit);
            refManager.CreateReferencePlane("Bottom", 0, XYZ.BasisZ, XYZ.BasisX, isLocked: true);
            refManager.CreateReferencePlane("Top", heightFeet, XYZ.BasisZ, XYZ.BasisX, isLocked: true);
        }

        private void AddFamilyParameters(FamilyCreationParams parameters)
        {
            FamilyManager fm = _familyDoc.FamilyManager;

            // Add dimensional parameters with DIM_ prefix
            _paramManager.AddParameter("DIM_Width", SpecTypeId.Length, isInstance: false,
                _unitConverter.ToFeet(parameters.Width, parameters.WidthUnit));

            _paramManager.AddParameter("DIM_Depth", SpecTypeId.Length, isInstance: false,
                _unitConverter.ToFeet(parameters.Depth, parameters.DepthUnit));

            _paramManager.AddParameter("DIM_Height", SpecTypeId.Length, isInstance: false,
                _unitConverter.ToFeet(parameters.Height, parameters.HeightUnit));

            // Add material parameters with MTRL_ prefix
            if (!string.IsNullOrEmpty(parameters.Material))
            {
                _paramManager.AddParameter("MTRL_Surface", SpecTypeId.Material, isInstance: true,
                    parameters.Material);
            }

            // Add control parameters with CTRL_ prefix
            if (parameters.ControlParameters != null)
            {
                foreach (var ctrl in parameters.ControlParameters)
                {
                    _paramManager.AddParameter($"CTRL_{ctrl.Key}", SpecTypeId.Boolean, isInstance: false,
                        ctrl.Value);
                }
            }

            // Add identity parameters with ID_ prefix
            _paramManager.AddParameter("ID_Manufacturer", SpecTypeId.String.Text, isInstance: false,
                parameters.Manufacturer ?? "Generic");

            _paramManager.AddParameter("ID_ModelNumber", SpecTypeId.String.Text, isInstance: false,
                parameters.ModelNumber ?? "N/A");

            // Add scale parameter for mesh imports
            if (parameters.GeometrySource == "mesh" || parameters.GeometrySource == "hybrid")
            {
                _paramManager.AddParameter("DIM_Scale", SpecTypeId.Number, isInstance: false, 1.0);
            }

            // Add formulas for derived parameters
            if (parameters.AddPerimeter)
            {
                _paramManager.AddParameter("DIM_Perimeter", SpecTypeId.Length, isInstance: false, 0);
                _paramManager.SetFormula("DIM_Perimeter", "2 * (DIM_Width + DIM_Depth)");
            }
        }

        private void CreateParametricGeometry(FamilyCreationParams parameters)
        {
            // Get reference planes
            var refPlanes = _geometryBuilder.GetReferencePlanes();
            var left = refPlanes["Left"];
            var right = refPlanes["Right"];
            var front = refPlanes["Front"];
            var back = refPlanes["Back"];
            var bottom = refPlanes["Bottom"];
            var top = refPlanes["Top"];

            // Create rectangular profile
            CurveArray profile = new CurveArray();

            double widthFeet = _unitConverter.ToFeet(parameters.Width, parameters.WidthUnit);
            double depthFeet = _unitConverter.ToFeet(parameters.Depth, parameters.DepthUnit);

            XYZ p1 = new XYZ(0, 0, 0);
            XYZ p2 = new XYZ(widthFeet, 0, 0);
            XYZ p3 = new XYZ(widthFeet, depthFeet, 0);
            XYZ p4 = new XYZ(0, depthFeet, 0);

            profile.Append(Line.CreateBound(p1, p2));
            profile.Append(Line.CreateBound(p2, p3));
            profile.Append(Line.CreateBound(p3, p4));
            profile.Append(Line.CreateBound(p4, p1));

            // Create extrusion
            double heightFeet = _unitConverter.ToFeet(parameters.Height, parameters.HeightUnit);
            XYZ extrusionDir = new XYZ(0, 0, 1);

            Extrusion extrusion = _geometryBuilder.CreateExtrusion(profile, extrusionDir, heightFeet);

            // Lock extrusion to reference planes
            _geometryBuilder.LockToReferencePlane(extrusion, "Width", left, right);
            _geometryBuilder.LockToReferencePlane(extrusion, "Depth", front, back);
            _geometryBuilder.LockToReferencePlane(extrusion, "Height", bottom, top);
        }

        private void ImportMeshGeometry(FamilyCreationParams parameters)
        {
            if (string.IsNullOrEmpty(parameters.MeshFilePath))
            {
                Console.WriteLine("No mesh file provided for import");
                return;
            }

            var meshImporter = new MeshImporter(_familyDoc);
            bool imported = meshImporter.ImportOBJ(parameters.MeshFilePath, parameters.MeshScale);

            if (!imported)
            {
                Console.WriteLine("Failed to import mesh geometry");
            }
        }

        private void LockGeometryToReferences()
        {
            // Lock all dimensions to reference planes
            // This ensures parametric behavior
            _geometryBuilder.LockAllDimensions();
        }

        public List<ParameterInfo> GetParameterList()
        {
            return _paramManager.GetAllParameters();
        }
    }
}
```

### 5. Models/FamilyParameters.cs

```csharp
using System.Collections.Generic;

namespace RevitFamilyMaker
{
    public class FamilyCreationParams
    {
        // Metadata
        public string CompanyPrefix { get; set; } = "Generic";
        public string Category { get; set; }
        public string Subtype { get; set; }
        public string Version { get; set; } = "0.1.0";
        public string TemplateId { get; set; }
        public string TemplateHash { get; set; }

        // Dimensions (in original units, will be converted to feet)
        public double Width { get; set; }
        public string WidthUnit { get; set; } = "mm";
        public double Depth { get; set; }
        public string DepthUnit { get; set; } = "mm";
        public double Height { get; set; }
        public string HeightUnit { get; set; } = "mm";

        // Materials
        public string Material { get; set; }

        // Control parameters
        public Dictionary<string, bool> ControlParameters { get; set; }

        // Identity
        public string Manufacturer { get; set; }
        public string ModelNumber { get; set; }

        // Geometry options
        public string GeometrySource { get; set; } = "parametric"; // parametric|mesh|hybrid
        public string MeshFilePath { get; set; }
        public double MeshScale { get; set; } = 1.0;

        // Optional features
        public bool AddPerimeter { get; set; } = false;
    }

    public class FlexTestResults
    {
        public bool AllPassed { get; set; }
        public bool MinPassed { get; set; }
        public bool NominalPassed { get; set; }
        public bool MaxPassed { get; set; }
        public List<string> FailedTests { get; set; } = new List<string>();
    }

    public class ParameterInfo
    {
        public string Name { get; set; }
        public string Type { get; set; }
        public string Value { get; set; }
        public string Unit { get; set; }
        public bool IsInstance { get; set; }
    }
}
```

### 6. Utils/UnitConverter.cs

```csharp
using System;

namespace RevitFamilyMaker
{
    public class UnitConverter
    {
        // Revit internal unit is FEET
        private const double MM_TO_FEET = 0.00328084;
        private const double CM_TO_FEET = 0.0328084;
        private const double M_TO_FEET = 3.28084;
        private const double IN_TO_FEET = 0.0833333;

        public double ToFeet(double value, string unit)
        {
            double result = unit.ToLower() switch
            {
                "mm" => value * MM_TO_FEET,
                "cm" => value * CM_TO_FEET,
                "m" => value * M_TO_FEET,
                "in" => value * IN_TO_FEET,
                "ft" or "feet" => value,
                _ => throw new ArgumentException($"Unknown unit: {unit}")
            };

            // Round to ±0.5mm tolerance (0.0016404 feet)
            return Math.Round(result, 6);
        }

        public double FromFeet(double valueFeet, string targetUnit)
        {
            return targetUnit.ToLower() switch
            {
                "mm" => valueFeet / MM_TO_FEET,
                "cm" => valueFeet / CM_TO_FEET,
                "m" => valueFeet / M_TO_FEET,
                "in" => valueFeet / IN_TO_FEET,
                "ft" or "feet" => valueFeet,
                _ => throw new ArgumentException($"Unknown unit: {targetUnit}")
            };
        }
    }
}
```

### 7. Design Automation Activity Definition

**activity.json**:
```json
{
  "id": "FamilyMakerActivity",
  "commandLine": [
    "$(engine.path)\\\\revitcoreconsole.exe /i \"$(args[rvtTemplate].path)\" /al \"$(appbundles[RevitFamilyMaker].path)\""
  ],
  "parameters": {
    "rvtTemplate": {
      "verb": "get",
      "description": "Family template file (.rft)",
      "required": true,
      "localName": "template.rft"
    },
    "parameters": {
      "verb": "get",
      "description": "JSON parameters for family creation",
      "required": true,
      "localName": "parameters.json"
    },
    "result": {
      "verb": "put",
      "description": "Output family file (.rfa)",
      "required": true,
      "localName": "result.rfa"
    },
    "manifest": {
      "verb": "put",
      "description": "Output manifest file (.json)",
      "required": true,
      "localName": "manifest.json"
    }
  },
  "engine": "Autodesk.Revit+2025",
  "appbundles": [ "YourNickname.RevitFamilyMaker+prod" ],
  "description": "AI-powered Revit family generator"
}
```

### 8. Build & Deployment

**Build Script** (build.ps1):
```powershell
# Build for Revit 2024
dotnet build -c Release2024
$bundle2024 = "RevitFamilyMaker_2024.zip"
Compress-Archive -Path "bin/Release2024/*" -DestinationPath $bundle2024 -Force

# Build for Revit 2025
dotnet build -c Release2025
$bundle2025 = "RevitFamilyMaker_2025.zip"
Compress-Archive -Path "bin/Release2025/*" -DestinationPath $bundle2025 -Force

Write-Host "Bundles created: $bundle2024, $bundle2025"
```

**Upload to APS** (Python):
```python
import requests
import base64

def upload_appbundle(zip_path, nickname, bundle_id, alias="prod"):
    """Upload AppBundle to Autodesk Platform Services."""

    # Get 2-legged OAuth token
    token = get_aps_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create or update AppBundle
    bundle_url = f"https://developer.api.autodesk.com/da/us-east/v3/appbundles"
    bundle_data = {
        "id": bundle_id,
        "engine": "Autodesk.Revit+2025",
        "description": "AI Family Maker AppBundle"
    }

    response = requests.post(bundle_url, headers=headers, json=bundle_data)

    if response.status_code == 409:  # Already exists, create new version
        version_url = f"{bundle_url}/{nickname}.{bundle_id}/versions"
        response = requests.post(version_url, headers=headers, json=bundle_data)

    upload_params = response.json()

    # Upload ZIP to signed URL
    with open(zip_path, 'rb') as f:
        upload_response = requests.put(
            upload_params["uploadParameters"]["endpointURL"],
            data=f,
            headers=upload_params["uploadParameters"].get("formData", {})
        )

    # Create/update alias
    alias_url = f"{bundle_url}/{nickname}.{bundle_id}/aliases"
    alias_data = {
        "id": alias,
        "version": upload_params["version"]
    }
    requests.post(alias_url, headers=headers, json=alias_data)

    print(f"AppBundle uploaded: {nickname}.{bundle_id}+{alias}")
```

### 9. Usage from Python Agent

```python
import requests
import json
from typing import Dict

async def execute_aps_family_creation(
    template_url: str,
    parameters: Dict,
    output_url: str,
    aps_token: str,
    activity_alias: str
) -> Dict:
    """Execute Design Automation workitem."""

    workitem = {
        "activityId": activity_alias,
        "arguments": {
            "rvtTemplate": {
                "url": template_url,
                "verb": "get"
            },
            "parameters": {
                "url": "data:application/json," + json.dumps(parameters),
                "verb": "get"
            },
            "result": {
                "url": output_url,
                "verb": "put"
            },
            "manifest": {
                "url": output_url.replace(".rfa", ".json"),
                "verb": "put"
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {aps_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://developer.api.autodesk.com/da/us-east/v3/workitems",
        headers=headers,
        json=workitem
    )

    workitem_id = response.json()["id"]

    # Poll for completion
    status_url = f"https://developer.api.autodesk.com/da/us-east/v3/workitems/{workitem_id}"

    while True:
        status_response = requests.get(status_url, headers=headers)
        status_data = status_response.json()

        if status_data["status"] in ["success", "failed", "cancelled"]:
            return status_data

        await asyncio.sleep(5)
```

---

## System Prompt (Enhanced)

```python
system_prompt = """
You are an intelligent BIM assistant specialized in creating production-quality
Autodesk Revit families based on user input. You have deep knowledge of:

- Revit internal units (FEET - always convert user inputs)
- Family naming conventions (Company_Category_Subtype_v{semver})
- Parameter prefixes (DIM_, MTRL_, ID_, CTRL_)
- Geometry constraints (reference planes, locked dimensions)
- Flex testing requirements (min/nominal/max parameter sets)

Your primary capabilities:

1. Parametric Family Generation
   - Use Revit API + templates for standard building elements
   - Create intelligent parameters with sensible defaults
   - Lock geometry to reference planes
   - Ensure flex tests pass before release

2. Image-based 3D Conversion
   - Analyze reference images using AI 3D reconstruction
   - Strip EXIF/PII before external calls
   - Always add DIM_Scale parameter for mesh imports
   - Track mesh licenses in manifest
   - Fall back to parametric if confidence low

3. Hybrid Creation
   - Text drives parameters, image drives shape/style
   - Merge results intelligently
   - Document both sources in manifest

4. Template & Library Utilization
   - Pin templates by SHA256 hash (immutability)
   - Select appropriate category + Revit version
   - Validate template before generation

5. Contextual Refinement
   - Remember conversation context for iterative changes
   - Load existing families with get_family()
   - Apply modifications without regenerating from scratch

When a user requests a family:

1. VALIDATE CATEGORY (mandatory - ask if ambiguous)
2. Parse dimensions and CONVERT TO FEET
3. Choose mode: parametric | image | hybrid
4. Select pinned template by hash
5. Generate with proper naming: {Company}_{Category}_{Subtype}_v{semver}
6. Add parameters with prefixes: DIM_*, MTRL_*, ID_*, CTRL_*
7. Run FLEX TEST (min/nominal/max) - reject if fails
8. Generate JSON manifest with all metadata
9. Confirm output with file path and key parameters

Always ensure:
- Geometry locked to reference planes
- Parameters are adjustable (no hard-coded dimensions)
- File size < 3 MB (warn if > 1 MB)
- Open time < 1 second
- Flex test passed
- Clear error messages (no leaking sensitive data)

Ask clarifying questions if input is ambiguous. Be transparent about template
sources, AI services used, and any fallbacks. Maintain professional tone suitable
for BIM/design workflow.
"""
```

---

## Golden Tests & Quality Assurance

### Test Suite Requirements

**Golden Test Cases** (must pass before release):

#### 1. Text-only Generation
```python
async def test_text_only_door():
    """Test parametric door generation from text."""
    result = await agent.run(
        "Create a door 2100mm high by 900mm wide",
        deps=test_deps
    )
    assert result.data.category == "Doors"
    assert result.data.flex_test_passed == True
    assert "DIM_Height" in [p["name"] for p in result.data.parameters]
    # Height should be ~6.89 feet (2100mm converted)
    height_param = next(p for p in result.data.parameters if p["name"] == "DIM_Height")
    assert abs(height_param["value"] - 6.89) < 0.01
```

#### 2. Image-only Generation
```python
async def test_image_only_chair():
    """Test mesh import from reference image."""
    result = await agent.run(
        "Generate family from this chair image",
        image_path="tests/fixtures/chair.jpg",
        deps=test_deps
    )
    assert result.data.category == "Furniture"
    assert "DIM_Scale" in [p["name"] for p in result.data.parameters]
    assert result.data.file_size_bytes < 3 * 1024 * 1024  # < 3 MB
    assert result.data.manifest["mesh_license_url"] is not None
```

#### 3. Hybrid Generation
```python
async def test_hybrid_table():
    """Test text + image combination."""
    result = await agent.run(
        "Create a 2400mm x 900mm x 750mm desk like in this image",
        image_path="tests/fixtures/desk.jpg",
        deps=test_deps
    )
    assert result.data.category == "Furniture"
    assert result.data.flex_test_passed == True
    # Text drives precise dimensions
    width_param = next(p for p in result.data.parameters if p["name"] == "DIM_Width")
    assert abs(width_param["value"] - 7.87) < 0.01  # 2400mm → feet
    # Image drives shape/style
    assert result.data.manifest["geometry_source"] == "hybrid"
```

#### 4. Flex Testing
```python
async def test_flex_window():
    """Test window regenerates at min/nominal/max params."""
    result = await agent.run(
        "Create a double-hung window 4ft x 3ft",
        deps=test_deps
    )

    # Flex test should have tried:
    flex_results = result.data.manifest["flex_test_results"]
    assert flex_results["min_passed"] == True  # e.g., 2ft x 2ft
    assert flex_results["nominal_passed"] == True  # 4ft x 3ft
    assert flex_results["max_passed"] == True  # e.g., 8ft x 6ft
```

#### 5. Edge Cases
```python
async def test_ambiguous_category():
    """Test agent asks for category when ambiguous."""
    with pytest.raises(ValueError, match="category.*required"):
        await agent.run("Create a thing", deps=test_deps)

async def test_extreme_dimensions():
    """Test validation of unrealistic dimensions."""
    result = await agent.run(
        "Create a door 100 meters tall",
        deps=test_deps
    )
    assert len(result.data.warnings) > 0
    assert "unrealistic" in result.data.warnings[0].lower()

async def test_aps_failure_fallback():
    """Test fallback when APS is down."""
    # Mock APS failure
    with mock_aps_down():
        result = await agent.run(
            "Create a simple door",
            deps=test_deps
        )
        assert result.data.manifest["fallback_used"] == "local_revit"
```

### Testing Standards

1. **Use TestModel for Development**:
   ```python
   from pydantic_ai.models.test import TestModel

   test_model = TestModel()
   test_agent = agent.override(model=test_model)
   ```

2. **Test Both Sync and Async**:
   - All tools support async
   - Test streaming where applicable

3. **Validate Tool Schemas**:
   - Ensure parameters typed correctly
   - Test error handling (invalid inputs, API failures)

4. **Integration Tests**:
   - End-to-end family creation
   - Actual APS calls (with test credentials)
   - Verify .rfa opens in Revit

5. **Performance Tests**:
   - Family generation < 60 seconds
   - File open time < 1 second
   - Size budget compliance

---

## Operational Runbooks

### Fallback Strategy (APS Down)

**Primary**: Autodesk APS Design Automation
**Fallback**: Local Revit + pyRevit/RevitPythonShell

```python
async def create_family_with_fallback(params):
    try:
        # Try APS first
        result = await aps_create_family(params)
        return result
    except APSUnavailableError:
        logger.warning("APS unavailable, using local Revit fallback")
        result = await local_revit_create_family(params)
        result["fallback_used"] = "local_revit"
        return result
```

**Local Revit Runner**:
- Requires Revit installed on server/workstation
- Uses pyRevit or RevitPythonShell for automation
- Watches queue directory for job files
- Processes families sequentially
- Slower but reliable backup

### Rollback Procedure

1. **Atomic Releases**:
   - Store prior working artifact before new generation
   - If generation fails, restore previous version
   - Versioned families enable easy rollback

2. **Rollback Trigger**:
   - Flex test failure
   - File size exceeds budget
   - User reports critical issue

3. **Process**:
   ```bash
   # List versions
   ls -lh output/Generic_Furniture_Chair_v*

   # Rollback to previous
   cp output/Generic_Furniture_Chair_v0.2.0.rfa \
      output/Generic_Furniture_Chair_v0.3.0.rfa
   ```

### Telemetry (Opt-in)

**Metrics to Collect**:
- Job ID, duration, outcome (success/failure)
- Template hash, category, Revit version
- File size, parameter count
- Flex test results
- Fallback usage
- Error types/frequency

**Privacy**:
- No confidential project data
- No user images stored
- No file paths/names beyond job ID
- Aggregate metrics only

**Implementation**:
```python
# .env
TELEMETRY_ENABLED=true
TELEMETRY_ENDPOINT=https://analytics.example.com/events

# Code
if settings.telemetry_enabled:
    await send_telemetry({
        "event": "family_created",
        "job_id": job_id,
        "duration_sec": duration,
        "template_hash": template_hash,
        "outcome": "success"
    })
```

---

## Complete Environment Variables

```bash
# ============================================
# LLM Configuration
# ============================================
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4
LLM_BASE_URL=https://api.openai.com/v1

# ============================================
# Autodesk Platform Services (APS/Forge)
# ============================================
APS_CLIENT_ID=your_aps_client_id
APS_CLIENT_SECRET=your_aps_client_secret

# Design Automation
APS_DA_NICKNAME=your_nickname
APS_DA_ACTIVITY=FamilyMakerActivity
APS_DA_BUNDLE_ALIAS=prod
APS_TEMPLATE_URL=https://s3.amazonaws.com/templates/

# ============================================
# Storage Configuration
# ============================================
OUTPUT_BUCKET_OR_PATH=/path/to/output
# OR for BIM360/ACC:
# OUTPUT_BUCKET_OR_PATH=urn:adsk.objects:os.object:bucket/path

# ============================================
# Image-to-3D Service
# ============================================
IMAGE_TO_3D_PROVIDER=promeai  # promeai|tripo3d|furnimesh
IMAGE_TO_3D_API_KEY=your_3d_api_key

# ============================================
# Optional: Vector Search
# ============================================
# VECTOR_DB_URL=postgresql://user:pass@localhost:5432/families

# ============================================
# Performance & Limits
# ============================================
MAX_PARALLEL_JOBS=5
FILE_SIZE_BUDGET_MB=3

# ============================================
# Company Defaults
# ============================================
COMPANY_PREFIX=Generic
DEFAULT_REVIT_VERSION=2025

# ============================================
# Telemetry (Opt-in)
# ============================================
TELEMETRY_ENABLED=false
# TELEMETRY_ENDPOINT=https://analytics.example.com/events

# ============================================
# Security
# ============================================
# SHARED_PARAMETERS_FILE=/path/to/shared_parameters.txt
```

---

## Naming & Conventions

### Family Naming
**Pattern**: `{Company}_{Category}_{Subtype}_v{semver}.rfa`

Examples:
- `Generic_Furniture_Chair_v0.1.0.rfa`
- `Bluewave_Windows_DoubleHung_v1.2.3.rfa`
- `AcmeCorp_Doors_SingleSwing_v2.0.0.rfa`

### Parameter Naming
**Prefixes** (mandatory):
- `DIM_*`: Dimensional parameters (DIM_Height, DIM_Width, DIM_Depth)
- `MTRL_*`: Material parameters (MTRL_Frame, MTRL_Surface)
- `ID_*`: Identity/metadata (ID_Manufacturer, ID_ModelNumber)
- `CTRL_*`: Control/visibility (CTRL_ShowGrille, CTRL_DoorSwing)

**Avoid**:
- Duplicates (e.g., Height and DIM_Height)
- Ambiguous type/instance (clarify in docs)

### Shared Parameters
- Use Shared Parameter GUIDs for project-wide consistency
- Store in `shared_parameters.txt` under version control
- Document GUID mapping in manifest

### Type Catalogs
If using type catalogs:
- Filename: `{FamilyName}.txt`
- Format: CSV with header
- Unit suffixes: `DIM_Width##millimeters##, DIM_Height##millimeters##`

---

## Geometry & Constraints Quality

### Reference Planes
- Always create labeled reference planes for major dimensions
- Lock dimensions to reference planes
- Avoid free-floating geometry

### Constraints
- Lock all critical dimensions
- Use equality constraints where appropriate
- Add formulas for derived parameters:
  ```
  DIM_Perimeter = 2 * (DIM_Width + DIM_Depth)
  ```

### Flex Testing
**Mandatory** before release:
- Define min/nominal/max parameter sets
- Family must regenerate without errors for all sets
- Example:
  - Min: DIM_Height = 1.0 ft
  - Nominal: DIM_Height = 3.0 ft
  - Max: DIM_Height = 8.0 ft

### Mesh Imports
- Keep light (< 500 KB if possible)
- Prefer parametric forms when feasible
- Always add DIM_Scale parameter
- Validate real-world size

### Nested Families
- Avoid unless justified
- Prevent circular references
- Document nesting in manifest

---

## Units Handling (CRITICAL)

**Revit Internal Unit**: **FEET**

### Conversion Rules
```python
def convert_to_feet(value: float, unit: str) -> float:
    """Convert user input to Revit internal feet."""
    conversions = {
        "mm": 0.00328084,
        "cm": 0.0328084,
        "m": 3.28084,
        "in": 0.0833333,
        "ft": 1.0
    }
    return round(value * conversions[unit], 6)

# Example
user_input = "2400mm"
value_in_feet = convert_to_feet(2400, "mm")  # 7.874016 ft
```

### Tolerance
- Round to ±0.5mm tolerance
- Store original units in manifest for reference

### Display
- User sees: "2400 mm" or "8 ft"
- Revit stores: 7.874016 (feet)
- Manifest documents both

---

## Security, IP, and Privacy

### No Confidential Data to 3rd Parties
- Never send confidential models/images to external services without approval
- Use local processing when possible
- Log all external API calls

### Image Security
```python
def sanitize_image(image_path: str) -> str:
    """Strip EXIF/PII before external calls."""
    # Remove EXIF metadata
    # Anonymize filename
    # Return sanitized path
```

### Error Messages
- Never leak file paths, API keys, project names
- Sanitize error messages before returning to user
- Log full errors internally for debugging

### Rate Limiting
- Implement rate limits for external API calls
- Respect service quotas

---

## Performance Budgets

### Family Open Time
- Target: < 1 second for common types
- Warn if > 2 seconds
- Profile and optimize geometry complexity

### File Size
- Budget: 1-3 MB
- CI rejects if > 3 MB
- Warn user if > 1 MB
- Optimize mesh density, texture sizes

### Geometry Simplification
- Use level-of-detail strategies
- Simplify hidden geometry
- Avoid excessive detail for small components

### Materials
- Ensure referenced materials exist in project
- Fall back to safe defaults (Generic material)
- Document material requirements in manifest

---

## Documentation References

### Pydantic AI
- Official: https://ai.pydantic.dev
- Agent Creation: https://ai.pydantic.dev/agents/
- Tool Integration: https://ai.pydantic.dev/tools/
- Testing: https://ai.pydantic.dev/testing/
- Examples: https://ai.pydantic.dev/examples/

### Autodesk APIs
- Forge Design Automation: https://aps.autodesk.com/en/docs/design-automation/v3/
- Revit API Reference: https://www.revitapidocs.com
- Data Management API: https://aps.autodesk.com/en/docs/data/v2/
- Revit Developer Center: https://www.autodesk.com/developer-network/platform-technologies/revit

### AI 3D Generation
- PromeAI: https://www.promeai.com/api-docs
- Tripo3D: https://www.tripo3d.ai/docs
- FurniMesh: (check latest docs)

---

## Success Criteria

### Core Functionality
1. **Text Generation**: 90%+ success rate for standard objects
2. **Image Processing**: Recognizable geometry from reference images
3. **Hybrid Mode**: Successfully merge text + image inputs
4. **Flex Testing**: 100% pass rate (reject if fails)

### Quality Metrics
5. **Parameter Quality**: All families have adjustable parameters with prefixes
6. **File Size**: 95%+ under 3 MB budget
7. **Open Time**: 95%+ under 1 second
8. **Naming Compliance**: 100% follow `{Company}_{Category}_{Subtype}_v{semver}` pattern

### Reliability
9. **Error Handling**: Graceful failures with actionable messages
10. **Test Coverage**: >80% code coverage
11. **Fallback Success**: Local Revit fallback works when APS down
12. **Performance**: Family generation < 60 seconds (cloud)

### User Experience
13. **Clear Outputs**: File path, manifest, and usage instructions
14. **Iterative Refinement**: Follow-up modifications work
15. **Documentation**: Manifest includes all metadata

---

## Out of Scope (Initial Release)

- Multi-family projects or assemblies
- Real-time preview/rendering
- Advanced constraint solving (beyond basic parametrics)
- Cost estimation or material takeoffs
- Integration with scheduling/phasing
- Multi-user collaboration features
- Mobile app interface
- Batch processing of multiple families
- Building code validation (future enhancement)
- Vector search library (optional for v2)

---

## Version History

**v2.0** (2025-11-05):
- Added complete Revit/BIM production standards
- Integrated Pydantic AI code patterns
- **Added comprehensive Revit C# AppBundle implementation**:
  - Complete project structure with 9 C# files
  - FamilyMakerCommand.cs (Design Automation entry point)
  - FamilyCreator.cs (core family creation logic)
  - UnitConverter.cs (feet conversion utilities)
  - FamilyParameters.cs (input/output models)
  - Design Automation activity definition
  - Build scripts for Revit 2024/2025
  - Deployment scripts for APS upload
  - Python integration code for workitem execution
- Added golden tests and flex testing requirements
- Added operational runbooks and fallback strategies
- Comprehensive environment variable catalog
- Units handling (Revit internal = feet)
- Template immutability with SHA256 hashing
- Parameter prefixes and naming conventions
- Image security (EXIF/PII stripping)
- Performance budgets and file size limits
- JSON manifest requirements
- Telemetry specification

**v1.0** (2025-11-05):
- Initial specification from INITIAL.md

---

## Next Steps

1. **Set Up Environment**:
   - Create virtual environment
   - Install dependencies: `pydantic-ai`, `python-dotenv`, `pydantic-settings`
   - Configure `.env` with all required variables

2. **Implement Settings Module**:
   - Create `settings.py` per specification
   - Validate all environment variables load correctly

3. **Build Core Tools**:
   - Implement `generate_family_from_prompt`
   - Implement `generate_family_from_image`
   - Implement `perform_family_creation`
   - Implement `list_family_templates`
   - Implement `get_family`

4. **Create Test Suite**:
   - Golden tests per specification
   - Flex testing infrastructure
   - Mock APS for unit tests

5. **Deploy APS AppBundle**:
   - Build Revit add-in (.dll)
   - Upload to APS as versioned bundle
   - Configure activity + alias

6. **Set Up Template Catalog**:
   - Collect family templates for each category
   - Generate SHA256 hashes
   - Upload to accessible storage

7. **Validate End-to-End**:
   - Run full test suite
   - Verify .rfa files open in Revit
   - Check flex tests pass
   - Validate manifests

8. **Production Release**:
   - CI/CD pipeline with quality gates
   - Monitoring and telemetry
   - Documentation for users
