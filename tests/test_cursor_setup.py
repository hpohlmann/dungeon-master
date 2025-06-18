"""
Unit tests for the Cursor rules setup functionality.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from dungeon_master.utils.cursor_setup import (
    CURSOR_RULE_FILES,
    copy_rule_file,
    create_cursor_rules_directory,
    get_templates_directory,
    remove_cursor_rules,
    setup_cursor_rules,
    verify_cursor_rules_setup,
)


class TestTemplatesDirectory:
    """Test templates directory detection."""

    def test_get_templates_directory_exists(self):
        """Test getting templates directory when it exists."""
        # This should work in the actual project structure
        try:
            templates_dir = get_templates_directory()
            assert templates_dir.exists()
            assert templates_dir.name == "cursor_rules"
            assert (templates_dir / "dungeon_master_workflow.mdc").exists()
        except FileNotFoundError:
            # Skip if running in isolated test environment
            pytest.skip("Templates directory not found in test environment")

    def test_get_templates_directory_not_found(self):
        """Test error handling when templates directory doesn't exist."""
        # We'll patch the exists method of the final templates directory path
        with patch.object(Path, 'exists', return_value=False):
            with pytest.raises(
                FileNotFoundError, match="Templates directory not found"
            ):
                get_templates_directory()


class TestCursorRulesDirectory:
    """Test cursor rules directory creation."""

    def test_create_cursor_rules_directory_new(self):
        """Test creating a new cursor rules directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            rules_dir = temp_path / ".cursor" / "rules"

            result = create_cursor_rules_directory(str(rules_dir))

            assert result == rules_dir
            assert rules_dir.exists()
            assert rules_dir.is_dir()

    def test_create_cursor_rules_directory_exists(self):
        """Test creating cursor rules directory when it already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            rules_dir = temp_path / ".cursor" / "rules"
            rules_dir.mkdir(parents=True)

            result = create_cursor_rules_directory(str(rules_dir))

            assert result == rules_dir
            assert rules_dir.exists()

    def test_create_cursor_rules_directory_permission_error(self):
        """Test error handling when directory creation fails."""
        # Try to create in a path that should fail (like root)
        with pytest.raises(OSError):
            create_cursor_rules_directory("/root/.cursor/rules")


class TestCopyRuleFile:
    """Test individual rule file copying."""

    def test_copy_rule_file_success(self):
        """Test successful rule file copying."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create source file
            source_dir = temp_path / "source"
            source_dir.mkdir()
            source_file = source_dir / "test.mdc"
            source_file.write_text("# Test Rule\n\nTest content")

            # Create destination directory
            dest_dir = temp_path / "dest"
            dest_dir.mkdir()

            # Copy file
            with patch("dungeon_master.utils.cursor_setup.console"):
                result = copy_rule_file("test.mdc", source_dir, dest_dir)

            assert result is True
            dest_file = dest_dir / "test.mdc"
            assert dest_file.exists()
            assert dest_file.read_text() == "# Test Rule\n\nTest content"

    def test_copy_rule_file_source_not_found(self):
        """Test copying when source file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            source_dir = temp_path / "source"
            source_dir.mkdir()
            dest_dir = temp_path / "dest"
            dest_dir.mkdir()

            with patch("dungeon_master.utils.cursor_setup.console"):
                result = copy_rule_file("nonexistent.mdc", source_dir, dest_dir)

            assert result is False

    def test_copy_rule_file_no_overwrite(self):
        """Test copying when destination exists and overwrite is False."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create source and destination files
            source_dir = temp_path / "source"
            source_dir.mkdir()
            source_file = source_dir / "test.mdc"
            source_file.write_text("Source content")

            dest_dir = temp_path / "dest"
            dest_dir.mkdir()
            dest_file = dest_dir / "test.mdc"
            dest_file.write_text("Existing content")

            # Try to copy without overwrite
            with patch("dungeon_master.utils.cursor_setup.console"):
                result = copy_rule_file(
                    "test.mdc", source_dir, dest_dir, overwrite=False
                )

            assert result is False
            assert dest_file.read_text() == "Existing content"

    def test_copy_rule_file_with_overwrite(self):
        """Test copying when destination exists and overwrite is True."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create source and destination files
            source_dir = temp_path / "source"
            source_dir.mkdir()
            source_file = source_dir / "test.mdc"
            source_file.write_text("New content")

            dest_dir = temp_path / "dest"
            dest_dir.mkdir()
            dest_file = dest_dir / "test.mdc"
            dest_file.write_text("Old content")

            # Copy with overwrite
            with patch("dungeon_master.utils.cursor_setup.console"):
                result = copy_rule_file(
                    "test.mdc", source_dir, dest_dir, overwrite=True
                )

            assert result is True
            assert dest_file.read_text() == "New content"


