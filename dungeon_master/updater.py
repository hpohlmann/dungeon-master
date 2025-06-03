# @track_context("document_updater.md")
"""
Updater module for validating context documents and managing updates.
Focuses on validation rather than content generation.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

from .utils import read_file_content, write_file_content, format_timestamp
from .generator import has_unfilled_placeholders, get_unfilled_sections
from .change_detector import ChangeDetector, ChangeAnalysis

logger = logging.getLogger(__name__)


def validate_context_document(context_doc_path: str) -> Tuple[bool, List[str]]:
    """
    Validate that a context document has been properly filled by Cursor.

    Args:
        context_doc_path: Path to the context document

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_issues)
    """
    content = read_file_content(context_doc_path)
    if not content:
        return False, [f"Context document not found: {context_doc_path}"]

    issues = []

    # Check for unfilled placeholders
    if has_unfilled_placeholders(content):
        unfilled_sections = get_unfilled_sections(content)
        issues.append(f"Document contains unfilled placeholders in: {', '.join(unfilled_sections)}")

    # Check for instruction block
    if re.search(r'> \*\*Instructions for Cursor\*\*', content):
        issues.append("Instructions block still present (should be removed when complete)")

    # Check minimum content requirements
    if not _has_meaningful_content(content):
        issues.append("Document appears to lack meaningful content")

    return len(issues) == 0, issues


def _has_meaningful_content(content: str) -> bool:
    """Check if document has meaningful content beyond placeholders."""
    # Remove common template text and placeholders
    cleaned_content = re.sub(r'<.*?>', '', content)  # Remove all placeholder text
    cleaned_content = re.sub(r'> \*\*Instructions.*?\*\*.*?(?=\n##|\Z)', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'#.*?\n', '', cleaned_content)  # Remove headers
    cleaned_content = re.sub(r'\*.*?\*', '', cleaned_content)  # Remove bold text
    cleaned_content = re.sub(r'`.*?`', '', cleaned_content)  # Remove code blocks
    cleaned_content = re.sub(r'-.*?\n', '', cleaned_content)  # Remove list items
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()  # Normalize whitespace

    # If there's substantial content left, it's probably meaningful
    # Reduced threshold for more realistic validation
    return len(cleaned_content) > 50  # Reduced from 100 to 50


def add_changelog_entry(context_doc_path: str, file_path: str, change_description: str = None) -> bool:
    """
    Add a changelog entry to an existing context document.

    Args:
        context_doc_path: Path to the context document
        file_path: Path to the file that changed
        change_description: Optional description of changes

    Returns:
        bool: True if update was successful
    """
    content = read_file_content(context_doc_path)
    if not content:
        logger.error(f"Could not read context document: {context_doc_path}")
        return False

    timestamp = format_timestamp()
    filename = Path(file_path).name

    # Generate changelog entry
    if change_description:
        entry = f"### [{timestamp}]\n- {change_description}"
    else:
        entry = f"### [{timestamp}]\n- Updated `{filename}` - please review and update context as needed"

    # Find changelog section and add entry
    changelog_pattern = r'(## Changelog\s*\n)(.*?)(\n---|\Z)'
    match = re.search(changelog_pattern, content, re.DOTALL)

    if match:
        # Insert new entry at the top of existing changelog
        existing_changelog = match.group(2).strip()
        if existing_changelog:
            new_changelog = f"{entry}\n\n{existing_changelog}"
        else:
            new_changelog = entry

        # Replace changelog section
        updated_content = re.sub(
            changelog_pattern,
            f"{match.group(1)}{new_changelog}{match.group(3)}",
            content,
            flags=re.DOTALL
        )
    else:
        # Add changelog section if it doesn't exist
        updated_content = content + f"\n\n## Changelog\n\n{entry}\n"

    # Update timestamp in footer
    footer_pattern = r'(\*This document is maintained by Cursor\. Last updated: ).*?(\*)'
    updated_content = re.sub(footer_pattern, f'\\g<1>{timestamp}\\g<2>', updated_content)

    return write_file_content(context_doc_path, updated_content)


def is_context_document_stale(file_path: str, context_doc_path: str) -> bool:
    """
    Check if a context document needs attention due to file changes.

    Args:
        file_path: Path to the tracked file
        context_doc_path: Path to the context document

    Returns:
        bool: True if context document needs attention
    """
    from pathlib import Path
    import os

    file_path_obj = Path(file_path)
    context_path_obj = Path(context_doc_path)

    # If context document doesn't exist, it's stale
    if not context_path_obj.exists():
        return True

    # If tracked file doesn't exist, context might be stale
    if not file_path_obj.exists():
        return True

    # If context document has unfilled placeholders, it's stale
    is_valid, _ = validate_context_document(context_doc_path)
    if not is_valid:
        return True

    # Compare modification times
    try:
        file_mtime = os.path.getmtime(file_path)
        context_mtime = os.path.getmtime(context_doc_path)

        # If file is significantly newer than context document, it's potentially stale
        # Allow some grace period (1 hour) for minor edits
        return (file_mtime - context_mtime) > 3600
    except OSError:
        # If we can't get modification times, assume stale
        return True


def get_validation_status(tracked_files: Dict[str, str], output_dir: Path) -> Dict[str, Dict[str, any]]:
    """
    Get validation status for all tracked files.

    Args:
        tracked_files: Dictionary mapping file_path -> context_document_name
        output_dir: Output directory for context documents

    Returns:
        Dict with validation status for each file
    """
    status = {}

    for file_path, context_doc_name in tracked_files.items():
        context_doc_path = output_dir / context_doc_name

        if not context_doc_path.exists():
            status[file_path] = {
                'context_doc': context_doc_name,
                'exists': False,
                'valid': False,
                'issues': ['Context document does not exist']
            }
        else:
            is_valid, issues = validate_context_document(str(context_doc_path))
            status[file_path] = {
                'context_doc': context_doc_name,
                'exists': True,
                'valid': is_valid,
                'issues': issues,
                'stale': is_context_document_stale(file_path, str(context_doc_path))
            }

    return status


def check_for_significant_changes(tracked_files: Dict[str, str]) -> Tuple[List[ChangeAnalysis], bool]:
    """
    Check tracked files for significant changes that require documentation updates.

    Args:
        tracked_files: Dictionary mapping file_path -> context_document_name

    Returns:
        Tuple[List[ChangeAnalysis], bool]: (significant_changes, should_block_commit)
    """
    detector = ChangeDetector()
    file_paths = list(tracked_files.keys())

    significant_changes = detector.get_significant_changes(file_paths)

    # Check if any changes require blocking
    should_block = any(change.is_significant for change in significant_changes)

    return significant_changes, should_block


def get_blocking_issues(validation_status: Dict[str, Dict[str, any]],
                       significant_changes: List[ChangeAnalysis] = None) -> List[str]:
    """
    Get list of issues that should block a commit.

    Args:
        validation_status: Status from get_validation_status
        significant_changes: List of significant changes detected

    Returns:
        List[str]: List of blocking issues
    """
    blocking_issues = []

    for file_path, status in validation_status.items():
        context_doc = status['context_doc']

        if not status['exists']:
            blocking_issues.append(f"Missing context document: {context_doc} (for {file_path})")
        elif not status['valid']:
            issue_list = ', '.join(status['issues'])
            blocking_issues.append(f"Context document needs completion: {context_doc} ({issue_list})")

    # Add significant change issues
    if significant_changes:
        for change in significant_changes:
            if change.is_significant:
                change_desc = '; '.join(change.changes[:3])  # Limit description length
                blocking_issues.append(f"Significant changes detected in {change.file_path}: {change_desc}")

    return blocking_issues


def mark_changes_as_reviewed(tracked_files: Dict[str, str]) -> bool:
    """
    Mark file changes as reviewed, updating the change detection cache.

    Args:
        tracked_files: Dictionary mapping file_path -> context_document_name

    Returns:
        bool: True if successful
    """
    try:
        detector = ChangeDetector()
        detector.mark_as_reviewed(list(tracked_files.keys()))
        return True
    except Exception as e:
        logger.error(f"Could not mark changes as reviewed: {e}")
        return False
