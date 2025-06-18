# Documentation for cursor

## Overview

The Cursor integration module manages the setup and maintenance of Cursor IDE rules for Dungeon Master. This module handles copying rule templates, verifying installations, and maintaining Cursor IDE configuration to ensure consistent development practices across the team.

## Dependencies

**Core Python Libraries:**

- `pathlib` - Modern file path handling
- `shutil` - File operations for copying templates

**External Libraries:**

- `rich.console` - Console output formatting

**Internal Dependencies:**

- Rule templates from `dungeon_master/templates/cursor_rules/` package directory

## Key Functions/Components

### Rule Management

- `setup_cursor_rules()` - Copies all rule templates to `.cursor/rules/`
- `verify_cursor_rules_setup()` - Checks if rules are properly installed
- `remove_cursor_rules()` - Removes installed Cursor rules

### Template Operations

- `get_templates_directory()` - Locates the templates directory within the package
- `copy_rule_file()` - Copies individual rule files with validation
- `create_cursor_rules_directory()` - Creates the .cursor/rules directory structure

## Usage Examples

```python
from dungeon_master.utils.cursor_setup import setup_cursor_rules

# Setup all Cursor rules
copied, failed = setup_cursor_rules()
print(f"Copied {len(copied)} rules, {len(failed)} failed")
```

## Diagrams

### Cursor Rules Setup Flow

```mermaid
sequenceDiagram
    participant DM as Dungeon Master
    participant Package as Package Templates
    participant Cursor as .cursor/rules/

    DM->>Package: Locate template files in package
    Package-->>DM: List of rule files

    loop For each rule file
        DM->>Cursor: Copy rule file
        Cursor-->>DM: Confirm copy
    end

    DM->>Cursor: Verify installation
    Cursor-->>DM: Installation status

    note over Package
        Templates located at:
        dungeon_master/templates/cursor_rules/
        (packaged with pip distribution)
    end note
```

## Notes

**Rule Files:**

- `dungeon_master_commands.mdc` - Command documentation
- `dungeon_master_enforcement.mdc` - Enforcement rules
- `dungeon_master_template.mdc` - Template guidelines
- `dungeon_master_workflow.mdc` - Workflow patterns

**Installation Process:**

- Creates `.cursor/rules/` directory if needed
- Copies all template files with verification
- Reports success/failure for each file

**Packaging Integration:**

- Templates are packaged within the `dungeon_master` module
- Ensures templates are available in pip installations
- **Fixed**: Template discovery now works correctly with packaged distributions
- No longer depends on project root structure for template location

---

_This documentation is linked to dungeon_master/utils/cursor_setup.py_
