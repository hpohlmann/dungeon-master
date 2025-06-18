"""
Unit tests for the lore file template system.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from dungeon_master.core.template import (
    get_default_template,
    get_custom_template,
    populate_template,
    create_lore_file,
    create_multiple_lore_files,
    is_template_file,
    get_template_sections,
    validate_lore_file,
    DEFAULT_TEMPLATE,
    REQUIRED_PLACEHOLDERS,
    DIAGRAM_PLACEHOLDERS
)


class TestTemplateRetrieval:
    """Test template retrieval functions."""

    def test_get_default_template(self):
        """Test getting the default template."""
        template = get_default_template()
        assert template == DEFAULT_TEMPLATE
        assert "{filename}" in template
        assert "{tracked_files}" in template
        assert "[PLEASE FILL OUT: Overview]" in template

    def test_get_custom_template(self):
        """Test loading custom templates."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            custom_content = "# Custom Template for {filename}\n\nTracked: {tracked_files}"
            f.write(custom_content)
            f.flush()
            temp_path = Path(f.name)
            
        try:
            template = get_custom_template(temp_path)
            assert template == custom_content
        finally:
            temp_path.unlink()

    def test_get_custom_template_file_not_found(self):
        """Test error handling for non-existent template files."""
        with pytest.raises(FileNotFoundError):
            get_custom_template(Path("non_existent_template.md"))

    def test_get_custom_template_encoding_error(self):
        """Test error handling for invalid encoding."""
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as f:
            # Write invalid UTF-8 bytes
            f.write(b'\xff\xfe\xfd')
            temp_path = Path(f.name)
            
        try:
            with pytest.raises(UnicodeDecodeError):
                get_custom_template(temp_path)
        finally:
            temp_path.unlink()


class TestTemplatePopulation:
    """Test template population functionality."""

    def test_populate_template_basic(self):
        """Test basic template population."""
        template = "# {filename}\n\nFiles: {tracked_files}"
        result = populate_template(
            template=template,
            filename="test",
            tracked_files=["file1.py", "file2.py"]
        )
        
        expected = "# test\n\nFiles: file1.py, file2.py"
        assert result == expected

    def test_populate_template_no_tracked_files(self):
        """Test template population with no tracked files."""
        template = "# {filename}\n\nFiles: {tracked_files}"
        result = populate_template(
            template=template,
            filename="test"
        )
        
        expected = "# test\n\nFiles: no files yet"
        assert result == expected

    def test_populate_template_empty_tracked_files(self):
        """Test template population with empty tracked files list."""
        template = "# {filename}\n\nFiles: {tracked_files}"
        result = populate_template(
            template=template,
            filename="test",
            tracked_files=[]
        )
        
        expected = "# test\n\nFiles: no files yet"
        assert result == expected

    def test_populate_template_custom_vars(self):
        """Test template population with custom variables."""
        template = "# {filename}\n\nAuthor: {author}\nVersion: {version}"
        result = populate_template(
            template=template,
            filename="test",
            custom_vars={"author": "Test Author", "version": "1.0.0"}
        )
        
        expected = "# test\n\nAuthor: Test Author\nVersion: 1.0.0"
        assert result == expected

    def test_populate_template_custom_vars_override(self):
        """Test that custom variables can override defaults."""
        template = "# {filename}\n\nFiles: {tracked_files}"
        result = populate_template(
            template=template,
            filename="test",
            tracked_files=["file1.py"],
            custom_vars={"tracked_files": "custom override"}
        )
        
        expected = "# test\n\nFiles: custom override"
        assert result == expected

    def test_populate_template_undefined_placeholder(self):
        """Test error handling for undefined placeholders."""
        template = "# {filename}\n\nUndefined: {undefined_var}"
        
        with pytest.raises(ValueError, match="undefined placeholder"):
            populate_template(template=template, filename="test")


