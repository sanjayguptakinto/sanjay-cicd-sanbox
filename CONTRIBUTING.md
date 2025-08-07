# Contributing to HAR Analyzer

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sanjayguptakinto/sanjay-cicd-sanbox.git
cd sanjay-cicd-sanbox

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
ruff check src/ tests/
black --check src/ tests/
mypy src/

# Run security scan
bandit -r src/
```

### Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [Ruff](https://docs.astral.sh/ruff/) for linting
- We use [MyPy](https://mypy.readthedocs.io/) for type checking
- Maximum line length is 88 characters
- Use type hints for all functions and methods

### Testing

- Write tests for all new functionality
- Maintain or improve test coverage
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Issue Reporting

When filing an issue, make sure to answer these five questions:

1. What version of Python are you using?
2. What operating system and processor architecture are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### Feature Requests

We love feature requests! Please create an issue describing:

- The problem you're trying to solve
- Your proposed solution
- Any alternative solutions you've considered

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
