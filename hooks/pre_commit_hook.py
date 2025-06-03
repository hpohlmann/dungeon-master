#!/usr/bin/env python3
# @track_context("pre_commit_hook.md")
"""
Pre-commit hook for Dungeon Master context tracking.

This script runs the core Dungeon Master workflow to enforce context documentation:
1. dm update - Create templates and update documentation
2. dm review - Check for significant changes needing review
3. dm validate - Validate that all documentation is complete

If any command fails, the commit is blocked with clear guidance.
"""

import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def run_dm_command(command_args: list[str]) -> tuple[int, str, str]:
    """
    Run a Dungeon Master CLI command and return the result.

    Args:
        command_args: List of command arguments (e.g., ['dm', 'update'])

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            timeout=30  # Prevent hanging
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 30 seconds"
    except Exception as e:
        return 1, "", f"Failed to run command: {e}"


def print_command_output(command: str, stdout: str, stderr: str):
    """Print the output from a command for user visibility."""
    if stdout.strip():
        print(stdout.strip())
    if stderr.strip():
        print(stderr.strip())


def main() -> int:
    """
    Main entry point for the pre-commit hook.

    Runs the core Dungeon Master workflow:
    1. dm update - Create/update templates and documentation
    2. dm review - Check for significant changes
    3. dm validate - Validate documentation completeness

    Returns:
        int: Exit code (0 for success, non-zero to block commit)
    """
    print("🏰 Dungeon Master: Enforcing context documentation...")

    # Step 1: Update documentation (create templates, update changelogs)
    print("\n📝 Step 1: Updating documentation...")
    exit_code, stdout, stderr = run_dm_command(['dm', 'update'])
    print_command_output('dm update', stdout, stderr)

    if exit_code != 0:
        print(f"\n❌ 'dm update' failed with exit code {exit_code}")
        print("Fix the issues above and try committing again.")
        return exit_code

    # Step 2: Review significant changes
    print("\n🔄 Step 2: Checking for significant changes...")
    exit_code, stdout, stderr = run_dm_command(['dm', 'review'])
    print_command_output('dm review', stdout, stderr)

    if exit_code != 0:
        print(f"\n❌ 'dm review' detected significant changes requiring attention")
        print("Review and update documentation, then run 'dm review --mark-reviewed'")
        print("\n💡 Note: If changes are minor (formatting, comments, small fixes),")
        print("   you can run 'dm review --mark-reviewed' to proceed without updating docs.")
        return exit_code

    # Step 3: Validate all documentation
    print("\n✅ Step 3: Validating documentation...")
    exit_code, stdout, stderr = run_dm_command(['dm', 'validate'])
    print_command_output('dm validate', stdout, stderr)

    if exit_code != 0:
        print(f"\n❌ 'dm validate' found incomplete documentation")
        print("Complete the templates and try committing again.")
        return exit_code

    print("\n🎯 All Dungeon Master checks passed! Commit proceeding...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
