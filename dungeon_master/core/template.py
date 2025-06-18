"""
Lore File Template System

This module provides functionality to create standardized lore documentation files
using templates with automatic placeholder population. It follows the template
structure defined in the PRD with required sections and mermaid diagrams.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any

# Default template as defined in the PRD
DEFAULT_TEMPLATE = """# Documentation for {filename}

## Overview

<!-- REQUIRED: Provide a brief overview of what this file does and its purpose -->

[PLEASE FILL OUT: Overview]

## Dependencies

<!-- List any important dependencies or related components -->

[PLEASE FILL OUT: Dependencies]

## Key Functions/Components

<!-- REQUIRED: Document the main functions, classes, or features -->

[PLEASE FILL OUT: Functions/Components]

## Usage Examples

<!-- Provide examples of how to use this code -->

[PLEASE FILL OUT: Examples]

## Diagrams

<!-- REQUIRED: Include professional-quality diagrams that illustrate the component's structure, behavior, or relationships -->
<!-- Use mermaid.js syntax for diagrams: https://mermaid-js.github.io/ -->
<!-- Include at least one diagram that best represents this component -->

### Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Component
    participant Service

    User->>Component: Action
    Component->>Service: Request
    Service-->>Component: Response
    Component-->>User: Result

    %% Replace with actual sequence flow relevant to this component
```

### Component/Architecture Diagram

```mermaid
flowchart TD
    A[Client] --> B[This Component]
    B --> C[Database]
    B --> D[External Service]

    %% Replace with actual architecture relevant to this component
