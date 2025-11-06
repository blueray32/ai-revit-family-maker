# Build script for RevitFamilyMaker AppBundle
# Compiles for both Revit 2024 and 2025
# Usage: .\build.ps1 [-Configuration Release] [-Clean]

param(
    [string]$Configuration = "Release",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ProjectFile = Join-Path $ProjectRoot "RevitAppBundle\RevitFamilyMaker.csproj"
$OutputDir = Join-Path $ProjectRoot "deployment\output"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "RevitFamilyMaker AppBundle Build Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Resolve dotnet CLI (covers both .NET Framework and .NET 8 targets)
try {
    $dotnet = Get-Command dotnet -ErrorAction Stop | Select-Object -First 1
} catch {
    Write-Error "dotnet CLI not found. Please install .NET SDK 8.0 or later."
    exit 1
}
$dotnetPath = $dotnet.Source

Write-Host "Using dotnet CLI: $dotnetPath" -ForegroundColor Green
Write-Host ""

Write-Host "Restoring NuGet packages..." -ForegroundColor Yellow
& $dotnetPath restore $ProjectFile
if ($LASTEXITCODE -ne 0) {
    Write-Error "dotnet restore failed."
    exit 1
}
Write-Host "Restore complete." -ForegroundColor Green
Write-Host ""

$configuration2024 = if ($Configuration -ieq "Debug") { "Debug" } else { "Release2024" }
$configuration2025 = if ($Configuration -ieq "Debug") { "Debug" } else { "Release2025" }
$configsToClean = @($configuration2024, $configuration2025) | Sort-Object -Unique

# Clean if requested
if ($Clean) {
    Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
    foreach ($config in $configsToClean) {
        & $dotnetPath clean $ProjectFile -c $config
        if ($LASTEXITCODE -ne 0) {
            Write-Error "dotnet clean failed for configuration '$config'."
            exit 1
        }
    }
    if (Test-Path $OutputDir) {
        Remove-Item -Recurse -Force $OutputDir
    }
    Write-Host "Clean complete." -ForegroundColor Green
    Write-Host ""
}

# Create output directory
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# Build for Revit 2024
Write-Host "Building for Revit 2024..." -ForegroundColor Yellow
$Output2024 = Join-Path $OutputDir "Revit2024"
New-Item -ItemType Directory -Force -Path $Output2024 | Out-Null

& $dotnetPath build $ProjectFile `
    -c $configuration2024 `
    "-p:OutputPath=$Output2024" `
    --no-restore `
    -v minimal

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed for Revit 2024"
    exit 1
}
Write-Host "Revit 2024 build complete." -ForegroundColor Green
Write-Host ""

# Build for Revit 2025
Write-Host "Building for Revit 2025..." -ForegroundColor Yellow
$Output2025 = Join-Path $OutputDir "Revit2025"
New-Item -ItemType Directory -Force -Path $Output2025 | Out-Null

& $dotnetPath publish $ProjectFile `
    -c $configuration2025 `
    -r win-x64 `
    --no-restore `
    --no-self-contained `
    "-o" $Output2025 `
    -v minimal

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed for Revit 2025"
    exit 1
}
Write-Host "Revit 2025 build complete." -ForegroundColor Green
Write-Host ""

# Create AppBundle zip files
Write-Host "Creating AppBundle packages..." -ForegroundColor Yellow

function Create-AppBundle {
    param(
        [string]$Version,
        [string]$SourceDir
    )

    $ZipName = "RevitFamilyMaker_$Version.zip"
    $ZipPath = Join-Path $OutputDir $ZipName

    # Copy PackageContents.xml
    $PackageXml = Join-Path $ProjectRoot "RevitAppBundle\PackageContents.xml"
    Copy-Item $PackageXml $SourceDir

    # Create zip
    if (Test-Path $ZipPath) {
        Remove-Item $ZipPath -Force
    }

    Compress-Archive -Path "$SourceDir\*" -DestinationPath $ZipPath -CompressionLevel Optimal

    Write-Host "  Created: $ZipName" -ForegroundColor Green
    $size = (Get-Item $ZipPath).Length / 1MB
    Write-Host "  Size: $($size.ToString('F2')) MB" -ForegroundColor Gray
}

Create-AppBundle -Version "2024" -SourceDir $Output2024
Create-AppBundle -Version "2025" -SourceDir $Output2025

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "AppBundle packages created in: $OutputDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Upload AppBundle to APS using deploy_appbundle.py" -ForegroundColor White
Write-Host "  2. Create APS Activity using the activity definition" -ForegroundColor White
Write-Host "  3. Update .env with activity alias and credentials" -ForegroundColor White
