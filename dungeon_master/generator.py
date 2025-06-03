# @track_context("template_generator.md")
"""
Generator module for creating context document templates.
Creates structured templates with placeholders for Cursor to fill.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
import logging

from .utils import read_file_content, format_timestamp, get_file_extension

logger = logging.getLogger(__name__)


def analyze_file_structure(file_path: str, file_content: str) -> Dict[str, List[str]]:
    """
    Analyze file structure to provide context for template generation.

    Args:
        file_path: Path to the file
        file_content: Content of the file

    Returns:
        Dict[str, List[str]]: Basic structural analysis for template context
    """
    extension = get_file_extension(file_path).lower()

    if extension == '.py':
        return _analyze_python_structure(file_content)
    elif extension in ['.js', '.ts', '.jsx', '.tsx']:
        return _analyze_javascript_structure(file_content)
    else:
        # Basic analysis for other file types
        lines = file_content.split('\n')
        return {
            'functions': [],
            'classes': [],
            'imports': [],
            'line_count': len(lines)
        }


def _analyze_python_structure(file_content: str) -> Dict[str, List[str]]:
    """Analyze Python file structure for template context."""
    try:
        tree = ast.parse(file_content)
    except SyntaxError as e:
        logger.warning(f"Could not parse Python file: {e}")
        return {'functions': [], 'classes': [], 'imports': []}

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            signature = f"{node.name}({', '.join(args)})"
            functions.append(signature)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append(f"{module}.{alias.name}" if module else alias.name)

    return {
        'functions': functions,
        'classes': classes,
        'imports': imports
    }


def _analyze_javascript_structure(file_content: str) -> Dict[str, List[str]]:
    """Analyze JavaScript/TypeScript file structure for template context."""
    functions = []
    classes = []
    imports = []

    # Simple regex patterns for basic analysis
    function_patterns = [
        r'function\s+(\w+)\s*\(',
        r'const\s+(\w+)\s*=\s*\(',
        r'let\s+(\w+)\s*=\s*\(',
        r'(\w+)\s*\([^)]*\)\s*=>\s*{',
    ]

    class_pattern = r'class\s+(\w+)'
    import_patterns = [
        r'import\s+.*?from\s+["\']([^"\']+)["\']',
        r'require\s*\(\s*["\']([^"\']+)["\']\s*\)',
    ]

    # Extract functions
    for pattern in function_patterns:
        matches = re.findall(pattern, file_content)
        functions.extend(matches)

    # Extract classes
    classes.extend(re.findall(class_pattern, file_content))

    # Extract imports
    for pattern in import_patterns:
        matches = re.findall(pattern, file_content)
        imports.extend(matches)

    return {
        'functions': list(set(functions)),
        'classes': list(set(classes)),
        'imports': list(set(imports))
    }


def generate_context_template(file_path: str) -> str:
    """
    Generate a context document template with Cursor-specific placeholders.

    Args:
        file_path: Path to the file to create template for

    Returns:
        str: Template markdown document with placeholders for Cursor
    """
    file_content = read_file_content(file_path)
    if not file_content:
        logger.error(f"Could not read file content for {file_path}")
        return ""

    filename = Path(file_path).name
    analysis = analyze_file_structure(file_path, file_content)

    # Generate template sections
    purpose_template = _generate_purpose_template(file_path, analysis)
    usage_template = _generate_usage_template(file_path, analysis)
    functions_template = _generate_functions_template(analysis)
    notes_template = _generate_notes_template()

    # Assemble the complete template
    template = f"""# {filename} - Context Documentation

> **Instructions for Cursor**: This is a context template. Please replace all placeholder text in angle brackets with meaningful documentation. Remove this instruction block when complete.

## Purpose

{purpose_template}

## Usage Summary

{usage_template}

## Key Functions or Classes

{functions_template}

## Usage Notes

{notes_template}

## Dependencies & Integration

<Describe how this file integrates with other parts of the system. What files import this? What does this file depend on? Are there any important architectural considerations?>

## Changelog

### [{format_timestamp()}]
- Context documentation created
- <Add meaningful changelog entries as the file evolves>

---
*This document is maintained by Cursor. Last updated: {format_timestamp()}*
"""

    return template


def _generate_purpose_template(file_path: str, analysis: Dict[str, List[str]]) -> str:
    """Generate purpose section template."""
    extension = get_file_extension(file_path).lower()
    file_type = _get_file_type_description(extension)

    if analysis.get('classes') and analysis.get('functions'):
        context_hint = f"This {file_type} contains {len(analysis['classes'])} class(es) and {len(analysis['functions'])} function(s)"
    elif analysis.get('classes'):
        context_hint = f"This {file_type} defines {len(analysis['classes'])} class(es): {', '.join(analysis['classes'][:3])}"
    elif analysis.get('functions'):
        context_hint = f"This {file_type} contains {len(analysis['functions'])} function(s)"
    else:
        context_hint = f"This {file_type}"

    return f"<Describe the overall intent and responsibility of this file. {context_hint}. What problem does it solve? What is its role in the larger system?>"


def _generate_usage_template(file_path: str, analysis: Dict[str, List[str]]) -> str:
    """Generate usage section template."""
    template_lines = [
        f"**File Location**: `{file_path}`",
        "",
        "**Primary Use Cases**:",
        "<List the main scenarios where this file/module is used>",
        "",
        "**Key Dependencies**:"
    ]

    if analysis.get('imports'):
        template_lines.append("<Review and document the purpose of these key imports:>")
        for imp in analysis['imports'][:5]:
            template_lines.append(f"- `{imp}`: <explain why this dependency is needed>")
        if len(analysis['imports']) > 5:
            template_lines.append(f"- ... and {len(analysis['imports']) - 5} more dependencies")
    else:
        template_lines.append("<List any important dependencies or note if this is a standalone module>")

    return '\n'.join(template_lines)


def _generate_functions_template(analysis: Dict[str, List[str]]) -> str:
    """Generate functions/classes section template."""
    sections = []

    if analysis.get('classes'):
        sections.append("**Classes:**")
        for cls in analysis['classes']:
            sections.append(f"- **{cls}**: <Describe the purpose and responsibility of this class>")
        sections.append("")

    if analysis.get('functions'):
        sections.append("**Key Functions:**")
        sections.append("<Document the most important functions - you don't need to list every function, focus on the key ones:>")
        # Show first 5 functions as examples
        for func in analysis['functions'][:5]:
            sections.append(f"- **{func}**: <Explain what this function does and when it's used>")

        if len(analysis['functions']) > 5:
            sections.append(f"- <Document other important functions from the remaining {len(analysis['functions']) - 5}>")
        sections.append("")

    if not analysis.get('classes') and not analysis.get('functions'):
        sections = ["<Describe the key components, exports, or functionality provided by this file>"]

    return '\n'.join(sections)


def _generate_notes_template() -> str:
    """Generate usage notes template."""
    return """<Document important usage patterns, gotchas, or considerations. For example:>
- <How should other parts of the system interact with this file?>
- <Are there any important patterns or conventions to follow?>
- <What are common mistakes or pitfalls to avoid?>
- <Any performance considerations or limitations?>"""


def _get_file_type_description(extension: str) -> str:
    """Get a human-readable description of file type based on extension."""
    descriptions = {
        '.py': 'Python module',
        '.js': 'JavaScript module',
        '.ts': 'TypeScript module',
        '.jsx': 'React component',
        '.tsx': 'TypeScript React component',
        '.java': 'Java class',
        '.cpp': 'C++ source',
        '.c': 'C source',
        '.h': 'C/C++ header',
        '.rs': 'Rust module',
        '.go': 'Go source',
        '.rb': 'Ruby module',
        '.php': 'PHP script',
        '.cs': 'C# class',
        '.kt': 'Kotlin source',
        '.swift': 'Swift source',
        '.sql': 'SQL script',
        '.sh': 'shell script',
        '.md': 'documentation'
    }

    return descriptions.get(extension, 'source code')


def has_unfilled_placeholders(content: str) -> bool:
    """
    Check if a context document still contains unfilled placeholder text.

    Args:
        content: Content of the context document

    Returns:
        bool: True if document contains placeholders that need to be filled
    """
    # Look for placeholder patterns
    placeholder_patterns = [
        r'<.*?Describe.*?>',
        r'<.*?List.*?>',
        r'<.*?Explain.*?>',
        r'<.*?Document.*?>',
        r'<.*?Add.*?>',
        r'<.*?Review.*?>',
        r'> \*\*Instructions for Cursor\*\*',  # Instruction block
    ]

    for pattern in placeholder_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True

    return False


def get_unfilled_sections(content: str) -> List[str]:
    """
    Get a list of sections that still need to be filled.

    Args:
        content: Content of the context document

    Returns:
        List[str]: List of section names that need attention
    """
    unfilled_sections = []

    # Check each section for placeholders
    section_checks = {
        'Purpose': r'## Purpose\s*\n(.*?)(?=\n## |\Z)',
        'Usage Summary': r'## Usage Summary\s*\n(.*?)(?=\n## |\Z)',
        'Key Functions': r'## Key Functions.*?\s*\n(.*?)(?=\n## |\Z)',
        'Usage Notes': r'## Usage Notes\s*\n(.*?)(?=\n## |\Z)',
        'Dependencies': r'## Dependencies.*?\s*\n(.*?)(?=\n## |\Z)',
    }

    for section_name, pattern in section_checks.items():
        match = re.search(pattern, content, re.DOTALL)
        if match:
            section_content = match.group(1)
            if re.search(r'<.*?(Describe|List|Explain|Document|Add|Review).*?>', section_content, re.IGNORECASE):
                unfilled_sections.append(section_name)

    # Check for instruction block
    if re.search(r'> \*\*Instructions for Cursor\*\*', content):
        unfilled_sections.append('Instructions block (remove when complete)')

    return unfilled_sections
