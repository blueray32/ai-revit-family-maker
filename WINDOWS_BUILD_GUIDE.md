# Windows Build Guide - Build the Real AppBundle

## Prerequisites

You'll need a Windows machine (physical, VM, or remote) with:

### Required Software:
1. **Visual Studio 2022** (Community Edition is free)
   - Download: https://visualstudio.microsoft.com/downloads/
   - During install, select: ".NET desktop development" workload

2. **Git for Windows** (to clone your repo)
   - Download: https://git-scm.com/download/win

3. **Python 3.9+** (for deployment script)
   - Download: https://www.python.org/downloads/

---

## Step-by-Step Build Instructions

### 1. Clone Your Repository

Open **PowerShell** or **Command Prompt**:

```powershell
# Navigate to where you want the project
cd C:\Users\YourUsername\Documents

# Clone your repo
git clone https://github.com/blueray32/ai-revit-family-maker.git
cd ai-revit-family-maker
```

---

### 2. Install Python Dependencies (Optional - for deployment)

```powershell
# Install Python packages
pip install requests python-dotenv pydantic-settings
```

---

### 3. Build the AppBundle

**Option A: Using MSBuild directly**

```powershell
cd RevitAppBundle

# Restore NuGet packages
dotnet restore RevitFamilyMaker.csproj

# Build for Revit 2025
msbuild RevitFamilyMaker.csproj /p:Configuration=Release2025 /p:Platform=x64 /v:minimal

# Build for Revit 2024 (optional)
msbuild RevitFamilyMaker.csproj /p:Configuration=Release2024 /p:Platform=x64 /v:minimal
```

**Option B: Using the automated script**

```powershell
cd RevitAppBundle

# Run the build script
powershell -ExecutionPolicy Bypass -File ..\deployment\scripts\build.ps1
```

---

### 4. Package the AppBundle

The build script should create:
- `deployment/output/RevitFamilyMaker_2025.zip`
- `deployment/output/RevitFamilyMaker_2024.zip`

If you built manually, package it:

```powershell
cd bin\Release2025

# Create Contents directory
New-Item -ItemType Directory -Force -Path "Contents"

# Copy DLLs
Copy-Item "*.dll" "Contents\" -Force

# Create Contents.xml
@"
<?xml version="1.0" encoding="utf-8"?>
<ApplicationPackage
  SchemaVersion="1.0"
  ProductType="Application"
  Name="RevitFamilyMaker"
  AppVersion="1.0.0"
  Description="AI-powered Revit family generator">
  <CompanyDetails Name="Revit Family Maker" />
  <Components Description="Revit Family Maker Components">
    <RuntimeRequirements OS="Win64" Platform="Revit" SeriesMin="R2025" SeriesMax="R2025" />
    <ComponentEntry AppName="RevitFamilyMaker" ModuleName="./Contents/RevitFamilyMaker.dll" />
  </Components>
</ApplicationPackage>
"@ | Out-File -FilePath "Contents.xml" -Encoding UTF8

# Create ZIP
Compress-Archive -Path "Contents.xml", "Contents" -DestinationPath "..\..\..\..\deployment\output\RevitFamilyMaker_2025.zip" -Force

Write-Host "✅ Created RevitFamilyMaker_2025.zip"
```

---

### 5. Transfer the ZIP to Your Mac

**Option A: Copy via network/USB**
```powershell
# The file is at:
# C:\Users\YourUsername\Documents\ai-revit-family-maker\deployment\output\RevitFamilyMaker_2025.zip
```

**Option B: Upload to GitHub** (if file is <25MB)
```powershell
# In the root directory
git add deployment/output/RevitFamilyMaker_2025.zip
git commit -m "build: add compiled AppBundle for Revit 2025"
git push
```

Then on Mac:
```bash
git pull
```

**Option C: Use cloud storage**
Upload to Dropbox/Google Drive/OneDrive and download on Mac

---

### 6. Deploy from Mac

Once you have `RevitFamilyMaker_2025.zip` on your Mac:

```bash
cd "/Users/ciarancox/AI Revit Family Maker Assistant"

# Ensure the file is in the right place
mv ~/Downloads/RevitFamilyMaker_2025.zip ./deployment/output/

# Deploy to APS
python deployment/scripts/deploy_appbundle.py --version 2025

# Test end-to-end
python -m revit_family_maker.cli
```

---

## Troubleshooting

### "MSBuild not found"

Make sure you opened **Developer Command Prompt for VS 2022** or **Developer PowerShell for VS 2022**.

Or add MSBuild to PATH:
```powershell
$env:Path += ";C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin"
```

### "Revit SDK not found"

The Revit SDK is downloaded automatically via NuGet. Ensure you ran:
```powershell
dotnet restore RevitFamilyMaker.csproj
```

### "DesignAutomationBridge not found"

This is expected - we removed it from the project file. The build should work without it.

### Build succeeds but no DLLs

Check the output path:
```powershell
dir RevitAppBundle\bin\Release2025
```

You should see:
- RevitFamilyMaker.dll
- Newtonsoft.Json.dll
- Autodesk.Revit.*.dll (from SDK)

---

## Quick Build Command (All-in-One)

```powershell
cd RevitAppBundle
dotnet restore && msbuild RevitFamilyMaker.csproj /p:Configuration=Release2025 /p:Platform=x64 && powershell -File ..\deployment\scripts\build.ps1
```

---

## Verify the Build

The ZIP should contain:
```
RevitFamilyMaker_2025.zip
├── Contents.xml
└── Contents/
    ├── RevitFamilyMaker.dll (your main code)
    ├── Newtonsoft.Json.dll
    └── Autodesk.Revit.*.dll (Revit API DLLs)
```

Check it:
```powershell
Expand-Archive -Path "deployment\output\RevitFamilyMaker_2025.zip" -DestinationPath "temp_check" -Force
dir temp_check
dir temp_check\Contents
```

---

## Alternative: Use a Cloud Windows VM

If you don't have local Windows access:

### Azure (Free Trial - $200 credit)
1. Create free account: https://azure.microsoft.com/free
2. Create Windows Server 2022 VM
3. RDP into it
4. Follow steps above

### AWS (Free Tier)
1. Launch Windows Server EC2 instance
2. RDP into it
3. Follow steps above

---

## Estimated Time

- **First time:** 15-20 minutes (installing VS, building)
- **Subsequent builds:** 2-3 minutes

---

## After Successful Build

You'll have a fully functional AI Revit Family Maker that can:
- Generate real Revit families from text prompts
- Execute in cloud via APS Design Automation
- Return production-ready .rfa files
- Handle parameters, dimensions, materials, constraints

🎉 **Your AI Revit Family Maker will be complete!** 🎉
