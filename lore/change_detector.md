# change_detector.py - Context Documentation

## Purpose

This module implements sophisticated change detection for tracked files, introduced in version 0.2.0 to ensure documentation stays current with code evolution. It analyzes file signatures including functions, classes, imports, and content hashes to detect significant structural changes that warrant documentation updates. The change detector prevents documentation from becoming stale by requiring human review when substantial modifications occur to tracked files.

## Usage Summary

**File Location**: `dungeon_master/change_detector.py`

**Primary Use Cases**:

- Track structural signatures of Python and JavaScript/TypeScript files over time
- Detect significant changes like new/removed functions, classes, or major content modifications
- Cache file signatures to enable comparison across commits
- Provide detailed change analysis for user review and approval
- Integrate with the commit workflow to block commits when significant changes need review

**Key Dependencies**:

- `ast`: Abstract Syntax Tree parsing for Python structural analysis
- `re`: Regular expression matching for JavaScript/TypeScript parsing and general pattern detection
- `hashlib`: MD5 content hashing for change detection
- `json`: Serialization of file signatures for caching
- `subprocess`: Git integration for commit history analysis
- `pathlib.Path`: File system operations and path handling
- `utils`: File reading operations and error handling

## Key Functions or Classes

**Classes**:

- **FileSignature**: Represents the structural signature of a file including functions, classes, imports, and content hash. Provides serialization/deserialization for caching.
- **ChangeAnalysis**: Analyzes differences between old and new file signatures, determining significance and describing specific changes.
- **ChangeDetector**: Main class that manages signature caching, change analysis, and reviewer approval workflow.

**Key Methods**:

- **ChangeDetector.analyze_changes(file_paths)**: Compares current file signatures against cached versions to identify modifications.
- **ChangeDetector.get_significant_changes(file_paths)**: Filters changes to only those requiring documentation review.
- **ChangeDetector.mark_as_reviewed(file_paths)**: Approves changes and updates cached signatures after review.
- **FileSignature.\_analyze_python_structure()**: Deep AST analysis of Python files for comprehensive structural tracking.
- **ChangeAnalysis.\_analyze_significance()**: Determines if changes are significant based on structural modifications and thresholds.

## Usage Notes

- Significant changes include: new/removed functions or classes, import changes, >20% line count changes
- Content-only changes (like comments or minor edits) typically don't trigger significance thresholds
- The cache file (`lore_cache.json`) tracks signatures across commits and should be gitignored
- Python files get deep AST analysis while JavaScript/TypeScript uses regex-based parsing
- Change significance is tuned to balance documentation quality with developer workflow disruption
- The system gracefully handles files that can't be parsed (syntax errors, binary files)
- Cache corruption is handled gracefully with automatic regeneration

## Dependencies & Integration

This module is central to the version 0.2.0 significant change detection feature:

- **Used by**: updater module for change analysis, CLI review command, pre-commit hook for blocking
- **Uses**: utils for file operations, ast for Python parsing, json for cache management
- **Integration flow**:
  1. Called during validation to check for significant changes
  2. Compares current file signatures against cached versions
  3. Determines if changes require documentation review
  4. Blocks commits until changes are reviewed and approved
  5. Updates cache when changes are marked as reviewed

The change detector ensures that documentation evolves with the codebase rather than becoming outdated over time.

## Changelog

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- Updated `change_detector.py` - please review and update context as needed

### [2025-06-02]

- **Implemented stricter change detection**: Now flags ALL content changes as potentially significant, requiring developer review
- Changed from lenient "assume not significant" to strict "assume potentially significant" approach
- Improves quality by ensuring no changes slip through with generic changelog entries
- Developers retain easy escape hatch via `dm review --mark-reviewed` for minor changes

### [2025-06-02]

- Context documentation created for change detector module
- Documented file signature analysis and caching mechanisms
- Added notes about significance thresholds and review workflow integration

---

_This document is maintained by Cursor. Last updated: 2025-06-02_
