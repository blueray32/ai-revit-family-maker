#!/bin/bash
# Script to update .env with your real APS credentials

echo "=========================================="
echo "Update APS Credentials"
echo "=========================================="
echo ""
echo "Please paste your FULL Client ID (starts with 3CA4):"
read -r CLIENT_ID

echo ""
echo "Please paste your FULL Client Secret (starts with ME99):"
read -r CLIENT_SECRET

echo ""
echo "Updating .env file..."

# Backup current .env
cp .env .env.backup

# Update credentials in .env
sed -i.tmp "s/APS_CLIENT_ID=.*/APS_CLIENT_ID=$CLIENT_ID/" .env
sed -i.tmp "s/APS_CLIENT_SECRET=.*/APS_CLIENT_SECRET=$CLIENT_SECRET/" .env
rm .env.tmp

# Also update region to EU
sed -i.tmp "s/APS_DA_ACTIVITY=.*/APS_DA_ACTIVITY=revfam.make:v1/" .env
rm .env.tmp 2>/dev/null || true

echo ""
echo "✅ .env file updated!"
echo ""
echo "Backup saved as: .env.backup"
echo ""
echo "Next: Test authentication with:"
echo "  python deployment/scripts/setup_aps.py --test-auth"
