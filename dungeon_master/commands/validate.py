# track_lore("commands/cli-system.md")
"""
Validate documentation for pre-commit hook.

This module handles the core pre-commit hook functionality that verifies
each tracked file has corresponding documentation and checks that changed
tracked files have updated documentation.
"""

from pathlib import Path
from rich.console import Console
from rich.table import Table

from dungeon_master.core.decorator_parser import scan_repository_for_lore_decorators
from dungeon_master.core.template import validate_lore_file
from dungeon_master.core.git_utils import get_changed_files
from dungeon_master.utils.config import load_config, get_lore_directory

console = Console()


def run_validate():
    """
    Core pre-commit hook functionality.

    Verifies:
    - Each tracked file has corresponding lore file
    - Changed tracked files have updated lore
    - Lore files contain more than just template content
    - Placeholder text in required sections is detected
    - Professional diagrams are included when required

    Blocks commits when validation fails.

    Returns:
        bool: True if validation passes, False if it fails
    """
    try:
        console.print("🔒 [bold green]Running Dungeon Master Validation[/bold green] 🔒")
        console.print()
        
        # Load configuration
        config = load_config()
        lore_root = get_lore_directory(config)
        lore_path = Path(lore_root)
        
        # Scan for decorators
        console.print("🔍 Scanning for track_lore decorators...")
        mapping = scan_repository_for_lore_decorators(config=config)
        
        if not mapping:
            console.print("  [green]No track_lore decorators found - validation passes[/green]")
            return True
            
        console.print(f"  Found [bold]{len(mapping)}[/bold] lore files referenced in code")
        console.print()
        
        # Check for missing lore files
        console.print("📋 Checking for missing documentation files...")
        missing_files = []
        template_files = []
        invalid_files = []
        
        for lore_file_path, tracked_files in mapping.items():
            full_path = lore_path / lore_file_path
            
            if not full_path.exists():
                missing_files.append((lore_file_path, tracked_files))
                console.print(f"  ❌ [red]MISSING: {lore_root}/{lore_file_path}[/red]")
                console.print(f"     [dim]Referenced in: {', '.join(tracked_files)}[/dim]")
            else:
                # Validate the lore file
                validation = validate_lore_file(full_path)
                
                if validation["is_template"]:
                    template_files.append((lore_file_path, tracked_files, validation))
                    console.print(f"  ⚠️ [yellow]TEMPLATE: {lore_root}/{lore_file_path}[/yellow]")
                    console.print(f"     [dim]Contains placeholder text - needs completion[/dim]")
                elif not validation["is_valid"]:
                    invalid_files.append((lore_file_path, tracked_files, validation))
                    console.print(f"  ❌ [red]INCOMPLETE: {lore_root}/{lore_file_path}[/red]")
                    console.print(f"     [dim]Missing required sections: {', '.join(validation['missing_sections'])}[/dim]")
                else:
                    console.print(f"  ✅ [green]VALID: {lore_root}/{lore_file_path}[/green]")
        
        console.print()
        
        # Check for files that need updates based on git changes
        console.print("📝 Checking for files needing updates...")
        changed_files = get_changed_files()
        
        if changed_files:
            needs_update = []
            
            for lore_file_path, tracked_files in mapping.items():
                # Check if any tracked files for this lore file have changed
                changed_tracked = [f for f in tracked_files if f in changed_files]
                if changed_tracked:
                    full_path = lore_path / lore_file_path
                    if full_path.exists():
                        # Check if lore file is also changed (updated)
                        lore_relative = str(Path(lore_root) / lore_file_path)
                        if lore_relative not in changed_files:
                            needs_update.append((lore_file_path, changed_tracked))
                            console.print(f"  ⚠️ [yellow]NEEDS UPDATE: {lore_root}/{lore_file_path}[/yellow]")
                            console.print(f"     [dim]Changed files: {', '.join(changed_tracked)}[/dim]")
                        else:
                            console.print(f"  ✅ [green]UPDATED: {lore_root}/{lore_file_path}[/green]")
                            console.print(f"     [dim]Both code and docs updated: {', '.join(changed_tracked)}[/dim]")
            
            if not any([missing_files, template_files, invalid_files, needs_update]):
                console.print("  ✅ [green]All documentation is up to date[/green]")
        else:
            console.print("  [dim]No changed files detected[/dim]")
        
        console.print()
        
        # Summary and validation result
        has_errors = bool(missing_files or template_files or invalid_files)
        has_warnings = bool(changed_files and any(lore_file for lore_file, _ in mapping.items() 
                                                if any(f in changed_files for f in mapping[lore_file])))
        
        if has_errors:
            console.print("❌ [bold red]VALIDATION FAILED[/bold red]")
            console.print()
            
            if missing_files:
                console.print("[red]MISSING FILES:[/red]")
                for lore_file, tracked_files in missing_files:
                    console.print(f"  → CREATE {lore_root}/{lore_file}")
                    console.print(f"    [dim]Run: dm create_lore {lore_file}[/dim]")
                console.print()
            
            if template_files:
                console.print("[yellow]TEMPLATE FILES (NEED COMPLETION):[/yellow]")
                for lore_file, tracked_files, validation in template_files:
                    console.print(f"  → COMPLETE {lore_root}/{lore_file}")
                    console.print(f"    [dim]Fill out placeholder sections with actual documentation[/dim]")
                console.print()
            
            if invalid_files:
                console.print("[red]INCOMPLETE FILES:[/red]")
                for lore_file, tracked_files, validation in invalid_files:
                    console.print(f"  → FIX {lore_root}/{lore_file}")
                    console.print(f"    [dim]Add missing sections: {', '.join(validation['missing_sections'])}[/dim]")
                console.print()
            
            console.print("[bold]❗ COMMIT BLOCKED[/bold]")
            console.print("Fix the above issues before committing.")
            return False
        
        elif has_warnings:
            console.print("⚠️ [bold yellow]VALIDATION WARNING[/bold yellow]")
            console.print("Code changes detected but documentation may need updates.")
            console.print("Review your documentation before committing.")
            console.print()
            console.print("✅ [green]Commit allowed (with warnings)[/green]")
            return True
        
        else:
            console.print("✅ [bold green]VALIDATION PASSED[/bold green]")
            console.print("All documentation is properly maintained.")
            return True
            
    except Exception as e:
        console.print(f"❌ [red]Validation error: {e}[/red]")
        return False
