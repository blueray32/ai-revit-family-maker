# 🚀 DEPLOY NOW - Step-by-Step Guide

**Complete deployment in the next 1-2 hours**

---

## ✅ What's Ready

- ✅ Python agent fully functional
- ✅ Real APS API client implemented
- ✅ C# AppBundle code complete
- ✅ Build scripts ready (Windows)
- ✅ Deployment scripts ready
- ✅ Template catalog system ready
- ✅ All tests passing

**Current Location:** `AI Revit Family Maker Assistant/`

---

## 🎯 Deployment Checklist

I've created a todo list to track your progress. Run `cat DEPLOY_NOW.md` anytime to see your status.

### Phase 1: Get APS Credentials (10 minutes)

**Status:** 🔄 IN PROGRESS

**Steps:**

1. **Go to APS Portal:**
   - Open: https://aps.autodesk.com/myapps
   - Sign in with your Autodesk account (or create one)

2. **Create or Select an App:**
   - Click "Create App" or select existing app
   - App Name: "Revit Family Maker" (or any name)
   - Description: "AI-powered Revit family generation"

3. **Enable Design Automation API:**
   - In your app settings
   - Check "Design Automation API v3"
   - Save

4. **Copy Credentials:**
   - Client ID: (looks like `abc123xyz...`)
   - Client Secret: (click "Show" to reveal)
   - **Keep these secret!**

5. **Update .env file:**
   ```bash
   # Open .env and replace these lines:
   APS_CLIENT_ID=your_actual_client_id_here
   APS_CLIENT_SECRET=your_actual_client_secret_here
   ```

6. **Test authentication:**
   ```bash
   python deployment/scripts/setup_aps.py --test-auth
   ```

**Expected output:**
```
🔐 Authenticating with APS...
✅ Authentication successful! Token expires in 3600 seconds.
```

---

### Phase 2: Build C# AppBundle (15-30 minutes)

**Status:** ⏳ PENDING (requires Windows)

**Requirements:**
- Windows 10/11
- Visual Studio 2019 or later (Community Edition is free)
- .NET Framework 4.8

**If you're on Mac/Linux:**
- Use a Windows VM (Parallels, VMware, VirtualBox)
- Use a Windows PC/laptop
- Use cloud Windows (Azure, AWS)
- Ask a teammate with Windows

**Steps on Windows:**

1. **Transfer the project to Windows:**
   ```bash
   # Zip the project
   zip -r RevitFamilyMaker.zip "AI Revit Family Maker Assistant/"

   # Transfer via USB, network, email, etc.
   ```

2. **Extract on Windows:**
   ```batch
   # Unzip to C:\Projects\
   # You should have: C:\Projects\AI Revit Family Maker Assistant\
   ```

3. **Open PowerShell or Command Prompt:**
   ```batch
   cd "C:\Projects\AI Revit Family Maker Assistant\deployment\scripts"
   ```

4. **Run build script:**

   **Option A: Batch file (recommended):**
   ```batch
   build.bat Release
   ```

   **Option B: PowerShell:**
   ```powershell
   .\build.ps1 -Configuration Release -Clean
   ```

5. **Wait for build to complete (5-10 minutes):**
   - It will build for Revit 2024
   - Then build for Revit 2025
   - Then create zip files

6. **Verify output:**
   ```batch
   dir ..\output\*.zip
   ```

   **Expected:**
   ```
   RevitFamilyMaker_2024.zip  (2-3 MB)
   RevitFamilyMaker_2025.zip  (2-3 MB)
   ```

7. **Transfer zip files back to Mac:**
   - Copy `deployment/output/RevitFamilyMaker_2024.zip` back to your Mac
   - Copy `deployment/output/RevitFamilyMaker_2025.zip` back to your Mac

**Troubleshooting:**

**Error: "MSBuild not found"**
```batch
# Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/downloads/
# Select: "Desktop development with C++" workload
```

**Error: "NuGet restore failed"**
```batch
# Restore NuGet packages manually
cd "C:\Projects\AI Revit Family Maker Assistant\RevitAppBundle"
nuget restore
```

**Error: "Revit API not found"**
```batch
# Install via NuGet Package Manager Console in Visual Studio
Install-Package Revit.RevitApi.x64 -Version 2024.0.0
Install-Package Autodesk.Forge.DesignAutomation.Revit -Version 24.0.0
```

