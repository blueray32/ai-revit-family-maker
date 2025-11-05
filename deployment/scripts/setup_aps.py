#!/usr/bin/env python3
"""
APS (Autodesk Platform Services) Setup and Testing Script
Helps configure and validate APS credentials

Usage:
    python setup_aps.py --test-auth          # Test authentication only
    python setup_aps.py --list-appbundles   # List your AppBundles
    python setup_aps.py --list-activities   # List your Activities
    python setup_aps.py --setup             # Interactive setup
"""

import argparse
import sys
from pathlib import Path

import requests

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class APSSetup:
    """Helper for APS setup and validation"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://developer.api.autodesk.com"
        self.da_base = f"{self.base_url}/da/us-east/v3"
        self.token = None

    def authenticate(self) -> bool:
        """Get 2-legged OAuth token"""
        print("🔐 Authenticating with APS...")

        url = f"{self.base_url}/authentication/v2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "code:all",
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()
            self.token = result["access_token"]
            expires_in = result.get("expires_in", 3600)
            print(f"✅ Authentication successful! Token expires in {expires_in} seconds.")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False

    def _headers(self) -> dict:
        """Get headers with bearer token"""
        if not self.token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_nickname(self) -> str:
        """Get APS nickname (forge ID)"""
        try:
            response = requests.get(f"{self.da_base}/forgeapps/me", headers=self._headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get nickname: {e}")
            return self.client_id.split("_")[0]  # Fallback

    def list_appbundles(self) -> list:
        """List all AppBundles"""
        print("\n📦 Listing AppBundles...")

        try:
            response = requests.get(f"{self.da_base}/appbundles", headers=self._headers())
            response.raise_for_status()
            bundles = response.json().get("data", [])

            if not bundles:
                print("  No AppBundles found.")
                return []

            print(f"  Found {len(bundles)} AppBundle(s):\n")
            for bundle in bundles:
                print(f"    • {bundle}")

            return bundles
        except Exception as e:
            print(f"❌ Failed to list AppBundles: {e}")
            return []

    def list_activities(self) -> list:
        """List all Activities"""
        print("\n⚙️  Listing Activities...")

        try:
            response = requests.get(f"{self.da_base}/activities", headers=self._headers())
            response.raise_for_status()
            activities = response.json().get("data", [])

            if not activities:
                print("  No Activities found.")
                return []

            print(f"  Found {len(activities)} Activity(ies):\n")
            for activity in activities:
                print(f"    • {activity}")

            return activities
        except Exception as e:
            print(f"❌ Failed to list Activities: {e}")
            return []

    def get_appbundle_details(self, bundle_id: str):
        """Get details of a specific AppBundle"""
        try:
            response = requests.get(f"{self.da_base}/appbundles/{bundle_id}", headers=self._headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get AppBundle details: {e}")
            return None

    def get_activity_details(self, activity_id: str):
        """Get details of a specific Activity"""
        try:
            response = requests.get(f"{self.da_base}/activities/{activity_id}", headers=self._headers())
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Failed to get Activity details: {e}")
            return None


def interactive_setup():
    """Interactive setup wizard"""
    print("=" * 60)
    print("APS Design Automation Setup Wizard")
    print("=" * 60)
    print()

    print("Step 1: Get your APS credentials")
    print("  1. Go to: https://aps.autodesk.com/myapps")
    print("  2. Create an app or select an existing one")
    print("  3. Copy your Client ID and Client Secret")
    print()

    client_id = input("Enter your APS Client ID: ").strip()
    client_secret = input("Enter your APS Client Secret: ").strip()

    if not client_id or not client_secret:
        print("❌ Client ID and Secret are required.")
        return

    print()
    aps = APSSetup(client_id, client_secret)

    if not aps.authenticate():
        return

    nickname = aps.get_nickname()
    print(f"📛 Your APS nickname: {nickname}")
    print()

    # List resources
    bundles = aps.list_appbundles()
    activities = aps.list_activities()

    # Generate .env template
    print()
    print("=" * 60)
    print("Configuration for .env file:")
    print("=" * 60)
    print()
    print(f"APS_CLIENT_ID={client_id}")
    print(f"APS_CLIENT_SECRET={client_secret}")

    if bundles:
        latest_bundle = bundles[-1]
        print(f"APS_DA_BUNDLE_ALIAS=production")
        print(f"# Latest bundle: {latest_bundle}")

    if activities:
        latest_activity = activities[-1]
        print(f"APS_DA_ACTIVITY={latest_activity}")
    else:
        print(f"APS_DA_ACTIVITY={nickname}.RevitFamilyMakerActivity+production")
        print(f"# ⚠️  No activities found - you need to create one!")

    print(f"APS_TEMPLATE_URL=https://your-storage.com/templates/")
    print()

    print("Next steps:")
    print("  1. Copy the above configuration to your .env file")
    print("  2. Build and deploy the AppBundle: deployment/scripts/build.ps1")
    print("  3. Upload AppBundle: python deployment/scripts/deploy_appbundle.py")
    print("  4. Create Activity using deployment/aps_activity.json")
    print("  5. Upload templates to cloud storage")
    print("  6. Test end-to-end: python main.py 'create a chair'")


def main():
    parser = argparse.ArgumentParser(description="APS Setup and Testing")
    parser.add_argument("--test-auth", action="store_true", help="Test authentication only")
    parser.add_argument("--list-appbundles", action="store_true", help="List your AppBundles")
    parser.add_argument("--list-activities", action="store_true", help="List your Activities")
    parser.add_argument("--setup", action="store_true", help="Interactive setup wizard")
    parser.add_argument("--client-id", help="APS Client ID (or use .env)")
    parser.add_argument("--client-secret", help="APS Client Secret (or use .env)")

    args = parser.parse_args()

    # Determine credentials source
    client_id = args.client_id
    client_secret = args.client_secret

    if not client_id or not client_secret:
        # Try to load from .env
        try:
            from revit_family_maker.settings import load_settings
            settings = load_settings()
            client_id = settings.aps_client_id
            client_secret = settings.aps_client_secret
            print("📋 Using credentials from .env file\n")
        except Exception as e:
            if args.setup:
                # Interactive setup will ask for credentials
                interactive_setup()
                return
            else:
                print(f"❌ Error loading settings: {e}")
                print("\nProvide credentials via:")
                print("  1. --client-id and --client-secret arguments")
                print("  2. .env file (APS_CLIENT_ID, APS_CLIENT_SECRET)")
                print("  3. --setup for interactive wizard")
                sys.exit(1)

    aps = APSSetup(client_id, client_secret)

    if args.setup:
        interactive_setup()
    elif args.test_auth:
        aps.authenticate()
    elif args.list_appbundles:
        if aps.authenticate():
            aps.list_appbundles()
    elif args.list_activities:
        if aps.authenticate():
            aps.list_activities()
    else:
        # Run all checks
        if aps.authenticate():
            aps.get_nickname()
            aps.list_appbundles()
            aps.list_activities()


if __name__ == "__main__":
    main()
