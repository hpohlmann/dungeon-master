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

- **Smart Directory Exclusion**: Comprehensive logic to exclude virtual environments (`venv`, `.venv`, `env`, etc.), build directories (`node_modules`, `__pycache__`, `dist`), and IDE directories (`.vscode`, `.idea`)
- **Virtual Environment Protection**: Prevents false positives from installed packages containing `@track_context` decorators
- **Efficient File Walking**: Uses in-place directory filtering to avoid walking into excluded directories for better performance
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

## Key Internal Functions

**Directory Exclusion Logic**:

- **`_should_exclude_directory(dir_name)`**: Determines if a directory should be excluded from file walking. Checks against comprehensive lists of virtual environments, build directories, IDE directories, and hidden directories.
- **`_get_all_project_files()`**: Centralized file discovery function that walks the project directory while excluding problematic directories. Uses in-place directory filtering for efficiency and returns normalized file paths.

**Core Command Functions**:

- **`cmd_update()`**: Handles template creation and validation workflow
- **`cmd_list()`**: Displays tracked files with status information
- **`cmd_validate()`**: Comprehensive validation and commit-blocking logic
- **`cmd_review()`**: Manages significant change approval workflow
- **`cmd_init()`**: Repository initialization with proper setup

---

## Changelog

### [2025-06-03]

- **MAJOR BUG FIX**: Fixed critical issue where virtual environment files were being flagged as tracked files
- **Added comprehensive directory exclusion**: New `_should_exclude_directory()` function excludes virtual environments (`venv`, `.venv`, `env`, `virtualenv`, `pyenv`, `conda`, etc.), build directories, and IDE directories
- **Added centralized file discovery**: New `_get_all_project_files()` function provides consistent, efficient file walking with proper exclusions
- **Updated all affected commands**: `cmd_list`, `cmd_validate`, and `cmd_review` now use centralized exclusion logic
- **Performance improvement**: Uses in-place directory filtering to avoid walking into excluded directories
- **Enhanced user experience**: Users no longer see false positives from installed packages in their virtual environments

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
