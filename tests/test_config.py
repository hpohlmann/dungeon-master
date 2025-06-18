"""
Tests for Dungeon Master Configuration System

This module contains comprehensive tests for configuration loading, saving,
validation, and integration with other system components.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Import the configuration module
from dungeon_master.utils.config import (
    DEFAULT_CONFIG,
    ConfigurationError,
    create_default_config,
    ensure_lore_directory_isolation,
    get_config_path,
    get_lore_directory,
    get_setting,
    get_template_content,
    is_test_environment,
    load_config,
    merge_config_with_args,
    save_config,
    update_setting,
    validate_config,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "version": "1.0.0",
        "enforceDocumentation": True,
        "loreDirectory": ".lore",
        "customTemplatePath": None,
        "requireDiagrams": True,
        "minSectionLength": 100,
        "verboseOutput": False,
        "requiredSections": ["Overview", "Functions/Components"],
    }


@pytest.fixture
def invalid_config():
    """Invalid configuration for testing validation."""
    return {
        "enforceDocumentation": "yes",  # Should be boolean
        "minSectionLength": -5,  # Should be positive
        "requiredSections": "not a list",  # Should be list
        "excludedDirectories": {"not": "a list"},  # Should be list
    }


class TestConfigurationBasics:
    """Test basic configuration operations."""

    def test_get_config_path_default(self):
        """Test getting default config path."""
        path = get_config_path()
        assert path == Path("dmconfig.json")

    def test_get_config_path_custom(self):
        """Test getting custom config path."""
        custom_path = "custom/config.json"
        path = get_config_path(custom_path)
        assert path == Path(custom_path)

    def test_load_config_defaults_when_no_file(self, temp_dir):
        """Test that default config is returned when no file exists."""
        config_path = temp_dir / "dmconfig.json"
        config = load_config(str(config_path))

        # Should return default configuration
        assert config == DEFAULT_CONFIG
        assert config["enforceDocumentation"] is True
        assert config["loreDirectory"] == ".lore"

    def test_load_config_from_file(self, temp_dir, sample_config):
        """Test loading configuration from file."""
        config_path = temp_dir / "dmconfig.json"

        # Create config file
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        config = load_config(str(config_path))

        # Should merge with defaults
        assert config["enforceDocumentation"] is True
        assert config["minSectionLength"] == 100  # From sample
        assert "excludedDirectories" in config  # From defaults

    def test_load_config_invalid_json(self, temp_dir):
        """Test error handling for invalid JSON."""
        config_path = temp_dir / "dmconfig.json"

        # Create invalid JSON file
        with open(config_path, "w") as f:
            f.write("{ invalid json }")

        with pytest.raises(ConfigurationError, match="Invalid JSON"):
            load_config(str(config_path))

    def test_load_config_not_dict(self, temp_dir):
        """Test error handling for non-dict JSON."""
        config_path = temp_dir / "dmconfig.json"

        # Create JSON array instead of object
        with open(config_path, "w") as f:
            json.dump(["not", "a", "dict"], f)

        with pytest.raises(ConfigurationError, match="must contain a JSON object"):
            load_config(str(config_path))

    def test_load_config_verbose_output(self, temp_dir, sample_config, capsys):
        """Test verbose output during config loading."""
        config_path = temp_dir / "dmconfig.json"

        # Create config file
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        load_config(str(config_path), verbose=True)

        captured = capsys.readouterr()
        assert "Loading configuration" in captured.out
        assert "custom settings" in captured.out


class TestConfigurationSaving:
    """Test configuration saving operations."""

    def test_save_config_basic(self, temp_dir, sample_config):
        """Test basic configuration saving."""
        config_path = temp_dir / "dmconfig.json"

        result = save_config(sample_config, str(config_path))

        assert result is True
        assert config_path.exists()

        # Verify content
        with open(config_path) as f:
            saved_config = json.load(f)

        assert saved_config["enforceDocumentation"] is True
        assert saved_config["minSectionLength"] == 100

    def test_save_config_creates_directory(self, temp_dir, sample_config):
        """Test that saving creates parent directories."""
        config_path = temp_dir / "nested" / "dir" / "dmconfig.json"

        result = save_config(sample_config, str(config_path))

        assert result is True
        assert config_path.exists()
        assert config_path.parent.exists()

    def test_save_config_filters_none_values(self, temp_dir):
        """Test that None values are filtered from saved config."""
        config_with_nones = {
            "enforceDocumentation": True,
            "customTemplatePath": None,
            "emptyList": [],
            "validSetting": "value",
        }

        config_path = temp_dir / "dmconfig.json"
        save_config(config_with_nones, str(config_path))

        # Load and check
        with open(config_path) as f:
            saved_config = json.load(f)

        assert "customTemplatePath" not in saved_config
        assert "emptyList" not in saved_config
        assert saved_config["validSetting"] == "value"

    def test_save_config_error_handling(self, temp_dir):
        """Test error handling during save."""
        # Try to save to a read-only directory (simulate permission error)
        config_path = temp_dir / "readonly" / "dmconfig.json"
        config_path.parent.mkdir()
        config_path.parent.chmod(0o444)  # Read-only

        try:
            result = save_config(DEFAULT_CONFIG, str(config_path))
            assert result is False
        finally:
            # Restore permissions for cleanup
            config_path.parent.chmod(0o755)


class TestConfigurationValidation:
    """Test configuration validation."""

    def test_validate_config_valid(self, sample_config):
        """Test validation of valid configuration."""
        errors = validate_config(sample_config)
        assert errors == []

    def test_validate_config_missing_required_keys(self):
        """Test validation with missing required keys."""
        incomplete_config = {"version": "1.0.0"}

        errors = validate_config(incomplete_config)

        assert len(errors) > 0
        assert any("loreDirectory" in error for error in errors)
        assert any("enforceDocumentation" in error for error in errors)

    def test_validate_config_invalid_types(self, invalid_config):
        """Test validation with invalid types."""
        errors = validate_config(invalid_config)

        assert len(errors) > 0
        assert any("must be a boolean" in error for error in errors)
        assert any("must be an integer" in error for error in errors)
        assert any("must be a list" in error for error in errors)

    def test_validate_config_numeric_ranges(self):
        """Test validation of numeric value ranges."""
        config = {
            "loreDirectory": ".lore",
            "enforceDocumentation": True,
            "requiredSections": ["test"],
            "minSectionLength": -1,  # Invalid
            "maxFileSize": 2**40,  # Too large
        }

        errors = validate_config(config)

        assert len(errors) >= 2
        assert any("minSectionLength" in error for error in errors)
        assert any("maxFileSize" in error for error in errors)

    def test_validate_config_custom_template_path(self, temp_dir):
        """Test validation with custom template path."""
        # Non-existent template path
        config = {
            "loreDirectory": ".lore",
            "enforceDocumentation": True,
            "requiredSections": ["test"],
            "customTemplatePath": str(temp_dir / "nonexistent.md"),
        }

        errors = validate_config(config)
        assert any("Custom template file not found" in error for error in errors)

        # Valid template path
        template_path = temp_dir / "template.md"
        template_path.write_text("# Template")
        config["customTemplatePath"] = str(template_path)

        errors = validate_config(config)
        assert not any("template" in error.lower() for error in errors)


class TestConfigurationUtilities:
    """Test configuration utility functions."""

    def test_create_default_config(self, temp_dir):
        """Test creating default configuration file."""
        config_path = temp_dir / "dmconfig.json"

        result = create_default_config(str(config_path), verbose=True)

        assert result is True
        assert config_path.exists()

        # Verify it's valid
        config = load_config(str(config_path))
        assert config["enforceDocumentation"] is True

    def test_create_default_config_exists(self, temp_dir):
        """Test creating default config when file already exists."""
        config_path = temp_dir / "dmconfig.json"
        config_path.write_text("{}")  # Create empty file

        result = create_default_config(str(config_path), verbose=True)

        assert result is True  # Should succeed without overwriting

    def test_get_setting_with_config(self, sample_config):
        """Test getting setting with provided config."""
        value = get_setting("minSectionLength", sample_config)
        assert value == 100

        # Test with default
        value = get_setting("nonexistent", sample_config, "default")
        assert value == "default"

    def test_get_setting_loads_config(self, temp_dir, sample_config):
        """Test getting setting loads config automatically."""
        config_path = temp_dir / "dmconfig.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        # Change to temp directory
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            value = get_setting("minSectionLength")
            assert value == 100
        finally:
            os.chdir(old_cwd)

    def test_update_setting(self, temp_dir, sample_config):
        """Test updating a specific setting."""
        config_path = temp_dir / "dmconfig.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        result = update_setting("minSectionLength", 200, str(config_path))

        assert result is True

        # Verify update
        updated_config = load_config(str(config_path))
        assert updated_config["minSectionLength"] == 200

    def test_update_setting_validation_failure(self, temp_dir, sample_config):
        """Test update setting with validation failure."""
        config_path = temp_dir / "dmconfig.json"
        with open(config_path, "w") as f:
            json.dump(sample_config, f)

        # Try to set invalid value
        result = update_setting("minSectionLength", -100, str(config_path))

        assert result is False


class TestTemplateIntegration:
    """Test integration with template system."""

    def test_get_template_content_default(self):
        """Test getting default template content."""
        with patch(
            "dungeon_master.core.template.get_default_template"
        ) as mock_template:
            mock_template.return_value = "# Default Template"

            content = get_template_content()

            assert content == "# Default Template"
            mock_template.assert_called_once()

    def test_get_template_content_custom(self, temp_dir):
        """Test getting custom template content."""
        template_path = temp_dir / "custom_template.md"
        template_content = "# Custom Template\n\nThis is custom."
        template_path.write_text(template_content)

        config = {"customTemplatePath": str(template_path)}

        content = get_template_content(config)
        assert content == template_content

    def test_get_template_content_custom_not_found(self):
        """Test error when custom template not found."""
        config = {"customTemplatePath": "/nonexistent/template.md"}

        with pytest.raises(ConfigurationError, match="Custom template file not found"):
            get_template_content(config)

    def test_get_template_content_custom_read_error(self, temp_dir):
        """Test error when custom template cannot be read."""
        template_path = temp_dir / "unreadable.md"
        template_path.write_bytes(b"\xff\xfe")  # Invalid UTF-8

        config = {"customTemplatePath": str(template_path)}

        with pytest.raises(ConfigurationError, match="Error reading custom template"):
            get_template_content(config)


class TestConfigMerging:
    """Test configuration merging with command-line arguments."""

    def test_merge_config_with_args_basic(self, sample_config):
        """Test basic config merging with args."""
        args = {"lore_dir": ".documentation", "verbose": True, "min_length": 150}

        merged = merge_config_with_args(sample_config, **args)

        assert merged["loreDirectory"] == ".documentation"
        assert merged["verboseOutput"] is True
        assert merged["minSectionLength"] == 150

        # Original should be unchanged
        assert sample_config["loreDirectory"] == ".lore"

    def test_merge_config_with_args_callable_mapping(self, sample_config):
        """Test config merging with callable mappings."""
        args = {"no_color": True}

        merged = merge_config_with_args(sample_config, **args)

        assert merged["colorOutput"] is False  # Inverted by callable

    def test_merge_config_with_args_none_values(self, sample_config):
        """Test config merging ignores None values."""
        args = {"lore_dir": None, "verbose": True, "min_length": None}

        merged = merge_config_with_args(sample_config, **args)

        assert merged["loreDirectory"] == ".lore"  # Unchanged
        assert merged["verboseOutput"] is True  # Changed
        assert merged["minSectionLength"] == 100  # Unchanged

    def test_merge_config_with_args_unknown_args(self, sample_config):
        """Test config merging ignores unknown arguments."""
        args = {"unknown_arg": "value", "verbose": True}

        merged = merge_config_with_args(sample_config, **args)

        assert "unknown_arg" not in merged
        assert merged["verboseOutput"] is True


class TestConfigurationErrorHandling:
    """Test error handling in configuration system."""

    def test_load_config_permission_error(self, temp_dir):
        """Test handling of permission errors during load."""
        config_path = temp_dir / "dmconfig.json"
        config_path.write_text('{"test": "value"}')
        config_path.chmod(0o000)  # No permissions

        try:
            with pytest.raises(
                ConfigurationError, match="Error reading configuration file"
            ):
                load_config(str(config_path))
        finally:
            # Restore permissions for cleanup
            config_path.chmod(0o644)

    def test_load_config_validation_errors(self, temp_dir, invalid_config):
        """Test handling of validation errors during load."""
        config_path = temp_dir / "dmconfig.json"
        with open(config_path, "w") as f:
            json.dump(invalid_config, f)

        with pytest.raises(ConfigurationError, match="Invalid configuration values"):
            load_config(str(config_path))

    def test_configuration_error_inheritance(self):
        """Test that ConfigurationError is properly defined."""
        error = ConfigurationError("test message")
        assert str(error) == "test message"
        assert isinstance(error, Exception)


class TestDefaultConfiguration:
    """Test the default configuration values."""

    def test_default_config_structure(self):
        """Test that default config has expected structure."""
        config = DEFAULT_CONFIG

        # Check essential keys exist
        essential_keys = [
            "version",
            "enforceDocumentation",
            "loreDirectory",
            "validateOnCommit",
            "requireDiagrams",
            "requiredSections",
        ]

        for key in essential_keys:
            assert key in config, f"Essential key '{key}' missing from default config"

    def test_default_config_types(self):
        """Test that default config values have correct types."""
        config = DEFAULT_CONFIG

        # Boolean settings
        bool_keys = ["enforceDocumentation", "validateOnCommit", "requireDiagrams"]
        for key in bool_keys:
            assert isinstance(config[key], bool), f"{key} should be boolean"

        # List settings
        list_keys = ["requiredSections", "excludedDirectories", "excludedFilePatterns"]
        for key in list_keys:
            assert isinstance(config[key], list), f"{key} should be list"

        # String settings
        string_keys = ["version", "loreDirectory", "encoding"]
        for key in string_keys:
            assert isinstance(config[key], str), f"{key} should be string"

    def test_default_config_values(self):
        """Test specific default configuration values."""
        config = DEFAULT_CONFIG

        assert config["loreDirectory"] == ".lore"
        assert config["enforceDocumentation"] is True
        assert config["encoding"] == "utf-8"
        assert ".git" in config["excludedDirectories"]
        assert "*.pyc" in config["excludedFilePatterns"]
        # Test that examples and tests are excluded by default
        assert "examples" in config["excludedDirectories"]
        assert "tests" in config["excludedDirectories"]


class TestEnvironmentDetection:
    """Test environment detection functionality."""

    def test_is_test_environment_pytest(self):
        """Test detection when running under pytest."""
        # This should be True since we're running under pytest
        assert is_test_environment() is True

    def test_is_test_environment_env_var(self):
        """Test detection via environment variable."""
        with patch.dict(os.environ, {"DM_TEST_MODE": "true"}):
            assert is_test_environment() is True

        with patch.dict(os.environ, {"DM_TEST_MODE": "false"}):
            # Still True because we're running under pytest
            assert is_test_environment() is True

    def test_get_lore_directory_test_mode(self):
        """Test lore directory in test mode."""
        # Should return .lore.dev when in test environment
        lore_dir = get_lore_directory()
        assert lore_dir == ".lore.dev"

    def test_get_lore_directory_production_mode(self):
        """Test lore directory in production mode."""
        # Mock to simulate production environment
        with patch(
            "dungeon_master.utils.config.is_test_environment", return_value=False
        ):
            lore_dir = get_lore_directory()
            assert lore_dir == ".lore"

    def test_get_lore_directory_with_config(self):
        """Test lore directory with custom config."""
        custom_config = {"loreDirectory": ".custom_lore"}

        # In production mode, should use config value
        with patch(
            "dungeon_master.utils.config.is_test_environment", return_value=False
        ):
            lore_dir = get_lore_directory(custom_config)
            assert lore_dir == ".custom_lore"

        # In test mode, should still return .lore.dev regardless of config
        lore_dir = get_lore_directory(custom_config)
        assert lore_dir == ".lore.dev"

    def test_ensure_lore_directory_isolation(self, temp_dir):
        """Test lore directory isolation setup."""
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Should create .lore.dev directory in test mode
            result = ensure_lore_directory_isolation()
            assert result is True

            lore_dev_path = temp_dir / ".lore.dev"
            assert lore_dev_path.exists()
            assert lore_dev_path.is_dir()
        finally:
            os.chdir(old_cwd)

    def test_ensure_lore_directory_isolation_gitignore(self, temp_dir):
        """Test that .lore.dev is added to .gitignore."""
        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Create initial .gitignore
            gitignore_path = temp_dir / ".gitignore"
            gitignore_path.write_text("# Initial content\n*.pyc\n")

            # Run isolation setup
            ensure_lore_directory_isolation()

            # Check that .lore.dev was added
            gitignore_content = gitignore_path.read_text()
            assert ".lore.dev/" in gitignore_content
            assert "*.pyc" in gitignore_content  # Original content preserved
        finally:
            os.chdir(old_cwd)


class TestEnvironmentIntegration:
    """Test integration between environment detection and other systems."""

    def test_template_system_uses_correct_directory(self, temp_dir):
        """Test that template system uses correct lore directory."""
        from dungeon_master.core.template import create_lore_file

        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # In test mode, should create in .lore.dev
            result = create_lore_file(lore_path="test.md", tracked_files=["test.py"])

            assert result is True

            # File should be created in .lore.dev, not .lore
            lore_dev_file = temp_dir / ".lore.dev" / "test.md"
            lore_file = temp_dir / ".lore" / "test.md"

            assert lore_dev_file.exists()
            assert not lore_file.exists()
        finally:
            os.chdir(old_cwd)

    def test_decorator_parser_respects_exclusions(self, temp_dir):
        """Test that decorator parser respects the new exclusion configuration."""
        from dungeon_master.core.decorator_parser import (
            scan_repository_for_lore_decorators,
        )

        old_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)

            # Create test files in various directories
            (temp_dir / "src").mkdir()
            (temp_dir / "examples").mkdir()
            (temp_dir / "tests").mkdir()

            # Create files with track_lore decorators
            src_file = temp_dir / "src" / "main.py"
            src_file.write_text('# track_lore("main.md")\ndef main(): pass')

            example_file = temp_dir / "examples" / "example.py"
            example_file.write_text('# track_lore("example.md")\ndef example(): pass')

            test_file = temp_dir / "tests" / "test.py"
            test_file.write_text('# track_lore("test.md")\ndef test(): pass')

            # Scan with default config (should exclude examples and tests)
            config = load_config()
            mapping = scan_repository_for_lore_decorators(
                repo_path=temp_dir, config=config
            )

            # Should only find src file, not examples or tests
            assert "main.md" in mapping
            assert "example.md" not in mapping
            assert "test.md" not in mapping
        finally:
            os.chdir(old_cwd)


if __name__ == "__main__":
    pytest.main([__file__])
