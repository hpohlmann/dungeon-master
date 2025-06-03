#!/usr/bin/env python3
# @track_context("installation_tests.md")
"""
Quick test script to verify Dungeon Master installation.
Run this after installing the package to ensure everything works.
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path

def test_import():
    """Test that the package can be imported."""
    print("🔍 Testing package import...")
    try:
        import dungeon_master
        print(f"✅ Successfully imported dungeon_master v{dungeon_master.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_cli():
    """Test that CLI commands work."""
    print("🔍 Testing CLI commands...")
    try:
        # Test help command
        result = subprocess.run([sys.executable, "-m", "dungeon_master.cli", "--help"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ CLI help command works")
        else:
            print(f"❌ CLI help failed: {result.stderr}")
            return False

        # Test console script
        result = subprocess.run(["dm", "--help"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Console script 'dm' works")
        else:
            print(f"⚠️  Console script might not be in PATH: {result.stderr}")

        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False

def test_workflow():
    """Test basic workflow in a temporary directory."""
    print("🔍 Testing basic workflow...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        try:
            # Initialize git repo
            subprocess.run(["git", "init"], capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], capture_output=True)

            # Initialize dungeon master
            result = subprocess.run([sys.executable, "-m", "dungeon_master.cli", "init"],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Init failed: {result.stderr}")
                return False

            # Create a test file with tracking
            test_file = Path("test_module.py")
            test_file.write_text('''# @track_context("test_module.md")

def hello_world():
    """A simple hello world function."""
    return "Hello, World!"

class TestClass:
    """A test class."""

    def __init__(self):
        self.value = 42

    def get_value(self):
        return self.value
''')

            # Test update command
            result = subprocess.run([sys.executable, "-m", "dungeon_master.cli", "update", str(test_file)],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Update failed: {result.stderr}")
                return False

            # Check if template was created
            template_path = Path("lore/test_module.md")
            if template_path.exists():
                print("✅ Template creation works")
                print(f"📄 Created: {template_path}")
            else:
                print("❌ Template was not created")
                return False

            # Test validation
            result = subprocess.run([sys.executable, "-m", "dungeon_master.cli", "validate"],
                                  capture_output=True, text=True)
            # Should fail because template has placeholders
            if result.returncode != 0:
                print("✅ Validation correctly detects incomplete templates")
            else:
                print("⚠️  Validation might not be working correctly")

            return True

        except Exception as e:
            print(f"❌ Workflow test failed: {e}")
            return False

def main():
    """Run all installation tests."""
    print("🧪 Testing Dungeon Master Installation")
    print("=" * 50)

    tests = [
        ("Package Import", test_import),
        ("CLI Commands", test_cli),
        ("Basic Workflow", test_workflow),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 Installation test successful!")
        print("🚀 Dungeon Master is ready to use!")
        print("\n📝 Next steps:")
        print("   1. Go to your project directory")
        print("   2. Run 'dm init'")
        print("   3. Add @track_context('filename.md') to important files")
        print("   4. Install pre-commit: 'pre-commit install'")
        print("   5. Start committing and let Cursor help with documentation!")
        return 0
    else:
        print("❌ Some tests failed. Check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
