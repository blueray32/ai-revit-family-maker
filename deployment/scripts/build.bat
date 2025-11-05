@echo off
REM Build script for RevitFamilyMaker AppBundle (Windows Batch)
REM Alternative to PowerShell for users without PS execution rights
REM Usage: build.bat [Release|Debug]

setlocal enabledelayedexpansion

REM Set configuration (default to Release)
set CONFIG=%1
if "%CONFIG%"=="" set CONFIG=Release

echo ============================================================
echo RevitFamilyMaker AppBundle Build Script
echo ============================================================
echo.

REM Find MSBuild
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

if not exist "%VSWHERE%" (
    echo ERROR: vswhere.exe not found
    echo Please install Visual Studio 2019 or later
    pause
    exit /b 1
)

for /f "delims=" %%i in ('"%VSWHERE%" -latest -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe') do set MSBUILD=%%i

if "%MSBUILD%"=="" (
    echo ERROR: MSBuild not found
    echo Please install Visual Studio 2019 or later
    pause
    exit /b 1
)

echo Using MSBuild: %MSBUILD%
echo.

REM Set paths
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..
set PROJECT_FILE=%PROJECT_ROOT%\RevitAppBundle\RevitFamilyMaker.csproj
set OUTPUT_DIR=%PROJECT_ROOT%\deployment\output

echo Project: %PROJECT_FILE%
echo Output: %OUTPUT_DIR%
echo.

REM Clean output directory
if exist "%OUTPUT_DIR%" (
    echo Cleaning output directory...
    rmdir /s /q "%OUTPUT_DIR%"
)
mkdir "%OUTPUT_DIR%"

REM Build for Revit 2024
echo.
echo ========================================
echo Building for Revit 2024...
echo ========================================
set OUTPUT_2024=%OUTPUT_DIR%\Revit2024
mkdir "%OUTPUT_2024%"

"%MSBUILD%" "%PROJECT_FILE%" /t:Build /p:Configuration=%CONFIG% /p:TargetFrameworkVersion=v4.8 /p:OutputPath="%OUTPUT_2024%" /p:DefineConstants=REVIT2024 /verbosity:minimal

if errorlevel 1 (
    echo.
    echo ERROR: Build failed for Revit 2024
    pause
    exit /b 1
)
echo.
echo SUCCESS: Revit 2024 build complete
echo.

REM Build for Revit 2025
echo ========================================
echo Building for Revit 2025...
echo ========================================
set OUTPUT_2025=%OUTPUT_DIR%\Revit2025
mkdir "%OUTPUT_2025%"

"%MSBUILD%" "%PROJECT_FILE%" /t:Build /p:Configuration=%CONFIG% /p:TargetFrameworkVersion=v4.8 /p:OutputPath="%OUTPUT_2025%" /p:DefineConstants=REVIT2025 /verbosity:minimal

if errorlevel 1 (
    echo.
    echo ERROR: Build failed for Revit 2025
    pause
    exit /b 1
)
echo.
echo SUCCESS: Revit 2025 build complete
echo.

REM Create AppBundle zip files
echo ========================================
echo Creating AppBundle packages...
echo ========================================
echo.

REM Copy PackageContents.xml to both output directories
copy "%PROJECT_ROOT%\RevitAppBundle\PackageContents.xml" "%OUTPUT_2024%"
copy "%PROJECT_ROOT%\RevitAppBundle\PackageContents.xml" "%OUTPUT_2025%"

REM Create zip files using PowerShell (available on Windows 10+)
powershell -Command "Compress-Archive -Path '%OUTPUT_2024%\*' -DestinationPath '%OUTPUT_DIR%\RevitFamilyMaker_2024.zip' -Force"
powershell -Command "Compress-Archive -Path '%OUTPUT_2025%\*' -DestinationPath '%OUTPUT_DIR%\RevitFamilyMaker_2025.zip' -Force"

echo.
echo SUCCESS: AppBundle packages created
echo   - RevitFamilyMaker_2024.zip
echo   - RevitFamilyMaker_2025.zip
echo.

REM Display file sizes
for %%f in ("%OUTPUT_DIR%\*.zip") do (
    set /a "size=%%~zf / 1048576"
    echo   %%~nxf: !size! MB
)

echo.
echo ============================================================
echo Build Complete!
echo ============================================================
echo.
echo AppBundle packages created in: %OUTPUT_DIR%
echo.
echo Next steps:
echo   1. Deploy to APS: python deployment/scripts/deploy_appbundle.py
echo   2. Create Activity using deployment/aps_activity.json
echo   3. Update .env with activity details
echo.
pause
