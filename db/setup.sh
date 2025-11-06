#!/bin/bash
# Archon Database Migration Setup Script
# ========================================

set -e

echo "=================================="
echo "Archon Migration Setup"
echo "=================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install Python 3: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Install pip: python3 -m ensurepip --upgrade"
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✓ Dependencies installed"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "WARNING: .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "✓ Created .env file"
    echo ""
    echo "IMPORTANT: Edit .env and add your Supabase credentials:"
    echo "  - SUPABASE_URL"
    echo "  - SUPABASE_SERVICE_KEY"
    echo ""
    echo "Get these from: Supabase Dashboard > Settings > API"
    echo ""
else
    echo "✓ .env file exists"
fi

# Make migrate.py executable
chmod +x migrate.py

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env with your Supabase credentials"
echo "  2. Run: python3 migrate.py status"
echo "  3. Run: python3 migrate.py up --dry-run"
echo "  4. Run: python3 migrate.py up"
echo ""
