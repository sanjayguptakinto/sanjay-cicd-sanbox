"""Custom exceptions for HAR Analyzer."""


class HARAnalyzerError(Exception):
    """Base exception for HAR Analyzer."""

    pass


class HARParsingError(HARAnalyzerError):
    """Raised when HAR file parsing fails."""

    pass


class InvalidHARFileError(HARAnalyzerError):
    """Raised when HAR file is invalid or corrupted."""

    pass


class ReportGenerationError(HARAnalyzerError):
    """Raised when report generation fails."""

    pass


class ConfigurationError(HARAnalyzerError):
    """Raised when configuration is invalid."""

    pass


class ValidationError(HARAnalyzerError):
    """Raised when input validation fails."""

    pass


class MemoryLimitExceededError(HARAnalyzerError):
    """Raised when memory usage exceeds configured limits."""

    pass
