# parser.py - Context Documentation

## Purpose

This module handles the detection and extraction of `@track_context` decorators from source files. It serves as the entry point for identifying which files should have context documentation generated and maintained. The parser uses regex-based pattern matching to find tracking decorators and validates the specified context document names, making it the foundational component that determines what files are managed by Dungeon Master.

## Usage Summary

**File Location**: `dungeon_master/parser.py`

**Primary Use Cases**:

- Scan source files to find `@track_context("filename.md")` decorators
- Extract context document names from tracking decorators
- Validate that context document names follow proper conventions
- Generate file summaries for template generation context
- Filter out binary files and focus on text-based source code

**Key Dependencies**:

- `re`: Regular expression matching for decorator pattern detection
- `typing`: Type hints for Dict, List, Optional
- `logging`: Error reporting and debugging information
- `utils`: File reading operations and text file detection

## Key Functions or Classes

**Key Functions**:

- **extract_track_context_decorator(file_content)**: Core function that uses regex to find `@track_context` decorators in the first 10 lines of files. Handles various quote styles and spacing.
- **parse_tracked_files(file_paths)**: Main entry point that processes multiple file paths and returns a mapping of tracked files to their context doc names.
- **validate_context_document_name(context_doc)**: Ensures context doc names are valid (end with .md, no path separators, not empty).
- **get_file_summary(file_path)**: Generates basic file statistics (line count, size) used for template generation context.

## Usage Notes

- The decorator must appear within the first 10 lines of a file to be detected
- Supports both single and double quotes in decorator syntax: `@track_context('file.md')` or `@track_context("file.md")`
- Automatically appends `.md` extension if not provided in the decorator
- Binary files are automatically skipped to avoid processing errors
- The regex pattern is case-insensitive for flexibility
- Handles whitespace variations in decorator syntax gracefully
- Files that can't be read (permissions, encoding issues) are silently skipped with logging

## Dependencies & Integration

This module is used early in the Dungeon Master workflow to identify files for processing:

- **Used by**: CLI commands including update/validate/list operations, pre-commit hook
- **Uses**: utils module for file operations and text file detection
- **Integration flow**:
  1. Called with list of file paths (from git or user input)
  2. Filters to text files only
  3. Reads file content and searches for decorators
  4. Returns mapping used by other modules for template generation and validation

The parser serves as the gatekeeper that determines which files enter the Dungeon Master workflow.

## Changelog

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]
- Updated `parser.py` - please review and update context as needed

### [2025-06-02]

- Context documentation created for file parser module
- Documented decorator detection logic and validation rules
- Added notes about binary file filtering and error handling
---

_This document is maintained by Cursor. Last updated: 2025-06-02_