---

### Phase 3: Deploy AppBundle to APS (5-10 minutes)

**Status:** ⏳ PENDING (after Phase 2 complete)

**Steps:**

1. **Ensure zip files are in deployment/output/:**
   ```bash
   ls -lh deployment/output/RevitFamilyMaker_*.zip
   ```

2. **Deploy for Revit 2024:**
   ```bash
   python deployment/scripts/deploy_appbundle.py \
       --version 2024 \
       --alias production \
       --description "Production AppBundle for AI Revit Family Maker"
   ```

3. **Wait for upload (2-3 minutes):**
   ```
   ============================================================
   APS AppBundle Deployment
   ============================================================
   Authenticating with APS...
     Authentication successful!
   Creating new AppBundle YOUR_NICKNAME.RevitFamilyMaker2024...
     Created AppBundle: YOUR_NICKNAME.RevitFamilyMaker2024+1
     Uploading: RevitFamilyMaker_2024.zip (2.34 MB)
     Upload complete!
     Creating alias 'production' pointing to version 1...
     Alias created: production

   ============================================================
   Deployment Successful!
   ============================================================
   ```

4. **Optional: Deploy for Revit 2025:**
   ```bash
   python deployment/scripts/deploy_appbundle.py \
       --version 2025 \
       --alias production
   ```

5. **Verify deployment:**
   ```bash
   python deployment/scripts/setup_aps.py --list-appbundles
   ```

**Expected output:**
```
📦 Listing AppBundles...
  Found 1 AppBundle(s):

    • YOUR_NICKNAME.RevitFamilyMaker2024+production
```

---

### Phase 4: Create APS Activity (10 minutes)

**Status:** ⏳ PENDING (after Phase 3 complete)

**What is an Activity?**
An Activity tells APS how to run your AppBundle - what inputs it needs, what outputs it produces.

**Steps:**

1. **Get your APS nickname:**
   ```bash
   python deployment/scripts/setup_aps.py --test-auth
   # Look for "Your APS nickname: ..."
   # Usually the first part of your Client ID
   ```

2. **Edit activity definition:**
   ```bash
   nano deployment/aps_activity.json
   # Or use any text editor
   ```

3. **Replace `{{NICKNAME}}`:**
   ```json
   {
     "id": "RevitFamilyMakerActivity",
     "appbundles": [
       "YOUR_ACTUAL_NICKNAME.RevitFamilyMaker2024+production"
     ],
     ...
   }
   ```

   Replace `{{NICKNAME}}` with your actual nickname everywhere in the file.

