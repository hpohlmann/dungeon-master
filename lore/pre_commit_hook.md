# pre_commit_hook.py - Context Documentation

## Purpose

This script serves as the enforcement mechanism for Dungeon Master's context documentation requirements, integrating directly with git's pre-commit workflow. The hook has been simplified to act as a lightweight orchestrator that runs the three core Dungeon Master CLI commands in sequence: `dm update`, `dm review`, and `dm validate`. This ensures consistent behavior between manual command usage and automated pre-commit enforcement.

## Usage Summary

**File Location**: `hooks/pre_commit_hook.py`

**Primary Use Cases**:

- Execute the complete Dungeon Master workflow automatically on every commit
- Enforce documentation requirements without duplicating CLI logic
- Provide clear, step-by-step feedback during the commit process
- Block commits when documentation issues are detected
- Maintain consistency between manual and automated workflows

**Key Dependencies**:

- `sys`: Exit code management for commit blocking
- `subprocess`: Execute CLI commands and capture output
- `logging`: Error reporting and debugging information
- `pathlib.Path`: Basic path operations (minimal usage)

## Key Functions or Classes

**Key Functions**:

- **main()**: Main entry point that orchestrates the three-step workflow
- **run_dm_command(command_args)**: Executes a Dungeon Master CLI command and captures the result with timeout protection
- **print_command_output(command, stdout, stderr)**: Displays command output for user visibility

**Workflow Steps**:

1. **`dm update`**: Creates templates for new tracked files and updates documentation changelogs
2. **`dm review`**: Checks for significant changes requiring human review and approval
3. **`dm validate`**: Validates that all context documents are complete and ready for commit

## Usage Notes

- The hook runs automatically on every git commit when pre-commit is configured
- Each step must pass before proceeding to the next step
- If any step fails, the commit is blocked with clear guidance on how to fix the issues
- The hook provides the same output as running the CLI commands manually
- Commands have a 30-second timeout to prevent hanging during git operations
- Exit code 0 allows commits to proceed, non-zero codes block commits
- The simplified approach eliminates code duplication and ensures consistent behavior

## Dependencies & Integration

This script serves as a thin integration layer between git and the Dungeon Master CLI:

- **Triggered by**: Git pre-commit hooks configured via `.pre-commit-config.yaml`
- **Executes**: The three core CLI commands: dm update, dm review, dm validate
- **Integration flow**:
  1. Git triggers the hook before allowing commits
  2. Hook runs `dm update` to handle template creation and changelog updates
  3. Hook runs `dm review` to check for significant changes needing approval
  4. Hook runs `dm validate` to ensure all documentation is complete
  5. If all commands succeed, commit proceeds; otherwise commit is blocked

The simplified approach ensures that pre-commit behavior matches manual CLI usage exactly, making debugging easier and reducing maintenance overhead.

## Changelog

### [2025-06-02]

- **MAJOR REFACTOR**: Simplified pre-commit hook to use CLI commands instead of duplicating logic
- Removed 150+ lines of complex orchestration code
- Now calls `dm update`, `dm review`, and `dm validate` in sequence
- Added `run_dm_command()` and `print_command_output()` utility functions
- Removed all direct imports of internal Dungeon Master modules
- Improved error handling with subprocess timeout protection
- Ensures consistent behavior between manual and automated workflows

### [2025-06-02]

- **Added developer guidance for minor changes**: Enhanced messaging to help developers understand when changes can be safely marked as reviewed without updating documentation
- Improved user experience during commit blocking by providing clear next steps for both significant and minor changes

### [2025-06-02]

- Context documentation created for pre-commit hook
- Documented integration with git workflow and commit blocking logic
- Added notes about user guidance and error handling patterns

---

_This document is maintained by Cursor. Last updated: 2025-06-02_