```

### Additional Diagrams

<!-- Add any other diagrams that help explain this component -->
<!-- Class diagrams, state diagrams, etc. as appropriate -->

## Notes

<!-- Any additional information that might be important -->

---

_This documentation is linked to {tracked_files}_
"""

# Template placeholders that need to be filled out
REQUIRED_PLACEHOLDERS = [
    "[PLEASE FILL OUT: Overview]",
    "[PLEASE FILL OUT: Dependencies]", 
    "[PLEASE FILL OUT: Functions/Components]",
    "[PLEASE FILL OUT: Examples]"
]

# Mermaid diagram placeholders that indicate template content
DIAGRAM_PLACEHOLDERS = [
    "%% Replace with actual sequence flow relevant to this component",
    "%% Replace with actual architecture relevant to this component"
]


def get_default_template() -> str:
    """
    Get the default lore file template.
    
    Returns:
        The default template string with placeholders
    """
    return DEFAULT_TEMPLATE


def get_custom_template(template_path: Path) -> str:
    """
    Load a custom template from a file.
    
    Args:
        template_path: Path to the custom template file
        
    Returns:
        The custom template content
        
    Raises:
        FileNotFoundError: If the template file doesn't exist
        UnicodeDecodeError: If the template file contains invalid UTF-8
    """
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
        
    try:
        return template_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Template file {template_path} contains invalid UTF-8 encoding: {e.reason}"
        )


def populate_template(
    template: str,
    filename: str,
    tracked_files: Optional[List[str]] = None,
    custom_vars: Optional[Dict[str, Any]] = None
) -> str:
    """
    Populate a template with the provided variables.
    
    Args:
        template: The template string with placeholders
        filename: The filename for the {filename} placeholder
        tracked_files: List of files tracked by this lore file
        custom_vars: Additional custom variables for template population
        
    Returns:
        The populated template content
    """
    if tracked_files is None:
        tracked_files = []
        
    if custom_vars is None:
        custom_vars = {}
    
    # Format tracked files for template
    if tracked_files:
        tracked_files_str = ', '.join(tracked_files)
    else:
        tracked_files_str = 'no files yet'
    
    # Create variables dictionary
    template_vars = {
        'filename': filename,
        'tracked_files': tracked_files_str,
        **custom_vars  # Allow custom variables to override defaults
    }
    
    # Populate template with variables
    try:
        return template.format(**template_vars)
    except KeyError as e:
        raise ValueError(f"Template contains undefined placeholder: {e}")


def create_lore_file(
    lore_path: str,
    tracked_files: Optional[List[str]] = None,
    template: Optional[str] = None,
    lore_root: str = ".lore",
    custom_vars: Optional[Dict[str, Any]] = None,
    overwrite: bool = False
) -> bool:
    """
    Create a new lore file with the template.
    
    Args:
        lore_path: Relative path to the lore file (e.g., "api/payments.md")
        tracked_files: List of source files that reference this lore
        template: Custom template to use (uses default if None)
        lore_root: Root directory for lore files (default: ".lore")
        custom_vars: Custom variables for template population
        overwrite: Whether to overwrite existing files
        
    Returns:
        True if file was created, False if it already existed and overwrite=False
        
    Raises:
        ValueError: If lore_path is invalid or template is malformed
        OSError: If file operations fail
    """
    if not lore_path or not lore_path.strip():
        raise ValueError("lore_path cannot be empty")
        
    # Clean and validate the lore path
    lore_path = lore_path.strip().replace('\\', '/')
    
    # Ensure the lore path is relative to lore directory
    full_lore_path = Path(lore_root) / lore_path
    
    # Create directory if it doesn't exist
    full_lore_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if file already exists
    if full_lore_path.exists() and not overwrite:
        return False
        
    # Get filename without extension for template
    filename = full_lore_path.stem
    
    # Use default template if none provided
    if template is None:
        template = get_default_template()
        
    # Populate template
    try:
        content = populate_template(
            template=template,
            filename=filename,
            tracked_files=tracked_files,
            custom_vars=custom_vars
        )
    except ValueError as e:
        raise ValueError(f"Failed to populate template for {lore_path}: {e}")
    
    # Write the file
    try:
        full_lore_path.write_text(content, encoding='utf-8')
    except OSError as e:
        raise OSError(f"Failed to write lore file {full_lore_path}: {e}")
        
    return True


def create_multiple_lore_files(
    lore_mapping: Dict[str, List[str]],
    template: Optional[str] = None,
    lore_root: str = ".lore",
    custom_vars: Optional[Dict[str, Any]] = None,
    overwrite: bool = False
) -> Dict[str, bool]:
    """
    Create multiple lore files from a mapping.
    
    Args:
        lore_mapping: Dictionary mapping lore paths to lists of tracked files
        template: Custom template to use (uses default if None)
        lore_root: Root directory for lore files
        custom_vars: Custom variables for template population
        overwrite: Whether to overwrite existing files
        
    Returns:
        Dictionary mapping lore paths to creation success (True/False)
    """
    results = {}
    
    for lore_path, tracked_files in lore_mapping.items():
        try:
            created = create_lore_file(
                lore_path=lore_path,
                tracked_files=tracked_files,
                template=template,
                lore_root=lore_root,
                custom_vars=custom_vars,
                overwrite=overwrite
            )
            results[lore_path] = created
        except (ValueError, OSError) as e:
            # Log the error but continue with other files
            print(f"Warning: Failed to create {lore_path}: {e}")
            results[lore_path] = False
            
    return results


def is_template_file(file_path: Path) -> bool:
    """
    Check if a lore file still contains template placeholders.
    
    This function analyzes the content to determine if the file
    has been properly filled out or still contains template content.
    
    Args:
        file_path: Path to the lore file to check
        
    Returns:
        True if the file appears to be template-only, False if it's been filled out
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file contains invalid UTF-8
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Lore file not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Lore file {file_path} contains invalid UTF-8 encoding: {e.reason}"
        )
    
    # Check for required placeholders that haven't been filled out
    for placeholder in REQUIRED_PLACEHOLDERS:
        if placeholder in content:
            return True
            
    # Check for diagram placeholders that haven't been replaced
    for placeholder in DIAGRAM_PLACEHOLDERS:
        if placeholder in content:
            return True
            
    return False


def get_template_sections(file_path: Path) -> Dict[str, bool]:
    """
    Analyze which sections of a lore file still need to be completed.
    
    Args:
        file_path: Path to the lore file to analyze
        
    Returns:
        Dictionary mapping section names to completion status (True if complete)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file contains invalid UTF-8
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Lore file not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Lore file {file_path} contains invalid UTF-8 encoding: {e.reason}"
        )
    
    sections = {
        "Overview": "[PLEASE FILL OUT: Overview]" not in content,
        "Dependencies": "[PLEASE FILL OUT: Dependencies]" not in content,
        "Functions/Components": "[PLEASE FILL OUT: Functions/Components]" not in content,
        "Examples": "[PLEASE FILL OUT: Examples]" not in content,
        "Diagrams": all(placeholder not in content for placeholder in DIAGRAM_PLACEHOLDERS)
    }
    
    return sections


def validate_lore_file(file_path: Path) -> Dict[str, Any]:
    """
    Validate a lore file and return detailed status information.
    
    Args:
        file_path: Path to the lore file to validate
        
    Returns:
        Dictionary containing validation results:
        - is_template: Whether the file is still template-only
        - sections: Section completion status
        - missing_sections: List of sections that need completion
        - is_valid: Overall validation status
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file contains invalid UTF-8
    """
    sections = get_template_sections(file_path)
    is_template = is_template_file(file_path)
    
    missing_sections = [
        section for section, complete in sections.items() if not complete
    ]
    
    # File is considered valid if all required sections are complete
    required_sections = ["Overview", "Functions/Components", "Diagrams"]
    is_valid = all(sections.get(section, False) for section in required_sections)
    
    return {
        "is_template": is_template,
        "sections": sections,
        "missing_sections": missing_sections,
        "is_valid": is_valid,
        "file_path": str(file_path)
    }
