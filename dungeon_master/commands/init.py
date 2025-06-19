# track_lore("commands/cli-system.md")
"""
Initialize Dungeon Master in the current repository.

This module handles the initialization of Dungeon Master environment,
including creating necessary directories, configuration files, and
setting up the pre-commit hook.
"""

import os
from pathlib import Path

from rich.console import Console

from dungeon_master.utils.config import create_default_config
from dungeon_master.utils.cursor_setup import setup_cursor_rules

console = Console()


def cleanup_lore_cache_files() -> bool:
    """
    Remove any cache files that might exist in the .lore directory.
    
    This ensures only one cache file exists in the project root,
    preventing token consumption from large cache files in AI context.
    
    Returns:
        True if cleanup completed successfully, False on error
    """
    try:
        lore_dir = Path(".lore")
        if not lore_dir.exists():
            return True
            
        # Find and remove any cache files in .lore directory
        cache_patterns = ["dmcache.json", ".dmcache.json", ".dmcache.tmp"]
        removed_files = []
        
        for pattern in cache_patterns:
            for cache_file in lore_dir.rglob(pattern):
                try:
                    cache_file.unlink()
                    removed_files.append(str(cache_file))
                except OSError:
                    pass  # File might not exist or no permissions
        
        if removed_files:
            console.print(f"  🧹 Cleaned up cache files from .lore directory: {', '.join(removed_files)}")
        
        return True
    except Exception as e:
        console.print(f"  ⚠️ [yellow]Warning: Could not clean .lore cache files: {e}[/yellow]")
        return True  # Don't fail init for cleanup issues


def create_lore_directory() -> bool:
    """
    Create the .lore directory if it doesn't exist.

    Returns:
        True if directory was created or already exists, False on error
    """
    lore_dir = Path(".lore")

    try:
        lore_dir.mkdir(exist_ok=True)
        console.print(f"  ✅ Created [cyan].lore/[/cyan] directory")
        return True
    except OSError as e:
        console.print(f"  ❌ [red]Failed to create .lore directory: {e}[/red]")
        return False


def create_config_files() -> bool:
    """
    Create dmconfig.json and dmcache.json configuration files.
    
    Both files are always created in the current working directory (project root).
    The cache file should never be created in subdirectories like .lore/.

    Returns:
        True if files were created successfully, False on error
    """
    try:
        # Create dmconfig.json using the configuration system
        if create_default_config(verbose=False):
            console.print(f"  ✅ Created [cyan]dmconfig.json[/cyan]")
        else:
            console.print(f"  ❌ [red]Failed to create dmconfig.json[/red]")
            return False

        # Create empty dmcache.json - ALWAYS in project root, never in subdirectories
        cache_content = """{
  "lastValidation": null,
  "reviewedFiles": {},
  "templateFiles": {}
}"""

        # Explicitly create in current directory (where dm init is run from)
        cache_path = "dmcache.json"
        with open(cache_path, "w") as f:
            f.write(cache_content)
        console.print(f"  ✅ Created [cyan]dmcache.json[/cyan] (single cache file in project root)")

        return True
    except OSError as e:
        console.print(f"  ❌ [red]Failed to create config files: {e}[/red]")
        return False


def update_gitignore() -> bool:
    """
    Update .gitignore with comprehensive patterns including virtual environments.

    Returns:
        True if .gitignore was updated successfully, False on error
    """
    try:
        from dungeon_master.utils.file_utils import get_gitignore_template
        
        gitignore_path = Path(".gitignore")
        
        # Get the template content
        try:
            template_content = get_gitignore_template()
        except FileNotFoundError as e:
            console.print(f"  ❌ [red]Error loading gitignore template: {e}[/red]")
            return False

        # Read existing .gitignore if it exists
        existing_content = ""
        if gitignore_path.exists():
            existing_content = gitignore_path.read_text(encoding="utf-8")

        # Split template into lines for checking
        template_lines = template_content.strip().split("\n")
        existing_lines = existing_content.strip().split("\n") if existing_content else []
        
        # Find lines that need to be added
        lines_to_add = []
        for line in template_lines:
            # Skip empty lines and comments for duplicate checking
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
                
            # Check if this pattern is already in .gitignore
            if line_stripped not in existing_content:
                lines_to_add.append(line_stripped)

        if lines_to_add:
            # Add missing patterns to .gitignore
            with open(".gitignore", "a", encoding="utf-8") as f:
                if existing_content and not existing_content.endswith("\n"):
                    f.write("\n")
                f.write("\n")
                f.write(template_content)
                f.write("\n")

            patterns_summary = ["virtual environments", "Python cache files", "Dungeon Master files"]
            console.print(
                f"  ✅ Updated [cyan].gitignore[/cyan] with {len(lines_to_add)} new patterns ({', '.join(patterns_summary)})"
            )
        else:
            console.print(
                f"  ✅ [cyan].gitignore[/cyan] already contains all necessary patterns"
            )

        return True
    except OSError as e:
        console.print(f"  ❌ [red]Failed to update .gitignore: {e}[/red]")
        return False


