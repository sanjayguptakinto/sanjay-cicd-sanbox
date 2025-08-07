"""HAR file parser module."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from har_analyzer.utils import (
    HARParsingError,
    categorize_resource_type,
    get_logger,
    safe_get,
    validate_har_file,
    validate_memory_usage,
)


class HARParser:
    """Parser for Chrome HAR files."""

    def __init__(self, memory_limit_mb: int = 1024):
        """Initialize HAR parser.

        Args:
            memory_limit_mb: Memory limit in megabytes
        """
        self.logger = get_logger(__name__)
        self.memory_limit_mb = memory_limit_mb
        self._data: Optional[Dict[str, Any]] = None
        self._entries: Optional[List[Dict[str, Any]]] = None

    def parse_file(self, file_path: Path) -> pd.DataFrame:
        """Parse HAR file and return structured data.

        Args:
            file_path: Path to HAR file

        Returns:
            DataFrame with parsed HAR data

        Raises:
            HARParsingError: If parsing fails
        """
        self.logger.info(f"Parsing HAR file: {file_path}")

        # Validate file
        validate_har_file(file_path)

        try:
            # Load HAR data
            with open(file_path, encoding="utf-8") as f:
                self._data = json.load(f)

            self._entries = self._data["log"]["entries"]
            self.logger.info(f"Found {len(self._entries)} entries in HAR file")

            # Convert to DataFrame
            df = self._convert_to_dataframe()

            self.logger.info(f"Successfully parsed {len(df)} requests")
            return df

        except Exception as e:
            self.logger.error(f"Failed to parse HAR file: {e}")
            raise HARParsingError(f"Failed to parse HAR file: {e}")

    def _convert_to_dataframe(self) -> pd.DataFrame:
        """Convert HAR entries to pandas DataFrame.

        Returns:
            DataFrame with processed HAR data
        """
        data = []
        total_entries = len(self._entries)

        for i, entry in enumerate(self._entries):
            if i % 100 == 0:  # Progress logging
                self.logger.debug(f"Processing entry {i+1}/{total_entries}")

                # Check memory usage
                from har_analyzer.utils.helpers import get_memory_usage

                current_memory = get_memory_usage()
                validate_memory_usage(current_memory, self.memory_limit_mb)

            try:
                processed_entry = self._process_entry(entry)
                if processed_entry:
                    data.append(processed_entry)
            except Exception as e:
                self.logger.warning(f"Failed to process entry {i}: {e}")
                continue

        if not data:
            raise HARParsingError("No valid entries found in HAR file")

        return pd.DataFrame(data)

    def _process_entry(self, entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single HAR entry.

        Args:
            entry: HAR entry dictionary

        Returns:
            Processed entry data or None if invalid
        """
        try:
            # Extract basic information
            url = safe_get(entry, "request", "url")
            if not url:
                return None

            # Response time
            response_time_ms = safe_get(entry, "time", default=0)

            # MIME type
            mime_type = safe_get(entry, "response", "content", "mimeType", default="")

            # Size calculation (try multiple sources)
            size_bytes = 0
            content = safe_get(entry, "response", "content", default={})

            if "size" in content:
                size_bytes = content["size"]
            elif safe_get(entry, "response", "bodySize", default=0) > 0:
                size_bytes = entry["response"]["bodySize"]
            elif safe_get(entry, "response", "encodedBodySize", default=0) > 0:
                size_bytes = entry["response"]["encodedBodySize"]

            # Parse start time
            start_time_str = safe_get(entry, "startedDateTime")
            start_time = None
            if start_time_str:
                try:
                    start_time = datetime.fromisoformat(
                        start_time_str.replace("Z", "+00:00")
                    )
                except ValueError:
                    # Fallback for different datetime formats
                    try:
                        start_time = datetime.strptime(
                            start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ"
                        )
                    except ValueError:
                        self.logger.warning(
                            f"Could not parse start time: {start_time_str}"
                        )

            # Status code
            status_code = safe_get(entry, "response", "status", default=0)

            # Method
            method = safe_get(entry, "request", "method", default="GET")

            # Timing breakdown
            timings = safe_get(entry, "timings", default={})
            blocked = safe_get(timings, "blocked", default=0)
            dns = safe_get(timings, "dns", default=0)
            connect = safe_get(timings, "connect", default=0)
            send = safe_get(timings, "send", default=0)
            wait = safe_get(timings, "wait", default=0)
            receive = safe_get(timings, "receive", default=0)

            return {
                "url": url,
                "method": method,
                "status_code": status_code,
                "type": categorize_resource_type(mime_type, url),
                "mime_type": mime_type,
                "response_time_ms": response_time_ms,
                "size_bytes": size_bytes,
                "size_kb": size_bytes / 1024 if size_bytes > 0 else 0,
                "start_time": start_time,
                "timing_blocked": blocked,
                "timing_dns": dns,
                "timing_connect": connect,
                "timing_send": send,
                "timing_wait": wait,
                "timing_receive": receive,
            }

        except Exception as e:
            self.logger.warning(f"Error processing entry: {e}")
            return None

    def get_metadata(self) -> Dict[str, Any]:
        """Get HAR file metadata.

        Returns:
            Dictionary with HAR metadata
        """
        if not self._data:
            return {}

        log = self._data.get("log", {})
        return {
            "version": safe_get(log, "version"),
            "creator": safe_get(log, "creator"),
            "browser": safe_get(log, "browser"),
            "pages": safe_get(log, "pages", default=[]),
            "entries_count": len(self._entries) if self._entries else 0,
        }
