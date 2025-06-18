# track_lore("core/engine.md")
"""
Lore Decorator Parser

This module provides functionality to detect and extract track_lore decorators
from Python and TypeScript files. It supports scanning individual files or
entire repositories to build a mapping of documentation files to source files.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional

# Regex patterns for track_lore decorators
# Python: Matches comments with the track_lore function call syntax
PY_PATTERN = r'#\s*track_lore\(\s*["\']([^"\']+)["\']\s*\)'

# TypeScript/JavaScript: Matches comments with the track_lore function call syntax
TS_PATTERN = r'//\s*track_lore\(\s*["\']([^"\']+)["\']\s*\)'

# Supported file extensions
PYTHON_EXTENSIONS = {'.py', '.pyx', '.pyi'}
TYPESCRIPT_EXTENSIONS = {'.ts', '.tsx', '.js', '.jsx'}
ALL_SUPPORTED_EXTENSIONS = PYTHON_EXTENSIONS | TYPESCRIPT_EXTENSIONS

# Default directories to skip during repository scanning (fallback if no config)
DEFAULT_SKIP_DIRECTORIES = {
    '.git', '.hg', '.svn',  # Version control
    '__pycache__', '.pytest_cache', '.mypy_cache',  # Python cache
    'node_modules', '.next', '.nuxt',  # JavaScript/Node
    '.venv', 'venv', 'env',  # Virtual environments
    'build', 'dist', '.build',  # Build artifacts
    '.taskmaster',  # Task management directory
    'examples',  # Example files
    'tests'  # Test files
}

## TODO: Add in .gitignore file skips during repository scanning

def get_file_extension(file_path: Path) -> str:
    """
    Get the lowercase file extension for a given file path.
    
    Args:
        file_path: Path object for the file
        
    Returns:
        Lowercase file extension (e.g., '.py', '.ts')
    """
    return file_path.suffix.lower()


def is_supported_file(file_path: Path) -> bool:
    """
    Check if a file type is supported for decorator parsing.
    
    Args:
        file_path: Path object for the file
        
    Returns:
        True if the file type is supported, False otherwise
    """
    return get_file_extension(file_path) in ALL_SUPPORTED_EXTENSIONS


def should_skip_directory(dir_path: Path, excluded_directories: Optional[List[str]] = None) -> bool:
    """
    Check if a directory should be skipped during repository scanning.
    
    Args:
        dir_path: Path object for the directory
        excluded_directories: Optional list of directory names to exclude (from config)
        
    Returns:
        True if the directory should be skipped, False otherwise
    """
    dir_name = dir_path.name.lower()
    
    # Use provided exclusions or fall back to defaults
    if excluded_directories is None:
        excluded_directories = list(DEFAULT_SKIP_DIRECTORIES)
    
    # Convert to lowercase for case-insensitive comparison
    excluded_directories_lower = [d.lower() for d in excluded_directories]
    
    # Skip known directories that shouldn't contain trackable code
    if dir_name in excluded_directories_lower:
        return True
        
    # Skip hidden directories (starting with .) except .lore and .lore.dev
    if dir_name.startswith('.') and dir_name not in {'.lore', '.lore.dev'}:
        return True
        
    return False


def extract_lore_paths(file_path: Path) -> List[str]:
    """
    Extract all lore file paths from track_lore decorators in a file.
    
    Args:
        file_path: Path to the source file to parse
        
    Returns:
        List of lore file paths found in the file
        
    Raises:
        ValueError: If the file type is not supported
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file contains invalid UTF-8
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
        
    if not is_supported_file(file_path):
        raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    lore_paths = []
    
    try:
        # Read file content with UTF-8 encoding
        content = file_path.read_text(encoding='utf-8')
        
        # Select regex pattern based on file extension
        ext = get_file_extension(file_path)
        if ext in PYTHON_EXTENSIONS:
            pattern = PY_PATTERN
        elif ext in TYPESCRIPT_EXTENSIONS:
            pattern = TS_PATTERN
        else:
            # This shouldn't happen due to is_supported_file check, but just in case
            return []
            
        # Find all matches
        matches = re.findall(pattern, content, re.MULTILINE)
        
        # Clean up and validate the paths
        for match in matches:
            # Strip whitespace and normalize path separators
            lore_path = match.strip().replace('\\', '/')
            
            # Skip empty paths
            if lore_path:
                lore_paths.append(lore_path)
                
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            f"File {file_path} contains invalid UTF-8 encoding: {e}"
        )
    except Exception as e:
        # Re-raise other exceptions with context
        raise Exception(f"Error processing {file_path}: {e}") from e
        
    return lore_paths


