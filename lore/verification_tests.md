# tests/verify_installation.py - Context Documentation

## Purpose

This file provides comprehensive verification tests for Dungeon Master installation, testing all core functionality to ensure the system is properly installed and ready for Cursor integration. It serves as both a validation tool and documentation of expected system behavior.

## Key Functionality

**Core Test Coverage**:

- **Import validation**: Ensures all modules can be imported successfully
- **Parser functionality**: Tests decorator extraction and validation logic
- **Template generation**: Creates test files and validates template creation with proper placeholder detection
- **Document validation**: Tests validation of both incomplete templates and completed documentation
- **CLI functionality**: Ensures command-line interface is accessible
- **Directory creation**: Validates output directory setup

**Template Testing Approach**:

- Creates temporary test files with `@track_context` decorators
- Generates templates and validates they contain proper structure
- Tests placeholder detection using angle bracket format: `<placeholder>`
- Validates completed documents pass validation while templates with unfilled placeholders fail
- Handles cleanup of temporary test files

**Validation Logic**:

- Tests both positive cases (valid documents) and negative cases (incomplete templates)
- Ensures placeholder detection works correctly with angle bracket format
- Validates error reporting for incomplete documentation
- Confirms successful validation for completed documents

## Usage Summary

**File Location**: `tests/verify_installation.py`

**Key Dependencies**:

- Core dungeon_master modules (parser, generator, updater, utils)
- Standard library modules (sys, os, pathlib)

**CLI Usage**:

```bash
python tests/verify_installation.py
```

**Integration**:

- Standalone verification script that can be run independently
- Tests all core functionality without requiring git or external dependencies
- Provides clear pass/fail feedback for each test component
- Used to validate installation before enabling pre-commit hooks

---

_This document is maintained by Cursor. Last updated: 2025-01-01_
