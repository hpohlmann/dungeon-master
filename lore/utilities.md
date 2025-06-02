# utils.py - Context Documentation

## Purpose

This module provides essential utility functions that serve as the foundation for all Dungeon Master operations. It handles core concerns like directory management, file I/O operations, git integration, and cross-platform compatibility. These utilities abstract away low-level details and provide a consistent interface for file system and git operations used throughout the application.

## Usage Summary

**File Location**: `dungeon_master/utils.py`

**Primary Use Cases**:

- Create and manage the `lore/` output directory for context documents
- Read and write files safely with proper error handling
- Interface with git to get staged and new files
- Determine file types and extensions for processing logic
- Generate consistent timestamps for changelog entries

**Key Dependencies**:

- `os`: Low-level operating system interface for file operations
- `subprocess`: Execute git commands and capture output
- `pathlib.Path`: Modern, object-oriented path handling
- `typing`: Type hints for List, Tuple, Optional
- `logging`: Centralized logging for error reporting and debugging

## Key Functions or Classes

**Key Functions**:

- **ensure_output_directory()**: Creates and returns the `lore/` directory path. Central function that establishes where context documents are stored.
- **get_git_changes()**: Retrieves staged and new files from git using subprocess calls. Critical for determining which files need processing.
- **read_file_content(file_path)**: Safely reads file content with comprehensive error handling for encoding issues and missing files.
- **write_file_content(file_path, content)**: Safely writes content to files, creating parent directories as needed.
- **is_text_file(file_path)**: Determines if a file should be processed based on its extension, filtering out binary files.
- **format_timestamp()**: Generates consistent YYYY-MM-DD timestamps for changelog entries and document updates.

## Usage Notes

- All file operations include comprehensive error handling and logging for troubleshooting
- The `ensure_output_directory()` function is idempotent - safe to call multiple times
- Git operations gracefully handle repositories that aren't initialized or don't have staged files
- File reading operations handle various encoding issues and binary files gracefully
- Path operations use `pathlib.Path` for cross-platform compatibility (Windows, macOS, Linux)
- The module follows the principle of "fail gracefully" - operations return None/empty lists rather than crashing

## Dependencies & Integration

This module is the foundational layer used by all other Dungeon Master components:

- **Used by**: CLI, pre-commit hook, parser, generator, updater, change detector
- **Imports from**: Only standard library modules (no internal dependencies)
- **Key integration points**:
  - Output directory management for all context document operations
  - Git integration for determining which files to process
  - File I/O abstraction used by template generation and validation
  - Timestamp generation for changelog maintenance

The utilities module is designed to be the stable foundation that other modules can rely on without circular dependencies.

## Changelog

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]
- Updated `utils.py` - please review and update context as needed

### [2025-06-02]

- Context documentation created for utilities module
- Documented all utility functions and their error handling patterns
- Added notes about cross-platform compatibility considerations
---

_This document is maintained by Cursor. Last updated: 2025-06-02_
