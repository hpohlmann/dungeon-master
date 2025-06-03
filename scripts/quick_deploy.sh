#!/bin/bash
# Quick Deploy Script for Dungeon Master
# Usage: ./scripts/quick_deploy.sh

set -e

echo "🚀 Quick Deploy for Dungeon Master"
echo "=================================="

# Get version
VERSION=$(python -c "import dungeon_master; print(dungeon_master.__version__)")
echo "📦 Version: $VERSION"

# Quick checks
if [[ ! -f "pyproject.toml" ]]; then
    echo "❌ Must run from project root"
    exit 1
fi

# Clean and build
echo "🧹 Cleaning..."
rm -rf build/ dist/ *.egg-info/

echo "🔨 Building..."
python -m build

echo "✅ Checking..."
twine check dist/*

echo "📤 Uploading to PyPI..."
twine upload dist/*

echo "🎉 Done! Version $VERSION deployed to PyPI"
echo "📋 Install with: pip install cursor-dungeon-master==$VERSION"
