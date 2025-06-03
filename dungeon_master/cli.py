# @track_context("cli.md")
"""
Command-line interface for Dungeon Master.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict

from . import (
    parse_tracked_files,
    generate_context_template,
    validate_context_document,
    ensure_output_directory,
    get_git_changes
)
from .updater import get_validation_status, get_blocking_issues
from .utils import write_file_content
from .change_detector import ChangeDetector


def _should_exclude_directory(dir_name: str) -> bool:
    """
    Check if a directory should be excluded from file walking.

    Args:
        dir_name: Directory name to check

    Returns:
        bool: True if directory should be excluded
    """
    # Hidden directories
    if dir_name.startswith('.'):
        return True

    # Common build and dependency directories
    build_dirs = {
        'node_modules', '__pycache__', 'build', 'dist', 'target',
        '.git', '.svn', '.hg', '.bzr',
        'bower_components', '.npm', '.yarn'
    }

    # Virtual environment directories (comprehensive list)
    venv_dirs = {
        'venv', 'env', 'virtualenv', 'pyenv', 'conda',
        '.venv', '.env', '.virtualenv', '.pyenv', '.conda',
        'ENV', 'env_name', 'venv_name'
    }

    # IDE and editor directories
    ide_dirs = {
        '.vscode', '.idea', '.eclipse', '.settings',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        '.coverage', '.tox', '.nox'
    }

    excluded_dirs = build_dirs | venv_dirs | ide_dirs

    return dir_name in excluded_dirs


def _get_all_project_files() -> List[str]:
    """
    Get all files in the current project, excluding virtual environments and build directories.

    Returns:
        List[str]: List of file paths relative to current directory
    """
    all_files = []
    for root, dirs, files in os.walk('.'):
        # Filter out excluded directories IN-PLACE to prevent walking into them
        dirs[:] = [d for d in dirs if not _should_exclude_directory(d)]

        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue

            file_path = os.path.join(root, file)
            # Normalize path and remove leading './'
            normalized_path = file_path.replace('./', '').replace('.\\', '')
            all_files.append(normalized_path)

    return all_files


def cmd_update(args) -> int:
    """
    Create templates or validate context documents for tracked files.

    Args:
        args: Command arguments

    Returns:
        int: Exit code
    """
    if args.files:
        # Update specific files
        tracked_files = parse_tracked_files(args.files)
    else:
        # Update all staged files
        staged_files, new_files = get_git_changes()
        all_files = list(set(staged_files + new_files))
        tracked_files = parse_tracked_files(all_files)

    if not tracked_files:
        print("No tracked files found.")
        return 0

    output_dir = ensure_output_directory()
    exit_code = 0

    for file_path, context_doc_name in tracked_files.items():
        context_doc_path = output_dir / context_doc_name
        print(f"Processing: {file_path} -> {context_doc_name}")

        try:
            if not context_doc_path.exists():
                # Create new template
                template_content = generate_context_template(file_path)
                if template_content:
                    success = write_file_content(str(context_doc_path), template_content)
                    if success:
                        print(f"  ✓ Created template {context_doc_name}")
                        print(f"    📝 Please use Cursor to complete the documentation")
                    else:
                        print(f"  ✗ Failed to create template {context_doc_name}")
                        exit_code = 1
                else:
                    print(f"  ✗ Failed to generate template for {context_doc_name}")
                    exit_code = 1
            else:
                # Validate existing document
                is_valid, issues = validate_context_document(str(context_doc_path))
                if is_valid:
                    print(f"  ✓ {context_doc_name} is complete and valid")
                else:
                    print(f"  ⚠️  {context_doc_name} needs completion:")
                    for issue in issues:
                        print(f"    • {issue}")
                    print(f"    📝 Please use Cursor to complete the documentation")
        except Exception as e:
            print(f"  ✗ Error: {e}")
            exit_code = 1

    return exit_code


def cmd_list(args) -> int:
    """
    List all tracked files and their context document status.

    Args:
        args: Command arguments

    Returns:
        int: Exit code
    """
    if args.all:
        # Find all tracked files in the repository (excluding venv and build dirs)
        all_files = _get_all_project_files()
        tracked_files = parse_tracked_files(all_files)
    else:
        # Only staged files
        staged_files, new_files = get_git_changes()
        all_files = list(set(staged_files + new_files))
        tracked_files = parse_tracked_files(all_files)

    if not tracked_files:
        print("No tracked files found.")
        return 0

    output_dir = ensure_output_directory()
    validation_status = get_validation_status(tracked_files, output_dir)

    print(f"Found {len(tracked_files)} tracked files:")
    print("=" * 70)

    for file_path, status in validation_status.items():
        context_doc_name = status['context_doc']

        print(f"📄 {file_path}")
        print(f"   📋 {context_doc_name}", end="")

        if not status['exists']:
            print(" (MISSING - template needed)")
        elif not status['valid']:
            print(" (INCOMPLETE - needs completion)")
            for issue in status['issues']:
                print(f"      • {issue}")
        else:
            print(" (✓ COMPLETE)")

        print()

    return 0


def cmd_validate(args) -> int:
    """
    Validate context documents and show what would block a commit.

    Args:
        args: Command arguments

    Returns:
        int: Exit code (0 if all valid, 1 if issues found)
    """
    if args.files:
        tracked_files = parse_tracked_files(args.files)
    else:
        # Find all tracked files (excluding venv and build dirs)
        all_files = _get_all_project_files()
        tracked_files = parse_tracked_files(all_files)

    if not tracked_files:
        print("No tracked files found.")
        return 0

    output_dir = ensure_output_directory()
    validation_status = get_validation_status(tracked_files, output_dir)

    # Check for significant changes
    from .updater import check_for_significant_changes
    significant_changes, changes_block = check_for_significant_changes(tracked_files)

    # Get blocking issues (including significant changes)
    blocking_issues = get_blocking_issues(validation_status, significant_changes)

    print("🔍 Context Documentation Validation")
    print("=" * 50)

    if significant_changes:
        print("\n🔄 Significant changes detected:")
        for change in significant_changes:
            print(f"\n   📄 {change.file_path}")
            for change_desc in change.changes:
                print(f"      • {change_desc}")

    if not blocking_issues:
        if significant_changes:
            print("\n⚠️  Significant changes detected but would not block commits.")
            print("   Consider running 'dm review' to manage these changes.")
        else:
            print("\n✅ All context documents are complete and valid!")
            print("   Commits will not be blocked.")
        return 0
    else:
        print("\n❌ Issues found that would block commits:")
        for issue in blocking_issues:
            print(f"   • {issue}")

        print("\n📝 Use Cursor to complete the documentation:")
        for file_path, status in validation_status.items():
            if not status['valid']:
                print(f"   • lore/{status['context_doc']}")

        if significant_changes:
            print("\n🔄 To resolve significant changes:")
            print("   • dm review --mark-reviewed")

        return 1


def cmd_init(args) -> int:
    """
    Initialize Dungeon Master in the current repository.

    Args:
        args: Command arguments

    Returns:
        int: Exit code
    """
    # Create output directory
    output_dir = ensure_output_directory()
    print(f"✓ Created output directory: {output_dir}")

    # Create a sample pre-commit config if it doesn't exist
    precommit_config = Path('.pre-commit-config.yaml')
    if not precommit_config.exists():
        config_content = """repos:
  - repo: local
    hooks:
      - id: dungeon-master
        name: Dungeon Master Context Tracking
        entry: python hooks/pre_commit_hook.py
        language: system
        pass_filenames: false
        always_run: true
