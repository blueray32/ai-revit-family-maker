# Dependency Specifications
## AI Revit Family Maker Assistant

**Generated**: 2025-11-05
**Philosophy**: Minimal config - essential environment variables only, single model provider, simple dataclass dependencies

---

## Essential Environment Variables

### LLM Configuration

```bash
# LLM Provider Settings
LLM_PROVIDER=openai                        # Provider name (openai for initial implementation)
LLM_API_KEY=sk-...                        # API key for LLM provider (REQUIRED)
LLM_MODEL=gpt-4                           # Model name (gpt-4, gpt-4-turbo, etc.)
LLM_BASE_URL=https://api.openai.com/v1   # Base URL for API (default: OpenAI)
```

**Required**: `LLM_API_KEY`
**Optional**: `LLM_PROVIDER`, `LLM_MODEL`, `LLM_BASE_URL` (have defaults)

---

### Autodesk Platform Services (APS/Forge)

```bash
# APS Credentials
APS_CLIENT_ID=your_aps_client_id           # Autodesk Platform Services client ID (REQUIRED)
APS_CLIENT_SECRET=your_aps_client_secret   # APS client secret (REQUIRED)

# Design Automation Configuration
APS_DA_NICKNAME=your_nickname              # Design Automation nickname (REQUIRED)
APS_DA_ACTIVITY=FamilyMakerActivity        # DA activity name (REQUIRED)
APS_DA_BUNDLE_ALIAS=prod                   # AppBundle alias (default: "prod")
APS_TEMPLATE_URL=https://bucket.s3.amazonaws.com/templates/  # Template catalog URL (REQUIRED)
```

**Required**: `APS_CLIENT_ID`, `APS_CLIENT_SECRET`, `APS_DA_NICKNAME`, `APS_DA_ACTIVITY`, `APS_TEMPLATE_URL`
**Optional**: `APS_DA_BUNDLE_ALIAS`

---

### Storage Configuration

```bash
# Output Location
OUTPUT_BUCKET_OR_PATH=/path/to/output     # Local path or BIM360 URN (REQUIRED)

# Examples:
# Local:  OUTPUT_BUCKET_OR_PATH=/Users/me/revit_families/output
# BIM360: OUTPUT_BUCKET_OR_PATH=urn:adsk.objects:os.object:bucket/path
```

**Required**: `OUTPUT_BUCKET_OR_PATH`

---

### Image-to-3D Service

```bash
# 3D Generation Provider
IMAGE_TO_3D_PROVIDER=promeai              # Provider: promeai|tripo3d|furnimesh
IMAGE_TO_3D_API_KEY=your_3d_api_key       # API key for 3D generation service (REQUIRED)
```

**Required**: `IMAGE_TO_3D_PROVIDER`, `IMAGE_TO_3D_API_KEY`

---

### Optional Configuration

```bash
# Performance & Limits (all optional with defaults)
MAX_PARALLEL_JOBS=5                        # Max concurrent APS jobs (default: 5)
FILE_SIZE_BUDGET_MB=3                      # Max .rfa file size in MB (default: 3)

# Company Defaults
COMPANY_PREFIX=Generic                     # Default company prefix (default: "Generic")
DEFAULT_REVIT_VERSION=2025                 # Default Revit version (default: "2025")

# Telemetry (opt-in, disabled by default)
TELEMETRY_ENABLED=false                    # Enable telemetry collection (default: false)
TELEMETRY_ENDPOINT=https://analytics.example.com/events  # Telemetry endpoint (if enabled)

# Optional: Vector Search (not implemented initially)
# VECTOR_DB_URL=postgresql://user:pass@localhost:5432/families
```

---

## Dependency Dataclass Structure

### RevitAgentDependencies

**Purpose**: Dependency injection for agent tools, contains all runtime configuration.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `aps_client_id` | `str` | Yes | APS client ID from env |
| `aps_client_secret` | `str` | Yes | APS client secret from env |
| `aps_activity_name` | `str` | Yes | Design Automation activity name |
| `aps_bundle_alias` | `str` | Yes | AppBundle alias (e.g., "prod") |
| `template_catalog_url` | `str` | Yes | URL to template catalog |
| `output_bucket` | `str` | Yes | Output location for .rfa files |
| `image_to_3d_api_key` | `str` | Yes | API key for 3D generation |
| `image_to_3d_provider` | `str` | Yes | Provider name (promeai, tripo3d, furnimesh) |
| `session_id` | `str \| None` | No | Optional session ID for tracking |

