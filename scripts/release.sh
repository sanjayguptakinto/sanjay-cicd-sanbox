#!/bin/bash

# Release script for HAR Analyzer
# This script builds and prepares a release

set -e

VERSION=${1:-"1.0.0"}
echo "🚀 Preparing release v$VERSION..."

# Ensure we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Run from project root."
    exit 1
fi

# Run quality checks
echo "🔍 Running quality checks..."
pre-commit run --all-files

# Run tests
echo "🧪 Running test suite..."
pytest --cov=src --cov-report=term-missing

# Build package
echo "📦 Building package..."
python -m build

# Check distribution
echo "✅ Checking distribution..."
python -m twine check dist/*

echo ""
echo "✅ Release v$VERSION is ready!"
echo "📦 Distribution files:"
ls -la dist/

echo ""
echo "🚀 Next steps:"
echo "   1. Test the wheel: pip install dist/har_analyzer-$VERSION-py3-none-any.whl"
echo "   2. Create git tag: git tag v$VERSION"
echo "   3. Push tag: git push origin v$VERSION"
echo "   4. Upload to PyPI: twine upload dist/*"
echo ""
