# Building the C# AppBundle via GitHub Actions (No Windows Required!)

## Overview
> ⚠️ **Heads-up:** Microsoft-hosted GitHub Actions runners cannot currently restore Autodesk's private `DesignAutomationBridge` package, so the workflow in this repo will fail unless you host your own Windows runner that already has the Revit SDK installed. The steps below remain useful if you bring your own runner or if Autodesk later exposes the dependency publicly; otherwise, plan on building locally or via a Windows VM.

Since you're on macOS, we'll use **GitHub Actions** to automatically build the C# AppBundle on Windows in the cloud **once a compatible runner is available**.

## ✅ Prerequisites Completed
- [x] APS credentials configured in .env
- [x] APS authentication tested successfully
- [x] GitHub Actions workflow created (`.github/workflows/build-appbundle.yml`)

## 🚀 Build Steps

### Option 1: Auto-Build (Push to GitHub)
```bash
# Commit and push the workflow
git add .github/workflows/build-appbundle.yml RevitAppBundle/
git commit -m "Add GitHub Actions workflow for AppBundle build"
git push origin master
```

The workflow will **automatically trigger** and build both Revit 2024 and 2025 versions.

### Option 2: Manual Trigger
1. Push the workflow file to GitHub (as above)
2. Go to your repository on GitHub
3. Click **Actions** tab
4. Click **Build Revit AppBundle** workflow
5. Click **Run workflow** → **Run workflow**

### Option 3: Local Windows Build (if you have Windows)
If you have access to a Windows machine:

```powershell
# On Windows with Visual Studio installed
cd RevitAppBundle
dotnet restore
msbuild RevitFamilyMaker.csproj /p:Configuration=Release2025 /p:Platform=x64

# Package for APS
powershell -File ../deployment/scripts/build.ps1
```

## 📥 Download Built Artifacts

After the GitHub Action completes (takes ~3-5 minutes):

1. Go to **Actions** tab → Click the completed workflow run
2. Scroll down to **Artifacts** section
3. Download:
   - `RevitFamilyMaker-2024.zip` (if targeting Revit 2024)
   - `RevitFamilyMaker-2025.zip` (if targeting Revit 2025)

4. Move the downloaded ZIP to your project:
```bash
# After downloading from GitHub
mv ~/Downloads/RevitFamilyMaker-2025.zip ./deployment/
```

## 🔍 Verify the AppBundle

```bash
# Check contents
unzip -l deployment/RevitFamilyMaker-2025.zip

# Should contain:
# - Contents.xml (package manifest)
# - Contents/RevitFamilyMaker.dll (main plugin)
# - Contents/Newtonsoft.Json.dll
# - Contents/DesignAutomationBridge.dll
```

## ⏭️ Next Steps

Once you have the AppBundle ZIP:

```bash
# Deploy to APS
python deployment/scripts/deploy_appbundle.py \
  --zip-path deployment/RevitFamilyMaker-2025.zip \
  --revit-version 2025

# Create the Activity
python deployment/scripts/setup_aps.py --create-activity

# Test end-to-end
python -m revit_family_maker.cli
```

## 🎯 Current Status

✅ **Completed:**
- APS credentials configured (EU region)
- APS authentication tested
- GitHub Actions workflow created

🔄 **In Progress:**
- Building C# AppBundle (waiting for GitHub Actions)

⏳ **Next:**
- Download built AppBundle.zip
- Deploy to APS
- Create Activity
- Upload templates
- Test end-to-end

## 📋 Alternative: Use Existing Pre-built AppBundle

If you have a previously built AppBundle .zip file, you can skip the build step and proceed directly to deployment:

```bash
python deployment/scripts/deploy_appbundle.py \
  --zip-path path/to/your/AppBundle.zip \
  --revit-version 2025
```

## 🐛 Troubleshooting

**GitHub Actions fails with "NuGet restore error":**
- Check that `RevitFamilyMaker.csproj` is committed
- Verify NuGet package references are correct

**MSBuild fails:**
- Check .NET Framework 4.8 compatibility
- Verify Revit SDK NuGet packages are available

**ZIP is too large (>10 MB):**
- Remove unnecessary dependencies
- Check for duplicate DLLs
- Ensure only required files are packaged

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [APS Design Automation - AppBundles](https://aps.autodesk.com/en/docs/design-automation/v3/reference/http/appbundles-POST/)
- [Revit SDK on NuGet](https://www.nuget.org/packages/Autodesk.Revit.SDK/)
