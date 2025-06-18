"""
Unit tests for the lore decorator parser.
"""

import tempfile
from pathlib import Path

import pytest

from dungeon_master.core.decorator_parser import (
    extract_lore_paths,
    extract_lore_paths_safe,
    find_files_for_lore,
    get_file_extension,
    get_lore_files_for_source,
    is_supported_file,
    scan_repository_for_lore_decorators,
    should_skip_directory,
)


class TestFileExtensions:
    """Test file extension handling."""

    def test_get_file_extension(self):
        """Test getting file extensions."""
        assert get_file_extension(Path("test.py")) == ".py"
        assert get_file_extension(Path("test.PY")) == ".py"  # Should be lowercase
        assert get_file_extension(Path("test.ts")) == ".ts"
        assert get_file_extension(Path("test.jsx")) == ".jsx"
        assert get_file_extension(Path("test")) == ""
        assert get_file_extension(Path("test.unknown")) == ".unknown"

    def test_is_supported_file(self):
        """Test checking if file types are supported."""
        # Python files
        assert is_supported_file(Path("test.py")) is True
        assert is_supported_file(Path("test.pyi")) is True
        assert is_supported_file(Path("test.pyx")) is True

        # TypeScript/JavaScript files
        assert is_supported_file(Path("test.ts")) is True
        assert is_supported_file(Path("test.tsx")) is True
        assert is_supported_file(Path("test.js")) is True
        assert is_supported_file(Path("test.jsx")) is True

        # Unsupported files
        assert is_supported_file(Path("test.txt")) is False
        assert is_supported_file(Path("test.md")) is False
        assert is_supported_file(Path("test.json")) is False


class TestDirectorySkipping:
    """Test directory skipping logic."""

    def test_should_skip_directory(self):
        """Test directory skipping logic."""
        # Should skip
        assert should_skip_directory(Path(".git")) is True
        assert should_skip_directory(Path("__pycache__")) is True
        assert should_skip_directory(Path("node_modules")) is True
        assert should_skip_directory(Path(".venv")) is True
        assert should_skip_directory(Path("build")) is True
        assert should_skip_directory(Path(".hidden")) is True

        # Should not skip
        assert should_skip_directory(Path("src")) is False
        assert should_skip_directory(Path("lib")) is False
        assert should_skip_directory(Path("components")) is False
        assert should_skip_directory(Path(".lore")) is False  # Special case