class TestLoreFileCreation:
    """Test lore file creation functionality."""

    def test_create_lore_file_basic(self):
        """Test basic lore file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            
            result = create_lore_file(
                lore_path="test.md",
                tracked_files=["src/test.py"],
                lore_root=str(lore_root)
            )
            
            assert result is True
            
            created_file = lore_root / "test.md"
            assert created_file.exists()
            
            content = created_file.read_text()
            assert "# Documentation for test" in content
            assert "src/test.py" in content

    def test_create_lore_file_nested_path(self):
        """Test creating lore files in nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            
            result = create_lore_file(
                lore_path="api/payments.md",
                tracked_files=["src/api/payments.py"],
                lore_root=str(lore_root)
            )
            
            assert result is True
            
            created_file = lore_root / "api" / "payments.md"
            assert created_file.exists()
            assert created_file.parent.name == "api"
            
            content = created_file.read_text()
            assert "# Documentation for payments" in content

    def test_create_lore_file_already_exists(self):
        """Test behavior when file already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            lore_root.mkdir()
            
            # Create file first time
            result1 = create_lore_file(
                lore_path="test.md",
                lore_root=str(lore_root)
            )
            assert result1 is True
            
            # Try to create again without overwrite
            result2 = create_lore_file(
                lore_path="test.md",
                lore_root=str(lore_root),
                overwrite=False
            )
            assert result2 is False

    def test_create_lore_file_overwrite(self):
        """Test overwriting existing files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            lore_root.mkdir()
            
            # Create file first time
            create_lore_file(
                lore_path="test.md",
                tracked_files=["original.py"],
                lore_root=str(lore_root)
            )
            
            # Overwrite with different content
            result = create_lore_file(
                lore_path="test.md",
                tracked_files=["updated.py"],
                lore_root=str(lore_root),
                overwrite=True
            )
            
            assert result is True
            
            # Verify content was updated
            created_file = lore_root / "test.md"
            content = created_file.read_text()
            assert "updated.py" in content
            assert "original.py" not in content

    def test_create_lore_file_custom_template(self):
        """Test creating lore files with custom templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            
            custom_template = "# Custom {filename}\n\nTracked: {tracked_files}"
            
            result = create_lore_file(
                lore_path="test.md",
                tracked_files=["test.py"],
                template=custom_template,
                lore_root=str(lore_root)
            )
            
            assert result is True
            
            created_file = lore_root / "test.md"
            content = created_file.read_text()
            assert content == "# Custom test\n\nTracked: test.py"

    def test_create_lore_file_invalid_path(self):
        """Test error handling for invalid paths."""
        with pytest.raises(ValueError, match="cannot be empty"):
            create_lore_file(lore_path="")

        with pytest.raises(ValueError, match="cannot be empty"):
            create_lore_file(lore_path="   ")

    def test_create_multiple_lore_files(self):
        """Test creating multiple lore files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            lore_root = temp_path / ".lore"
            
            mapping = {
                "auth.md": ["src/auth.py", "src/login.py"],
                "api/payments.md": ["src/api/payments.py"],
                "docs/readme.md": []
            }
            
            results = create_multiple_lore_files(
                lore_mapping=mapping,
                lore_root=str(lore_root)
            )
            
            # All should be created successfully
            for lore_path in mapping.keys():
                assert results[lore_path] is True
                
            # Verify files exist
            assert (lore_root / "auth.md").exists()
            assert (lore_root / "api" / "payments.md").exists()
            assert (lore_root / "docs" / "readme.md").exists()
            
            # Verify content
            auth_content = (lore_root / "auth.md").read_text()
            assert "src/auth.py, src/login.py" in auth_content


class TestTemplateValidation:
    """Test template validation functionality."""

    def test_is_template_file_with_placeholders(self):
        """Test detecting files that still contain template placeholders."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(DEFAULT_TEMPLATE.format(
                filename="test",
                tracked_files="test.py"
            ))
            f.flush()
            temp_path = Path(f.name)
            
        try:
            assert is_template_file(temp_path) is True
        finally:
            temp_path.unlink()

    def test_is_template_file_filled_out(self):
        """Test detecting files that have been properly filled out."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            content = """# Documentation for test

## Overview

This is a real overview that has been filled out.

## Dependencies

- Real dependency 1
- Real dependency 2

## Key Functions/Components

Real function documentation here.

## Usage Examples

Real usage examples.

## Diagrams

### Custom Diagram

```mermaid
graph TD
    A[Real] --> B[Diagram]
```

## Notes

Real notes.

---

_This documentation is linked to test.py_
"""
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
            
        try:
            assert is_template_file(temp_path) is False
        finally:
            temp_path.unlink()

    def test_get_template_sections(self):
        """Test analyzing which sections need completion."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            # Partially filled template
            content = DEFAULT_TEMPLATE.format(
                filename="test",
                tracked_files="test.py"
            ).replace("[PLEASE FILL OUT: Overview]", "Real overview content")
            
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
            
        try:
            sections = get_template_sections(temp_path)
            
            assert sections["Overview"] is True  # Filled out
            assert sections["Dependencies"] is False  # Still placeholder
            assert sections["Functions/Components"] is False  # Still placeholder
            assert sections["Examples"] is False  # Still placeholder
            assert sections["Diagrams"] is False  # Still has placeholders
        finally:
            temp_path.unlink()

    def test_validate_lore_file(self):
        """Test comprehensive lore file validation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            # Template with some sections filled
            content = DEFAULT_TEMPLATE.format(
                filename="test",
                tracked_files="test.py"
            ).replace(
                "[PLEASE FILL OUT: Overview]", "Real overview"
            ).replace(
                "[PLEASE FILL OUT: Functions/Components]", "Real functions"
            )
            
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
            
        try:
            validation = validate_lore_file(temp_path)
            
            assert validation["is_template"] is True  # Still has some placeholders
            assert validation["is_valid"] is False  # Missing required Diagrams section
            assert "Dependencies" in validation["missing_sections"]
            assert "Examples" in validation["missing_sections"]
            assert "Diagrams" in validation["missing_sections"]
            assert "Overview" not in validation["missing_sections"]  # Filled out
        finally:
            temp_path.unlink()

    def test_validate_lore_file_fully_complete(self):
        """Test validation of a fully completed lore file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            content = """# Documentation for test

## Overview

Complete overview content.

## Dependencies

Complete dependencies.

## Key Functions/Components

Complete functions documentation.

## Usage Examples

Complete examples.

## Diagrams

### Custom Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant System
    User->>System: Custom action
    System-->>User: Custom response
```

### Custom Architecture

```mermaid
graph TD
    A[Custom] --> B[Architecture]
```

## Notes

Complete notes.

---

_This documentation is linked to test.py_
"""
            f.write(content)
            f.flush()
            temp_path = Path(f.name)
            
        try:
            validation = validate_lore_file(temp_path)
            
            assert validation["is_template"] is False
            assert validation["is_valid"] is True
            assert len(validation["missing_sections"]) == 0
        finally:
            temp_path.unlink()

    def test_validation_file_not_found(self):
        """Test error handling for non-existent files in validation."""
        with pytest.raises(FileNotFoundError):
            is_template_file(Path("non_existent.md"))
            
        with pytest.raises(FileNotFoundError):
            get_template_sections(Path("non_existent.md"))
            
        with pytest.raises(FileNotFoundError):
            validate_lore_file(Path("non_existent.md")) 