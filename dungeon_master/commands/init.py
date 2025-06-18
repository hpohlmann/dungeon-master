"""
Initialize Dungeon Master in the current repository.

This module handles the initialization of Dungeon Master environment,
including creating necessary directories, configuration files, and
setting up the pre-commit hook.
"""

import os
from pathlib import Path
from rich.console import Console
from dungeon_master.utils.cursor_setup import setup_cursor_rules, verify_cursor_rules_setup
from dungeon_master.utils.config import create_default_config

console = Console()


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
        
        # Create empty dmcache.json
        cache_content = """{
  "lastValidation": null,
  "reviewedFiles": {},
  "templateFiles": {}
}"""
        
        with open("dmcache.json", "w") as f:
            f.write(cache_content)
        console.print(f"  ✅ Created [cyan]dmcache.json[/cyan]")
        
        return True
    except OSError as e:
        console.print(f"  ❌ [red]Failed to create config files: {e}[/red]")
        return False


def update_gitignore() -> bool:
    """
    Update .gitignore to exclude dmcache.json.
    
    Returns:
        True if .gitignore was updated successfully, False on error
    """
    try:
        gitignore_path = Path(".gitignore")
        
        # Read existing .gitignore if it exists
        existing_content = ""
        if gitignore_path.exists():
            existing_content = gitignore_path.read_text()
        
        # Check if dmcache.json is already ignored
        if "dmcache.json" not in existing_content:
            # Add dmcache.json to .gitignore
            with open(".gitignore", "a") as f:
                if existing_content and not existing_content.endswith('\n'):
                    f.write('\n')
                f.write('\n# Dungeon Master cache file\ndmcache.json\n')
            
            console.print(f"  ✅ Updated [cyan].gitignore[/cyan] to exclude [cyan]dmcache.json[/cyan]")
        else:
            console.print(f"  ✅ [cyan].gitignore[/cyan] already excludes [cyan]dmcache.json[/cyan]")
        
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
            console.print(f"  ⚠️  [yellow]No .git directory found - skipping pre-commit hook setup[/yellow]")
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
        console.print("[bold green]✅ Initialization complete! Your project is now protected by Dungeon Master.[/bold green]")
        console.print()
        console.print("📚 [bold]Next steps:[/bold]")
        console.print("  1. Add [cyan]# track_lore(\"filename.md\")[/cyan] decorators to your code files")
        console.print("  2. Run [cyan]dm create-lore[/cyan] to generate documentation templates")
        console.print("  3. Fill out the generated documentation templates")
        console.print("  4. Use [cyan]dm review[/cyan] to check documentation status")
    else:
        console.print("[bold red]❌ Initialization completed with some errors. Check the output above for details.[/bold red]")
    
    return success
