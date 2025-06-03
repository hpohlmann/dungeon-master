# @track_context("file_parser.md")
"""
Parser module for identifying and extracting tracking decorators from files.
"""

import re
from typing import Dict, List, Optional
import logging

from .utils import read_file_content, is_text_file

logger = logging.getLogger(__name__)

# Regex pattern to match @track_context decorators
TRACK_CONTEXT_PATTERN = re.compile(
    r'#\s*@track_context\s*\(\s*["\']([^"\']+)["\']\s*\)',
    re.IGNORECASE
)


def extract_track_context_decorator(file_content: str) -> Optional[str]:
    """
    Extract the context document name from @track_context decorator.

    Args:
        file_content: Content of the file to parse

    Returns:
        Optional[str]: Context document name or None if not found
    """
    if not file_content:
        return None

    # Look for the decorator in the first few lines (typically at the top)
    lines = file_content.split('\n')[:10]  # Check first 10 lines

    for line in lines:
        match = TRACK_CONTEXT_PATTERN.search(line)
        if match:
            context_doc = match.group(1)
            # Ensure it ends with .md
            if not context_doc.endswith('.md'):
                context_doc += '.md'
            return context_doc

    return None


def parse_tracked_files(file_paths: List[str]) -> Dict[str, str]:
    """
    Parse a list of files to find those with @track_context decorators.

    Args:
        file_paths: List of file paths to parse

    Returns:
        Dict[str, str]: Mapping of file_path -> context_document_name
    """
    tracked_files = {}

    for file_path in file_paths:
        # Skip non-text files
        if not is_text_file(file_path):
            continue

        file_content = read_file_content(file_path)
        if file_content is None:
            continue

        context_doc = extract_track_context_decorator(file_content)
        if context_doc:
            tracked_files[file_path] = context_doc
            logger.info(f"Found tracked file: {file_path} -> {context_doc}")

    return tracked_files


def validate_context_document_name(context_doc: str) -> bool:
    """
    Validate that the context document name is properly formatted.

    Args:
        context_doc: The context document name

    Returns:
        bool: True if valid, False otherwise
    """
    if not context_doc:
        return False

    # Should end with .md
    if not context_doc.endswith('.md'):
        return False

    # Should not contain path separators (should be just a filename)
    if '/' in context_doc or '\\' in context_doc:
        return False

    # Should not be empty after removing .md
    if len(context_doc.replace('.md', '').strip()) == 0:
        return False

    return True


def get_file_summary(file_path: str) -> Dict[str, str]:
    """
    Get basic summary information about a file.

    Args:
        file_path: Path to the file

    Returns:
        Dict[str, str]: Basic file information
    """
    file_content = read_file_content(file_path)
    if not file_content:
        return {
            'file_path': file_path,
            'line_count': '0',
            'size': '0 bytes'
        }

    lines = file_content.split('\n')
    return {
        'file_path': file_path,
        'line_count': str(len(lines)),
        'size': f"{len(file_content)} bytes"
    }
