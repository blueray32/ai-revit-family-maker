# AI Revit Family Maker - Production Deployment Guide

This guide walks you through deploying the AI Revit Family Maker to production using Autodesk Platform Services (APS) Design Automation.

---

## Prerequisites

### Required Accounts and Credentials

1. **Autodesk Platform Services (APS) Account**
   - Sign up at: https://aps.autodesk.com/
   - Create an app in the APS portal
   - Note your **Client ID** and **Client Secret**
   - Enable **Design Automation API** for your app

2. **OpenAI API Key**
   - Sign up at: https://platform.openai.com/
   - Generate an API key
   - Ensure you have credits/billing set up

3. **Cloud Storage** (for templates and outputs)
   - Option A: **APS OSS** (Object Storage Service)
   - Option B: **AWS S3** with IAM credentials
   - Option C: **Azure Blob Storage** with SAS tokens

### Required Software

- **Windows 10/11** (for building C# AppBundle)
- **Visual Studio 2019+** with .NET Framework 4.8
- **PowerShell 5.1+** (for build script)
- **Python 3.11+** (for deployment script and agent)
- **Revit 2024 or 2025** (for local testing only, not required for production)

---

## Step 1: Configure Environment Variables

Create or update `.env` in the project root:

```bash
# LLM Configuration
LLM_PROVIDER=openai
LLM_API_KEY=sk-proj-YOUR_OPENAI_KEY_HERE
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1

# APS / Forge Design Automation
APS_CLIENT_ID=YOUR_APS_CLIENT_ID
APS_CLIENT_SECRET=YOUR_APS_CLIENT_SECRET
APS_DA_ACTIVITY=YOUR_NICKNAME.RevitFamilyMakerActivity+production
APS_DA_BUNDLE_ALIAS=production
APS_TEMPLATE_URL=https://your-storage.com/templates/

# Image-to-3D Service (optional, can stay stubbed)
IMAGE_TO_3D_API_KEY=stub
IMAGE_TO_3D_ENDPOINT=https://stub.example.com

# Output Configuration
OUTPUT_BUCKET_OR_PATH=your-oss-bucket-or-path
```

**Important:**
- Replace `YOUR_NICKNAME` with your APS nickname (usually your Client ID prefix)
- Replace template and output URLs with your actual cloud storage

---

## Step 2: Build the C# AppBundle

The AppBundle is a .NET DLL that runs inside Revit in the cloud.

### 2.1 Verify Project Structure

Ensure you have:
```
RevitAppBundle/
├── RevitFamilyMaker.csproj
├── PackageContents.xml
├── FamilyMakerCommand.cs
├── FamilyCreator.cs
├── FlexTester.cs
├── Models/
│   └── FamilyParameters.cs
└── Utils/
    └── UnitConverter.cs
```

### 2.2 Install NuGet Dependencies

Open PowerShell in the `RevitAppBundle` directory:

```powershell
nuget restore
```

This installs:
- `Revit.RevitApi.x64` (2024 and 2025)
- `Autodesk.Forge.DesignAutomation.Revit` (24.0.0 / 25.0.0)
- `Newtonsoft.Json` (13.0.3)

### 2.3 Build for Both Versions

Run the build script:

```powershell
cd deployment/scripts
.\build.ps1 -Configuration Release -Clean
```

This creates:
```
deployment/output/
├── Revit2024/
│   ├── RevitFamilyMaker.dll
│   ├── PackageContents.xml
│   └── [dependencies]
├── Revit2025/
│   ├── RevitFamilyMaker.dll
│   ├── PackageContents.xml
│   └── [dependencies]
├── RevitFamilyMaker_2024.zip
└── RevitFamilyMaker_2025.zip
```

**Troubleshooting:**
- If MSBuild not found, install Visual Studio Build Tools
- If Revit API missing, install via NuGet Package Manager
- Ensure .NET Framework 4.8 SDK is installed

---

## Step 3: Deploy AppBundle to APS

### 3.1 Authenticate with APS

Test your credentials:

```python
from revit_family_maker.settings import load_settings
settings = load_settings()
print(f"Client ID: {settings.aps_client_id}")
```

### 3.2 Upload AppBundle

Deploy for Revit 2024:

```bash
python deployment/scripts/deploy_appbundle.py \
    --version 2024 \
    --alias production \
    --description "RevitFamilyMaker production build"
```

Deploy for Revit 2025 (optional):

```bash
python deployment/scripts/deploy_appbundle.py \
    --version 2025 \
    --alias production \
    --description "RevitFamilyMaker production build"
```

**Expected Output:**
```
========================================================
APS AppBundle Deployment
========================================================
Bundle Name: RevitFamilyMaker2024
Engine: Autodesk.Revit+2024
Zip Path: deployment/output/RevitFamilyMaker_2024.zip
Alias: production
========================================================

Authenticating with APS...
  Authentication successful!
Creating new AppBundle YOUR_NICKNAME.RevitFamilyMaker2024+Autodesk.Revit+2024...
  Created AppBundle: YOUR_NICKNAME.RevitFamilyMaker2024+1
  Uploading: RevitFamilyMaker_2024.zip (2.34 MB)
  Upload complete!
  Creating alias 'production' pointing to version 1...
  Alias created: production

========================================================
Deployment Successful!
========================================================
AppBundle ID: YOUR_NICKNAME.RevitFamilyMaker2024+1
Version: 1
Alias: production
```

---

## Step 4: Create APS Activity

An **Activity** defines how the AppBundle runs and what inputs/outputs it expects.

### 4.1 Prepare Activity Definition

Edit `deployment/aps_activity.json` and replace `{{NICKNAME}}` with your APS nickname:

```json
{
  "id": "RevitFamilyMakerActivity",
  "engine": "Autodesk.Revit+2024",
  "appbundles": [
    "YOUR_NICKNAME.RevitFamilyMaker2024+production"
  ],
  ...
}
```

### 4.2 Create Activity via API

Use the APS Design Automation API or Postman:

**Endpoint:**
```
POST https://developer.api.autodesk.com/da/us-east/v3/activities
```

**Headers:**
```
Authorization: Bearer {YOUR_2_LEGGED_TOKEN}
Content-Type: application/json
```

**Body:** Contents of `deployment/aps_activity.json`

**Response:**
```json
{
  "id": "YOUR_NICKNAME.RevitFamilyMakerActivity+1",
  "engine": "Autodesk.Revit+2024",
  "appbundles": ["YOUR_NICKNAME.RevitFamilyMaker2024+production"],
  ...
}
```

### 4.3 Create Activity Alias

Create a `production` alias:

```
POST https://developer.api.autodesk.com/da/us-east/v3/activities/YOUR_NICKNAME.RevitFamilyMakerActivity/aliases
```

**Body:**
```json
{
  "id": "production",
  "version": 1
}
```

### 4.4 Update Environment Variables

Update `.env`:

```bash
APS_DA_ACTIVITY=YOUR_NICKNAME.RevitFamilyMakerActivity+production
```

---

## Step 5: Set Up Template Catalog

### 5.1 Obtain Revit Templates

See `templates/README.md` for detailed instructions.

**Quick Start:**
1. Copy templates from Revit installation:
   ```
   C:\ProgramData\Autodesk\RVT 2024\Family Templates\English\
   ```
2. Choose categories: `Generic Model.rft`, `Furniture.rft`, etc.
3. Test templates in Revit (open, add parameters, save)

### 5.2 Upload Templates to Cloud Storage

**Option A: APS OSS**
```bash
# Create bucket
curl -X POST https://developer.api.autodesk.com/oss/v2/buckets \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"bucketKey":"your-templates-bucket","policyKey":"transient"}'

# Upload template
curl -X PUT https://developer.api.autodesk.com/oss/v2/buckets/your-templates-bucket/objects/furniture.rft \
  -H "Authorization: Bearer $TOKEN" \
  --data-binary @templates/2024/Furniture.rft
```

**Option B: AWS S3**
```bash
aws s3 cp templates/2024/Furniture.rft s3://your-bucket/templates/2024/
```

### 5.3 Generate Template Hashes

```bash
# Linux/Mac
sha256sum templates/2024/Furniture.rft

# Windows
Get-FileHash templates/2024/Furniture.rft -Algorithm SHA256
```

### 5.4 Update Template Catalog

Edit `revit_family_maker/tools.py` - update the `TEMPLATE_CATALOG` dict:

```python
TEMPLATE_CATALOG = {
    "furniture_chair_v1": {
        "id": "furniture_chair_v1",
        "category": "Furniture",
        "url": "https://your-storage.com/templates/2024/Furniture.rft",
        "hash": "sha256:YOUR_TEMPLATE_HASH",
        "revit_version": "2024",
    },
    # Add more...
}
```

---

## Step 6: Test the Complete Pipeline

### 6.1 Unit Tests (No API Calls)

```bash
pytest tests/ -v
```

Expected: 30+ tests passing

### 6.2 Integration Test (Stubbed Services)

```bash
python test_real_tools.py
```

This tests:
- Tool invocation
- Parameter parsing
- Unit conversion
- Manifest generation

### 6.3 Real APS Test (End-to-End)

Replace stubbed APS functions in `tools.py`:

```python
async def execute_aps_workitem(...):
    # Real implementation using requests + APS WorkItem API
    pass
```

Then run:

```bash
python main.py "Create a modern office chair, 600mm wide, 650mm deep, 900mm tall"
```

**Expected Flow:**
1. Agent parses prompt
2. Calls `generate_family_from_prompt` tool
3. Tool creates APS WorkItem with template + parameters
4. APS runs Revit, executes AppBundle
5. AppBundle creates family, runs flex test
6. Downloads `.rfa` and `.json` manifest
7. Agent returns family details to user

---

## Step 7: Production Deployment Checklist

- [ ] Environment variables configured (`.env`)
- [ ] AppBundle built and uploaded to APS
- [ ] APS Activity created with correct AppBundle reference
- [ ] Activity alias points to latest version
- [ ] Template catalog populated with tested templates
- [ ] Templates uploaded to cloud storage
- [ ] Template URLs accessible to APS
- [ ] Stubbed functions replaced with real implementations:
  - [ ] `execute_aps_workitem()` in `tools.py`
  - [ ] `generate_3d_from_image()` in `tools.py` (if using image-to-3D)
- [ ] All tests passing (unit + integration)
- [ ] End-to-end test with real APS successful
- [ ] Error handling tested (missing templates, invalid params, APS failures)
- [ ] Rate limiting configured (if needed)
- [ ] Logging and telemetry configured
- [ ] Cost monitoring set up (APS credits, OpenAI tokens)

---

## Step 8: Monitoring and Maintenance

### Cost Tracking

- **APS Design Automation**: ~$0.50 per compute hour
- **OpenAI API**: varies by model (gpt-4o-mini is cheaper)
- **Cloud Storage**: S3/OSS storage + bandwidth

### Logging

The agent logs to console. For production, add structured logging:

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
```

### Error Monitoring

Monitor for:
- APS WorkItem failures (check status codes)
- Template not found errors
- Parameter validation failures
- Flex test failures
- Timeout errors (APS jobs have 10-minute limit)

### Updating AppBundle

To deploy a new version:

1. Make code changes
2. Rebuild: `.\build.ps1 -Clean`
3. Deploy: `python deploy_appbundle.py --version 2024 --alias dev`
4. Test with `dev` alias
5. Promote to `production`: update alias to new version

---

## Troubleshooting

### AppBundle Build Fails

**Problem:** MSBuild not found
**Solution:** Install Visual Studio Build Tools or full Visual Studio

**Problem:** Revit API references missing
**Solution:** Install via NuGet: `Install-Package Revit.RevitApi.x64 -Version 2024.0.0`

### AppBundle Upload Fails

**Problem:** 401 Unauthorized
**Solution:** Check APS Client ID/Secret, regenerate token

**Problem:** 404 Not Found
**Solution:** Verify base URL is `https://developer.api.autodesk.com/da/us-east/v3`

### Activity Fails

**Problem:** "AppBundle not found"
**Solution:** Ensure AppBundle alias exists and is referenced correctly

**Problem:** "Template file not found"
**Solution:** Verify template URL is accessible to APS (signed URL or public)

### Family Creation Fails

**Problem:** "Parameter not found: DIM_Width"
**Solution:** Template doesn't have required parameters - add them or use a different template

**Problem:** "Flex test failed"
**Solution:** Parameter values may be out of bounds - check template constraints

---

## Security Best Practices

1. **Never commit secrets** - use `.env` and `.gitignore`
2. **Rotate credentials regularly** - APS Client Secret, OpenAI keys
3. **Use short-lived tokens** - APS 2-legged tokens expire in 1 hour
4. **Validate inputs** - all user inputs are validated by Pydantic models
5. **Strip PII from images** - EXIF data removed before API calls
6. **Rate limit API calls** - prevent abuse and cost overruns
7. **Use least privilege** - APS app only needs Design Automation scope

---

## Next Steps

1. **Scale horizontally** - run multiple agent instances for concurrent requests
2. **Add caching** - cache template metadata, common prompts
3. **Implement webhooks** - async WorkItem status updates
4. **Build UI** - web interface for non-technical users
5. **Expand templates** - add more categories and subcategories
6. **Integrate image-to-3D** - replace stub with real service (e.g., Meshroom, Polycam API)
7. **Add type catalogs** - auto-generate `.txt` type catalogs for families

---

## Support and Resources

- **APS Design Automation Docs**: https://aps.autodesk.com/en/docs/design-automation/v3/
- **Revit API Docs**: https://www.revitapidocs.com/
- **Pydantic AI Docs**: https://ai.pydantic.dev/
- **Project GitHub**: [Your repo URL]
- **Issues**: Report bugs in GitHub Issues

---

## Deployment Summary

You now have:

✅ C# AppBundle compiled for Revit 2024/2025
✅ AppBundle deployed to APS Design Automation
✅ APS Activity configured to run the AppBundle
✅ Python agent with 5 tools and OpenAI integration
✅ Template catalog structure and guide
✅ Comprehensive test suite
✅ Production-ready deployment scripts

**You're ready to generate Revit families with AI!** 🎉
