# generator.py - Context Documentation

## Purpose

This module is responsible for creating structured context document templates with intelligent placeholders for Cursor to fill. It analyzes source code structure using AST parsing for Python and regex patterns for JavaScript/TypeScript, then generates comprehensive Markdown templates with sections for purpose, usage, functions, and integration details. The generator creates the scaffolding that ensures consistent, thorough documentation across all tracked files.

## Usage Summary

**File Location**: `dungeon_master/generator.py`

**Primary Use Cases**:

- Generate context document templates from source code analysis
- Analyze Python files using AST parsing to extract functions, classes, and imports
- Analyze JavaScript/TypeScript files using regex patterns for basic structure detection
- Create structured Markdown templates with Cursor-specific placeholders
- Detect unfilled placeholders in existing context documents for validation

**Key Dependencies**:

- `ast`: Abstract Syntax Tree parsing for Python source code analysis
- `re`: Regular expression matching for JavaScript/TypeScript parsing and placeholder detection
- `pathlib.Path`: File path operations and extension detection
- `typing`: Type hints for Dict, List, Optional, Set
- `logging`: Error reporting for parsing failures
- `utils`: File reading, timestamp formatting, and file extension detection

## Key Functions or Classes

**Key Functions**:

- **generate_context_template(file_path)**: Main entry point that creates a complete context document template by analyzing file structure and generating appropriate sections.
- **analyze_file_structure(file_path, file_content)**: Dispatches to language-specific analysis functions based on file extension to extract structural information.
- **\_analyze_python_structure(file_content)**: Uses AST parsing to extract functions, classes, and imports from Python files with full signature analysis.
- **\_analyze_javascript_structure(file_content)**: Uses regex patterns to extract basic structural elements from JavaScript/TypeScript files.
- **has_unfilled_placeholders(content)**: Detects whether a context document still contains template placeholders that need completion.
- **get_unfilled_sections(content)**: Returns specific sections that still need to be filled, used for detailed validation feedback.

## Usage Notes

- Python files get sophisticated AST-based analysis with function signatures and complete import tracking
- JavaScript/TypeScript files use simpler regex-based analysis due to parsing complexity
- Templates include specific instructions for Cursor about how to complete the documentation
- All generated templates follow a consistent structure with Purpose, Usage, Functions, Notes, Dependencies, and Changelog sections
- The placeholder detection is robust and handles various formatting styles
- File analysis gracefully handles syntax errors in source code
- Templates are designed to be self-documenting with clear instructions for completion

## Dependencies & Integration

This module is central to the template creation workflow:

- **Used by**: CLI update command, pre-commit hook for new tracked files
- **Uses**: utils for file operations, ast for Python parsing, re for pattern matching
- **Integration flow**:
  1. Called when a tracked file needs a new context document
  2. Analyzes source code structure based on file type
  3. Generates structured Markdown template with placeholders
  4. Returns template content for writing to lore/ directory

The generator creates the foundation that other modules validate and update, making it crucial for maintaining documentation quality and consistency.

## Changelog

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]
- Updated `generator.py` - please review and update context as needed

### [2025-06-02]

- Context documentation created for template generator module
- Documented AST parsing logic for Python and regex patterns for JavaScript
- Added notes about placeholder detection and validation integration
---

_This document is maintained by Cursor. Last updated: 2025-06-02_
