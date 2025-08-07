"""Unit tests for HAR parser."""

import json
import pytest
from pathlib import Path

from har_analyzer.core.parser import HARParser
from har_analyzer.utils.exceptions import (
    HARParsingError,
    InvalidHARFileError,
    ValidationError,
)


class TestHARParser:
    """Test cases for HARParser class."""

    def test_parse_valid_har_file(self, sample_har_file: Path):
        """Test parsing a valid HAR file."""
        parser = HARParser()
        df = parser.parse_file(sample_har_file)

        assert len(df) == 2
        assert list(df.columns) == [
            "url",
            "method",
            "status_code",
            "type",
            "mime_type",
            "response_time_ms",
            "size_bytes",
            "size_kb",
            "start_time",
            "timing_blocked",
            "timing_dns",
            "timing_connect",
            "timing_send",
            "timing_wait",
            "timing_receive",
        ]

        # Check specific values
        js_row = df[df["type"] == "JS"].iloc[0]
        assert js_row["response_time_ms"] == 150
        assert js_row["size_kb"] == 1.0
        assert js_row["method"] == "GET"
        assert js_row["status_code"] == 200

        css_row = df[df["type"] == "CSS"].iloc[0]
        assert css_row["response_time_ms"] == 100
        assert css_row["size_kb"] == 0.5

    def test_parse_nonexistent_file(self, tmp_path: Path):
        """Test parsing a nonexistent file."""
        parser = HARParser()
        nonexistent_file = tmp_path / "nonexistent.har"

        with pytest.raises(InvalidHARFileError):
            parser.parse_file(nonexistent_file)

    def test_parse_invalid_json(self, tmp_path: Path):
        """Test parsing invalid JSON file."""
        parser = HARParser()
        invalid_file = tmp_path / "invalid.har"

        with open(invalid_file, "w") as f:
            f.write("invalid json content")

        with pytest.raises(InvalidHARFileError):
            parser.parse_file(invalid_file)

    def test_parse_invalid_har_structure(self, tmp_path: Path):
        """Test parsing file with invalid HAR structure."""
        parser = HARParser()
        invalid_har = tmp_path / "invalid_structure.har"

        # Missing required fields
        with open(invalid_har, "w") as f:
            json.dump({"invalid": "structure"}, f)

        with pytest.raises(ValidationError):
            parser.parse_file(invalid_har)

    def test_get_metadata(self, sample_har_file: Path, sample_har_data):
        """Test metadata extraction."""
        parser = HARParser()
        parser.parse_file(sample_har_file)
        metadata = parser.get_metadata()

        assert metadata["version"] == "1.2"
        assert metadata["creator"]["name"] == "Test"
        assert metadata["entries_count"] == 2

    def test_memory_limit_validation(self, sample_har_file: Path):
        """Test memory limit validation."""
        # Use a reasonable memory limit for small test file
        parser = HARParser(memory_limit_mb=512)
        df = parser.parse_file(sample_har_file)
        assert len(df) == 2
