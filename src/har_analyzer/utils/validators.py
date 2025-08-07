"""Input validation utilities for HAR Analyzer."""

import json
from pathlib import Path

from har_analyzer.utils.exceptions import InvalidHARFileError, ValidationError


def validate_har_file(file_path: Path) -> None:
    """Validate HAR file format and structure.

    Args:
        file_path: Path to HAR file

    Raises:
        InvalidHARFileError: If file is invalid
        ValidationError: If file structure is invalid
    """
    if not file_path.exists():
        raise InvalidHARFileError(f"HAR file not found: {file_path}")

    if not file_path.suffix.lower() == ".har":
        raise InvalidHARFileError(f"File must have .har extension: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise InvalidHARFileError(f"Invalid JSON in HAR file: {e}")
    except UnicodeDecodeError as e:
        raise InvalidHARFileError(f"Invalid encoding in HAR file: {e}")

    # Validate HAR structure
    if not isinstance(data, dict):
        raise ValidationError("HAR file must contain a JSON object")

    if "log" not in data:
        raise ValidationError("HAR file must contain a 'log' object")

    log = data["log"]
    if not isinstance(log, dict):
        raise ValidationError("HAR 'log' must be an object")

    if "entries" not in log:
        raise ValidationError("HAR log must contain 'entries' array")

    entries = log["entries"]
    if not isinstance(entries, list):
        raise ValidationError("HAR entries must be an array")

    if len(entries) == 0:
        raise ValidationError("HAR file contains no entries")

    # Validate first entry structure
    if entries:
        entry = entries[0]
        required_fields = ["request", "response", "time", "startedDateTime"]
        for field in required_fields:
            if field not in entry:
                raise ValidationError(f"HAR entry missing required field: {field}")


def validate_output_directory(output_dir: Path) -> None:
    """Validate and create output directory.

    Args:
        output_dir: Path to output directory

    Raises:
        ValidationError: If directory cannot be created or accessed
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise ValidationError(f"No permission to create output directory: {output_dir}")
    except OSError as e:
        raise ValidationError(f"Cannot create output directory: {output_dir} - {e}")

    if not output_dir.is_dir():
        raise ValidationError(f"Output path is not a directory: {output_dir}")

    # Test write permissions
    test_file = output_dir / ".test_write"
    try:
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        raise ValidationError(f"No write permission in output directory: {output_dir}")


def validate_memory_usage(current_mb: float, limit_mb: int) -> None:
    """Validate memory usage against limits.

    Args:
        current_mb: Current memory usage in MB
        limit_mb: Memory limit in MB

    Raises:
        MemoryLimitExceededError: If memory usage exceeds limit
    """
    from har_analyzer.utils.exceptions import MemoryLimitExceededError

    if current_mb > limit_mb:
        raise MemoryLimitExceededError(
            f"Memory usage ({current_mb:.1f}MB) exceeds limit ({limit_mb}MB)"
        )
