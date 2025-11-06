#!/usr/bin/env python3
"""
Simple script to update .env with your APS credentials
"""

import sys
from pathlib import Path

def update_env():
    print("=" * 60)
    print("Update APS Credentials in .env")
    print("=" * 60)
    print()
    print("Please paste your credentials from the APS portal:")
    print()

    # Get credentials
    client_id = input("Client ID (starts with 3CA4): ").strip()
    client_secret = input("Client Secret (starts with ME99): ").strip()

    if not client_id or not client_secret:
        print("\n❌ Both Client ID and Secret are required!")
        return False

    # Read current .env
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print(f"\n❌ .env file not found at: {env_path}")
        return False

    # Backup
    backup_path = env_path.with_suffix(".env.backup")
    env_path.read_text()  # Test read
    backup_path.write_text(env_path.read_text())
    print(f"\n✅ Backup created: {backup_path.name}")

    # Update .env
    lines = []
    with open(env_path) as f:
        for line in f:
            if line.startswith("APS_CLIENT_ID="):
                lines.append(f"APS_CLIENT_ID={client_id}\n")
            elif line.startswith("APS_CLIENT_SECRET="):
                lines.append(f"APS_CLIENT_SECRET={client_secret}\n")
            elif line.startswith("APS_REGION="):
                lines.append("APS_REGION=eu-west\n")
            elif line.strip() == "":
                # Add APS_REGION if it doesn't exist yet
                if lines and not any("APS_REGION=" in l for l in lines):
                    if any("APS_CLIENT_SECRET=" in l for l in lines[-5:]):
                        lines.append("APS_REGION=eu-west\n")
                lines.append(line)
            else:
                lines.append(line)

    # Add APS_REGION if still not present
    if not any("APS_REGION=" in l for l in lines):
        # Find APS section and add it
        for i, line in enumerate(lines):
            if "APS_CLIENT_SECRET=" in line:
                lines.insert(i + 1, "APS_REGION=eu-west\n")
                break

    # Write back
    with open(env_path, 'w') as f:
        f.writelines(lines)

    print(f"✅ Updated: {env_path}")
    print()
    print("Changes made:")
    print(f"  APS_CLIENT_ID = {client_id[:10]}...{client_id[-4:]}")
    print(f"  APS_CLIENT_SECRET = {client_secret[:4]}...{client_secret[-4:]}")
    print(f"  APS_REGION = eu-west")
    print()
    print("Next step: Test authentication")
    print("  python deployment/scripts/setup_aps.py --test-auth")
    return True

if __name__ == "__main__":
    try:
        success = update_env()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