"""
        with open(precommit_config, 'w') as f:
            f.write(config_content)
        print(f"✓ Created pre-commit config: {precommit_config}")
    else:
        print(f"ℹ Pre-commit config already exists: {precommit_config}")

    print("\n🎯 Dungeon Master initialization complete!")
    print("\nThis system creates a structured integration point where Cursor")
    print("collaborates with you to maintain repository documentation.")
    print("\n📝 To start tracking a file, add this comment at the top:")
    print('# @track_context("my_context_doc.md")')
    print("\n🛡️  When you commit tracked files:")
    print("   • Templates are created for new tracked files")
    print("   • Commits are blocked until templates are completed")
    print("   • Use Cursor to fill in the documentation")
    print("   • Commits proceed once documentation is complete")

    return 0


def cmd_review(args) -> int:
    """
    Mark significant changes as reviewed, allowing commits to proceed.

    Args:
        args: Command arguments

    Returns:
        int: Exit code
    """
    if args.files:
        tracked_files = parse_tracked_files(args.files)
        file_paths = args.files
    else:
        # Find all tracked files (excluding venv and build dirs)
        all_files = _get_all_project_files()
        tracked_files = parse_tracked_files(all_files)
        file_paths = list(tracked_files.keys())

    if not tracked_files:
        print("No tracked files found.")
        return 0

    # Check for significant changes
    detector = ChangeDetector()
    significant_changes = detector.get_significant_changes(file_paths)

    if not significant_changes:
        print("✅ No significant changes detected that require review.")
        return 0

    print("🔍 Significant changes detected:")
    print("=" * 50)

    for change in significant_changes:
        print(f"\n📄 {change.file_path}")
        for change_desc in change.changes:
            print(f"   • {change_desc}")

    if args.mark_reviewed:
        # Mark as reviewed without prompting
        detector.mark_as_reviewed(file_paths)
        print(f"\n✅ Marked {len(significant_changes)} file(s) as reviewed.")
        print("   Future commits will proceed unless new significant changes are made.")
        return 0
    else:
        print(f"\n📝 To allow commits to proceed, mark these changes as reviewed:")
        print(f"   dm review --mark-reviewed")
        print(f"\n💡 Update documentation if changes affect core functionality, OR")
        print(f"   mark as reviewed if changes are minor/cosmetic:")
        print(f"")
        print(f"   🔍 REVIEW REQUIRED if changes affect:")
        print(f"      • Core logic or system behavior")
        print(f"      • API interfaces or function signatures")
        print(f"      • Critical functionality or user workflows")
        print(f"")
        print(f"   ✅ SAFE TO MARK REVIEWED if changes are:")
        print(f"      • Formatting, comments, or documentation")
        print(f"      • Minor bug fixes without behavior changes")
        print(f"      • Refactoring that doesn't change functionality")
        return 1


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Dungeon Master: Context-tracking pre-commit tool for Cursor integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dm init                    # Initialize in current repo
  dm update                  # Process all staged tracked files
  dm update file1.py file2.py  # Process specific files
  dm list                    # List staged tracked files
  dm list --all              # List all tracked files
  dm validate                # Check what would block commits
  dm review                  # Check for significant changes
  dm review --mark-reviewed  # Mark changes as reviewed
"""
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Update command
    update_parser = subparsers.add_parser('update', help='Create templates or validate context documents')
    update_parser.add_argument('files', nargs='*', help='Specific files to process')
    update_parser.set_defaults(func=cmd_update)

    # List command
    list_parser = subparsers.add_parser('list', help='List tracked files and their status')
    list_parser.add_argument('--all', action='store_true', help='List all tracked files, not just staged')
    list_parser.set_defaults(func=cmd_list)

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate context documents')
    validate_parser.add_argument('files', nargs='*', help='Specific files to validate')
    validate_parser.set_defaults(func=cmd_validate)

    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize Dungeon Master')
    init_parser.set_defaults(func=cmd_init)

    # Review command
    review_parser = subparsers.add_parser('review', help='Review significant changes in tracked files')
    review_parser.add_argument('files', nargs='*', help='Specific files to review')
    review_parser.add_argument('--mark-reviewed', action='store_true', help='Mark changes as reviewed')
    review_parser.set_defaults(func=cmd_review)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