**Usage**:

```python
from dataclasses import dataclass

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
    image_to_3d_provider: str
    session_id: str | None = None
```

**Notes**:
- All sensitive data from environment variables
- Injected into tools via `RunContext[RevitAgentDependencies]`
- Simple dataclass (no complex logic)
- Immutable after initialization

---

## Python Package Requirements

### Core Dependencies

```txt
# Pydantic AI Framework
pydantic-ai>=0.0.13              # Core agent framework
pydantic>=2.0.0                  # Data validation
pydantic-settings>=2.0.0         # Environment variable management

# Environment Configuration
python-dotenv>=1.0.0             # .env file loading

# HTTP Clients
httpx>=0.27.0                    # Async HTTP client
requests>=2.31.0                 # Sync HTTP client (for compatibility)

# Async Support
asyncio                          # Built-in (Python 3.7+)

# Image Processing
Pillow>=10.0.0                   # Image manipulation (EXIF stripping)

# Retry Logic
tenacity>=8.2.0                  # Retry/backoff for external APIs

# Testing
pytest>=7.4.0                    # Test framework
pytest-asyncio>=0.21.0           # Async test support
pytest-mock>=3.12.0              # Mocking utilities
```

### Optional Dependencies

```txt
# Vector Search (not implemented initially)
# pgvector>=0.2.0
# psycopg2-binary>=2.9.0

# Performance Monitoring
# prometheus-client>=0.18.0

# Structured Logging
# structlog>=23.2.0
```

### Development Dependencies

```txt
# Code Quality
black>=23.0.0                    # Code formatting
ruff>=0.1.0                      # Linting
mypy>=1.7.0                      # Type checking

# Documentation
mkdocs>=1.5.0                    # Documentation generator
mkdocs-material>=9.4.0           # Material theme
```

---

## Settings Module Structure

### settings.py

**Purpose**: Load and validate all environment variables using pydantic-settings.

**Key Classes**:

1. **Settings**: Main configuration class
   - Loads from `.env` file
   - Validates required fields
   - Provides defaults for optional fields

2. **load_settings()**: Factory function
   - Calls `load_dotenv()` first
   - Creates and returns Settings instance
   - Raises clear errors if required vars missing

3. **get_llm_model()**: LLM provider factory
   - Creates OpenAIProvider from settings
   - Returns configured model for agent

**Configuration**:

```python
model_config = ConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,      # Allow lowercase env vars
    extra="ignore"             # Ignore unknown env vars
)
```

**Error Handling**:
- Raise ValueError if required API keys missing
- Provide helpful error messages with next steps
- Never log sensitive values

---

## Configuration Notes

### Security Best Practices

1. **Never commit .env files** to version control
2. **Provide .env.example** with dummy values
3. **Validate all required vars** at startup
4. **Sanitize error messages** (no credential leaks)
5. **Use least-privilege credentials** for APS

### Environment Variable Naming

- Prefix with service name: `APS_*`, `LLM_*`, `IMAGE_TO_3D_*`
- Use SCREAMING_SNAKE_CASE
- Be descriptive: `APS_CLIENT_ID` not `CLIENT_ID`
- Group related vars together

### Default Values

**Have defaults**:
- `LLM_PROVIDER="openai"`
- `LLM_MODEL="gpt-4"`
- `APS_DA_BUNDLE_ALIAS="prod"`
- `COMPANY_PREFIX="Generic"`
- `DEFAULT_REVIT_VERSION="2025"`
- `MAX_PARALLEL_JOBS=5`
- `FILE_SIZE_BUDGET_MB=3`

**No defaults** (must be provided):
- All API keys and secrets
- Service endpoints (APS_TEMPLATE_URL, OUTPUT_BUCKET_OR_PATH)
- Service identifiers (APS_DA_NICKNAME, APS_DA_ACTIVITY)

