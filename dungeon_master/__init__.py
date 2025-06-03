"""
Dungeon Master: A context-tracking pre-commit tool.

Maintains human-readable, file-linked context documents in Markdown format.
This is a structured integration point where Cursor collaborates with users
to maintain a self-updating knowledge base.
"""

__version__ = "0.3.1"
__author__ = "Dungeon Master Team"
__description__ = "Context-tracking pre-commit tool for Cursor integration"

from .parser import parse_tracked_files
from .generator import generate_context_template, has_unfilled_placeholders
from .updater import validate_context_document, add_changelog_entry
from .utils import ensure_output_directory, get_git_changes

__all__ = [
    "parse_tracked_files",
    "generate_context_template",
    "has_unfilled_placeholders",
    "validate_context_document",
    "add_changelog_entry",
    "ensure_output_directory",
    "get_git_changes",
]
