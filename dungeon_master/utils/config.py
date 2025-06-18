# track_lore("core/configuration.md")
"""
Configuration System for Dungeon Master

This module provides functionality to load, save, and manage configuration
for Dungeon Master using dmconfig.json with sensible defaults and validation.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from rich.console import Console

console = Console()

# Default configuration with comprehensive settings
DEFAULT_CONFIG = {
    # Core settings
    "version": "1.0.0",
    "enforceDocumentation": True,
    "loreDirectory": ".lore",
    "validateOnCommit": True,
    # Template settings
    "customTemplatePath": None,  # Use built-in template if None
    "requireDiagrams": True,
    "requiredSections": ["Overview", "Functions/Components", "Diagrams"],
    # Validation settings
    "minSectionLength": 50,
    "validatePlaceholders": True,
    "validateDiagramContent": True,
    "allowEmptyExamples": False,
    # Directory settings
    "cursorRulesDirectory": ".cursor/rules",
    "cacheFile": "dmcache.json",
    "configFile": "dmconfig.json",
    # Exclusion patterns
    "excludedDirectories": [
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "node_modules",
        ".next",
        ".nuxt",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        ".build",
        ".taskmaster",
        "examples",  # Exclude example files from production documentation
        "tests",  # Exclude test files from production documentation
    ],
    "excludedFilePatterns": [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.dll",
        "*.dylib",
        "*.egg-info",
        "*.dist-info",
        ".DS_Store",
        "Thumbs.db",
    ],
    # Hook settings
    "preCommitEnabled": True,
    "preCommitScript": "dm validate",
    # Output settings
    "verboseOutput": False,
    "colorOutput": True,
    "showProgressBars": True,
    # Advanced settings
    "maxFileSize": 10485760,  # 10MB in bytes
    "encoding": "utf-8",
    "gitIgnoreCacheFile": True,
}

# Configuration file name
CONFIG_FILE = "dmconfig.json"


class ConfigurationError(Exception):
    """Raised when there's an error with configuration loading or validation."""

    pass


def get_config_path(config_file: Optional[str] = None) -> Path:
    """
    Get the path to the configuration file.

    Args:
        config_file: Optional custom config file path

    Returns:
        Path to the configuration file
    """
    if config_file:
        return Path(config_file)
    return Path(CONFIG_FILE)


def load_config(
    config_file: Optional[str] = None, verbose: bool = False
) -> Dict[str, Any]:
    """
    Load configuration from dmconfig.json, using defaults for missing values.

    Args:
        config_file: Optional path to config file (defaults to dmconfig.json)
        verbose: Whether to print loading information

    Returns:
        Dictionary containing configuration settings

    Raises:
        ConfigurationError: If config file exists but is invalid
    """
    config = DEFAULT_CONFIG.copy()
    config_path = get_config_path(config_file)

    if verbose:
        console.print(f"Loading configuration from [cyan]{config_path}[/cyan]")

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)

            if not isinstance(user_config, dict):
                raise ConfigurationError(
                    f"Configuration file must contain a JSON object"
                )

            # Validate and merge user configuration
            invalid_keys = []
            for key, value in user_config.items():
                if key in config:
                    # Validate type compatibility for critical settings
                    if key in [
                        "requiredSections",
                        "excludedDirectories",
                        "excludedFilePatterns",
                    ]:
                        if not isinstance(value, list):
                            invalid_keys.append(f"{key} must be a list")
                            continue
                    elif key in [
                        "enforceDocumentation",
                        "validateOnCommit",
                        "requireDiagrams",
                    ]:
                        if not isinstance(value, bool):
                            invalid_keys.append(f"{key} must be a boolean")
                            continue
                    elif key in ["minSectionLength", "maxFileSize"]:
                        if not isinstance(value, int) or value < 0:
                            invalid_keys.append(f"{key} must be a non-negative integer")
                            continue

                    config[key] = value
                else:
                    if verbose:
                        console.print(
                            f"  [yellow]Warning: Unknown config key '{key}' ignored[/yellow]"
                        )

            if invalid_keys:
                raise ConfigurationError(
                    f"Invalid configuration values: {', '.join(invalid_keys)}"
                )

            if verbose:
                console.print(
                    f"  ✅ Loaded configuration with {len(user_config)} custom settings"
                )

        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {e}")
        except (OSError, UnicodeDecodeError) as e:
            raise ConfigurationError(f"Error reading configuration file: {e}")
    else:
        if verbose:
            console.print(f"  📝 Using default configuration (no {config_path} found)")

    return config


def save_config(
    config: Dict[str, Any], config_file: Optional[str] = None, verbose: bool = False
) -> bool:
    """
    Save configuration to dmconfig.json.

    Args:
        config: Configuration dictionary to save
        config_file: Optional path to config file (defaults to dmconfig.json)
        verbose: Whether to print saving information

    Returns:
        True if configuration was saved successfully, False otherwise
    """
    config_path = get_config_path(config_file)

    if verbose:
        console.print(f"Saving configuration to [cyan]{config_path}[/cyan]")

    try:
        # Create directory if it doesn't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)

        # Filter out None values and empty lists for cleaner output
        clean_config = {}
        for key, value in config.items():
            if value is not None and (not isinstance(value, list) or value):
                clean_config[key] = value

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(clean_config, f, indent=2, sort_keys=True)

        if verbose:
            console.print(f"  ✅ Configuration saved successfully")

        return True
    except (OSError, TypeError) as e:
        error_msg = f"Error saving configuration: {e}"
        if verbose:
            console.print(f"  ❌ [red]{error_msg}[/red]")
        else:
            console.print(f"❌ [red]{error_msg}[/red]")
        return False


def get_template_content(config: Optional[Dict[str, Any]] = None) -> str:
    """
    Get the documentation template content, either custom or default.

    Args:
        config: Optional configuration dictionary (loads if not provided)

    Returns:
        Template content as string

    Raises:
        ConfigurationError: If custom template is specified but cannot be loaded
    """
    if config is None:
        config = load_config()

    custom_template_path = config.get("customTemplatePath")

    if custom_template_path:
        template_path = Path(custom_template_path)

        if not template_path.exists():
            raise ConfigurationError(f"Custom template file not found: {template_path}")

        try:
            return template_path.read_text(encoding=config.get("encoding", "utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            raise ConfigurationError(f"Error reading custom template: {e}")

    # Return default template from template module
    from dungeon_master.core.template import get_default_template

    return get_default_template()


def validate_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate a configuration dictionary and return list of errors.

    Args:
        config: Configuration dictionary to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    # Check required keys exist
    required_keys = ["loreDirectory", "enforceDocumentation", "requiredSections"]
    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required configuration key: {key}")

    # Validate paths
    if "customTemplatePath" in config and config["customTemplatePath"]:
        template_path = Path(config["customTemplatePath"])
        if not template_path.exists():
            errors.append(f"Custom template file not found: {template_path}")

    # Validate numeric values
    numeric_settings = {
        "minSectionLength": (0, 10000),
        "maxFileSize": (1024, 1073741824),  # 1KB to 1GB
    }

    for key, (min_val, max_val) in numeric_settings.items():
        if key in config:
            value = config[key]
            if not isinstance(value, int) or value < min_val or value > max_val:
                errors.append(
                    f"{key} must be an integer between {min_val} and {max_val}"
                )

    # Validate lists
    list_settings = ["requiredSections", "excludedDirectories", "excludedFilePatterns"]
    for key in list_settings:
        if key in config and not isinstance(config[key], list):
            errors.append(f"{key} must be a list")

    # Validate boolean settings
    bool_settings = ["enforceDocumentation", "validateOnCommit", "requireDiagrams"]
    for key in bool_settings:
        if key in config and not isinstance(config[key], bool):
            errors.append(f"{key} must be a boolean")

    return errors


def create_default_config(
    config_file: Optional[str] = None, verbose: bool = False
) -> bool:
    """
    Create a default configuration file.

    Args:
        config_file: Optional path to config file (defaults to dmconfig.json)
        verbose: Whether to print creation information

    Returns:
        True if configuration was created successfully, False otherwise
    """
    config_path = get_config_path(config_file)

    if config_path.exists():
        if verbose:
            console.print(
                f"Configuration file [cyan]{config_path}[/cyan] already exists"
            )
        return True

    return save_config(DEFAULT_CONFIG, config_file, verbose)


def get_setting(
    key: str, config: Optional[Dict[str, Any]] = None, default: Any = None
) -> Any:
    """
    Get a specific configuration setting.

    Args:
        key: Configuration key to retrieve
        config: Optional configuration dictionary (loads if not provided)
        default: Default value if key not found

    Returns:
        Configuration value or default
    """
    if config is None:
        config = load_config()

    return config.get(key, default)


def update_setting(
    key: str, value: Any, config_file: Optional[str] = None, verbose: bool = False
) -> bool:
    """
    Update a specific configuration setting and save.

    Args:
        key: Configuration key to update
        value: New value for the setting
        config_file: Optional path to config file
        verbose: Whether to print update information

    Returns:
        True if setting was updated successfully, False otherwise
    """
    try:
        config = load_config(config_file)
        config[key] = value

        # Validate the updated configuration
        errors = validate_config(config)
        if errors:
            if verbose:
                console.print(
                    f"❌ [red]Configuration validation failed: {', '.join(errors)}[/red]"
                )
            return False

        return save_config(config, config_file, verbose)
    except ConfigurationError as e:
        if verbose:
            console.print(f"❌ [red]Error updating configuration: {e}[/red]")
        return False


def merge_config_with_args(config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    """
    Merge configuration with command-line arguments or runtime parameters.

    Args:
        config: Base configuration dictionary
        **kwargs: Additional parameters to merge (command-line args override config)

    Returns:
        Merged configuration dictionary
    """
    merged_config = config.copy()

    # Define mappings from command-line argument names to config keys
    arg_mappings = {
        "lore_dir": "loreDirectory",
        "template_path": "customTemplatePath",
        "verbose": "verboseOutput",
        "no_color": lambda cfg, val: cfg.update({"colorOutput": not val}),
        "require_diagrams": "requireDiagrams",
        "min_length": "minSectionLength",
    }

    for arg_name, value in kwargs.items():
        if value is None:
            continue

        if arg_name in arg_mappings:
            mapping = arg_mappings[arg_name]
            if callable(mapping):
                mapping(merged_config, value)
            else:
                merged_config[mapping] = value

    return merged_config


def is_test_environment() -> bool:
    """
    Detect if running in test environment.

    Returns:
        True if running in test environment, False otherwise
    """
    return (
        "pytest" in sys.modules
        or "unittest" in sys.modules
        or os.getenv("DM_TEST_MODE") == "true"
        or
        # Check for actual test runners, not just filenames containing "test"
        (len(sys.argv) > 1 and sys.argv[0].endswith("pytest"))  # pytest runner
        or (len(sys.argv) > 1 and "pytest" in sys.argv)  # pytest in arguments
        or (
            len(sys.argv) > 1 and "-m" in sys.argv and "pytest" in sys.argv
        )  # python -m pytest
    )


def get_lore_directory(config: Optional[Dict[str, Any]] = None) -> str:
    """
    Get appropriate lore directory based on environment.

    Args:
        config: Optional configuration dictionary

    Returns:
        Lore directory path ('.lore.dev' for test, '.lore' for production)
    """
    if is_test_environment():
        return ".lore.dev"

    if config is None:
        config = load_config()

    return config.get("loreDirectory", ".lore")


def ensure_lore_directory_isolation() -> bool:
    """
    Ensure test environment is properly isolated.

    Returns:
        True if environment is properly set up, False otherwise
    """
    if is_test_environment():
        lore_dev_path = Path(".lore.dev")
        lore_dev_path.mkdir(exist_ok=True)

        # Add .lore.dev to .gitignore if not already there
        gitignore_path = Path(".gitignore")
        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if ".lore.dev" not in content:
                with open(gitignore_path, "a") as f:
                    f.write("\n# Dungeon Master test environment\n.lore.dev/\n")

        return True

    return True  # Production environment doesn't need special setup
