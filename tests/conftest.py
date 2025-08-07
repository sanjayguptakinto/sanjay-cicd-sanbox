"""Test configuration and fixtures."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from har_analyzer.config import HARAnalyzerConfig


@pytest.fixture
def sample_har_data() -> dict[str, Any]:
    """Create sample HAR data for testing."""
    return {
        "log": {
            "version": "1.2",
            "creator": {"name": "Test", "version": "1.0"},
            "entries": [
                {
                    "request": {
                        "method": "GET",
                        "url": "https://example.com/script.js",
                    },
                    "response": {
                        "status": 200,
                        "content": {"size": 1024, "mimeType": "application/javascript"},
                    },
                    "time": 150,
                    "startedDateTime": "2025-01-01T10:00:00.000Z",
                    "timings": {
                        "blocked": 10,
                        "dns": 20,
                        "connect": 30,
                        "send": 5,
                        "wait": 75,
                        "receive": 10,
                    },
                },
                {
                    "request": {
                        "method": "GET",
                        "url": "https://example.com/style.css",
                    },
                    "response": {
                        "status": 200,
                        "content": {"size": 512, "mimeType": "text/css"},
                    },
                    "time": 100,
                    "startedDateTime": "2025-01-01T10:00:01.000Z",
                    "timings": {
                        "blocked": 5,
                        "dns": 0,
                        "connect": 0,
                        "send": 3,
                        "wait": 85,
                        "receive": 7,
                    },
                },
            ],
        }
    }


@pytest.fixture
def sample_har_file(sample_har_data: dict[str, Any], tmp_path: Path) -> Path:
    """Create a temporary HAR file for testing."""
    har_file = tmp_path / "test.har"
    with open(har_file, "w", encoding="utf-8") as f:
        json.dump(sample_har_data, f)
    return har_file


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create sample DataFrame for testing."""
    return pd.DataFrame(
        [
            {
                "url": "https://example.com/script.js",
                "method": "GET",
                "status_code": 200,
                "type": "JS",
                "mime_type": "application/javascript",
                "response_time_ms": 150,
                "size_bytes": 1024,
                "size_kb": 1.0,
                "start_time": datetime(2025, 1, 1, 10, 0, 0),
                "timing_blocked": 10,
                "timing_dns": 20,
                "timing_connect": 30,
                "timing_send": 5,
                "timing_wait": 75,
                "timing_receive": 10,
            },
            {
                "url": "https://example.com/style.css",
                "method": "GET",
                "status_code": 200,
                "type": "CSS",
                "mime_type": "text/css",
                "response_time_ms": 100,
                "size_bytes": 512,
                "size_kb": 0.5,
                "start_time": datetime(2025, 1, 1, 10, 0, 1),
                "timing_blocked": 5,
                "timing_dns": 0,
                "timing_connect": 0,
                "timing_send": 3,
                "timing_wait": 85,
                "timing_receive": 7,
            },
        ]
    )


@pytest.fixture
def test_config() -> HARAnalyzerConfig:
    """Create test configuration."""
    return HARAnalyzerConfig(output_dir="test_output", debug=True, max_memory_mb=512)


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir
