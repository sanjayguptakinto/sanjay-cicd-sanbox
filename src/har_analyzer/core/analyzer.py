"""Main HAR analyzer module."""

from pathlib import Path
from typing import Any, Optional

import pandas as pd

from har_analyzer.config import HARAnalyzerConfig
from har_analyzer.core.metrics import PerformanceMetrics
from har_analyzer.core.parser import HARParser
from har_analyzer.utils import (
    HARAnalyzerError,
    get_logger,
    get_memory_usage,
)


class HARAnalyzer:
    """Main HAR analyzer class."""

    def __init__(self, config: Optional[HARAnalyzerConfig] = None):
        """Initialize HAR analyzer.

        Args:
            config: Configuration object, uses default if None
        """
        self.config = config or HARAnalyzerConfig()
        self.logger = get_logger(__name__)

        # Initialize components
        self.parser = HARParser(memory_limit_mb=self.config.max_memory_mb)
        self.metrics = PerformanceMetrics(self.config.thresholds)

        # Analysis results
        self.data: Optional[pd.DataFrame] = None
        self.metadata: Optional[dict[str, Any]] = None
        self.analysis_results: Optional[dict[str, Any]] = None

    def analyze_file(self, har_file_path: Path) -> dict[str, Any]:
        """Analyze a HAR file and generate comprehensive results.

        Args:
            har_file_path: Path to HAR file

        Returns:
            Dictionary with analysis results

        Raises:
            HARAnalyzerError: If analysis fails
        """
        self.logger.info(f"Starting analysis of HAR file: {har_file_path}")

        try:
            # Parse HAR file
            self.logger.info("Parsing HAR file...")
            self.data = self.parser.parse_file(har_file_path)
            self.metadata = self.parser.get_metadata()

            # Perform analysis
            self.logger.info("Calculating performance metrics...")
            results = self._perform_analysis()

            self.logger.info("Analysis completed successfully")
            self.analysis_results = results
            return results

        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            raise HARAnalyzerError(f"Analysis failed: {e}")

    def _perform_analysis(self) -> dict[str, Any]:
        """Perform comprehensive performance analysis.

        Returns:
            Dictionary with analysis results
        """
        if self.data is None:
            raise HARAnalyzerError("No data available for analysis")

        # Basic statistics
        total_requests = len(self.data)
        total_time = self.data["response_time_ms"].sum()
        total_size = self.data["size_kb"].sum()
        avg_response = self.data["response_time_ms"].mean()

        self.logger.debug(
            f"Basic stats: {total_requests} requests, "
            f"{total_time/1000:.1f}s total time, "
            f"{total_size/1024:.1f}MB total size"
        )

        # Performance metrics
        summary_by_type = self.metrics.calculate_summary_by_type(self.data)
        percentiles = self.metrics.calculate_percentiles(self.data)
        grade, emoji, explanation = self.metrics.calculate_performance_grade(self.data)

        # Top resources
        top_slow = self.metrics.get_top_resources(
            self.data, "response_time_ms", self.config.report.top_n_resources
        )
        top_large = self.metrics.get_top_resources(
            self.data, "size_kb", self.config.report.top_n_resources
        )

        # Advanced analysis
        core_web_vitals = self.metrics.calculate_core_web_vitals(self.data)
        timing_breakdown = self.metrics.analyze_timing_breakdown(self.data)
        performance_issues = self.metrics.detect_performance_issues(self.data)

        # Memory usage tracking
        memory_usage = get_memory_usage()

        return {
            "metadata": self.metadata,
            "basic_stats": {
                "total_requests": total_requests,
                "total_time_ms": total_time,
                "total_size_kb": total_size,
                "avg_response_time_ms": avg_response,
                "memory_usage_mb": memory_usage,
            },
            "performance_grade": {
                "grade": grade,
                "emoji": emoji,
                "explanation": explanation,
            },
            "summary_by_type": summary_by_type,
            "percentiles": percentiles,
            "top_resources": {
                "slowest": top_slow,
                "largest": top_large,
            },
            "core_web_vitals": core_web_vitals,
            "timing_breakdown": timing_breakdown,
            "performance_issues": performance_issues,
            "resource_breakdown": self._calculate_resource_breakdown(),
        }

    def _calculate_resource_breakdown(self) -> dict[str, Any]:
        """Calculate detailed resource breakdown.

        Returns:
            Dictionary with resource breakdown data
        """
        if self.data is None:
            return {}

        # By resource type
        type_counts = self.data["type"].value_counts().to_dict()
        type_sizes = self.data.groupby("type")["size_kb"].sum().to_dict()

        # By status code
        status_counts = self.data["status_code"].value_counts().to_dict()

        # By method
        method_counts = self.data["method"].value_counts().to_dict()

        # Time distribution
        time_bins = pd.cut(
            self.data["response_time_ms"],
            bins=[0, 100, 500, 1000, 2000, float("inf")],
            labels=["<100ms", "100-500ms", "500ms-1s", "1s-2s", ">2s"],
        )
        time_distribution = time_bins.value_counts().to_dict()

        return {
            "by_type": {
                "counts": type_counts,
                "sizes_kb": type_sizes,
            },
            "by_status": status_counts,
            "by_method": method_counts,
            "time_distribution": time_distribution,
        }

    def export_data(self, output_file: Path, format: str = "csv") -> None:
        """Export analyzed data to file.

        Args:
            output_file: Output file path
            format: Export format ('csv', 'json', 'excel')

        Raises:
            HARAnalyzerError: If export fails
        """
        if self.data is None:
            raise HARAnalyzerError("No data available for export")

        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() == "csv":
                self.data.to_csv(output_file, index=False)
            elif format.lower() == "json":
                self.data.to_json(output_file, orient="records", indent=2)
            elif format.lower() == "excel":
                self.data.to_excel(output_file, index=False)
            else:
                raise ValueError(f"Unsupported export format: {format}")

            self.logger.info(f"Data exported to: {output_file}")

        except Exception as e:
            raise HARAnalyzerError(f"Export failed: {e}")

    def get_summary_text(self) -> str:
        """Get a text summary of the analysis.

        Returns:
            Formatted text summary
        """
        if not self.analysis_results:
            return "No analysis results available"

        basic = self.analysis_results["basic_stats"]
        grade = self.analysis_results["performance_grade"]
        issues = self.analysis_results["performance_issues"]

        summary = f"""
HAR Analysis Summary
===================

📊 Total Requests: {basic['total_requests']:,}
⏱️ Total Load Time: {basic['total_time_ms']/1000:.1f} seconds
📦 Total Data Size: {basic['total_size_kb']/1024:.1f} MB
🎯 Average Response: {basic['avg_response_time_ms']:.0f}ms

{grade['emoji']} Overall Grade: {grade['grade']}
{grade['explanation']}

"""

        if issues:
            summary += "\n🚨 Performance Issues Detected:\n"
            for issue in issues:
                summary += f"• {issue['description']} - {issue['recommendation']}\n"

        return summary
