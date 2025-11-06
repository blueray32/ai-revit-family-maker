# Add GitHub Actions Workflow

Your code is pushed to: **https://github.com/blueray32/ai-revit-family-maker**

However, the workflow file couldn't be pushed due to token permissions. Here's the easiest way to add it:

## Option 1: Add via GitHub Web Interface (Easiest - 2 minutes)

1. **Go to your repository:**
   https://github.com/blueray32/ai-revit-family-maker

2. **Click "Add file" → "Create new file"**

3. **In the filename box, type:**
   ```
   .github/workflows/build-appbundle.yml
   ```
   (GitHub will automatically create the folders)

4. **Paste this content:**

```yaml
name: Build Revit AppBundle

on:
  workflow_dispatch:
  push:
    branches: [master, main]
    paths:
      - 'RevitAppBundle/**'
      - '.github/workflows/build-appbundle.yml'

jobs:
  build:
    runs-on: windows-latest

    strategy:
      matrix:
        revit_version: [2024, 2025]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Setup MSBuild
        uses: microsoft/setup-msbuild@v2

      - name: Restore NuGet packages
        run: dotnet restore RevitAppBundle/RevitFamilyMaker.csproj

      - name: Build AppBundle for Revit ${{ matrix.revit_version }}
        run: |
          msbuild RevitAppBundle/RevitFamilyMaker.csproj `
            /p:Configuration=Release${{ matrix.revit_version }} `
            /p:Platform=x64 `
            /p:OutputPath=bin/Release${{ matrix.revit_version }}/ `
            /v:minimal

      - name: Create AppBundle ZIP
        shell: pwsh
        run: |
          $version = "${{ matrix.revit_version }}"
          $binPath = "RevitAppBundle/bin/Release$version"
          $zipPath = "RevitFamilyMaker_$version.zip"

          $packageXml = @"
          <?xml version="1.0" encoding="utf-8"?>
          <ApplicationPackage
            SchemaVersion="1.0"
            ProductType="Application"
            Name="RevitFamilyMaker"
            AppVersion="1.0.0"
            Description="AI-powered Revit family generator">
            <CompanyDetails Name="Revit Family Maker" Email="contact@example.com" Url="https://example.com" />
            <Components Description="Revit Family Maker Components">
              <RuntimeRequirements OS="Win64" Platform="Revit" SeriesMin="R$version" SeriesMax="R$version" />
              <ComponentEntry AppName="RevitFamilyMaker" ModuleName="./Contents/RevitFamilyMaker.dll" AppDescription="Family Maker Command" LoadOnRevitStartup="False" />
            </Components>
          </ApplicationPackage>
          "@

          New-Item -ItemType Directory -Force -Path "$binPath/Contents"
          $packageXml | Out-File -FilePath "$binPath/Contents.xml" -Encoding UTF8

          Copy-Item "$binPath/*.dll" "$binPath/Contents/" -Force
          Copy-Item "$binPath/Contents.xml" "$binPath/" -Force

          Compress-Archive -Path "$binPath/Contents.xml", "$binPath/Contents" -DestinationPath $zipPath -Force

          Write-Host "✅ Created $zipPath"

      - name: Upload AppBundle artifact
        uses: actions/upload-artifact@v4
        with:
          name: RevitFamilyMaker-${{ matrix.revit_version }}
          path: RevitFamilyMaker_${{ matrix.revit_version }}.zip
          retention-days: 30

      - name: Display build info
        shell: pwsh
        run: |
          $zipPath = "RevitFamilyMaker_${{ matrix.revit_version }}.zip"
          $size = (Get-Item $zipPath).Length / 1MB
          Write-Host "📦 AppBundle for Revit ${{ matrix.revit_version }}: $([math]::Round($size, 2)) MB"
```

5. **Click "Commit changes"** (commit directly to master)

---

## Option 2: Copy from local file

The workflow file is already in your local repo. You can copy it:

```bash
# The file is here:
cat .github/workflows/build-appbundle.yml

# Or open in editor:
open .github/workflows/build-appbundle.yml
```

Then follow steps 1-5 above to paste it into GitHub.

---

## After Adding the Workflow

### Manually Trigger the Build:

1. Go to: https://github.com/blueray32/ai-revit-family-maker/actions
2. Click "Build Revit AppBundle" on the left
3. Click "Run workflow" button → "Run workflow"
4. Wait ~3-5 minutes for the build to complete

### Download the Built AppBundle:

1. Click on the completed workflow run
2. Scroll down to "Artifacts"
3. Download `RevitFamilyMaker-2025.zip`

### Deploy to APS:

```bash
# Move downloaded file to deployment folder
mv ~/Downloads/RevitFamilyMaker-2025.zip ./deployment/output/

# Deploy to APS
python deployment/scripts/deploy_appbundle.py --version 2025
```

---

## Alternative: Fix GitHub Token (More Complex)

If you want to push workflow files from CLI in future:

1. Go to: https://github.com/settings/tokens
2. Click on your token
3. Add "workflow" scope
4. Update token in: `gh auth login`

Then you can push the workflow:
```bash
git add .github/workflows/build-appbundle.yml
git commit -m "feat: add workflow for AppBundle builds"
git push
```

---

## Quick Link

**Add workflow file now:** https://github.com/blueray32/ai-revit-family-maker/new/master?filename=.github/workflows/build-appbundle.yml

Copy the YAML content above and paste it!
