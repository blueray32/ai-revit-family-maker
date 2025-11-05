# AI Revit Family Maker - Quick Start Guide

Get up and running with the AI Revit Family Maker in **5 simple steps**.

---

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (choose your platform)
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate   # Windows

# Install Python packages
pip install -r requirements.txt
```

**Required packages:**
- `pydantic-ai` - AI agent framework
- `pydantic` & `pydantic-settings` - Data validation and configuration
- `httpx` - HTTP client
- `Pillow` - Image processing
- `tenacity` - Retry logic
- `pytest` - Testing framework

---

## Step 2: Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
# OpenAI API Key (required)
LLM_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
LLM_MODEL=gpt-4o-mini

# APS Credentials (required for production)
APS_CLIENT_ID=your_aps_client_id
APS_CLIENT_SECRET=your_aps_client_secret
APS_DA_ACTIVITY=your_nickname.RevitFamilyMakerActivity+production
APS_TEMPLATE_URL=https://your-storage.com/templates/

# Optional: Image-to-3D service
IMAGE_TO_3D_API_KEY=stub
IMAGE_TO_3D_ENDPOINT=https://stub.example.com
```

### Get Your OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key and paste it into `.env`

### Get Your APS Credentials

1. Go to: https://aps.autodesk.com/myapps
2. Create a new app or select existing
3. Copy **Client ID** and **Client Secret**
4. Paste into `.env`

**Use the setup wizard:**

```bash
python deployment/scripts/setup_aps.py --setup
```

This will:
- Test your APS credentials
- List existing AppBundles and Activities
- Generate the correct `.env` configuration

---

## Step 3: Test the Agent (Without APS)

Run unit tests to verify everything works:

```bash
pytest tests/ -v
```

**Expected output:** 30+ tests passing

Run a real test with the OpenAI API (stubbed APS):

```bash
python test_real_tools.py
```

This will call the agent with real prompts and show you how it parses dimensions, converts units, and generates manifests.

---

## Step 4: Deploy to Production (Optional)

If you want to generate **real Revit families** (not just stubs), you need to:

### 4.1 Build the C# AppBundle

**Requirements:** Windows, Visual Studio, .NET Framework 4.8

```powershell
cd deployment/scripts
.\build.ps1 -Configuration Release -Clean
```

This creates `RevitFamilyMaker_2024.zip` and `RevitFamilyMaker_2025.zip` in `deployment/output/`.

### 4.2 Deploy AppBundle to APS

```bash
python deployment/scripts/deploy_appbundle.py --version 2024 --alias production
```

### 4.3 Create APS Activity

Edit `deployment/aps_activity.json` and replace `{{NICKNAME}}` with your APS nickname.

Then create the activity via the APS API (use Postman, curl, or the deployment script).

### 4.4 Set Up Template Catalog

1. Obtain Revit templates (see `templates/README.md`)
2. Upload to cloud storage (S3, Azure, or APS OSS)
3. Update `APS_TEMPLATE_URL` in `.env`

**Full instructions:** See `deployment/DEPLOYMENT_GUIDE.md`

---

## Step 5: Use the Agent

### CLI Usage

```bash
python main.py "Create a modern office chair, 600mm wide, 650mm deep, 900mm tall"
```

**Expected flow:**

1. Agent asks: "What category should this be? Furniture, Equipment, or Other?"
2. You respond: "Furniture"
3. Agent parses dimensions, converts to feet
4. Agent calls the `generate_family_from_prompt` tool
5. Tool creates Revit family (or stub if APS not configured)
6. Agent returns family details:

```json
{
  "family_name": "Generic_Furniture_Default_v0.1.0",
  "file_path": "Generic_Furniture_Default_v0.1.0.rfa",
  "manifest": {
    "parameters": [
      {"name": "DIM_Width", "value": "1.96850", "unit": "feet"},
      {"name": "DIM_Depth", "value": "2.13255", "unit": "feet"},
      {"name": "DIM_Height", "value": "2.95276", "unit": "feet"}
    ],
    "flex_test_passed": true
  }
}
```

### Python API Usage

