#!/bin/bash
# Build and Deploy Script for Dungeon Master PyPI Package
# Usage: ./scripts/build_and_deploy.sh [--test-pypi]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're deploying to test PyPI
TEST_PYPI=false
if [[ "$1" == "--test-pypi" ]]; then
    TEST_PYPI=true
    print_warning "Deploying to Test PyPI"
else
    print_status "Deploying to Production PyPI"
fi

# Get the current version
CURRENT_VERSION=$(python -c "import dungeon_master; print(dungeon_master.__version__)")
print_status "Building Dungeon Master version: $CURRENT_VERSION"

# Verify we're in the correct directory
if [[ ! -f "pyproject.toml" ]] || [[ ! -f "setup.py" ]] || [[ ! -d "dungeon_master" ]]; then
    print_error "This script must be run from the project root directory"
    exit 1
fi

# Verify git status is clean (optional warning)
if ! git diff-index --quiet HEAD --; then
    print_warning "Working directory has uncommitted changes"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborting deployment"
        exit 1
    fi
fi

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    print_warning "No virtual environment detected. Activating venv..."
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment not found. Please create one or activate manually."
        exit 1
    fi
fi

# Install/upgrade build dependencies
print_status "Installing build dependencies..."
pip install --upgrade pip build twine wheel setuptools

# Clean up previous builds
print_status "Cleaning up previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Run tests before building
print_status "Running verification tests..."
if python tests/verify_installation.py; then
    print_success "All tests passed"
else
    print_error "Tests failed. Aborting deployment."
    exit 1
fi

# Build the package
print_status "Building package..."
python -m build

# Verify the build
print_status "Verifying build artifacts..."
if [[ ! -d "dist" ]] || [[ -z "$(ls -A dist/)" ]]; then
    print_error "Build failed - no artifacts in dist/ directory"
    exit 1
fi

# List built artifacts
print_status "Built artifacts:"
ls -la dist/

# Check the package with twine
print_status "Checking package integrity..."
twine check dist/*

# Upload to PyPI
if [[ "$TEST_PYPI" == "true" ]]; then
    print_status "Uploading to Test PyPI..."
    print_warning "Note: You'll need Test PyPI credentials"
    twine upload --repository testpypi dist/*
    print_success "Package uploaded to Test PyPI!"
    echo -e "${BLUE}Test your package with:${NC}"
    echo "pip install --index-url https://test.pypi.org/simple/ cursor-dungeon-master==$CURRENT_VERSION"
else
    print_status "Uploading to Production PyPI..."
    print_warning "Note: You'll need PyPI credentials (API token recommended)"

    # Confirm production deployment
    echo -e "${YELLOW}You are about to deploy version $CURRENT_VERSION to Production PyPI.${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Deployment cancelled"
        exit 1
    fi

    twine upload dist/*
    print_success "Package uploaded to Production PyPI!"
    echo -e "${BLUE}Install with:${NC}"
    echo "pip install cursor-dungeon-master==$CURRENT_VERSION"
fi

# Create git tag (optional)
read -p "Create git tag v$CURRENT_VERSION? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if git tag -a "v$CURRENT_VERSION" -m "Release version $CURRENT_VERSION"; then
        print_success "Git tag v$CURRENT_VERSION created"
        read -p "Push tag to remote? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git push origin "v$CURRENT_VERSION"
            print_success "Tag pushed to remote"
        fi
    else
        print_warning "Tag creation failed (may already exist)"
    fi
fi

print_success "🎉 Deployment completed successfully!"
print_status "Version $CURRENT_VERSION is now available on PyPI"

# Show next steps
echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Update project documentation with new version"
echo "2. Announce the release"
echo "3. Close any related GitHub issues"
echo "4. Update any dependent projects"
