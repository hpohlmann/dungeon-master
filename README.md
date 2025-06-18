# Dungeon Master

A lightweight pre-commit hook system designed to enforce documentation updates alongside code changes.

## Overview

Dungeon Master ensures that documentation remains current with codebase changes by blocking commits when documentation isn't updated for modified files. It uses a decorator-based system to track which files are associated with which documentation.

## Features

- Pre-commit hook to enforce documentation updates
- Decorator system for associating files with documentation
- Rich formatted CLI output for documentation status
- Template system for standardized documentation
- Support for professional diagrams using mermaid.js
- Cursor IDE integration

## Installation

```bash
pip install dungeon-master
```

## Quick Start

1. Initialize Dungeon Master in your repository:

```bash
dm init
```

2. Add decorators to your files:

```python
# track_lore("payments.md")
def process_payment():
    # ...
```

3. Create documentation files:

```bash
dm create_lore
```

4. Fill out the documentation templates

5. Check documentation status:

```bash
dm review
```

## Commands

- `dm init` - Initialize Dungeon Master in your repository
- `dm validate` - Validate documentation status (used by pre-commit hook)
- `dm review` - Display documentation status with rich formatting
- `dm create_lore` - Create missing documentation files
- `dm map` - Generate visual repository structure

## Documentation

For full documentation, see the [docs](docs/) directory.

## License

[MIT](LICENSE)
