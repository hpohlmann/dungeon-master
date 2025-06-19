# track_lore("utils/utilities.md")
"""
File System Utilities

This module provides file system operations and utilities for Dungeon Master,
including template loading and file manipulation functions.
"""

from pathlib import Path
from typing import Optional


def get_gitignore_template() -> str:
    """
    Get the gitignore template content from the package templates.

    Returns:
        Gitignore template content as string

    Raises:
        FileNotFoundError: If the gitignore template doesn't exist
    """
    # Get the package directory (dungeon_master)
    package_dir = Path(__file__).parent.parent

    # Template is in the templates directory
    template_path = package_dir / "templates" / "gitignore.template"

    if not template_path.exists():
        raise FileNotFoundError(f"Gitignore template not found: {template_path}")

    try:
        return template_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise FileNotFoundError(f"Error reading gitignore template: {e}")


def ensure_directory(directory_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory to create

    Returns:
        True if directory exists or was created successfully, False otherwise
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False
