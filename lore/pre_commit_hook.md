# pre_commit_hook.py - Context Documentation

## Purpose

This script serves as the enforcement mechanism for Dungeon Master's context documentation requirements, integrating directly with git's pre-commit workflow. It acts as a quality gate that blocks commits when tracked files lack proper context documentation or when significant changes haven't been reviewed. The hook orchestrates all Dungeon Master components to create templates, validate documents, and ensure documentation stays current with code changes.

## Usage Summary

**File Location**: `hooks/pre_commit_hook.py`

**Primary Use Cases**:

- Block commits when tracked files have incomplete context documentation
- Generate new context document templates for newly tracked files
- Validate existing context documents for completeness and quality
- Detect and enforce review of significant file changes
- Provide clear user guidance on how to resolve documentation issues

**Key Dependencies**:

- `sys`: Exit code management for commit blocking and path manipulation
- `logging`: Comprehensive logging for debugging hook execution
- `pathlib.Path`: File system operations and path handling
- `typing`: Type hints for List, Tuple, Dict
- All Dungeon Master modules: parser, generator, updater, utils, change_detector

## Key Functions or Classes

**Key Functions**:

- **main()**: Main entry point that orchestrates the entire pre-commit validation workflow
- **process_new_tracked_files(tracked_files, output_dir)**: Creates context document templates for files that don't have them yet
- **update_existing_documents(tracked_files, output_dir)**: Adds changelog entries to existing valid context documents
- **print_commit_blocked_message()**: Provides comprehensive user guidance when commits are blocked
- **print_success_message()**: Confirms successful validation and documents what was updated

## Usage Notes

- The hook runs automatically on every git commit for repositories with Dungeon Master configured
- Exit code 0 allows commits to proceed, non-zero exit codes block commits
- The hook provides detailed feedback about what needs to be fixed before commits can proceed
- All file processing is done on staged files to avoid interfering with working directory changes
- The hook gracefully handles repositories without git or with no staged files
- Error handling is comprehensive to prevent the hook from breaking git workflows
- The hook integrates with the change detection system to enforce documentation review requirements

## Dependencies & Integration

This script is the primary integration point between Dungeon Master and git workflows:

- **Triggered by**: Git pre-commit hooks when commits are attempted
- **Uses**: All core Dungeon Master modules for complete workflow orchestration
- **Integration flow**:
  1. Git triggers the hook before allowing commits
  2. Hook identifies staged tracked files using the parser
  3. Creates templates for new tracked files using the generator
  4. Validates existing documents using the updater
  5. Checks for significant changes using the change detector
  6. Blocks commits if any issues are found, or allows them to proceed
  7. Updates changelogs and cache files when commits are successful

The pre-commit hook ensures that documentation requirements are enforced consistently across all team members and that documentation quality is maintained as part of the development workflow.

## Changelog

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]
- Updated `pre_commit_hook.py` - please review and update context as needed

### [2025-06-02]

- Context documentation created for pre-commit hook
- Documented integration with git workflow and commit blocking logic
- Added notes about user guidance and error handling patterns
---

_This document is maintained by Cursor. Last updated: 2025-06-02_