4. **Get APS token:**
   ```bash
   # In a new terminal, run:
   python -c "
   from revit_family_maker.settings import load_settings
   from revit_family_maker.aps_client import APSClient
   import asyncio

   settings = load_settings()
   client = APSClient(settings.aps_client_id, settings.aps_client_secret)
   token = asyncio.run(client.authenticate())
   print(token.access_token)
   "
   ```

   Copy the token (it's very long, starts with `eyJ...`)

5. **Create Activity using curl:**
   ```bash
   curl -X POST https://developer.api.autodesk.com/da/us-east/v3/activities \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d @deployment/aps_activity.json
   ```

6. **Create Activity alias:**
   ```bash
   curl -X POST https://developer.api.autodesk.com/da/us-east/v3/activities/YOUR_NICKNAME.RevitFamilyMakerActivity/aliases \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"id": "production", "version": 1}'
   ```

7. **Update .env:**
   ```bash
   # Edit .env and update:
   APS_DA_ACTIVITY=YOUR_NICKNAME.RevitFamilyMakerActivity+production
   ```

8. **Verify:**
   ```bash
   python deployment/scripts/setup_aps.py --list-activities
   ```

**Expected output:**
```
⚙️  Listing Activities...
  Found 1 Activity(ies):

    • YOUR_NICKNAME.RevitFamilyMakerActivity+production
```

---

### Phase 5: Set Up Templates (30-60 minutes)

**Status:** ⏳ PENDING

**Quick Start: 3 Templates**

**Option A: Copy from Revit Installation**

1. **Locate Revit templates:**
   - Windows: `C:\ProgramData\Autodesk\RVT 2024\Family Templates\English\`
   - Mac: (if you have Revit installed via Boot Camp)

2. **Copy these 3 templates:**
   - `Generic Model.rft` (required - fallback)
   - `Furniture.rft` (common use case)
   - `Casework.rft` (another common case)

3. **Put them in your project:**
   ```bash
   mkdir -p templates/2024
   # Copy the .rft files to templates/2024/
   ```

**Option B: Download Community Templates**

- Revit City: https://www.revitcity.com/downloads.php?type=families
- BIMObject: https://www.bimobject.com/
- National BIM Library: https://www.nationalbimlibrary.com/

**Upload to Cloud Storage**

**If using AWS S3:**
```bash
# Install AWS CLI if needed
pip install awscli

# Configure (one-time)
aws configure

# Upload templates
aws s3 mb s3://your-revit-templates
aws s3 cp templates/2024/ s3://your-revit-templates/2024/ --recursive

# Get URL
aws s3 presign s3://your-revit-templates/2024/Furniture.rft
# Or make bucket public and use: https://your-revit-templates.s3.amazonaws.com/2024/
```

**If using Azure Blob:**
```bash
# Install Azure CLI
brew install azure-cli  # Mac

# Login (one-time)
az login

# Create storage
az storage account create --name revittemplates --resource-group mygroup
az storage container create --name templates --account-name revittemplates --public-access blob

# Upload
az storage blob upload-batch -d templates -s templates/2024/ --account-name revittemplates

# Get URL
echo "https://revittemplates.blob.core.windows.net/templates/2024/"
```

**If using APS OSS (Object Storage Service):**
```bash
# This requires APS API calls - easiest via Python
python -c "
from revit_family_maker.aps_client import get_aps_client
from revit_family_maker.settings import load_settings
import asyncio

async def upload():
    settings = load_settings()
    client = get_aps_client(settings.aps_client_id, settings.aps_client_secret)

    # Create bucket
    # ... (implementation in APS docs)

    # Upload files
    # ... (implementation in APS docs)

asyncio.run(upload())
"
```

**Update .env:**
```bash
# Edit .env:
APS_TEMPLATE_URL=https://your-storage-url/templates/
# Examples:
# APS_TEMPLATE_URL=https://your-bucket.s3.amazonaws.com/templates/
# APS_TEMPLATE_URL=https://yourstorage.blob.core.windows.net/templates/
```

---

### Phase 6: Test End-to-End (5 minutes)

**Status:** ⏳ PENDING (after all phases complete)

**Steps:**

1. **Create output directory:**
   ```bash
   mkdir -p output/families
   ```

2. **Update .env output path:**
   ```bash
   # Edit .env:
   OUTPUT_BUCKET_OR_PATH=output/families
   ```

3. **Run the agent:**
   ```bash
   python main.py "Create a modern office chair, 600mm wide, 650mm deep, 900mm tall"
   ```

4. **Agent will ask for category:**
   ```
   What category should this be?
   ```

   Type: `Furniture`

5. **Wait for generation (1-3 minutes):**
   ```
   ✅ APS authenticated
   🔧 Executing APS workitem:
     Template: https://your-storage.com/templates/2024/Furniture.rft
     Activity: YOUR_NICKNAME.RevitFamilyMakerActivity+production
   ✅ WorkItem created: abc-123-def
   📊 WorkItem status: pending
   📊 WorkItem status: inprogress
   📊 WorkItem status: success
   ✅ WorkItem completed successfully
   📥 Downloading outputFamily...
   ✅ Downloaded outputFamily (524288 bytes)
   📥 Downloading outputManifest...
   ✅ Downloaded outputManifest (2048 bytes)
   💾 Saved: output/families/Generic_Furniture_2024_v0.1.0.rfa (524288 bytes)
   💾 Saved: output/families/Generic_Furniture_2024_v0.1.0.json
   ```

6. **Verify files:**
   ```bash
   ls -lh output/families/
   cat output/families/Generic_Furniture_2024_v0.1.0.json
   ```

7. **Open in Revit (if you have it):**
   - Open Revit 2024/2025
   - File → Open → Select the `.rfa` file
   - Check parameters: DIM_Width, DIM_Depth, DIM_Height
   - Try changing parameter values
   - Family should update without errors

**Success Indicators:**

- ✅ `.rfa` file exists and is > 100 KB
- ✅ `.json` manifest exists
- ✅ Manifest shows `"flex_test_passed": true`
- ✅ Parameters are present with correct values
- ✅ File opens in Revit without errors

---

## 🐛 Common Issues

### Phase 1 Issues

**"Authentication failed"**
- Check Client ID and Secret are correct (no extra spaces)
- Make sure Design Automation API is enabled in your app
- Try regenerating Client Secret in APS portal

### Phase 2 Issues

**"Cannot find MSBuild"**
- Install Visual Studio (Community Edition is free)
- Or install Build Tools only
- Restart after installation

**"NuGet packages not found"**
- Open Visual Studio
- Tools → NuGet Package Manager → Manage NuGet Packages for Solution
- Click "Restore" button

### Phase 3 Issues

**"AppBundle upload failed"**
- Check file exists: `ls deployment/output/RevitFamilyMaker_2024.zip`
- Check file size is reasonable (2-5 MB)
- Try uploading again (sometimes network issues)

### Phase 4 Issues

**"Activity creation failed"**
- Make sure AppBundle is deployed first (Phase 3)
- Check nickname is correct in JSON
- Verify token hasn't expired (get a new one)

### Phase 5 Issues

**"Template not accessible from APS"**
- Templates must be publicly accessible OR use signed URLs
- Test template URL in browser: `curl -I https://your-url/template.rft`
- Should return 200 OK, not 403 Forbidden

### Phase 6 Issues

**"WorkItem failed"**
- Check APS report URL in error message
- Common causes:
  - Template URL not accessible
  - Invalid parameters.json
  - AppBundle error (check C# code)

**"Template file not found"**
- Verify APS_TEMPLATE_URL in .env is correct
- Check template exists at that URL
- Try with absolute URL first

---

## 📊 Time Estimates

| Phase | Time | Can Skip? |
|-------|------|-----------|
| 1. APS Credentials | 10 min | No |
| 2. Build C# | 15-30 min | No |
| 3. Deploy AppBundle | 5-10 min | No |
| 4. Create Activity | 10 min | No |
| 5. Upload Templates | 30-60 min | Start with 3 |
| 6. Test | 5 min | No |
| **Total** | **1-2 hours** | - |

---

## 💰 Costs

- APS Account: Free tier available
- APS Design Automation: ~$0.01-0.03 per family
- OpenAI API: ~$0.002-0.004 per family
- Cloud Storage: ~$0.001/GB/month (negligible)

**Total per family:** ~$0.01-0.04

---

## ✅ Checklist

Copy this to track your progress:

```
Phase 1: APS Credentials
[ ] Created APS account
[ ] Created app
[ ] Enabled Design Automation API
[ ] Copied Client ID and Secret
[ ] Updated .env
[ ] Tested authentication

Phase 2: Build C# AppBundle
[ ] Have Windows PC/VM
[ ] Have Visual Studio installed
[ ] Transferred project to Windows
[ ] Ran build script
[ ] Got RevitFamilyMaker_2024.zip
[ ] Got RevitFamilyMaker_2025.zip
[ ] Transferred zip files back

Phase 3: Deploy AppBundle
[ ] Deployed for Revit 2024
[ ] Verified deployment
[ ] (Optional) Deployed for Revit 2025

Phase 4: Create Activity
[ ] Got APS nickname
[ ] Edited aps_activity.json
[ ] Created Activity via API
[ ] Created Activity alias
[ ] Updated .env with activity ID
[ ] Verified activity exists

Phase 5: Upload Templates
[ ] Got 3-5 Revit templates
[ ] Set up cloud storage
[ ] Uploaded templates
[ ] Made templates accessible
[ ] Updated .env with URL
[ ] Tested template URL accessibility

Phase 6: Test End-to-End
[ ] Created output directory
[ ] Ran python main.py with prompt
[ ] Got .rfa file
[ ] Got .json manifest
[ ] Verified flex test passed
[ ] (Optional) Opened in Revit
```

---

## 🎉 You're Doing It!

Follow the phases in order. Each phase builds on the previous one.

**Current Status:** Check your todo list!

**Need help?** Read the detailed guides:
- `LETS_MAKE_IT_PRODUCTION.md` - Detailed instructions
- `deployment/DEPLOYMENT_GUIDE.md` - Troubleshooting reference

**Let's make it happen!** 🚀
