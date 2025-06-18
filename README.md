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

## Development

### Setting Up Development Environment

1. Clone the repository:

```bash
git clone <repository-url>
cd dm
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
pip install -e .
```

Or use the Makefile shortcut:

```bash
make dev-setup
```

### Development Commands

We provide a Makefile with common development tasks:

```bash
make help        # Show available commands
make test        # Run tests with coverage
make lint        # Run linting checks
make format      # Format code with black and isort
make type-check  # Run mypy type checking
make clean       # Clean up build artifacts
make build       # Build the package
```

### Requirements Files

- `requirements.txt` - Production dependencies only
- `requirements-dev.txt` - Development dependencies (includes production deps)

### Code Quality

This project uses several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **pytest** - Testing framework
- **pytest-cov** - Test coverage

Run `make lint` to check all quality standards, or `make format` to auto-fix formatting issues.

### Testing

Run tests with coverage reporting:

```bash
make test
```

Or run pytest directly:

```bash
pytest --cov=dungeon_master --cov-report=html
```

### Package Structure

```
dungeon_master/
├── cli.py              # Main CLI entry point
├── commands/           # Command implementations
├── core/              # Core functionality
├── utils/             # Utility modules
└── hooks/             # Git hook implementations
```

## Documentation

For full documentation, see the [docs](docs/) directory.

## License

[MIT](LICENSE)
