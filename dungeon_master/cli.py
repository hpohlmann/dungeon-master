# track_lore("cli/main-interface.md")
#!/usr/bin/env python3
"""
Dungeon Master CLI - Documentation enforcement system.

This module provides the main command-line interface for Dungeon Master,
a pre-commit hook system that enforces documentation updates alongside code changes.
"""

import sys

import click
from rich.console import Console

# Initialize rich console for formatted output
console = Console()


@click.group()
@click.version_option()
def main():
    """
    Dungeon Master - Documentation enforcement system.

    Dungeon Master is a lightweight pre-commit hook system designed to enforce
    documentation updates alongside code changes. It ensures documentation
    remains current with codebase changes by blocking commits when documentation
    isn't updated for modified files.
    """
    pass


@main.command()
def init():
    """Initialize Dungeon Master in the current repository.

    Creates the necessary directory structure, configuration files,
    and sets up the pre-commit hook to enforce documentation requirements.
    """
    from dungeon_master.commands.init import run_init

    success = run_init()
    if not success:
        sys.exit(1)


@main.command()
def validate():
    """Validate documentation for pre-commit hook.

    Core pre-commit hook functionality that verifies each tracked file
    has corresponding documentation and checks that changed tracked files
    have updated documentation. Blocks commits when validation fails.
    """
    from dungeon_master.commands.validate import run_validate

    success = run_validate()
    if not success:
        sys.exit(1)


@main.command()
@click.option(
    "--mark-reviewed",
    metavar="FILE",
    help="Mark a specific file as reviewed to bypass validation. "
    "USE WITH EXTREME CAUTION - only for truly minor changes that "
    "do not affect documented behavior.",
)
def review(mark_reviewed):
    """Review documentation status.

    Display documentation status using rich formatting. Shows which lore files
    require updates, identifies template-only documentation, and provides
    clear visualization of documentation needs.
    """
    from dungeon_master.commands.review import run_review

    success = run_review(mark_reviewed)
    if not success:
        sys.exit(1)


@main.command()
@click.argument("lore_file", required=False)
def create_lore(lore_file):
    """Create missing documentation files.

    Scans all track_lore decorators in the codebase and creates missing
    documentation files with the standard template. Creates any necessary
    subdirectories within the .lore/ directory.

    Args:
        lore_file: Optional specific lore file to create
    """
    from dungeon_master.commands.create_lore import run_create_lore

    success = run_create_lore(lore_file)
    if not success:
        sys.exit(1)


@main.command()
def map():
    """Generate a visual map of repository structure.

    Creates a file tree map showing relationships between source files
    and documentation. Saves the output as map.md in the .lore/ directory.
    """
    from dungeon_master.commands.map import run_map

    success = run_map()
    if not success:
        sys.exit(1)


# Command aliases for convenience
@main.command(name="dm")
@click.pass_context
def dm_alias(ctx):
    """Alias for the main command group."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def cli():
    """Entry point for the CLI when installed as a package."""
    main()


if __name__ == "__main__":
    main()