```python
from revit_family_maker.agent import create_agent
from revit_family_maker.dependencies import RevitAgentDependencies
from revit_family_maker.settings import load_settings

# Load settings
settings = load_settings()

# Create dependencies
deps = RevitAgentDependencies(
    aps_client_id=settings.aps_client_id,
    aps_client_secret=settings.aps_client_secret,
    aps_activity_name=settings.aps_da_activity,
    aps_bundle_alias=settings.aps_da_bundle_alias,
    template_catalog_url=settings.aps_template_url,
    image_to_3d_api_key=settings.image_to_3d_api_key,
    image_to_3d_endpoint=settings.image_to_3d_endpoint,
    output_bucket=settings.output_bucket_or_path,
)

# Create agent
agent = create_agent()

# Run
result = agent.run_sync(
    "Create a conference table, 2400mm x 1200mm x 750mm",
    deps=deps
)

print(result.output)
```

### Example Prompts

**Text-only (parametric):**
- "Create an office chair, 600mm wide, 650mm deep, 900mm high"
- "Make a conference table, 2.4m x 1.2m x 75cm"
- "Generate a cabinet, width: 36 inches, depth: 24 inches, height: 84 inches"

**Image-only (mesh-based):**
- "Here's an image of a chair I want to model" (attach image)
- Uses image-to-3D service to generate mesh
- Imports mesh into Revit family

**Hybrid (image + text):**
- "Use this image for the shape, but make it 800mm wide" (attach image)
- Combines AI-generated mesh with parametric dimensions

**With materials:**
- "Create a wooden chair, 600mm wide, walnut finish"
- "Make a steel desk, 1500mm x 800mm, brushed aluminum"

---

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'pydantic_ai'"

**Solution:** Install dependencies:

```bash
pip install -r requirements.txt
```

### Issue: "Field required" errors in tests

**Solution:** Create `.env` file with required variables.

### Issue: "Authentication failed" with APS

**Solution:** Check your Client ID and Secret in `.env`. Run the setup wizard:

```bash
python deployment/scripts/setup_aps.py --test-auth
```

### Issue: Agent returns stubbed results

**Solution:** This is expected! The APS integration is stubbed by default. To get real Revit families:

1. Build and deploy the C# AppBundle (Step 4)
2. Replace stubbed functions in `revit_family_maker/tools.py`:
   - `execute_aps_workitem()` - implement real APS WorkItem creation
   - `generate_3d_from_image()` - integrate real image-to-3D service

---

## Architecture Overview

```
User Prompt → Pydantic AI Agent → Tools → APS Design Automation → Revit Family (.rfa)
                      ↓
            OpenAI GPT-4o-mini
              (parses dimensions,
               selects category,
               manages workflow)
```

**Key Components:**

1. **Pydantic AI Agent** (`revit_family_maker/agent.py`)
   - Orchestrates the workflow
   - Calls tools based on user intent
   - Validates all inputs with Pydantic models

2. **Tools** (`revit_family_maker/tools.py`)
   - `generate_family_from_prompt()` - Text-based family generation
   - `generate_family_from_image()` - Image-based family generation
   - `perform_family_creation()` - Hybrid mode
   - `list_family_templates()` - Browse available templates
   - `get_family()` - Retrieve existing families

3. **C# AppBundle** (`RevitAppBundle/`)
   - Runs inside Revit on APS cloud
   - Creates parametric families
   - Runs flex tests (min/nominal/max)
   - Outputs `.rfa` + `.json` manifest

4. **Template Catalog** (`revit_family_maker/templates.py`)
   - Manages Revit templates
   - Maps categories to templates
   - Tracks template versions and hashes

---

## What's Next?

- **Add more templates** - Expand the template catalog with your own .rft files
- **Integrate image-to-3D** - Replace the stub with a real service (Meshroom, Polycam API)
- **Build a UI** - Create a web interface for non-technical users
- **Scale horizontally** - Run multiple agent instances for concurrent requests
- **Add type catalogs** - Auto-generate `.txt` type catalogs for families
- **Implement caching** - Cache template metadata and common prompts

---

## Resources

- **Full Documentation:** `README.md`
- **Deployment Guide:** `deployment/DEPLOYMENT_GUIDE.md`
- **Testing Guide:** `TESTING_GUIDE.md`
- **Template Setup:** `templates/README.md`
- **APS Docs:** https://aps.autodesk.com/en/docs/design-automation/v3/
- **Pydantic AI Docs:** https://ai.pydantic.dev/

---

## Support

Having issues? Check:

1. `TESTING_GUIDE.md` - Comprehensive testing instructions
2. `deployment/DEPLOYMENT_GUIDE.md` - Production setup troubleshooting
3. GitHub Issues - Report bugs and request features

---

**You're ready to generate Revit families with AI!** 🎉

Start with: `python main.py "Create a desk, 1500mm x 800mm x 750mm"`
