"""Utility functions for HAR Analyzer."""

from datetime import datetime
from typing import Any, Union

import psutil


def get_memory_usage() -> float:
    """Get current memory usage in MB.

    Returns:
        Memory usage in megabytes
    """
    process = psutil.Process()
    return float(process.memory_info().rss / 1024 / 1024)


def format_bytes(bytes_value: Union[int, float]) -> str:
    """Format bytes value to human-readable string.

    Args:
        bytes_value: Value in bytes

    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    if bytes_value < 1024:
        return f"{bytes_value:.1f} B"
    elif bytes_value < 1024**2:
        return f"{bytes_value/1024:.1f} KB"
    elif bytes_value < 1024**3:
        return f"{bytes_value/(1024**2):.1f} MB"
    else:
        return f"{bytes_value/(1024**3):.1f} GB"


def format_duration(milliseconds: float) -> str:
    """Format duration in milliseconds to human-readable string.

    Args:
        milliseconds: Duration in milliseconds

    Returns:
        Formatted string (e.g., "1.5s")
    """
    if milliseconds < 1000:
        return f"{milliseconds:.0f}ms"
    elif milliseconds < 60000:
        return f"{milliseconds/1000:.1f}s"
    else:
        return f"{milliseconds/60000:.1f}m"


def generate_timestamp(format_str: str = "%d%m%Y%H%M%S") -> str:
    """Generate timestamp string.

    Args:
        format_str: Datetime format string

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_str)


def categorize_resource_type(mime_type: str, url: str) -> str:
    """Categorize resource type based on MIME type and URL.

    Args:
        mime_type: MIME type from response
        url: Resource URL

    Returns:
        Resource category (JS, CSS, Image, etc.)
    """
    mime_type = mime_type.lower()
    url = url.lower()

    if "javascript" in mime_type or url.endswith(".js"):
        return "JS"
    elif "css" in mime_type or url.endswith(".css"):
        return "CSS"
    elif "image" in mime_type or any(
        url.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
    ):
        return "Image"
    elif "html" in mime_type or url.endswith(".html"):
        return "HTML"
    elif "font" in mime_type or any(
        url.endswith(ext) for ext in [".woff", ".woff2", ".ttf", ".otf"]
    ):
        return "Font"
    elif "json" in mime_type or "api" in url:
        return "API"
    elif "video" in mime_type:
        return "Video"
    elif "audio" in mime_type:
        return "Audio"
    else:
        return "Other"


def safe_get(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    """Safely get nested dictionary values.

    Args:
        data: Dictionary to search
        keys: Nested keys to traverse
        default: Default value if key not found

    Returns:
        Value at nested key path or default
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current
