"""
Dungeon Master - Documentation enforcement system.

A lightweight pre-commit hook system designed to enforce documentation updates
alongside code changes. Ensures documentation remains current with codebase
changes by blocking commits when documentation isn't updated for modified files.
"""

__version__ = "0.1.0"
__author__ = "Dungeon Master Team"
__email__ = "team@dungeonmaster.dev"
__description__ = "A lightweight pre-commit hook system for documentation enforcement"

# Export main CLI function for entry point
from dungeon_master.cli import cli, main

__all__ = ["main", "cli", "__version__"]
