#!/usr/bin/env python3
# @track_context("verification_tests.md")
"""
Verification script for Dungeon Master installation.
Tests core functionality without requiring external dependencies.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from dungeon_master import (
            parse_tracked_files,
            generate_context_template,
            validate_context_document,
            ensure_output_directory,
            get_git_changes
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_parser():
    """Test the parser functionality."""
    print("Testing parser...")
    try:
        from dungeon_master.parser import extract_track_context_decorator, validate_context_document_name

        # Test decorator extraction
        content = "# @track_context('test.md')\nclass MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result == "test.md", f"Expected 'test.md', got '{result}'"

        # Test validation
        assert validate_context_document_name("test.md") == True
        assert validate_context_document_name("invalid") == False

        print("✓ Parser tests passed")
        return True
    except Exception as e:
        print(f"✗ Parser test failed: {e}")
        return False

def test_template_generator():
    """Test the template generator functionality."""
    print("Testing template generator...")
    try:
        from dungeon_master.generator import generate_context_template, has_unfilled_placeholders

        # Create a test file
        test_file = "test_file.py"
        test_content = """# @track_context('test.md')
import os
import sys

class TestClass:
    def method1(self, arg1, arg2):
        pass

    def method2(self):
        return True

def function1():
    pass
"""
        with open(test_file, 'w') as f:
            f.write(test_content)

        # Test template generation
        template = generate_context_template(test_file)
        assert template, "Template should not be empty"
        assert "Instructions for Cursor" in template, "Template should contain Cursor instructions"
        assert "<Describe the overall intent" in template, "Template should contain placeholders"

        # Test placeholder detection
        assert has_unfilled_placeholders(template) == True, "Should detect unfilled placeholders"

        # Clean up
        os.remove(test_file)

        print("✓ Template generator tests passed")
        return True
    except Exception as e:
        print(f"✗ Template generator test failed: {e}")
        # Clean up on failure
        if os.path.exists("test_file.py"):
            os.remove("test_file.py")
        return False

def test_validation():
    """Test the validation functionality."""
    print("Testing validation...")
    try:
        from dungeon_master.updater import validate_context_document
        from dungeon_master.utils import write_file_content

        # Create a test template with placeholders
        template_content = """# test.py - Context Documentation

> **Instructions for Cursor**: This is a context template.

## Purpose

<Describe the overall intent and responsibility of this file>

## Usage Summary

**File Location**: `test.py`

**Key Dependencies**:
<List any important dependencies>

---
*This document is maintained by Cursor. Last updated: 2025-06-02*
"""

        test_doc = "test_context.md"
        write_file_content(test_doc, template_content)

        # Test validation - should fail with unfilled template
        is_valid, issues = validate_context_document(test_doc)
        assert is_valid == False, "Template with placeholders should not be valid"
        assert len(issues) > 0, "Should report issues"

        # Create a completed document
        completed_content = """# test.py - Context Documentation

## Purpose

This file provides test functionality for the application.

## Usage Summary

**File Location**: `test.py`

**Key Dependencies**:
- No external dependencies

---
*This document is maintained by Cursor. Last updated: 2025-06-02*
"""

        write_file_content(test_doc, completed_content)

        # Test validation - should pass
        is_valid, issues = validate_context_document(test_doc)
        assert is_valid == True, "Completed document should be valid"
        assert len(issues) == 0, "Should have no issues"

        # Clean up
        os.remove(test_doc)

        print("✓ Validation tests passed")
        return True
    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        # Clean up on failure
        if os.path.exists("test_context.md"):
            os.remove("test_context.md")
        return False

def test_cli_functionality():
    """Test CLI functionality."""
    print("Testing CLI...")
    try:
        from dungeon_master.cli import main

        # Test that CLI can be imported and main function exists
        assert callable(main)

        print("✓ CLI tests passed")
        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False

def test_directory_creation():
    """Test directory creation."""
    print("Testing directory creation...")
    try:
        from dungeon_master.utils import ensure_output_directory

        output_dir = ensure_output_directory()
        assert output_dir.exists()
        assert output_dir.name == "lore"

        print("✓ Directory creation tests passed")
        return True
    except Exception as e:
        print(f"✗ Directory creation test failed: {e}")
        return False

def main():
    """Run all verification tests."""
    print("=" * 50)
    print("Dungeon Master Installation Verification")
    print("=" * 50)

    tests = [
        test_imports,
        test_parser,
        test_template_generator,
        test_validation,
        test_cli_functionality,
        test_directory_creation
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All verification tests passed!")
        print("Dungeon Master is ready for Cursor integration!")
        print("\n📝 This system creates templates for Cursor to fill,")
        print("   ensuring structured documentation maintenance.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
