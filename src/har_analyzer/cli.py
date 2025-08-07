"""Command-line interface for HAR Analyzer."""

import sys
from pathlib import Path
from typing import Optional

import click

from har_analyzer import __version__
from har_analyzer.config import HARAnalyzerConfig
from har_analyzer.core.analyzer import HARAnalyzer
from har_analyzer.reports.pdf_generator import PDFReportGenerator
from har_analyzer.utils import HARAnalyzerError, get_logger, setup_logging


@click.command()
@click.version_option(version=__version__)
@click.argument("har_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    default="output",
    help="Output directory for reports (default: output)",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Configuration file path",
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["pdf", "json", "csv"], case_sensitive=False),
    default="pdf",
    help="Output format (default: pdf)",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--debug", is_flag=True, help="Enable debug logging")
@click.option(
    "--memory-limit", type=int, default=1024, help="Memory limit in MB (default: 1024)"
)
@click.option(
    "--no-report", is_flag=True, help="Skip report generation, only perform analysis"
)
def main(
    har_file: Path,
    output_dir: Path,
    config: Optional[Path],
    format: str,
    verbose: bool,
    debug: bool,
    memory_limit: int,
    no_report: bool,
) -> None:
    """Analyze Chrome HAR files and generate performance reports.

    HAR_FILE: Path to the Chrome HAR file to analyze
    """
    # Setup logging
    log_level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    setup_logging(level=log_level, debug=debug)
    logger = get_logger(__name__)

    try:
        # Load configuration
        if config:
            logger.info(f"Loading configuration from: {config}")
            analyzer_config = HARAnalyzerConfig.from_file(config)
        else:
            analyzer_config = HARAnalyzerConfig()

        # Override config with CLI options
        analyzer_config.output_dir = str(output_dir)
        analyzer_config.max_memory_mb = memory_limit
        analyzer_config.debug = debug

        logger.info(f"HAR Analyzer v{__version__}")
        logger.info(f"Analyzing: {har_file}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Memory limit: {memory_limit}MB")

        # Initialize analyzer
        analyzer = HARAnalyzer(analyzer_config)

        # Perform analysis
        click.echo("🚀 Starting HAR analysis...")
        results = analyzer.analyze_file(har_file)

        # Display summary
        click.echo("\n" + analyzer.get_summary_text())

        # Export data if requested
        if format in ["csv", "json"]:
            export_file = output_dir / f"har_analysis.{format}"
            click.echo(f"💾 Exporting data to: {export_file}")
            analyzer.export_data(export_file, format)

        # Generate report
        if not no_report and format == "pdf":
            click.echo("📄 Generating PDF report...")
            generator = PDFReportGenerator(analyzer_config)
            report_path = generator.generate_report(results, output_dir)
            click.echo(f"✅ Report generated: {report_path}")

        # Show performance issues
        issues = results.get("performance_issues", [])
        if issues:
            click.echo("\n🚨 Performance Issues Detected:")
            for issue in issues:
                severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    issue["severity"], "ℹ️"
                )
                click.echo(f"{severity_icon} {issue['description']}")
                click.echo(f"   💡 {issue['recommendation']}")

        click.echo(f"\n🎉 Analysis complete! Check {output_dir} for outputs.")

    except HARAnalyzerError as e:
        logger.error(f"Analysis failed: {e}")
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\n⚠️ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


@click.group()
def cli() -> None:
    """HAR Analyzer CLI tools."""
    pass


@cli.command()
@click.argument("output_file", type=click.Path(path_type=Path))
def generate_config(output_file: Path) -> None:
    """Generate a default configuration file."""
    config = HARAnalyzerConfig()
    config.to_file(output_file)
    click.echo(f"✅ Default configuration saved to: {output_file}")


@cli.command()
@click.argument("har_file", type=click.Path(exists=True, path_type=Path))
def validate(har_file: Path) -> None:
    """Validate a HAR file format."""
    from har_analyzer.utils.validators import validate_har_file

    try:
        validate_har_file(har_file)
        click.echo(f"✅ HAR file is valid: {har_file}")
    except Exception as e:
        click.echo(f"❌ HAR file validation failed: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
