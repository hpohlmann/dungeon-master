# test_parser.py - Context Documentation

## Purpose

This module provides comprehensive unit testing for the parser module's decorator detection and file analysis functionality. It ensures that the core logic for identifying `@track_context` decorators works correctly across various edge cases, quote styles, and error conditions. The tests serve as both quality assurance and documentation of expected parser behavior, helping maintain reliability of the fundamental file tracking mechanism.

## Usage Summary

**File Location**: `tests/test_parser.py`

**Primary Use Cases**:

- Validate `@track_context` decorator extraction across different syntax variations
- Test context document name validation rules and edge cases
- Ensure robust handling of malformed or missing decorators
- Verify file summary generation functionality
- Provide regression protection for parser functionality changes

**Key Dependencies**:

- `pytest`: Modern testing framework with fixtures and parameterized tests
- `dungeon_master.parser`: All parser functions being tested
- Standard library: No external dependencies beyond pytest for clean testing

## Key Functions or Classes

**Test Classes**:

- **TestExtractTrackContextDecorator**: Comprehensive testing of decorator extraction logic including quote styles, spacing, and error conditions
- **TestValidateContextDocumentName**: Validation rule testing for context document names
- **TestParseTrackedFiles**: Integration testing of file parsing workflow with temporary files
- **TestGetFileSummary**: File summary generation testing for various file types and edge cases

**Key Test Scenarios**:

- Single and double quote decorator syntax variations
- Whitespace and formatting tolerance in decorator detection
- Missing .md extension handling and automatic appending
- Binary file filtering and error handling
- Empty and malformed file content processing

## Usage Notes

- Tests use pytest fixtures to create temporary files for integration testing
- All file operations are performed in isolated temporary directories
- Tests cover both positive cases (valid decorators) and negative cases (missing/invalid decorators)
- Binary file handling is tested to ensure the parser doesn't crash on non-text files
- Edge cases include empty files, files with encoding issues, and malformed syntax
- The test suite serves as living documentation of parser behavior expectations

## Dependencies & Integration

This test module ensures the reliability of the parser module which is foundational to Dungeon Master:

- **Tests**: `dungeon_master.parser` module exclusively
- **Uses**: pytest for test framework, temporary file creation for isolation
- **Quality assurance flow**:
  1. Unit tests validate individual function behavior
  2. Integration tests verify complete file processing workflows
  3. Edge case testing ensures robustness in production environments
  4. Regression testing protects against behavior changes during development

The parser tests are critical because parser failures would break the entire Dungeon Master workflow.

## Changelog

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `test_parser.py` - please review and update context as needed

### [2025-06-02]

- Context documentation created for parser tests
- Documented test coverage for decorator detection and validation
- Added notes about edge case testing and regression protection
---

_This document is maintained by Cursor. Last updated: 2025-06-02_
