"""
Command-line interface for Dungeon Master.
"""

import argparse
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
        # Find all tracked files in the repository
        import os
        all_files = []
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and common build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist']]
            for file in files:
                file_path = os.path.join(root, file)
                if not file.startswith('.'):
                    all_files.append(file_path.replace('./', ''))
        
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
        # Find all tracked files
        import os
        all_files = []
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist']]
            for file in files:
                file_path = os.path.join(root, file)
                if not file.startswith('.'):
                    all_files.append(file_path.replace('./', ''))
        
        tracked_files = parse_tracked_files(all_files)
    
    if not tracked_files:
        print("No tracked files found.")
        return 0
    
    output_dir = ensure_output_directory()
    validation_status = get_validation_status(tracked_files, output_dir)
    blocking_issues = get_blocking_issues(validation_status)
    
    print("🔍 Context Documentation Validation")
    print("=" * 50)
    
    if not blocking_issues:
        print("✅ All context documents are complete and valid!")
        print("   Commits will not be blocked.")
        return 0
    else:
        print("❌ Issues found that would block commits:")
        for issue in blocking_issues:
            print(f"   • {issue}")
        
        print("\n📝 Use Cursor to complete the documentation:")
        for file_path, status in validation_status.items():
            if not status['valid']:
                print(f"   • dungeon_master/{status['context_doc']}")
        
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


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Dungeon Master: Context-tracking pre-commit tool for Cursor integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  dungeon_master init                    # Initialize in current repo
  dungeon_master update                  # Process all staged tracked files
  dungeon_master update file1.py file2.py  # Process specific files
  dungeon_master list                    # List staged tracked files
  dungeon_master list --all              # List all tracked files
  dungeon_master validate                # Check what would block commits
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