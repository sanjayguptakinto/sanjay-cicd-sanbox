# HAR Analyzer - Professional Performance Analysis Tool

├── 📁 docs/                      # HAR files for CI/CD analysis
│   ├── *.har                     # Production HAR files (processed by CI/CD)
│   └── test/                     # Sample/test HAR files (ignored by CI/CD)
│       ├── example-ecommerce.har # Good performance example
│       └── slow-performance.har  # Poor performance example
└── 📚 Documentation filesI/CD Pipeline](https://github.com/sanjayguptakinto/sanjay-cicd-sanbox/actions/workflows/cicd-sandbox.yml/badge.svg)](https://github.com/sanjayguptakinto/sanjay-cicd-sanbox/actions)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A comprehensive, enterprise-grade Chrome HAR (HTTP Archive) file analyzer with advanced performance analysis, professional PDF reporting, and CI/CD integration.

## 🚀 Features

### Core Capabilities
- **🔍 Advanced HAR Analysis**: Deep parsing of Chrome DevTools HAR files
- **📊 Performance Grading**: A+ to D rating system with industry-standard thresholds
- **📈 Comprehensive Metrics**: Response times, payload analysis, Core Web Vitals approximation
- **📄 Professional Reports**: Multi-page PDF reports with executive summaries
- **🎯 Issue Detection**: Automated performance bottleneck identification
- **⚡ CLI Interface**: Modern command-line tool with rich options

### Enterprise Features
- **🏗️ Modular Architecture**: Clean, maintainable, and extensible codebase
- **🔐 Security**: Input validation, memory limits, and secure processing
- **🧪 Comprehensive Testing**: 90%+ test coverage with unit and integration tests
- **📝 Type Safety**: Full type hints and mypy validation
- **🚀 CI/CD Ready**: Automated testing, security scanning, and deployment
- **🐳 Container Support**: Docker-ready for cloud deployments

## 📁 Project Structure

```
sanjay-cicd-sandbox/
├── 📋 pyproject.toml              # Modern Python packaging configuration
├── 📄 LICENSE                     # MIT License
├── 📖 CHANGELOG.md               # Version history and changes
├── 🤝 CONTRIBUTING.md            # Contribution guidelines
├── 🔧 .pre-commit-config.yaml    # Code quality automation
├── 🏗️ src/
│   └── har_analyzer/             # Main Python package
│       ├── core/                 # Core analysis engines
│       │   ├── analyzer.py       # Main analysis orchestrator
│       │   ├── parser.py         # HAR file parsing
│       │   └── metrics.py        # Performance calculations
│       ├── reports/              # Report generation
│       │   └── pdf_generator.py  # Professional PDF reports
│       ├── utils/                # Utilities and helpers
│       │   ├── logging.py        # Structured logging
│       │   ├── validators.py     # Input validation
│       │   ├── exceptions.py     # Custom exceptions
│       │   └── helpers.py        # Utility functions
│       ├── config.py             # Configuration management
│       └── cli.py                # Command-line interface
├── 🧪 tests/                     # Comprehensive test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── fixtures/                 # Test data
│   └── conftest.py              # Test configuration
├── 🔄 .github/workflows/         # Enhanced CI/CD pipelines
├── � docs/                      # HAR files for CI/CD analysis
│   ├── *.har                     # HAR files (processed automatically in CI/CD)
│   └── examples/                 # Sample HAR files
└── 📚 Documentation files
```

## 🚀 Quick Start

### Installation

#### Option 1: Install from Source (Recommended)
```bash
# Clone the repository
git clone https://github.com/sanjayguptakinto/sanjay-cicd-sanbox.git
cd sanjay-cicd-sanbox

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Option 2: Install Package Only
```bash
pip install -e "."
```

### Basic Usage

#### Command Line Interface
```bash
# Analyze a HAR file
har-analyzer path/to/your/file.har

# Specify output directory
har-analyzer file.har --output-dir reports/

# Export as CSV/JSON
har-analyzer file.har --format csv

# Enable verbose logging
har-analyzer file.har --verbose

# Get help
har-analyzer --help
```

#### Python API
```python
from pathlib import Path
from har_analyzer import HARAnalyzer
from har_analyzer.config import HARAnalyzerConfig

# Basic analysis
analyzer = HARAnalyzer()
results = analyzer.analyze_file(Path("sample.har"))

# Custom configuration
config = HARAnalyzerConfig(
    output_dir="custom_output",
    debug=True,
    max_memory_mb=2048
)
analyzer = HARAnalyzer(config)
results = analyzer.analyze_file(Path("large_file.har"))

# Generate summary
print(analyzer.get_summary_text())
```

## 📊 Analysis Features

### Performance Metrics
- **Response Time Analysis**: Mean, median, percentiles (P90, P95, P99)
- **Payload Analysis**: Total size, breakdown by resource type
- **Resource Categorization**: JS, CSS, Images, HTML, API, Fonts, Other
- **Core Web Vitals**: FCP and LCP approximations from HAR data
- **Timing Breakdown**: DNS, Connect, Send, Wait, Receive phases

### Performance Grading System
| Grade | Criteria | Status |
|-------|----------|--------|
| **A+ EXCELLENT** | Avg < 200ms & P95 < 500ms | 🟢 |
| **B GOOD** | Avg < 400ms & P95 < 1000ms | 🟡 |
| **C NEEDS IMPROVEMENT** | Avg < 800ms & P95 < 2000ms | 🟠 |
| **D POOR** | Above thresholds | 🔴 |

### Issue Detection
- Slow-loading resources (>2s)
- Large files (>1MB)
- Too many requests (>100)
- Failed requests (4xx/5xx status codes)
- Memory usage monitoring

## 📄 Generated Reports

### PDF Report Structure (7 Pages)
1. **Executive Summary**: Key metrics, performance grade, recommendations
2. **Response Time Analysis**: Detailed tables by resource type
3. **Payload Analysis**: Size breakdown and optimization opportunities
4. **Top Slowest Resources**: Resource-specific performance bottlenecks
5. **Top Largest Files**: Size optimization candidates
6. **Performance Dashboard**: Visual charts and percentile analysis
7. **Recommendations**: Actionable optimization strategies

### Export Formats
- **PDF**: Professional multi-page reports (default)
- **CSV**: Raw data for further analysis
- **JSON**: Structured data for API integration

## 🛠️ Development

### Setup Development Environment
```bash
# Clone and setup
git clone https://github.com/sanjayguptakinto/sanjay-cicd-sanbox.git
cd sanjay-cicd-sanbox

# Install with all dependencies
pip install -e ".[dev,test]"

# Setup pre-commit hooks
pre-commit install
```

### Code Quality Tools
```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type checking
mypy src/

# Security scan
bandit -r src/

# Run all quality checks
pre-commit run --all-files
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests only
```

### Building and Packaging
```bash
# Build package
python -m build

# Install from wheel
pip install dist/*.whl
```

## 🚀 CI/CD Pipeline

### Automated Workflows
- **Code Quality**: Black formatting, Ruff linting, MyPy type checking
- **Security Scanning**: Bandit security analysis, Safety dependency checking
- **Multi-Version Testing**: Python 3.9, 3.10, 3.11, 3.12
- **Performance Testing**: Memory usage and processing time benchmarks
- **Integration Testing**: CLI and API functionality validation
- **Container Building**: Docker image creation and testing
- **Automated Releases**: Semantic versioning and GitHub releases

### Pipeline Features
- **Dependency Caching**: Faster builds with pip and action caching
- **Parallel Jobs**: Concurrent quality checks and testing
- **Security First**: Required security scans before deployment
- **Multi-Environment**: Dev, staging, production deployment support
- **Artifact Management**: Build artifacts and reports with retention policies

## 🔧 Configuration

### Configuration File (`config.yaml`)
```yaml
# Performance thresholds
thresholds:
  a_plus: 200          # A+ grade threshold (ms)
  b: 400              # B grade threshold (ms)
  c: 800              # C grade threshold (ms)
  p95_a_plus: 500     # A+ 95th percentile threshold (ms)
  p95_b: 1000         # B 95th percentile threshold (ms)
  p95_c: 2000         # C 95th percentile threshold (ms)

# Report configuration
report:
  format: "pdf"        # Output format
  page_size: "A4"     # Page size
  include_timeline: true
  include_percentiles: true
  top_n_resources: 5   # Number of top resources to show

# System settings
output_dir: "output"
debug: false
max_memory_mb: 1024
```

### Environment Variables
```bash
export HAR_ANALYZER_CONFIG="path/to/config.yaml"
export HAR_ANALYZER_OUTPUT_DIR="custom_output"
export HAR_ANALYZER_DEBUG="true"
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Run quality checks (`pre-commit run --all-files`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Chrome DevTools team for HAR format specification
- The Python data science community for excellent libraries
- GitHub Actions for CI/CD infrastructure

## 📞 Support

For questions, issues, or contributions:
- 🐛 **Issues**: [GitHub Issues](https://github.com/sanjayguptakinto/sanjay-cicd-sanbox/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sanjayguptakinto/sanjay-cicd-sanbox/discussions)
- 📧 **Email**: sanjay.gupta@kinto-technologies.com

---

**Built with ❤️ by Sanjay Gupta | Kinto Technologies**

### CI/CD Pipeline
- **🔄 Automated Workflows**: GitHub Actions integration
- **🐍 Python Environment**: Automated setup and dependency management
- **📦 Artifact Management**: Report upload and retention
- **🚀 Manual & Automated Triggers**: Workflow dispatch capability

## 🚀 Quick Start

### Running HAR Analysis Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjayguptakinto/sanjay-cicd-sanbox.git
   cd sanjay-cicd-sanbox
   ```

2. **Install the package**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Run analysis**
   ```bash
   chmod +x run-analyzer.sh
   ./run-analyzer.sh
   ```

4. **View results**
   ```bash
   open output/performance_analysis_report_*.pdf
   ```

### Running via GitHub Actions

1. **Go to Actions tab** in GitHub repository
2. **Select "CI/CD Sandbox" workflow**
3. **Click "Run workflow"**
4. **Choose environment** (dev/lab/stg/inte/prod)
5. **Download artifacts** from completed workflow run

## 📊 HAR Analysis Features

The repository includes a sophisticated HAR (HTTP Archive) analyzer tool with modern Python packaging and CLI interface.

**Key Capabilities:**
- Professional PDF reports with visualizations
- Performance grading system (A+ to D)
- Timestamped output for tracking
- CI/CD integration with GitHub Actions
- Command-line interface with comprehensive options

**Quick Start:**
```bash
# Install the package
pip install -e ".[dev]"

# Use the CLI
har-analyzer your-file.har --output-dir reports --format pdf
```

## 🔧 Configuration

### CI/CD Workflow
Edit `.github/workflows/cicd-sandbox.yml` for:
- Trigger conditions (manual dispatch, push, PR)
- Environment selection (dev/lab/stg/inte/prod)
- Artifact retention periods
- Workflow steps and dependencies

### HAR Analyzer
Configure the HAR analyzer using:
- `config.yaml` - Main configuration file
- `pyproject.toml` - Tool configurations (Black, Ruff, MyPy, etc.)
- Environment variables for runtime settings

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Chrome browser** (for HAR file generation)
- **GitHub account** (for CI/CD features)

*Dependencies are managed through `pyproject.toml` and installed automatically with the package*

## 📖 Usage Examples

### GitHub Actions Workflow
1. Go to **Actions** tab in GitHub repository
2. Select **"CI/CD Sandbox"** workflow
3. Click **"Run workflow"** and choose environment
4. The workflow will automatically analyze all `*.har` files in the main `docs/` directory (subdirectories are ignored)
5. Download HAR analysis reports from completed run (1-day retention)

### Local HAR Analysis
```bash
# Install the package
pip install -e ".[dev]"

# Basic usage
har-analyzer your-file.har

# Advanced usage with options
har-analyzer your-file.har --output-dir reports --format pdf --verbose

# Check output/ folder for timestamped PDF reports
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for demonstration and testing purposes as part of CI/CD sandbox experimentation.

## 👤 Author

**Sanjay Gupta**
- Email: sanjay.gupta@kinto-technologies.com
- GitHub: [@sanjayguptakinto](https://github.com/sanjayguptakinto)

## 🆘 Support

For detailed documentation:
- **HAR Analyzer**: Check the `src/har_analyzer/` module documentation and `config.yaml`
- **GitHub Actions**: Review workflow logs in the Actions tab
- **Issues**: Create an issue in this repository

---

*This repository demonstrates CI/CD best practices, automated testing, and performance analysis tooling.*