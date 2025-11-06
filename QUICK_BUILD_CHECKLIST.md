# ✅ Quick Build Checklist

## What You Need

🖥️ **Windows Machine** (physical, VM, or remote desktop)
- Can be your own PC, a VM (Azure/AWS), or remote Windows access

---

## The 5-Minute Build Process

### On Windows:

```powershell
# 1. Clone repo
git clone https://github.com/blueray32/ai-revit-family-maker.git
cd ai-revit-family-maker\RevitAppBundle

# 2. Restore & Build
dotnet restore
msbuild RevitFamilyMaker.csproj /p:Configuration=Release2025 /p:Platform=x64

# 3. Package (use the automated script)
cd ..
powershell -File deployment\scripts\build.ps1

# Done! File is at: deployment\output\RevitFamilyMaker_2025.zip
```

### Transfer to Mac:

Copy `RevitFamilyMaker_2025.zip` from Windows to your Mac via:
- USB drive
- Network share
- Git (commit & push from Windows, pull on Mac)
- Cloud storage (Dropbox, Drive, etc.)

### On Mac (Deploy):

```bash
cd "/Users/ciarancox/AI Revit Family Maker Assistant"

# Move the built file
mv ~/Downloads/RevitFamilyMaker_2025.zip ./deployment/output/

# Deploy to APS
python deployment/scripts/deploy_appbundle.py --version 2025

# Test it!
python -m revit_family_maker.cli
```

---

## Prerequisite: Visual Studio 2022

**First time only** (15 minutes):
1. Download: https://visualstudio.microsoft.com/downloads/
2. Install: Select ".NET desktop development" workload
3. Restart Windows

---

## Don't Have Windows?

### Option 1: Azure Free Trial
- $200 credit, no commitment
- https://azure.microsoft.com/free
- Spin up Windows Server VM
- RDP in and build

### Option 2: AWS Free Tier
- Windows Server EC2 instance
- https://aws.amazon.com/free
- RDP in and build

### Option 3: Ask a Friend
- Clone your repo: `git clone https://github.com/blueray32/ai-revit-family-maker.git`
- Run the 3 commands above
- Send you the ZIP file

---

## After Deploy

**Test your AI Revit Family Maker:**

```bash
python -m revit_family_maker.cli
```

Type a prompt like:
```
Generate a modern office desk family with:
- Width: 60 inches
- Depth: 30 inches
- Height: 29 inches
- Material: Wood
```

The agent will:
1. Analyze your prompt with AI
2. Generate parameters JSON
3. Submit WorkItem to APS
4. Run Revit in the cloud
5. Download the .rfa file
6. Save to `output/families/`

🎉 **You'll have a real Revit family file!**

---

## Need Help?

**Full Guide:** See `WINDOWS_BUILD_GUIDE.md`

**Repository:** https://github.com/blueray32/ai-revit-family-maker

**Deployment Docs:** See `DEPLOYMENT_COMPLETE.md`
