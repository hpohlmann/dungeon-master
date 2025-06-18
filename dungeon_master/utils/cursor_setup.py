# track_lore("integrations/cursor.md")
"""
Cursor Rules Setup Utilities

This module provides functionality to set up Cursor IDE integration by copying
pre-created rule files from the templates directory to the .cursor/rules directory.
"""

import shutil
from pathlib import Path
from typing import List, Tuple

from rich.console import Console

console = Console()

# Define the rule files to be copied
CURSOR_RULE_FILES = [
    "dungeon_master_workflow.mdc",
    "dungeon_master_enforcement.mdc",
    "dungeon_master_commands.mdc",
    "dungeon_master_template.mdc",
]

# Default cursor rules directory
DEFAULT_CURSOR_RULES_DIR = ".cursor/rules"


def get_templates_directory() -> Path:
    """
    Get the path to the templates/cursor_rules directory.

    Returns:
        Path to the templates/cursor_rules directory within the package

    Raises:
        FileNotFoundError: If the templates directory doesn't exist
    """
    # Get the package directory (dungeon_master)
    package_dir = Path(__file__).parent.parent

    # Templates are now inside the package
    templates_dir = package_dir / "templates" / "cursor_rules"

    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    return templates_dir


def create_cursor_rules_directory(
    cursor_rules_dir: str = DEFAULT_CURSOR_RULES_DIR,
) -> Path:
    """
    Create the .cursor/rules directory if it doesn't exist.

    Args:
        cursor_rules_dir: Path to the cursor rules directory

    Returns:
        Path object for the created directory

    Raises:
        OSError: If directory creation fails
    """
    rules_path = Path(cursor_rules_dir)

    try:
        rules_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create cursor rules directory {rules_path}: {e}")

    return rules_path


def copy_rule_file(
    rule_file: str, templates_dir: Path, cursor_rules_dir: Path, overwrite: bool = True
) -> bool:
    """
    Copy a single rule file from templates to cursor rules directory.

    Args:
        rule_file: Name of the rule file to copy
        templates_dir: Source templates directory
        cursor_rules_dir: Destination cursor rules directory
        overwrite: Whether to overwrite existing files

    Returns:
        True if file was copied successfully, False otherwise
    """
    source_path = templates_dir / rule_file
    dest_path = cursor_rules_dir / rule_file

    # Check if source file exists
    if not source_path.exists():
        console.print(f"  ❌ [red]Source file not found: {source_path}[/red]")
        return False

    # Check if destination exists and overwrite is False
    if dest_path.exists() and not overwrite:
        console.print(f"  ⏭️  [yellow]Skipped {rule_file} (already exists)[/yellow]")
        return False

    try:
        # Copy the file with metadata
        shutil.copy2(source_path, dest_path)
        console.print(
            f"  ✅ Copied [cyan]{rule_file}[/cyan] to [cyan]{dest_path}[/cyan]"
        )
        return True
    except (OSError, shutil.Error) as e:
        console.print(f"  ❌ [red]Error copying {rule_file}: {e}[/red]")
        return False


def setup_cursor_rules(
    cursor_rules_dir: str = DEFAULT_CURSOR_RULES_DIR,
    overwrite: bool = True,
    verbose: bool = True,
) -> Tuple[List[str], List[str]]:
    """
    Set up Cursor rules by copying template files.

    Args:
        cursor_rules_dir: Path to the cursor rules directory
        overwrite: Whether to overwrite existing rule files
        verbose: Whether to print progress messages

    Returns:
        Tuple of (successfully_copied_files, failed_files)

    Raises:
        FileNotFoundError: If templates directory doesn't exist
        OSError: If cursor rules directory cannot be created
    """
    if verbose:
        console.print("🧙 [bold green]Setting up Cursor rules...[/bold green]")

    # Get templates directory
    try:
        templates_dir = get_templates_directory()
    except FileNotFoundError as e:
        if verbose:
            console.print(f"❌ [red]{e}[/red]")
        raise

    # Create cursor rules directory
    try:
        rules_path = create_cursor_rules_directory(cursor_rules_dir)
        if verbose:
            console.print(f"📁 Created/verified directory: [cyan]{rules_path}[/cyan]")
    except OSError as e:
        if verbose:
            console.print(f"❌ [red]{e}[/red]")
        raise

    # Copy each rule file
    copied_files = []
    failed_files = []

    if verbose:
        console.print("📝 Copying rule files...")

    for rule_file in CURSOR_RULE_FILES:
        success = copy_rule_file(
            rule_file=rule_file,
            templates_dir=templates_dir,
            cursor_rules_dir=rules_path,
            overwrite=overwrite,
        )

        if success:
            copied_files.append(rule_file)
        else:
            failed_files.append(rule_file)

    # Summary
    if verbose:
        if copied_files:
            console.print(
                f"✨ [bold green]Successfully copied {len(copied_files)} rule files[/bold green]"
            )
        if failed_files:
            console.print(
                f"⚠️  [bold yellow]Failed to copy {len(failed_files)} files: {', '.join(failed_files)}[/bold yellow]"
            )

    return copied_files, failed_files


def verify_cursor_rules_setup(
    cursor_rules_dir: str = DEFAULT_CURSOR_RULES_DIR,
) -> Tuple[List[str], List[str]]:
    """
    Verify that all expected Cursor rule files are present.

    Args:
        cursor_rules_dir: Path to the cursor rules directory

    Returns:
        Tuple of (present_files, missing_files)
    """
    rules_path = Path(cursor_rules_dir)
    present_files = []
    missing_files = []

    for rule_file in CURSOR_RULE_FILES:
        file_path = rules_path / rule_file
        if file_path.exists():
            present_files.append(rule_file)
        else:
            missing_files.append(rule_file)

    return present_files, missing_files


def remove_cursor_rules(
    cursor_rules_dir: str = DEFAULT_CURSOR_RULES_DIR, verbose: bool = True
) -> bool:
    """
    Remove Cursor rule files (useful for cleanup or reset).

    Args:
        cursor_rules_dir: Path to the cursor rules directory
        verbose: Whether to print progress messages

    Returns:
        True if all files were removed successfully, False otherwise
    """
    if verbose:
        console.print("🧹 [bold yellow]Removing Cursor rules...[/bold yellow]")

    rules_path = Path(cursor_rules_dir)
    success = True

    for rule_file in CURSOR_RULE_FILES:
        file_path = rules_path / rule_file
        if file_path.exists():
            try:
                file_path.unlink()
                if verbose:
                    console.print(f"  ✅ Removed [cyan]{rule_file}[/cyan]")
            except OSError as e:
                if verbose:
                    console.print(f"  ❌ [red]Error removing {rule_file}: {e}[/red]")
                success = False
        elif verbose:
            console.print(f"  ⏭️  [dim]{rule_file} not found[/dim]")

    return success
