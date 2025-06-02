# dungeon_master/cli.py - Context Documentation

## Purpose

This file implements the primary command-line interface for Dungeon Master, providing intuitive commands for developers to manage context documentation throughout their development workflow. It serves as the main user interaction point with the system, offering commands for initialization, file processing, validation, and change management.

## Key Functionality

**Core Command Structure**:

- **dm init**: Initialize Dungeon Master in a repository with proper directory setup
- **dm update**: Process tracked files, create templates, or validate existing documentation
- **dm list**: Display tracked files and their documentation status with filtering options
- **dm validate**: Check documentation completeness and identify commit-blocking issues
- **dm review**: Manage significant changes with developer-friendly guidance

**Change Detection Integration**:

- Seamlessly integrates with `ChangeDetector` for identifying significant modifications
- Provides clear guidance on when documentation updates are required vs. safe to mark as reviewed
- Implements developer-friendly escape hatches for minor changes (formatting, comments, small fixes)
- Uses stricter change detection that flags all content changes as potentially significant

**File Discovery & Processing**:

- Efficient file walking with proper exclusion of hidden and build directories
- Consolidated import handling for clean code organization
- Supports both staged-file processing and repository-wide analysis
- Handles multiple file processing with clear per-file status reporting

**User Experience Features**:

- Rich command-line help with practical examples
- Color-coded status indicators (✓, ⚠️, ✗) for quick visual scanning
- Detailed guidance messages that help developers make informed decisions
- Progress indicators and clear error reporting

## Usage Summary

**File Location**: `dungeon_master/cli.py`

**Key Dependencies**:

- `argparse`: Command-line argument parsing and help generation
- `os`: File system operations (consolidated import for clean code)
- `pathlib.Path`: Modern path handling and directory operations
- Core dungeon_master modules: parser, generator, updater, utils, change_detector

**CLI Examples**:

```bash
dm init                    # Initialize in current repo
dm update                  # Process all staged tracked files
dm update file1.py file2.py  # Process specific files
dm list                    # List staged tracked files
dm list --all              # List all tracked files
dm validate                # Check what would block commits
dm review                  # Check for significant changes
dm review --mark-reviewed  # Mark changes as reviewed
```

**Command Integration**:

- Used by pre-commit hooks for automated validation
- Supports both interactive and non-interactive workflows
- Provides detailed exit codes for CI/CD integration
- Maintains clear separation between user commands and internal logic

---

## Changelog

### [2025-01-01]

- Consolidated multiple inline `import os` statements into single top-level import for better code organization
- Removed redundant import statements from `cmd_list`, `cmd_validate`, and `cmd_review` functions

### [2025-06-02]

- Implemented stricter change detection that flags ALL content changes as potentially significant
- Added comprehensive developer guidance with clear criteria for when to review vs. mark as reviewed
- Enhanced user experience with detailed messaging about change types and appropriate actions
- Added escape hatch guidance for minor changes (formatting, comments, small fixes)

### [2025-06-02]

- Updated change detection integration to use new ChangeDetector class
- Improved file discovery logic with proper directory exclusions
- Enhanced command output formatting with better status indicators

### [2025-06-02]

- Initial CLI implementation with full command structure
- Implemented core commands: init, update, list, validate, review
- Added comprehensive help text and command examples
- Integrated with core Dungeon Master functionality

---

_This document is maintained by Cursor. Last updated: 2025-01-01_