class TestSetupCursorRules:
    """Test the main setup function."""

    def test_setup_cursor_rules_success(self):
        """Test successful cursor rules setup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create mock templates directory with rule files
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()
            for rule_file in CURSOR_RULE_FILES:
                (templates_dir / rule_file).write_text(f"# {rule_file}\n\nRule content")

            # Set up destination
            rules_dir = temp_path / ".cursor" / "rules"

            # Mock get_templates_directory to return our test directory
            with patch(
                "dungeon_master.utils.cursor_setup.get_templates_directory",
                return_value=templates_dir,
            ):
                with patch("dungeon_master.utils.cursor_setup.console"):
                    copied_files, failed_files = setup_cursor_rules(
                        str(rules_dir), verbose=False
                    )

            assert len(copied_files) == len(CURSOR_RULE_FILES)
            assert len(failed_files) == 0

            # Verify all files were copied
            for rule_file in CURSOR_RULE_FILES:
                dest_file = rules_dir / rule_file
                assert dest_file.exists()
                assert f"# {rule_file}" in dest_file.read_text()

    def test_setup_cursor_rules_templates_not_found(self):
        """Test setup when templates directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_dir = Path(temp_dir) / ".cursor" / "rules"

            with patch(
                "dungeon_master.utils.cursor_setup.get_templates_directory",
                side_effect=FileNotFoundError("Templates not found"),
            ):
                with patch("dungeon_master.utils.cursor_setup.console"):
                    with pytest.raises(FileNotFoundError):
                        setup_cursor_rules(str(rules_dir), verbose=False)

    def test_setup_cursor_rules_partial_failure(self):
        """Test setup with some files missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create templates directory with only some rule files
            templates_dir = temp_path / "templates"
            templates_dir.mkdir()

            # Only create the first two rule files
            for rule_file in CURSOR_RULE_FILES[:2]:
                (templates_dir / rule_file).write_text(f"# {rule_file}\n\nRule content")

            rules_dir = temp_path / ".cursor" / "rules"

            with patch(
                "dungeon_master.utils.cursor_setup.get_templates_directory",
                return_value=templates_dir,
            ):
                with patch("dungeon_master.utils.cursor_setup.console"):
                    copied_files, failed_files = setup_cursor_rules(
                        str(rules_dir), verbose=False
                    )

            assert len(copied_files) == 2
            assert len(failed_files) == 2


class TestVerifyCursorRulesSetup:
    """Test cursor rules verification."""

    def test_verify_cursor_rules_setup_all_present(self):
        """Test verification when all files are present."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            rules_dir = temp_path / ".cursor" / "rules"
            rules_dir.mkdir(parents=True)

            # Create all rule files
            for rule_file in CURSOR_RULE_FILES:
                (rules_dir / rule_file).write_text("Rule content")

            present_files, missing_files = verify_cursor_rules_setup(str(rules_dir))

            assert len(present_files) == len(CURSOR_RULE_FILES)
            assert len(missing_files) == 0
            assert set(present_files) == set(CURSOR_RULE_FILES)

    def test_verify_cursor_rules_setup_some_missing(self):
        """Test verification when some files are missing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            rules_dir = temp_path / ".cursor" / "rules"
            rules_dir.mkdir(parents=True)

            # Create only half the rule files
            present_rule_files = CURSOR_RULE_FILES[:2]
            for rule_file in present_rule_files:
                (rules_dir / rule_file).write_text("Rule content")

            present_files, missing_files = verify_cursor_rules_setup(str(rules_dir))

            assert len(present_files) == 2
            assert len(missing_files) == 2
            assert set(present_files) == set(present_rule_files)
            assert set(missing_files) == set(CURSOR_RULE_FILES[2:])

    def test_verify_cursor_rules_setup_directory_not_exist(self):
        """Test verification when rules directory doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_dir = Path(temp_dir) / "nonexistent" / ".cursor" / "rules"

            present_files, missing_files = verify_cursor_rules_setup(str(rules_dir))

            assert len(present_files) == 0
            assert len(missing_files) == len(CURSOR_RULE_FILES)
            assert set(missing_files) == set(CURSOR_RULE_FILES)


class TestRemoveCursorRules:
    """Test cursor rules removal."""

    def test_remove_cursor_rules_success(self):
        """Test successful removal of cursor rules."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            rules_dir = temp_path / ".cursor" / "rules"
            rules_dir.mkdir(parents=True)

            # Create rule files
            rule_paths = []
            for rule_file in CURSOR_RULE_FILES:
                rule_path = rules_dir / rule_file
                rule_path.write_text("Rule content")
                rule_paths.append(rule_path)

            # Verify files exist
            for rule_path in rule_paths:
                assert rule_path.exists()

            # Remove rules
            with patch("dungeon_master.utils.cursor_setup.console"):
                result = remove_cursor_rules(str(rules_dir), verbose=False)

            assert result is True

            # Verify files are removed
            for rule_path in rule_paths:
                assert not rule_path.exists()

    def test_remove_cursor_rules_no_files(self):
        """Test removal when no rule files exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            rules_dir = Path(temp_dir) / ".cursor" / "rules"

            with patch("dungeon_master.utils.cursor_setup.console"):
                result = remove_cursor_rules(str(rules_dir), verbose=False)

            # Should still return True (success) even if no files to remove
            assert result is True
