# @track_context("utilities.md")
"""
Shared utility functions for Dungeon Master.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def ensure_output_directory() -> Path:
    """
    Ensure the /lore/ output directory exists.

    Returns:
        Path: The path to the lore directory
    """
    output_dir = Path("lore")
    output_dir.mkdir(exist_ok=True)
    return output_dir


def get_git_changes() -> Tuple[List[str], List[str]]:
    """
    Get staged files and new files from Git.

    Returns:
        Tuple[List[str], List[str]]: (staged_files, new_files)
    """
    try:
        # Get staged files
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        staged_files = [f.strip() for f in result.stdout.split('\n') if f.strip()]

        # Get new (untracked) files that are staged
        result = subprocess.run(
            ["git", "ls-files", "--others", "--cached", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        )
        new_files = [f.strip() for f in result.stdout.split('\n') if f.strip()]

        return staged_files, new_files

    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        return [], []


def read_file_content(file_path: str) -> Optional[str]:
    """
    Read content from a file safely.

    Args:
        file_path: Path to the file to read

    Returns:
        Optional[str]: File content or None if file doesn't exist/can't be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError, UnicodeDecodeError) as e:
        logger.warning(f"Could not read file {file_path}: {e}")
        return None


def write_file_content(file_path: str, content: str) -> bool:
    """
    Write content to a file safely.

    Args:
        file_path: Path to the file to write
        content: Content to write

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except (IOError, UnicodeEncodeError) as e:
        logger.error(f"Could not write file {file_path}: {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension from a file path.

    Args:
        file_path: Path to the file

    Returns:
        str: File extension (e.g., '.py', '.js')
    """
    return Path(file_path).suffix


def is_text_file(file_path: str) -> bool:
    """
    Check if a file is likely a text file based on extension.

    Args:
        file_path: Path to the file

    Returns:
        bool: True if likely a text file
    """
    text_extensions = {
        '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.hpp',
        '.rs', '.go', '.rb', '.php', '.cs', '.kt', '.swift',
        '.md', '.txt', '.json', '.yaml', '.yml', '.xml', '.html',
        '.css', '.scss', '.sass', '.sql', '.sh', '.bash', '.zsh'
    }

    extension = get_file_extension(file_path).lower()
    return extension in text_extensions


def format_timestamp() -> str:
    """
    Format current timestamp for changelog entries.

    Returns:
        str: Formatted timestamp (YYYY-MM-DD)
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")