def extract_lore_paths_safe(file_path: Path) -> List[str]:
    """
    Safely extract lore paths from a file, returning empty list on any error.
    
    This is a convenience function for repository scanning where we don't want
    individual file errors to stop the entire process.
    
    Args:
        file_path: Path to the source file to parse
        
    Returns:
        List of lore file paths found in the file, or empty list if any error occurs
    """
    try:
        return extract_lore_paths(file_path)
    except Exception:
        # Silently ignore errors during repository scanning
        # Individual files with issues shouldn't stop the entire process
        return []


def scan_repository_for_lore_decorators(
    repo_path: Optional[Path] = None,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    config: Optional[Dict] = None
) -> Dict[str, List[str]]:
    """
    Scan a repository for track_lore decorators and build a mapping.
    
    Args:
        repo_path: Root path to scan (defaults to current directory)
        include_patterns: List of glob patterns to include (overrides default extensions)
        exclude_patterns: List of glob patterns to exclude
        config: Optional configuration dictionary with exclusion settings
        
    Returns:
        Dictionary mapping lore file paths to lists of source files that reference them
        
    Example:
        {
            "payments.md": ["src/api/payment.py", "src/models/payment.py"],
            "auth.md": ["src/auth/login.py"]
        }
    """
    if repo_path is None:
        repo_path = Path.cwd()
    else:
        repo_path = Path(repo_path)
        
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository path not found: {repo_path}")
    
    # Get exclusion settings from config if provided
    excluded_directories = None
    if config:
        excluded_directories = config.get("excludedDirectories", list(DEFAULT_SKIP_DIRECTORIES))
        
    lore_mapping: Dict[str, List[str]] = {}
    
    # Use custom directory walker that respects exclusions from the start
    # This avoids the performance issue of globbing through virtual environments
    def walk_directory(current_path: Path) -> List[Path]:
        """Walk directory tree, skipping excluded directories."""
        files = []
        
        try:
            for item in current_path.iterdir():
                if item.is_dir():
                    # Skip excluded directories entirely - don't even recurse into them
                    if should_skip_directory(item, excluded_directories):
                        continue
                    # Recursively walk non-excluded directories
                    files.extend(walk_directory(item))
                elif item.is_file():
                    # Only include supported file types (unless custom include_patterns)
                    if include_patterns:
                        # If custom patterns, check against them
                        if any(item.match(pattern) for pattern in include_patterns):
                            files.append(item)
                    else:
                        # Default: only supported extensions
                        if is_supported_file(item):
                            files.append(item)
        except (PermissionError, OSError):
            # Skip directories we can't read
            pass
            
        return files
    
    # Get all files using our custom walker (no more glob performance issues!)
    file_paths = walk_directory(repo_path)
    
    for file_path in file_paths:
        # Apply additional exclude patterns if specified
        if exclude_patterns:
            if any(file_path.match(pattern) for pattern in exclude_patterns):
                continue
        
        # Extract lore paths from this file
        lore_paths = extract_lore_paths_safe(file_path)
        
        # Add to mapping
        for lore_path in lore_paths:
            if lore_path not in lore_mapping:
                lore_mapping[lore_path] = []
            
            # Store relative path from repo root for consistency
            try:
                relative_path = file_path.relative_to(repo_path)
                lore_mapping[lore_path].append(str(relative_path))
            except ValueError:
                # File is outside repo_path, use absolute path
                lore_mapping[lore_path].append(str(file_path))
    
    return lore_mapping


def find_files_for_lore(lore_file: str, repo_path: Optional[Path] = None) -> List[str]:
    """
    Find all source files that reference a specific lore file.
    
    Args:
        lore_file: The lore file path to search for
        repo_path: Root path to scan (defaults to current directory)
        
    Returns:
        List of source file paths that reference the lore file
    """
    mapping = scan_repository_for_lore_decorators(repo_path)
    return mapping.get(lore_file, [])


def get_lore_files_for_source(source_file: Path, repo_path: Optional[Path] = None) -> List[str]:
    """
    Get all lore files referenced by a specific source file.
    
    Args:
        source_file: Path to the source file
        repo_path: Root path (used for relative path calculation)
        
    Returns:
        List of lore file paths referenced by the source file
    """
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")
        
    return extract_lore_paths(source_file)
