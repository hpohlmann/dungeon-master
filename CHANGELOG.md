# 📜 Changelog

All notable changes to the Dungeon Master project will be documented in this scroll.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] 🔮

### ⚔️ Planned

- 🔮 Enhanced AI Integration - Multiple AI provider support
- 🗺️ Advanced Analytics - Documentation coverage metrics
- ⚡ IDE Plugins - VSCode and IntelliJ integration
- 🏹 Custom Templates - Configurable documentation structures
- 💎 Quality Metrics - Documentation completeness scoring

---

## [0.3.1] - 2025-01-01 ⚔️

### 🔧 **Critical Bug Fix**

#### 🛡️ **Virtual Environment Protection**

- **MAJOR BUG FIX**: Fixed critical issue where virtual environment files were incorrectly flagged as tracked files
- **Smart Directory Exclusion**: Added comprehensive logic to exclude virtual environments (`venv`, `.venv`, `env`, `virtualenv`, `pyenv`, `conda`, etc.)
- **Build Directory Filtering**: Enhanced exclusion of build directories (`node_modules`, `__pycache__`, `dist`, `build`, etc.)
- **IDE Directory Exclusion**: Added filtering for IDE directories (`.vscode`, `.idea`, `.eclipse`, etc.)

#### ⚡ **Performance & User Experience**

- **Efficient File Walking**: Uses in-place directory filtering to avoid walking into excluded directories
- **Centralized Discovery**: New `_get_all_project_files()` function provides consistent file discovery across all commands
- **Enhanced User Experience**: Users no longer see false positives from installed packages in their virtual environments
- **Cross-Platform Compatibility**: Handles both Unix (`./`) and Windows (`.\`) path separators

### 🏹 **Technical Implementation**

- Added `_should_exclude_directory()` function with comprehensive exclusion rules
- Updated `cmd_list`, `cmd_validate`, and `cmd_review` to use centralized file discovery
- Improved path normalization and handling across different operating systems

### 🎯 **Impact**

This release resolves a major user experience issue where Dungeon Master would incorrectly identify files from installed packages (including its own source code in virtual environments) as files that needed documentation. Users can now safely use `dm list --all`, `dm validate`, and other commands without seeing false positives from their virtual environments.

---

## [0.3.0] - 2025-01-01 🏰

### 📜 **Documentation & UX Revolution**

#### 🎨 **Major Documentation Overhaul**

- **Restructured README**: Simplified structure with clearer examples and step-by-step guides
- **Enhanced Template Examples**: Before/after documentation examples showing Cursor's role
- **Improved Quick Start**: Streamlined 3-command setup process
- **Better Visual Hierarchy**: Commands organized in clean table format with clear sections

#### 🏰 **Consistent D&D Theming**

- **Unified Emoji System**: Consistent D&D-themed emojis throughout all documentation
- **Thematic Messaging**: All CLI output and documentation uses D&D metaphors
- **Brand Consistency**: From 🏰 Dungeon Master to ⚔️ enforcement to 📜 documentation

#### 🎯 **Developer Experience Improvements**

- **Professional CHANGELOG**: Created comprehensive version history following industry standards
- **Clear Value Proposition**: Better communication of AI-assisted documentation workflow
- **Practical Examples**: Real authentication service examples throughout documentation
- **Visual Project Structure**: Clear file organization with thematic emojis

### ✨ **Quality & Organization**

- Separated version history into dedicated CHANGELOG.md
- Enhanced README readability and scanning
- Improved new user onboarding experience
- Professional documentation standards implementation

---

## [0.2.1] - 2025-01-01 🛡️

### 🔧 Fixed

- **Test Placeholder Format**: Updated `tests/verify_installation.py` to use angle bracket placeholders (`<>`) instead of parentheses
- **Import Consolidation**: Consolidated multiple inline `import os` statements in CLI for cleaner code organization
- **Documentation Validation**: Fixed false positive placeholder detection in instruction blocks

### 📜 Documentation

- Updated context documentation for verification tests and CLI modules
- Improved code organization and maintainability
- Enhanced test reliability with proper placeholder format

---

## [0.2.0] - 2025-06-02 🎲

### 🆕 Major Features

#### 🔮 **Significant Change Detection**

- **Smart Change Analysis**: Automatically detects when tracked files have substantial changes (new/removed functions, classes, major modifications)
- **Review Workflow**: New `dm review` command to manage significant changes with developer guidance
- **Intelligent Blocking**: Commits blocked when significant changes haven't been reviewed
- **File Signature Caching**: Advanced caching system (`lore_cache.json`) to track file changes over time

#### ⚔️ **Enhanced CLI Experience**

- **Stricter Validation**: All content changes now flagged as potentially significant
- **Developer Guidance**: Clear criteria for when to review vs. mark as reviewed
- **Escape Hatches**: Easy approval for minor changes (formatting, comments, small fixes)
- **Rich Messaging**: Comprehensive help text with practical examples

### 🛡️ Workflow Updates

- Pre-commit hook validates both template completion AND significant changes
- Developers must review substantial changes before commits proceed
- Context documentation updates enforced when code changes substantially
- Human-in-the-loop approval maintains documentation quality

### ✨ Benefits

- 📜 Documentation stays current with code evolution
- 🎯 Prevents outdated documentation from becoming stale
- 💎 Quality maintenance through development lifecycle
- ⚡ Streamlined workflow for different change types

---

## [0.1.0] - 2025-06-01 🏰

### 🚀 Initial Release

#### 🏰 **Core Features**

- **File Tracking**: Simple `@track_context("filename.md")` decorator system
- **Template Generation**: Intelligent templates with Cursor-specific placeholders and instructions
- **Commit Blocking**: Automatic enforcement until templates are completed
- **Validation Engine**: Comprehensive checks for placeholder completion and documentation quality

#### 🗡️ **CLI Tools**

- `dm init` - Repository initialization with proper setup
- `dm update` - Template creation and validation for tracked files
- `dm list` - Status overview of tracked files and documentation
- `dm validate` - Pre-commit validation preview

#### ⚔️ **Integration**

- **Pre-commit Hook**: Seamless integration with git workflow
- **Multi-language Support**: Python (full AST), JavaScript/TypeScript (regex), others (basic)
- **Template Structure**: Standardized documentation format with Purpose, Usage, Functions, Dependencies

#### 🎯 **Philosophy**

- Structured collaboration between AI (Cursor) and developers
- Enforcement of documentation quality without auto-generation
- Current, consistent, and meaningful documentation through commit-time validation

### 🏹 **Technical Foundation**

- Python 3.10+ compatibility
- SQLAlchemy-style file tracking and validation
- Robust error handling and user-friendly messaging
- Cross-platform file operations with pathlib

---

## 📖 **Version Legend**

- 🏰 **Major Release** - Significant new features and capabilities
- 🛡️ **Minor Release** - Enhancements, improvements, and fixes
- ⚔️ **Patch Release** - Bug fixes and small improvements
- 🔮 **Unreleased** - Features in development

---

## 🎯 **Contributing to History**

When contributing changes:

1. 📜 **Update this changelog** with your changes
2. ⚔️ **Follow the D&D emoji theming** for consistency
3. 🛡️ **Use appropriate version bumping** (major.minor.patch)
4. 🏰 **Document breaking changes** clearly
5. 💎 **Include migration guides** for major updates

---

🏰 _"Every commit tells a story, and every story deserves proper documentation."_
