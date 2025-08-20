#!/bin/bash

# MKV Video Compressor Build Script
# This script builds the project for distribution

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_error "Python 3.8 or higher is required (found: $python_version)"
    exit 1
fi

print_status "Using Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install build dependencies
print_status "Installing build dependencies..."
pip install build twine wheel setuptools

# Install project dependencies
print_status "Installing project dependencies..."
pip install -r requirements.txt

# Install development dependencies
print_status "Installing development dependencies..."
pip install pytest pytest-cov black flake8 mypy

# Run tests
print_status "Running tests..."
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    print_error "Tests failed! Please fix issues before building."
    exit 1
fi

# Check code style
print_status "Checking code style..."
black --check src/ || {
    print_warning "Code style issues found. Run 'black src/' to fix."
}

flake8 src/ || {
    print_warning "Linting issues found."
}

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
print_status "Building package..."
python -m build

# Check the built package
print_status "Checking built package..."
twine check dist/*

print_status "Build completed successfully!"
print_status "Built packages:"
ls -la dist/

echo ""
print_status "To install the package locally:"
echo "  pip install dist/mkv_video_compressor-*.whl"
echo ""
print_status "To upload to PyPI (test):"
echo "  twine upload --repository testpypi dist/*"
echo ""
print_status "To upload to PyPI (production):"
echo "  twine upload dist/*"