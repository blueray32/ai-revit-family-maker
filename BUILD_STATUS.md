# Build Status & Path Forward

## Current Status – 6 Nov 2025

✅ **Real Revit 2025 AppBundle built & deployed**

- Built both target frameworks locally (`dotnet build -c Release2024`, `dotnet publish -c Release2025 -r win-x64 --self-contained false`)
- Packaged the publish output plus `PackageContents.xml` into `deployment/output/RevitFamilyMaker_2025.zip` (≈295 KB, contains real DLLs)
- Ran `python deploy_fresh.py` to push the ZIP to APS and repoint alias `1`
- Activity `1Jp7…FamilyMakerActivity+1` now references the freshly uploaded bundle version

⚠️ **GitHub Actions builds still fail** because the Microsoft-hosted runner cannot access Autodesk's private DesignAutomationBridge dependency. Use local builds (mac cross-compile or Windows VM) until Autodesk exposes the package via a public feed.

📦 **Artifacts in repo**

- `deployment/output/RevitFamilyMaker_2025.zip` – latest build that is live in APS
- `RevitAppBundle/bin/Release2025/.../publish/` – source of truth for DLLs that were zipped
- `deployment/output/RevitFamilyMaker_2024/` – contains the older 2024 build output (not zipped/deployed this run)

🛰️ **APS state**

- AppBundle IDs available via `python deployment/scripts/setup_aps.py --list-appbundles`
  - `...FamilyMaker2025+1` points to the latest upload (alias `1`)
- Activity IDs confirmed via `--list-activities`
  - `...FamilyMakerActivity+1` now references the new bundle alias

🔄 **If you need to rebuild**

1. `dotnet restore RevitAppBundle/RevitFamilyMaker.csproj`
2. `dotnet build -c Release2024` (optional) and `dotnet publish -c Release2025 -r win-x64 --self-contained false`
3. Copy the publish folder into `deployment/output/Revit2025` and re-zip (use `deployment/scripts/build.ps1` on Windows or manual copy on macOS)
4. `python deploy_fresh.py` (or `python deployment/scripts/deploy_appbundle.py --version 2025 --alias 1` once it handles 409s gracefully)

🧪 **Verification**

- `python -m revit_family_maker.cli` – run an end-to-end job; expect the resulting `.rfa` and manifest to land in your configured output path
- `python deployment/scripts/setup_aps.py --test-auth` – confirm tokens if anything fails

📋 **Outstanding work**

- Decide whether to keep GH Actions workflow (currently broken) or disable it to avoid future noise
- Optionally repeat the packaging/deployment flow for the Revit 2024 configuration so both versions stay in sync
- Validate a real APS WorkItem to ensure the new DLL works with Autodesk’s runtime
