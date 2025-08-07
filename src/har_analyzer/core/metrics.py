"""Performance metrics calculation module."""

from typing import Any, Dict, List, Tuple

import pandas as pd

from har_analyzer.config import PerformanceThresholds
from har_analyzer.utils import get_logger


class PerformanceMetrics:
    """Calculator for performance metrics and analysis."""

    def __init__(self, thresholds: PerformanceThresholds):
        """Initialize metrics calculator.

        Args:
            thresholds: Performance thresholds for grading
        """
        self.logger = get_logger(__name__)
        self.thresholds = thresholds

    def calculate_summary_by_type(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate performance summary by resource type.

        Args:
            df: DataFrame with HAR data

        Returns:
            Summary DataFrame grouped by resource type
        """
        self.logger.debug("Calculating performance summary by type")

        summary = (
            df.groupby("type")
            .agg(
                {
                    "url": "count",
                    "response_time_ms": [
                        "mean",
                        "max",
                        "min",
                        "std",
                        lambda x: x.quantile(0.90),
                        lambda x: x.quantile(0.95),
                    ],
                    "size_kb": ["sum", "mean", "max", "min"],
                    "status_code": lambda x: (x == 200).sum()
                    / len(x)
                    * 100,  # Success rate
                }
            )
            .round(2)
        )

        # Flatten column names
        summary.columns = [
            "requests_count",
            "avg_response_time_ms",
            "max_response_time_ms",
            "min_response_time_ms",
            "std_response_time_ms",
            "p90_response_time_ms",
            "p95_response_time_ms",
            "total_size_kb",
            "avg_size_kb",
            "max_size_kb",
            "min_size_kb",
            "success_rate_percent",
        ]

        return summary.reset_index()

    def calculate_percentiles(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate response time percentiles.

        Args:
            df: DataFrame with HAR data

        Returns:
            Dictionary with percentile values
        """
        percentiles = [50, 75, 90, 95, 99]
        result = {}

        for p in percentiles:
            result[f"p{p}"] = df["response_time_ms"].quantile(p / 100)

        return result

    def get_top_resources(
        self, df: pd.DataFrame, metric: str, n: int = 5
    ) -> Dict[str, pd.DataFrame]:
        """Get top N resources by metric for each resource type.

        Args:
            df: DataFrame with HAR data
            metric: Metric to sort by ('response_time_ms' or 'size_kb')
            n: Number of top resources to return

        Returns:
            Dictionary mapping resource type to top resources DataFrame
        """
        top_resources = {}

        for resource_type in df["type"].unique():
            type_df = df[df["type"] == resource_type]
            if len(type_df) > 0:
                top_n = type_df.nlargest(min(n, len(type_df)), metric)[
                    ["url", metric, "type", "method", "status_code"]
                ]
                top_resources[resource_type] = top_n

        return top_resources

    def calculate_performance_grade(self, df: pd.DataFrame) -> Tuple[str, str, str]:
        """Calculate overall performance grade.

        Args:
            df: DataFrame with HAR data

        Returns:
            Tuple of (grade, emoji, explanation)
        """
        avg_response = df["response_time_ms"].mean()
        p95_response = df["response_time_ms"].quantile(0.95)

        if (
            avg_response < self.thresholds.a_plus
            and p95_response < self.thresholds.p95_a_plus
        ):
            return (
                "A+ EXCELLENT",
                "🟢",
                "Outstanding performance! Fast loading times across all resources.",
            )
        elif avg_response < self.thresholds.b and p95_response < self.thresholds.p95_b:
            return (
                "B GOOD",
                "🟡",
                "Good performance with room for optimization. Some resources may be slower.",
            )
        elif avg_response < self.thresholds.c and p95_response < self.thresholds.p95_c:
            return (
                "C NEEDS IMPROVEMENT",
                "🟠",
                "Moderate performance issues. Optimization recommended for better user experience.",
            )
        else:
            return (
                "D POOR - URGENT ACTION NEEDED",
                "🔴",
                "Poor performance affecting user experience. Immediate optimization required.",
            )

    def calculate_core_web_vitals(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate Core Web Vitals metrics approximation.

        Args:
            df: DataFrame with HAR data

        Returns:
            Dictionary with Core Web Vitals metrics
        """
        # Note: These are approximations based on HAR data
        # Real Core Web Vitals require browser performance APIs

        # First Contentful Paint approximation (first HTML response)
        html_requests = df[df["type"] == "HTML"]
        fcp_approx = (
            html_requests["response_time_ms"].min() if len(html_requests) > 0 else 0
        )

        # Largest Contentful Paint approximation (largest image + time)
        image_requests = df[df["type"] == "Image"]
        if len(image_requests) > 0:
            largest_image = image_requests.loc[image_requests["size_kb"].idxmax()]
            lcp_approx = largest_image["response_time_ms"]
        else:
            lcp_approx = fcp_approx

        # Cumulative Layout Shift (cannot be calculated from HAR)
        cls_approx = None

        return {
            "fcp_approximation_ms": fcp_approx,
            "lcp_approximation_ms": lcp_approx,
            "cls_approximation": cls_approx,
            "note": "These are approximations based on HAR data. Real Core Web Vitals require browser performance APIs.",
        }

    def analyze_timing_breakdown(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Analyze timing breakdown by phase.

        Args:
            df: DataFrame with HAR data

        Returns:
            Dictionary with timing analysis
        """
        timing_columns = [
            "timing_blocked",
            "timing_dns",
            "timing_connect",
            "timing_send",
            "timing_wait",
            "timing_receive",
        ]

        # Filter out negative values (HAR format quirk)
        timing_df = df[timing_columns].copy()
        timing_df[timing_df < 0] = 0

        return {
            "averages": timing_df.mean().to_dict(),
            "medians": timing_df.median().to_dict(),
            "p95": timing_df.quantile(0.95).to_dict(),
            "totals": timing_df.sum().to_dict(),
        }

    def detect_performance_issues(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect common performance issues.

        Args:
            df: DataFrame with HAR data

        Returns:
            List of detected issues with recommendations
        """
        issues = []

        # Slow resources
        slow_threshold = 2000  # 2 seconds
        slow_resources = df[df["response_time_ms"] > slow_threshold]
        if len(slow_resources) > 0:
            issues.append(
                {
                    "type": "slow_resources",
                    "severity": "high",
                    "count": len(slow_resources),
                    "description": f"{len(slow_resources)} resources taking over {slow_threshold}ms",
                    "recommendation": "Optimize slow-loading resources, consider CDN, compression",
                }
            )

        # Large resources
        large_threshold = 1024  # 1MB
        large_resources = df[df["size_kb"] > large_threshold]
        if len(large_resources) > 0:
            issues.append(
                {
                    "type": "large_resources",
                    "severity": "medium",
                    "count": len(large_resources),
                    "description": f"{len(large_resources)} resources over {large_threshold}KB",
                    "recommendation": "Optimize file sizes, use compression, lazy loading",
                }
            )

        # Too many requests
        total_requests = len(df)
        if total_requests > 100:
            issues.append(
                {
                    "type": "too_many_requests",
                    "severity": "medium",
                    "count": total_requests,
                    "description": f"High number of requests ({total_requests})",
                    "recommendation": "Combine files, use sprite sheets, reduce dependencies",
                }
            )

        # Failed requests
        failed_requests = df[df["status_code"] >= 400]
        if len(failed_requests) > 0:
            issues.append(
                {
                    "type": "failed_requests",
                    "severity": "high",
                    "count": len(failed_requests),
                    "description": f"{len(failed_requests)} failed requests (4xx/5xx status)",
                    "recommendation": "Fix broken links and server errors",
                }
            )

        return issues