def setup_pre_commit_hook() -> bool:
    """
    Set up the pre-commit hook for Dungeon Master.

    Returns:
        True if hook was set up successfully, False on error
    """
    try:
        # Create .git/hooks directory if it doesn't exist
        hooks_dir = Path(".git/hooks")
        if not hooks_dir.exists():
            console.print(
                f"  ⚠️  [yellow]No .git directory found - skipping pre-commit hook setup[/yellow]"
            )
            return True

        hooks_dir.mkdir(exist_ok=True)

        # Create pre-commit hook script
        hook_content = """#!/bin/bash
# Dungeon Master pre-commit hook
# This hook validates that documentation is updated for code changes

echo "🔒 Running Dungeon Master validation..."

# Run dm validate command
dm validate

# Exit with the same code as dm validate
exit $?
"""

        hook_path = hooks_dir / "pre-commit"
        hook_path.write_text(hook_content)

        # Make the hook executable
        os.chmod(hook_path, 0o755)

        console.print(f"  ✅ Set up [cyan]pre-commit hook[/cyan]")
        return True
    except OSError as e:
        console.print(f"  ❌ [red]Failed to set up pre-commit hook: {e}[/red]")
        return False


def run_init() -> bool:
    """
    Initialize Dungeon Master in the current repository.

    Creates:
    - .lore/ directory if it doesn't exist
    - .cursor/rules/ directory if it doesn't exist
    - Copies cursor rule files from templates
    - Creates dmconfig.json and dmcache.json files
    - Updates .gitignore to exclude dmcache.json
    - Sets up pre-commit hook

    Returns:
        True if initialization was successful, False otherwise
    """
    console.print("✨ [bold green]Initializing Dungeon Master[/bold green] ✨")
    console.print()

    success = True

    # Create directory structure
    console.print("📁 Creating directory structure...")
    success &= create_lore_directory()

    # Clean up any cache files in .lore directory (ensures single cache file in root)
    cleanup_lore_cache_files()

    # Set up Cursor rules
    console.print()
    try:
        copied_files, failed_files = setup_cursor_rules()
        if failed_files:
            success = False
    except (FileNotFoundError, OSError) as e:
        console.print(f"❌ [red]Failed to set up Cursor rules: {e}[/red]")
        success = False

    # Create configuration files
    console.print()
    console.print("📝 Creating configuration files...")
    success &= create_config_files()

    # Update .gitignore
    console.print()
    console.print("🔮 Setting up gitignore...")
    success &= update_gitignore()

    # Set up pre-commit hook
    console.print()
    console.print("🪝 Setting up pre-commit hook...")
    success &= setup_pre_commit_hook()

    # Final summary
    console.print()
    if success:
        console.print(
            "[bold green]✅ Initialization complete! Your project is now protected by Dungeon Master.[/bold green]"
        )
        console.print()
        console.print("📚 [bold]Next steps:[/bold]")
        console.print(
            '  1. Add [cyan]# track_lore("path/filename.md")[/cyan] decorators to your code files'
        )
        console.print(
            "  2. Run [cyan]dm create-lore[/cyan] to generate documentation templates"
        )
        console.print("  3. Fill out the generated documentation templates")
        console.print("  4. Use [cyan]dm review[/cyan] to check documentation status")
    else:
        console.print(
            "[bold red]❌ Initialization completed with some errors. Check the output above for details.[/bold red]"
        )

    return success
