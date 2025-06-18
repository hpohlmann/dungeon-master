# track_lore("commands/cli-system.md")
"""
Create missing documentation files.

This module handles creating missing documentation files based on track_lore
decorators found in the codebase, with the standard template.
"""

from pathlib import Path
from rich.console import Console
from rich.table import Table

from dungeon_master.core.decorator_parser import scan_repository_for_lore_decorators
from dungeon_master.core.template import create_multiple_lore_files
from dungeon_master.utils.config import load_config, get_lore_directory

console = Console()


def run_create_lore(lore_file=None):
    """
    Create missing documentation files.

    Scans all track_lore decorators in codebase and creates missing
    documentation files with the standard template. Creates any necessary
    subdirectories within .lore/ directory.

    Args:
        lore_file (str, optional): Specific lore file to create.
                                  If None, scans for all missing files.

    Returns:
        bool: True if files created successfully
    """
    try:
        console.print("🔮 [bold green]Creating Lore Files[/bold green] 🔮")
        console.print()
        
        # Load configuration
        config = load_config()
        lore_root = get_lore_directory(config)
        lore_path = Path(lore_root)
        
        # Scan for decorators
        console.print("🔍 Scanning for track_lore decorators...")
        mapping = scan_repository_for_lore_decorators(config=config)
        
        if not mapping:
            console.print("  [yellow]No track_lore decorators found in codebase[/yellow]")
            return True
            
        console.print(f"  Found [bold]{len(mapping)}[/bold] unique lore files referenced in code")
        console.print()
        
        # Filter to specific file if requested
        if lore_file:
            if lore_file in mapping:
                mapping = {lore_file: mapping[lore_file]}
            else:
                console.print(f"❌ [red]Lore file '{lore_file}' not found in any track_lore decorators[/red]")
                return False
        
        # Check which files already exist
        console.print("📝 Checking documentation status...")
        existing = []
        missing = []
        
        for lore_file_path in mapping.keys():
            full_path = lore_path / lore_file_path
            if full_path.exists():
                existing.append(lore_file_path)
                console.print(f"  ✅ [cyan]{lore_root}/{lore_file_path}[/cyan] (exists)")
            else:
                missing.append(lore_file_path)
                console.print(f"  ❌ [cyan]{lore_root}/{lore_file_path}[/cyan] (missing)")
        
        if not missing:
            console.print("✨ [bold green]All lore files already exist![/bold green]")
            return True
            
        console.print()
        
        # Create necessary directories
        console.print("📁 Creating necessary directories...")
        dirs_created = set()
        for lore_file_path in missing:
            parent_dir = (lore_path / lore_file_path).parent
            if parent_dir != lore_path and not parent_dir.exists():
                parent_dir.mkdir(parents=True, exist_ok=True)
                # Display just the created directory name, not the full path
                rel_parts = parent_dir.parts[len(lore_path.parts):]
                if rel_parts:
                    dir_display = f"{lore_root}/" + "/".join(rel_parts) + "/"
                    if dir_display not in dirs_created:
                        console.print(f"  ✅ Created [cyan]{dir_display}[/cyan] directory")
                        dirs_created.add(dir_display)
        
        console.print()
        
        # Create missing lore files
        console.print("📑 Creating missing lore files with templates...")
        
        missing_mapping = {lore_file: mapping[lore_file] for lore_file in missing}
        results = create_multiple_lore_files(
            lore_mapping=missing_mapping,
            lore_root=lore_root
        )
        
        # Report results
        success_count = 0
        for lore_file_path, success in results.items():
            if success:
                console.print(f"  ✅ Created [cyan]{lore_root}/{lore_file_path}[/cyan] with documentation template")
                success_count += 1
            else:
                console.print(f"  ❌ [red]Failed to create {lore_root}/{lore_file_path}[/red]")
        
        console.print()
        
        if success_count == len(missing):
            console.print("✨ [bold green]Complete![/bold green] All lore files are now created.")
            console.print("⚠️ [bold yellow]WARNING:[/bold yellow] FILL OUT ALL TEMPLATES WITH ACTUAL DOCUMENTATION BEFORE COMMITTING.")
            return True
        else:
            console.print(f"⚠️ [yellow]Partial success: {success_count}/{len(missing)} files created[/yellow]")
            return False
            
    except Exception as e:
        console.print(f"❌ [red]Error creating lore files: {e}[/red]")
        return False
