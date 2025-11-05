#!/usr/bin/env python3
"""
APS Design Automation AppBundle Deployment Script
Uploads RevitFamilyMaker AppBundle to Autodesk Platform Services

Usage:
    python deploy_appbundle.py --version 2024 --alias production
    python deploy_appbundle.py --version 2025 --alias dev --description "Development build"
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from revit_family_maker.settings import load_settings


class APSAuthenticator:
    """Handles APS OAuth authentication"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://developer.api.autodesk.com"
        self.token = None

    def get_token(self) -> str:
        """Get 2-legged OAuth token"""
        if self.token:
            return self.token

        url = f"{self.base_url}/authentication/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "code:all",
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        result = response.json()
        self.token = result["access_token"]
        return self.token


class AppBundleDeployer:
    """Handles AppBundle deployment to APS Design Automation"""

    def __init__(self, auth: APSAuthenticator, nickname: str = "revitfamilymaker"):
        self.auth = auth
        self.nickname = nickname
        self.base_url = "https://developer.api.autodesk.com/da/us-east/v3"

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Content-Type": "application/json",
        }

    def create_or_update_appbundle(
        self,
        bundle_name: str,
        engine: str,
        description: str,
        zip_path: Path,
    ) -> dict:
        """Create or update an AppBundle"""

        # Check if AppBundle exists
        qualified_id = f"{self.nickname}.{bundle_name}+{engine}"
        url = f"{self.base_url}/appbundles/{qualified_id}"

        response = requests.get(url, headers=self._headers())
        exists = response.status_code == 200

        if exists:
            print(f"AppBundle {qualified_id} exists, creating new version...")
            return self._create_appbundle_version(bundle_name, zip_path)
        else:
            print(f"Creating new AppBundle {qualified_id}...")
            return self._create_appbundle(bundle_name, engine, description, zip_path)

    def _create_appbundle(
        self, bundle_name: str, engine: str, description: str, zip_path: Path
    ) -> dict:
        """Create new AppBundle"""

        payload = {
            "id": bundle_name,
            "engine": engine,
            "description": description,
        }

        url = f"{self.base_url}/appbundles"
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        result = response.json()

        print(f"  Created AppBundle: {result['id']}")

        # Upload zip
        self._upload_appbundle(result["uploadParameters"], zip_path)

        return result

    def _create_appbundle_version(self, bundle_name: str, zip_path: Path) -> dict:
        """Create new version of existing AppBundle"""

        qualified_id = f"{self.nickname}.{bundle_name}"
        url = f"{self.base_url}/appbundles/{qualified_id}/versions"

        response = requests.post(url, headers=self._headers())
        response.raise_for_status()
        result = response.json()

        print(f"  Created version: {result['version']}")

        # Upload zip
        self._upload_appbundle(result["uploadParameters"], zip_path)

        return result

    def _upload_appbundle(self, upload_params: dict, zip_path: Path):
        """Upload AppBundle zip to signed URL"""

        print(f"  Uploading: {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")

        with open(zip_path, "rb") as f:
            files = {"file": f}
            data = upload_params["formData"]
            response = requests.post(upload_params["endpointURL"], data=data, files=files)
            response.raise_for_status()

        print("  Upload complete!")

    def create_alias(self, bundle_name: str, version: int, alias_name: str) -> dict:
        """Create or update an alias pointing to a specific version"""

        qualified_id = f"{self.nickname}.{bundle_name}"
        url = f"{self.base_url}/appbundles/{qualified_id}/aliases"

        # Check if alias exists
        alias_url = f"{url}/{alias_name}"
        response = requests.get(alias_url, headers=self._headers())
        exists = response.status_code == 200

        payload = {"version": version, "id": alias_name}

        if exists:
            print(f"  Updating alias '{alias_name}' to version {version}...")
            response = requests.patch(alias_url, headers=self._headers(), json=payload)
        else:
            print(f"  Creating alias '{alias_name}' pointing to version {version}...")
            response = requests.post(url, headers=self._headers(), json=payload)

        response.raise_for_status()
        result = response.json()

        print(f"  Alias created: {result['id']}")
        return result


def main():
    parser = argparse.ArgumentParser(description="Deploy RevitFamilyMaker AppBundle to APS")
    parser.add_argument(
        "--version",
        choices=["2024", "2025"],
        required=True,
        help="Revit version (2024 or 2025)",
    )
    parser.add_argument(
        "--alias",
        default="production",
        help="Alias name for this version (default: production)",
    )
    parser.add_argument(
        "--description",
        default="RevitFamilyMaker AppBundle",
        help="AppBundle description",
    )
    parser.add_argument(
        "--nickname",
        default=None,
        help="APS nickname (default: from settings)",
    )

    args = parser.parse_args()

    # Load settings
    try:
        settings = load_settings()
    except Exception as e:
        print(f"Error loading settings: {e}")
        print("Make sure .env file exists with APS_CLIENT_ID and APS_CLIENT_SECRET")
        sys.exit(1)

    # Determine paths
    project_root = Path(__file__).parent.parent.parent
    zip_path = project_root / "deployment" / "output" / f"RevitFamilyMaker_{args.version}.zip"

    if not zip_path.exists():
        print(f"Error: AppBundle zip not found: {zip_path}")
        print("Run build.ps1 first to create the AppBundle packages")
        sys.exit(1)

    # Determine engine
    engine_map = {
        "2024": "Autodesk.Revit+2024",
        "2025": "Autodesk.Revit+2025",
    }
    engine = engine_map[args.version]
    bundle_name = f"RevitFamilyMaker{args.version}"

    print("=" * 60)
    print("APS AppBundle Deployment")
    print("=" * 60)
    print(f"Bundle Name: {bundle_name}")
    print(f"Engine: {engine}")
    print(f"Zip Path: {zip_path}")
    print(f"Alias: {args.alias}")
    print("=" * 60)
    print()

    # Authenticate
    print("Authenticating with APS...")
    auth = APSAuthenticator(settings.aps_client_id, settings.aps_client_secret)
    try:
        auth.get_token()
        print("  Authentication successful!")
    except Exception as e:
        print(f"  Authentication failed: {e}")
        sys.exit(1)

    # Deploy
    nickname = args.nickname or settings.aps_client_id.split("_")[0]
    deployer = AppBundleDeployer(auth, nickname=nickname)

    try:
        result = deployer.create_or_update_appbundle(
            bundle_name=bundle_name,
            engine=engine,
            description=args.description,
            zip_path=zip_path,
        )

        version = result.get("version", 1)
        deployer.create_alias(bundle_name, version, args.alias)

        print()
        print("=" * 60)
        print("Deployment Successful!")
        print("=" * 60)
        print(f"AppBundle ID: {result['id']}")
        print(f"Version: {version}")
        print(f"Alias: {args.alias}")
        print()
        print("Next steps:")
        print(f"  1. Update APS Activity to use this AppBundle")
        print(f"  2. Test with: {nickname}.{bundle_name}+{args.alias}")

    except Exception as e:
        print(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