class TestDecoratorExtraction:
    """Test decorator extraction from file content."""

    def test_extract_lore_paths_python(self):
        """Test extracting lore paths from Python files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                '''
# track_lore("test.md")
# track_lore("api/docs.md")
def test_function():
    # track_lore("internal.md")
    pass

class TestClass:
    """Test class."""
    # track_lore("class-docs.md")
    pass
'''
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths(temp_path)
            expected = ["test.md", "api/docs.md", "internal.md", "class-docs.md"]
            assert paths == expected
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_typescript(self):
        """Test extracting lore paths from TypeScript files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ts", delete=False) as f:
            f.write(
                """
// track_lore("auth.md")
// track_lore("frontend/auth.md")
interface User {
    id: string;
}

// track_lore("user-manager.md")
export class UserManager {
    // track_lore("config.md")
    constructor() {}
}
"""
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths(temp_path)
            expected = ["auth.md", "frontend/auth.md", "user-manager.md", "config.md"]
            assert paths == expected
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_single_quotes(self):
        """Test extracting lore paths with single quotes."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                """
# track_lore('single-quotes.md')
# track_lore("double-quotes.md")
def test():
    pass
"""
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths(temp_path)
            expected = ["single-quotes.md", "double-quotes.md"]
            assert paths == expected
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_malformed(self):
        """Test handling malformed decorators."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                """
# track_lore("valid.md")
# track_lore(missing-quotes.md)
# track_lore("unclosed.md
# not_track_lore("ignored.md")
# track_lore("")  # Empty path should be ignored
def test():
    pass
"""
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths(temp_path)
            # Should only find the valid one
            expected = ["valid.md"]
            assert paths == expected
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_no_decorators(self):
        """Test files with no decorators."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                '''
def test_function():
    """A test function with no decorators."""
    return True

class TestClass:
    pass
'''
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths(temp_path)
            assert paths == []
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_file_not_found(self):
        """Test error handling for non-existent files."""
        with pytest.raises(FileNotFoundError):
            extract_lore_paths(Path("non_existent_file.py"))

    def test_extract_lore_paths_unsupported_type(self):
        """Test error handling for unsupported file types."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = Path(f.name)

        try:
            with pytest.raises(ValueError, match="Unsupported file type"):
                extract_lore_paths(temp_path)
        finally:
            temp_path.unlink()

    def test_extract_lore_paths_safe(self):
        """Test safe extraction that doesn't raise exceptions."""
        # Test with non-existent file
        paths = extract_lore_paths_safe(Path("non_existent.py"))
        assert paths == []

        # Test with unsupported file type
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = Path(f.name)

        try:
            paths = extract_lore_paths_safe(temp_path)
            assert paths == []
        finally:
            temp_path.unlink()


class TestRepositoryScanning:
    """Test repository scanning functionality."""

    def test_scan_repository_for_lore_decorators(self):
        """Test scanning a repository for decorators."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            py_file = temp_path / "test.py"
            py_file.write_text('# track_lore("python-doc.md")\ndef test(): pass')

            ts_file = temp_path / "test.ts"
            ts_file.write_text('// track_lore("ts-doc.md")\nfunction test() {}')

            # Create file in subdirectory
            sub_dir = temp_path / "src"
            sub_dir.mkdir()
            sub_file = sub_dir / "module.py"
            sub_file.write_text('# track_lore("module-doc.md")\nclass Module: pass')

            # Scan repository
            mapping = scan_repository_for_lore_decorators(temp_path)

            expected_mapping = {
                "python-doc.md": ["test.py"],
                "ts-doc.md": ["test.ts"],
                "module-doc.md": ["src/module.py"],
            }

            assert mapping == expected_mapping

    def test_scan_repository_with_exclude_patterns(self):
        """Test repository scanning with exclude patterns."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            include_file = temp_path / "include.py"
            include_file.write_text('# track_lore("include.md")\ndef test(): pass')

            exclude_file = temp_path / "exclude.py"
            exclude_file.write_text('# track_lore("exclude.md")\ndef test(): pass')

            # Scan with exclude pattern
            mapping = scan_repository_for_lore_decorators(
                temp_path, exclude_patterns=["exclude.py"]
            )

            assert "include.md" in mapping
            assert "exclude.md" not in mapping

    def test_find_files_for_lore(self):
        """Test finding files for a specific lore file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create test files
            file1 = temp_path / "file1.py"
            file1.write_text('# track_lore("shared.md")\ndef test1(): pass')

            file2 = temp_path / "file2.py"
            file2.write_text('# track_lore("shared.md")\ndef test2(): pass')

            file3 = temp_path / "file3.py"
            file3.write_text('# track_lore("other.md")\ndef test3(): pass')

            # Find files for shared.md
            files = find_files_for_lore("shared.md", temp_path)

            # Should find both file1.py and file2.py
            assert len(files) == 2
            assert "file1.py" in files
            assert "file2.py" in files

    def test_get_lore_files_for_source(self):
        """Test getting lore files for a specific source file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(
                """
# track_lore("doc1.md")
# track_lore("doc2.md")
def test():
    # track_lore("doc3.md")
    pass
"""
            )
            f.flush()
            temp_path = Path(f.name)

        try:
            lore_files = get_lore_files_for_source(temp_path)
            expected = ["doc1.md", "doc2.md", "doc3.md"]
            assert lore_files == expected
        finally:
            temp_path.unlink()


class TestRealFiles:
    """Test with real example files in the repository."""

    def test_python_example_file(self):
        """Test parsing the real Python example file."""
        example_file = Path("examples/python_example/example.py")
        if example_file.exists():
            paths = extract_lore_paths(example_file)
            # Should find the decorators we added
            assert "payments.md" in paths
            assert "api/payments.md" in paths
            assert len(paths) >= 2  # At least the ones we know about

    def test_typescript_example_file(self):
        """Test parsing the real TypeScript example file."""
        example_file = Path("examples/typescript_example/example.ts")
        if example_file.exists():
            paths = extract_lore_paths(example_file)
            # Should find the decorators we added
            assert "auth.md" in paths
            assert "frontend/auth.md" in paths
            assert len(paths) >= 2  # At least the ones we know about
