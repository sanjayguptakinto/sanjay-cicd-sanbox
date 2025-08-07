"""HAR Analyzer - A comprehensive Chrome HAR file analyzer with PDF reporting."""

__version__ = "1.0.0"
__author__ = "Sanjay Gupta"
__email__ = "sanjay.gupta@kinto-technologies.com"

# Import main classes for easier access
try:
    from har_analyzer.core.analyzer import HARAnalyzer
    from har_analyzer.core.parser import HARParser
    from har_analyzer.reports.pdf_generator import PDFReportGenerator

    __all__ = ["HARAnalyzer", "HARParser", "PDFReportGenerator"]
except ImportError:
    # Handle import issues during development/testing
    __all__ = []
