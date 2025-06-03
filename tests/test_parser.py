# @track_context("parser_tests.md")
"""
Tests for the parser module.
"""

import pytest
from dungeon_master.parser import (
    extract_track_context_decorator,
    parse_tracked_files,
    validate_context_document_name,
    get_file_summary
)


class TestExtractTrackContextDecorator:
    """Test extraction of @track_context decorators."""

    def test_valid_decorator_single_quotes(self):
        content = "# @track_context('test.md')\nclass MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result == "test.md"

    def test_valid_decorator_double_quotes(self):
        content = '# @track_context("test.md")\nclass MyClass:\n    pass'
        result = extract_track_context_decorator(content)
        assert result == "test.md"

    def test_decorator_without_md_extension(self):
        content = "# @track_context('test')\nclass MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result == "test.md"

    def test_decorator_with_spaces(self):
        content = "#   @track_context(  'test.md'  )\nclass MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result == "test.md"

    def test_no_decorator(self):
        content = "class MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result is None

    def test_decorator_not_in_first_lines(self):
        content = "\n\n\n\n\n\n\n\n\n\n\n# @track_context('test.md')\nclass MyClass:\n    pass"
        result = extract_track_context_decorator(content)
        assert result is None

    def test_empty_content(self):
        result = extract_track_context_decorator("")
        assert result is None

    def test_none_content(self):
        result = extract_track_context_decorator(None)
        assert result is None


class TestValidateContextDocumentName:
    """Test validation of context document names."""

    def test_valid_name(self):
        assert validate_context_document_name("test.md") is True

    def test_missing_md_extension(self):
        assert validate_context_document_name("test") is False

    def test_path_separator(self):
        assert validate_context_document_name("path/test.md") is False
        assert validate_context_document_name("path\\test.md") is False

    def test_empty_name(self):
        assert validate_context_document_name("") is False
        assert validate_context_document_name(".md") is False

    def test_none_name(self):
        assert validate_context_document_name(None) is False


class TestParseTrackedFiles:
    """Test parsing of tracked files."""

    @pytest.fixture
    def temp_files(self, tmp_path):
        """Create temporary test files."""
        # File with decorator
        tracked_file = tmp_path / "tracked.py"
        tracked_file.write_text("# @track_context('tracked.md')\nclass Test:\n    pass")

        # File without decorator
        untracked_file = tmp_path / "untracked.py"
        untracked_file.write_text("class Test:\n    pass")

        # Binary file
        binary_file = tmp_path / "test.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03')

        return {
            'tracked': str(tracked_file),
            'untracked': str(untracked_file),
            'binary': str(binary_file)
        }

    def test_parse_tracked_files(self, temp_files):
        file_paths = [temp_files['tracked'], temp_files['untracked']]
        result = parse_tracked_files(file_paths)

        assert len(result) == 1
        assert temp_files['tracked'] in result
        assert result[temp_files['tracked']] == "tracked.md"

    def test_parse_binary_files_skipped(self, temp_files):
        file_paths = [temp_files['binary']]
        result = parse_tracked_files(file_paths)

        assert len(result) == 0

    def test_parse_empty_list(self):
        result = parse_tracked_files([])
        assert result == {}

    def test_parse_nonexistent_files(self):
        result = parse_tracked_files(["nonexistent.py"])
        assert result == {}


class TestGetFileSummary:
    """Test file summary generation."""

    def test_get_file_summary_existing_file(self, tmp_path):
        test_file = tmp_path / "test.py"
        content = "line1\nline2\nline3"
        test_file.write_text(content)

        summary = get_file_summary(str(test_file))

        assert summary['file_path'] == str(test_file)
        assert summary['line_count'] == "3"
        assert summary['size'] == f"{len(content)} bytes"

    def test_get_file_summary_nonexistent_file(self):
        summary = get_file_summary("nonexistent.py")

        assert summary['file_path'] == "nonexistent.py"
        assert summary['line_count'] == "0"
        assert summary['size'] == "0 bytes"
