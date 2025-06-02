# cli.py - Context Documentation

## Purpose

This module provides the command-line interface for Dungeon Master, serving as the primary entry point for user interactions. It implements a comprehensive CLI with subcommands for initializing repositories, managing context documentation, validating templates, and reviewing significant changes. The module acts as the orchestrator that ties together all other Dungeon Master components to provide a cohesive user experience.

## Usage Summary

**File Location**: `dungeon_master/cli.py`

**Primary Use Cases**:

- Initialize Dungeon Master in new repositories (`dm init`)
- Generate and update context doc templates (`dm update`)
- Show tracked files and their doc status via `dm list`
- Validate context docs for completeness via `dm validate`
- Manage and approve significant file changes via `dm review`

**Key Dependencies**:

- `argparse`: Provides robust command-line argument parsing and help generation
- `sys`: Used for exit codes and system-level operations
- `pathlib.Path`: Modern path handling for cross-platform file operations
- `typing.List`, `typing.Dict`: Type hints for better code maintainability
- Internal modules: Imports core functionality from parser, generator, updater, and utils

## Key Functions or Classes

**Key Functions**:

- **cmd_update(args)**: Creates templates or validates existing context docs for tracked files. Handles both specific files and staged files from git.
- **cmd_list(args)**: Shows tracked files and their context doc status. Supports `--all` flag to show all tracked files vs just staged ones.
- **cmd_validate(args)**: Validates context docs and shows what would block a commit. Checks for incomplete templates and significant changes.
- **cmd_init(args)**: Initializes Dungeon Master in the current repository. Creates output directory and sample pre-commit configuration.
- **cmd_review(args)**: Manages significant change detection. Allows checking changes and marking them as approved with --mark-reviewed.
- **main()**: Entry point that sets up argument parsing with subcommands and delegates to appropriate command handlers.

## Usage Notes

- The CLI follows standard Unix conventions with clear help messages and appropriate exit codes
- All commands that modify files provide clear feedback about what was created or updated
- Error handling is comprehensive with user-friendly messages for common failure scenarios
- The `validate` command serves as a dry-run to show what the pre-commit hook would do
- Commands automatically detect git repository context and work with staged files when appropriate
- The CLI is designed to be both interactive (for developers) and scriptable (for automation)

## Dependencies & Integration

This module serves as the main interface layer that orchestrates all other Dungeon Master components:

- **Imports from**: All core modules (parser, generator, updater, utils, change_detector)
- **Used by**: Console scripts defined in setup.py (`dm` and `dungeon-master` commands)
- **Integration points**:
  - Git integration through utils.get_git_changes()
  - File system operations through ensure_output_directory()
  - Template generation through generate_context_template()
  - Validation through validate_context_document()
  - Change detection through ChangeDetector class

The CLI is the primary way users interact with Dungeon Master, making it a critical component for user experience and adoption.

## Changelog

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- Updated `cli.py` - please review and update context as needed

### [2025-06-02]

- **Enhanced review command messaging**: Added comprehensive guidance for developers on when changes require documentation updates vs. when they can be safely marked as reviewed
- Added detailed criteria for REVIEW REQUIRED vs. SAFE TO MARK REVIEWED scenarios
- Improved user experience by clarifying when `dm review --mark-reviewed` is appropriate

### [2025-06-02]

- Context documentation created for CLI module
- Added comprehensive documentation for all command functions
- Documented integration points with other modules

---

_This document is maintained by Cursor. Last updated: 2025-06-02_
