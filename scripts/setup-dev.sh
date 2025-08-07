#!/bin/bash

# Development setup script
# This script sets up the development environment for HAR Analyzer

set -e

echo "🚀 Setting up HAR Analyzer development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.9"

if python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install package in development mode
echo "📦 Installing HAR Analyzer in development mode..."
pip install -e ".[dev,test]"

# Install pre-commit hooks
echo "🔗 Setting up pre-commit hooks..."
pre-commit install

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🚀 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run tests: pytest"
echo "   3. Run quality checks: pre-commit run --all-files"
echo "   4. Start developing!"
echo ""
