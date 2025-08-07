"""Configuration management for HAR Analyzer."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class PerformanceThresholds(BaseModel):
    """Performance thresholds for grading."""

    a_plus: float = Field(default=200, description="A+ grade threshold (ms)")
    b: float = Field(default=400, description="B grade threshold (ms)")
    c: float = Field(default=800, description="C grade threshold (ms)")
    p95_a_plus: float = Field(
        default=500, description="A+ 95th percentile threshold (ms)"
    )
    p95_b: float = Field(default=1000, description="B 95th percentile threshold (ms)")
    p95_c: float = Field(default=2000, description="C 95th percentile threshold (ms)")


class ReportConfig(BaseModel):
    """Report generation configuration."""

    format: str = Field(default="pdf", description="Output format")
    page_size: str = Field(default="A4", description="Page size")
    include_timeline: bool = Field(default=True, description="Include timeline chart")
    include_percentiles: bool = Field(
        default=True, description="Include percentile analysis"
    )
    top_n_resources: int = Field(
        default=5, description="Number of top resources to show"
    )


class HARAnalyzerConfig(BaseModel):
    """Main configuration for HAR Analyzer."""

    input_file: Optional[str] = Field(default=None, description="Input HAR file path")
    output_dir: str = Field(default="output", description="Output directory")
    thresholds: PerformanceThresholds = Field(default_factory=PerformanceThresholds)
    report: ReportConfig = Field(default_factory=ReportConfig)
    debug: bool = Field(default=False, description="Enable debug logging")
    max_memory_mb: int = Field(default=1024, description="Maximum memory usage in MB")

    @classmethod
    def from_file(cls, config_path: Path) -> "HARAnalyzerConfig":
        """Load configuration from YAML file."""
        if not config_path.exists():
            return cls()

        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls(**data)

    def to_file(self, config_path: Path) -> None:
        """Save configuration to YAML file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)


# Default configuration
DEFAULT_CONFIG = HARAnalyzerConfig()
