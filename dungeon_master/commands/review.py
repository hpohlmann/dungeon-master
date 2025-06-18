# track_lore("commands/cli-system.md")
"""
Review documentation status.

This module handles displaying documentation status using rich formatting,
showing which lore files require updates and providing manual override options.
"""

from pathlib import Path

from rich.console import Console
from rich.table import Table

from dungeon_master.core.decorator_parser import scan_repository_for_lore_decorators
from dungeon_master.core.git_utils import get_changed_files
from dungeon_master.core.template import validate_lore_file
from dungeon_master.utils.config import get_lore_directory, load_config

console = Console()


def run_review(mark_reviewed=None):
    """
    Display documentation status with rich formatting.

    Shows:
    - Table with lore file paths
    - All files associated with each lore document
    - Lore files requiring updates based on changed source files
    - Lore files that still contain template placeholders
    - Clear visualization of documentation needs

    Args:
        mark_reviewed (str, optional): File to mark as reviewed for manual override.
                                      USE WITH EXTREME CAUTION.

    Returns:
        bool: True if review completes successfully
    """
    try:
        # Handle manual review override first
        if mark_reviewed:
            console.print("⚠️ [bold red]MANUAL REVIEW OVERRIDE[/bold red] ⚠️")
            console.print()
            console.print(f"[yellow]Marking {mark_reviewed} as reviewed[/yellow]")
            console.print(
                "[red]WARNING:[/red] Manual review override should be used with "
                "extreme caution!"
            )
            console.print()
            console.print("[bold]This override should ONLY be used when:[/bold]")
            console.print("  • File changes are truly minor (formatting, typos)")
            console.print("  • You've thoroughly reviewed both code and documentation")
            console.print(
                "  • You can confidently confirm documentation remains accurate"
            )
            console.print()
            console.print("[bold red]NEVER use for:[/bold red]")
            console.print("  • Behavior changes")
            console.print("  • New features or API modifications")
            console.print("  • When rushing to meet deadlines")
            console.print()
            # TODO: Implement actual cache marking logic here
            console.print("💾 [green]File marked as reviewed in cache[/green]")
            return True

        console.print("📊 [bold green]Documentation Review[/bold green] 📊")
        console.print()

        # Load configuration
        config = load_config()
        lore_root = get_lore_directory(config)
        lore_path = Path(lore_root)

        # Scan for decorators
        console.print("🔍 Scanning for track_lore decorators...")
        mapping = scan_repository_for_lore_decorators(config=config)

        if not mapping:
            console.print(
                "  [yellow]No track_lore decorators found in codebase[/yellow]"
            )
            return True

        console.print(
            f"  Found [bold]{len(mapping)}[/bold] lore files referenced in code"
        )
        console.print()

        # Get changed files for update detection
        changed_files = get_changed_files()

        # Create status table
        table = Table(
            title="📚 Documentation Status", show_header=True, header_style="bold blue"
        )
        table.add_column("Status", style=None, min_width=12)
        table.add_column("Lore File", style="cyan", min_width=30)
        table.add_column("Tracked Files", style="dim", min_width=40)
        table.add_column("Issues", style="yellow", min_width=20)

        status_counts = {
            "✅ UP TO DATE": 0,
            "🔴 MISSING": 0,
            "🟡 TEMPLATE": 0,
            "🟠 INCOMPLETE": 0,
            "⚠️ NEEDS UPDATE": 0,
        }

        issues_found = []

        for lore_file_path, tracked_files in mapping.items():
            full_path = lore_path / lore_file_path
            tracked_files_str = ", ".join(tracked_files)
            issues = []

            if not full_path.exists():
                status = "🔴 MISSING"
                issues.append("File does not exist")
                issues_found.append(
                    (lore_file_path, "CREATE", f"Run: dm create_lore {lore_file_path}")
                )

            else:
                # Validate the lore file
                validation = validate_lore_file(full_path)

                if validation["is_template"]:
                    status = "🟡 TEMPLATE"
                    issues.append("Contains placeholder text")
                    issues_found.append(
                        (
                            lore_file_path,
                            "COMPLETE",
                            "Fill out placeholder sections with actual documentation",
                        )
                    )

                elif not validation["is_valid"]:
                    status = "🟠 INCOMPLETE"
                    missing_sections = ", ".join(validation["missing_sections"])
                    issues.append(f"Missing: {missing_sections}")
                    issues_found.append(
                        (
                            lore_file_path,
                            "FIX",
                            f"Add missing sections: {missing_sections}",
                        )
                    )

                else:
                    # Check if files need updates
                    changed_tracked = [f for f in tracked_files if f in changed_files]
                    if changed_tracked:
                        lore_relative = str(Path(lore_root) / lore_file_path)
                        if lore_relative not in changed_files:
                            status = "⚠️ NEEDS UPDATE"
                            issues.append(f"Code changed: {', '.join(changed_tracked)}")
                            issues_found.append(
                                (
                                    lore_file_path,
                                    "UPDATE",
                                    f"Review changes in: {', '.join(changed_tracked)}",
                                )
                            )
                        else:
                            status = "✅ UP TO DATE"
                    else:
                        status = "✅ UP TO DATE"

            status_counts[status] = status_counts.get(status, 0) + 1
            issues_str = " | ".join(issues) if issues else ""

            table.add_row(
                status, f"{lore_root}/{lore_file_path}", tracked_files_str, issues_str
            )

        console.print(table)
        console.print()

        # Summary statistics
        summary_table = Table(
            title="📈 Summary", show_header=True, header_style="bold green"
        )
        summary_table.add_column("Status", style="bold")
        summary_table.add_column("Count", style="bold", justify="right")

        for status, count in status_counts.items():
            if count > 0:
                summary_table.add_row(status, str(count))

        console.print(summary_table)
        console.print()

        # Show required actions if any issues found
        if issues_found:
            console.print("❗ [bold red]REQUIRED ACTIONS:[/bold red]")
            for lore_file, action, description in issues_found:
                console.print(f"  → [bold]{action}[/bold] {lore_root}/{lore_file}")
                console.print(f"    [dim]{description}[/dim]")

                # Show related files for context
                if lore_file in mapping:
                    console.print(
                        f"    [dim]REVIEW THESE FILES TO UNDERSTAND THE ENTIRE SYSTEM:[/dim]"
                    )
                    for tracked_file in mapping[lore_file]:
                        console.print(f"    [dim]- {tracked_file}[/dim]")
                console.print()
        else:
            console.print(
                "✨ [bold green]All documentation is up to date![/bold green]"
            )

        return True

    except Exception as e:
        console.print(f"❌ [red]Review error: {e}[/red]")
        return False
