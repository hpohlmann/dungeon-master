# track_lore("core/engine.md")
"""
Git utilities for Dungeon Master.

This module provides git-related functionality for tracking file changes,
determining modified files, and integrating with git workflows.
"""

import subprocess
from pathlib import Path
from typing import List, Set


def is_git_repository() -> bool:
    """
    Check if the current directory is a git repository.
    
    Returns:
        bool: True if in a git repository, False otherwise
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def get_changed_files(include_staged=True, include_unstaged=True) -> List[str]:
    """
    Get list of changed files in the git repository.
    
    Args:
        include_staged (bool): Include staged changes
        include_unstaged (bool): Include unstaged changes
        
    Returns:
        List[str]: List of changed file paths relative to repository root
    """
    if not is_git_repository():
        return []
    
    changed_files = set()
    
    try:
        # Get staged changes
        if include_staged:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            changed_files.update(staged_files)
        
        # Get unstaged changes
        if include_unstaged:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            unstaged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            changed_files.update(unstaged_files)
        
        # Remove empty strings
        changed_files.discard('')
        
        return list(changed_files)
        
    except subprocess.CalledProcessError:
        return []


def get_tracked_files() -> List[str]:
    """
    Get list of all files tracked by git.
    
    Returns:
        List[str]: List of tracked file paths relative to repository root
    """
    if not is_git_repository():
        return []
    
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True
        )
        tracked_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return [f for f in tracked_files if f]  # Remove empty entries
        
    except subprocess.CalledProcessError:
        return []


def get_untracked_files() -> List[str]:
    """
    Get list of untracked files in the git repository.
    
    Returns:
        List[str]: List of untracked file paths relative to repository root
    """
    if not is_git_repository():
        return []
    
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        )
        untracked_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        return [f for f in untracked_files if f]  # Remove empty entries
        
    except subprocess.CalledProcessError:
        return []


def is_file_tracked(file_path: str) -> bool:
    """
    Check if a specific file is tracked by git.
    
    Args:
        file_path (str): Path to the file to check
        
    Returns:
        bool: True if file is tracked, False otherwise
    """
    if not is_git_repository():
        return False
    
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
        
    except subprocess.CalledProcessError:
        return False


def get_git_root() -> Path:
    """
    Get the root directory of the git repository.
    
    Returns:
        Path: Path to git repository root
        
    Raises:
        RuntimeError: If not in a git repository
    """
    if not is_git_repository():
        raise RuntimeError("Not in a git repository")
    
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True
        )
        return Path(result.stdout.strip())
        
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get git root: {e}")


def get_current_branch() -> str:
    """
    Get the name of the current git branch.
    
    Returns:
        str: Current branch name, or empty string if not in a git repository
    """
    if not is_git_repository():
        return ""
    
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
        
    except subprocess.CalledProcessError:
        return ""


def has_uncommitted_changes() -> bool:
    """
    Check if there are any uncommitted changes in the repository.
    
    Returns:
        bool: True if there are uncommitted changes, False otherwise
    """
    if not is_git_repository():
        return False
    
    changed_files = get_changed_files(include_staged=True, include_unstaged=True)
    return len(changed_files) > 0
