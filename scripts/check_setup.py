#!/usr/bin/env python3
"""
Setup Verification Script
Checks that all components are properly configured
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def print_status(component: str, status: bool, message: str = ""):
    """Print status with emoji"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {component}")
    if message:
        print(f"   {message}")


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_ok = version >= (3, 11)
    print_status(
        "Python Version",
        is_ok,
        f"Python {version.major}.{version.minor}.{version.micro}"
        if is_ok
        else f"Need Python 3.11+, found {version.major}.{version.minor}",
    )
    return is_ok


def check_dependencies():
    """Check required Python packages"""
    required = [
        "pydantic_ai",
        "pydantic",
        "pydantic_settings",
        "httpx",
        "PIL",
        "tenacity",
        "pytest",
    ]

    all_ok = True
    for package in required:
        try:
            if package == "pydantic_settings":
                __import__("pydantic_settings")
            elif package == "PIL":
                __import__("PIL")
            else:
                __import__(package)
            print_status(f"Package: {package}", True)
        except ImportError:
            print_status(f"Package: {package}", False, "Not installed")
            all_ok = False

    return all_ok


def check_env_file():
    """Check .env file exists and has required variables"""
    env_path = Path(__file__).parent.parent / ".env"

    if not env_path.exists():
        print_status(".env File", False, "File not found - copy from .env.example")
        return False

    required_vars = ["LLM_API_KEY", "APS_CLIENT_ID", "APS_CLIENT_SECRET"]
    missing = []

    with open(env_path) as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content:
                missing.append(var)

    if missing:
        print_status(".env File", False, f"Missing: {', '.join(missing)}")
        return False

    print_status(".env File", True, "All required variables present")
    return True


def check_settings():
    """Check settings can be loaded"""
    try:
        from revit_family_maker.settings import load_settings

        settings = load_settings()
        print_status("Settings", True, f"LLM Model: {settings.llm_model}")
        return True
    except Exception as e:
        print_status("Settings", False, str(e))
        return False


def check_tests():
    """Check if tests can run"""
    try:
        import pytest

        print_status("Test Framework", True, "pytest installed")
        return True
    except ImportError:
        print_status("Test Framework", False, "pytest not installed")
        return False


def check_project_structure():
    """Check project structure"""
    root = Path(__file__).parent.parent
    required_dirs = [
        "revit_family_maker",
        "tests",
        "RevitAppBundle",
        "deployment",
        "templates",
    ]

    all_ok = True
    for dir_name in required_dirs:
        dir_path = root / dir_name
        exists = dir_path.exists()
        print_status(f"Directory: {dir_name}", exists)
        all_ok = all_ok and exists

    return all_ok


def main():
    """Run all checks"""
    print("=" * 60)
    print("  AI Revit Family Maker - Setup Verification")
    print("=" * 60)
    print()

    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Project Structure": check_project_structure(),
        ".env File": check_env_file(),
        "Settings": check_settings(),
        "Test Framework": check_tests(),
    }

    print()
    print("=" * 60)
    print("  Summary")
    print("=" * 60)
    print()

    passed = sum(results.values())
    total = len(results)

    print(f"Checks Passed: {passed}/{total}")
    print()

    if passed == total:
        print("✅ All checks passed! You're ready to use the AI Revit Family Maker.")
        print()
        print("Next steps:")
        print("  1. Test with stubbed services:")
        print("     python main.py 'create a chair, 600mm wide'")
        print()
        print("  2. Deploy to production:")
        print("     See QUICKSTART.md and DEPLOYMENT_GUIDE.md")
        print()
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Quick fixes:")

        if not results[".env File"]:
            print("  • Copy .env.example to .env:")
            print("    cp .env.example .env")
            print("  • Add your OpenAI API key")

        if not results["Dependencies"]:
            print("  • Install dependencies:")
            print("    pip install -r requirements.txt")

        print()
        print("For detailed setup instructions, see:")
        print("  • QUICKSTART.md - Quick start guide")
        print("  • README.md - Full documentation")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
