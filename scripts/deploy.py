#!/usr/bin/env python3
"""
Deployment script for cursor-dungeon-master package.

This script helps with versioning, building, and publishing to PyPI.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def get_current_version():
    """Get the current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    with open(pyproject_path) as f:
        for line in f:
            if line.strip().startswith("version ="):
                version = line.split("=")[1].strip().strip('"')
                return version
    
    raise ValueError("Version not found in pyproject.toml")


def update_version(new_version):
    """Update the version in pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace version line
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("version ="):
            lines[i] = f'version = "{new_version}"'
            break
    
    pyproject_path.write_text("\n".join(lines))
    print(f"Updated version to {new_version}")


def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")


def check_package():
    """Check the package with twine."""
    print("Checking package...")
    run_command("twine check dist/*")


def publish_test():
    """Publish to Test PyPI."""
    print("Publishing to Test PyPI...")
    run_command("twine upload --repository testpypi dist/*")


def publish_pypi():
    """Publish to PyPI."""
    print("Publishing to PyPI...")
    run_command("twine upload dist/*")


def clean_build():
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    run_command("rm -rf build/ dist/ *.egg-info/", check=False)


def main():
    parser = argparse.ArgumentParser(description="Deploy cursor-dungeon-master package")
    parser.add_argument("--version", help="Set new version")
    parser.add_argument("--build", action="store_true", help="Build package")
    parser.add_argument("--check", action="store_true", help="Check package")
    parser.add_argument("--test", action="store_true", help="Publish to Test PyPI")
    parser.add_argument("--publish", action="store_true", help="Publish to PyPI")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--all", action="store_true", help="Full release process")
    
    args = parser.parse_args()
    
    if args.version:
        update_version(args.version)
    
    if args.clean or args.all:
        clean_build()
    
    if args.build or args.all:
        build_package()
    
    if args.check or args.all:
        check_package()
    
    if args.test:
        publish_test()
    
    if args.publish or args.all:
        # Final confirmation for PyPI
        current_version = get_current_version()
        response = input(f"Publish version {current_version} to PyPI? (y/N): ")
        if response.lower() == "y":
            publish_pypi()
        else:
            print("Publishing cancelled.")
    
    if not any(vars(args).values()):
        parser.print_help()


if __name__ == "__main__":
    main() 