### Multi-Environment Support

**Development**:
```bash
LLM_MODEL=gpt-3.5-turbo          # Cheaper for testing
TELEMETRY_ENABLED=false
OUTPUT_BUCKET_OR_PATH=/tmp/revit_test
```

**Production**:
```bash
LLM_MODEL=gpt-4                  # Production quality
TELEMETRY_ENABLED=true
OUTPUT_BUCKET_OR_PATH=urn:adsk.objects:os.object:prod-bucket/families
```

---

## Dependency Initialization Flow

```
1. Application starts
   ↓
2. load_dotenv() - Load .env file
   ↓
3. Settings() - Validate environment variables
   ↓
4. get_llm_model() - Create LLM provider
   ↓
5. Agent() - Initialize with model and deps_type
   ↓
6. RevitAgentDependencies() - Inject into tool context
   ↓
7. Tools access via ctx.deps.*
```

---

## .env.example Template

```bash
# ============================================
# LLM Configuration (REQUIRED)
# ============================================
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-openai-api-key-here
LLM_MODEL=gpt-4
LLM_BASE_URL=https://api.openai.com/v1

# ============================================
# Autodesk Platform Services (REQUIRED)
# ============================================
APS_CLIENT_ID=your_aps_client_id
APS_CLIENT_SECRET=your_aps_client_secret
APS_DA_NICKNAME=your_nickname
APS_DA_ACTIVITY=FamilyMakerActivity
APS_DA_BUNDLE_ALIAS=prod
APS_TEMPLATE_URL=https://s3.amazonaws.com/your-bucket/templates/

# ============================================
# Storage (REQUIRED)
# ============================================
OUTPUT_BUCKET_OR_PATH=/path/to/output

# ============================================
# Image-to-3D Service (REQUIRED)
# ============================================
IMAGE_TO_3D_PROVIDER=promeai
IMAGE_TO_3D_API_KEY=your_3d_api_key

# ============================================
# Optional Configuration
# ============================================
MAX_PARALLEL_JOBS=5
FILE_SIZE_BUDGET_MB=3
COMPANY_PREFIX=Generic
DEFAULT_REVIT_VERSION=2025

# ============================================
# Telemetry (Optional)
# ============================================
TELEMETRY_ENABLED=false
# TELEMETRY_ENDPOINT=https://analytics.example.com/events
```

---

## Validation Strategy

### Startup Validation

```python
def validate_dependencies():
    """Validate all dependencies at startup."""
    try:
        settings = load_settings()
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
        print("\n🔍 Check your .env file:")
        print("  - LLM_API_KEY is required")
        print("  - APS_CLIENT_ID and APS_CLIENT_SECRET are required")
        print("  - OUTPUT_BUCKET_OR_PATH must be set")
        sys.exit(1)

    print("✅ All dependencies validated")
    return settings
```

### Runtime Validation

- Validate APS credentials on first use
- Check template catalog reachable
- Verify output location writable
- Test image-to-3D service connectivity

---

## Summary

### Required Environment Variables (9)
1. `LLM_API_KEY`
2. `APS_CLIENT_ID`
3. `APS_CLIENT_SECRET`
4. `APS_DA_NICKNAME`
5. `APS_DA_ACTIVITY`
6. `APS_TEMPLATE_URL`
7. `OUTPUT_BUCKET_OR_PATH`
8. `IMAGE_TO_3D_PROVIDER`
9. `IMAGE_TO_3D_API_KEY`

### Python Packages (Core: 8)
1. pydantic-ai
2. pydantic
3. pydantic-settings
4. python-dotenv
5. httpx
6. Pillow
7. tenacity
8. pytest (dev)

### Dependency Dataclass (1)
- `RevitAgentDependencies` (9 fields, 8 required + 1 optional)

### Configuration Modules (1)
- `settings.py` (Settings class + load_settings() + get_llm_model())

---

## Next Steps for Implementation

1. Create virtual environment: `python -m venv venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in values
4. Implement `settings.py` module
5. Test configuration loading: `python -m settings`
6. Validate all environment variables load correctly
