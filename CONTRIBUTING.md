# Contributing to WHOOP MCP Server

Thank you for your interest in contributing to the WHOOP MCP Server! This document provides guidelines and information for contributors.

## 🤝 Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A WHOOP account for testing
- Basic understanding of MCP (Model Context Protocol)

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/whoop-mcp-server.git
   cd whoop-mcp-server
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks (optional but recommended):**
   ```bash
   pre-commit install
   ```

5. **Run tests to ensure everything works:**
   ```bash
   pytest
   ```

## 🛠️ Development Workflow

### Branch Naming

- `feature/description` - For new features
- `bugfix/description` - For bug fixes
- `docs/description` - For documentation changes
- `refactor/description` - For code refactoring

### Making Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes following our coding standards**

3. **Run tests and linting:**
   ```bash
   # Run tests
   pytest
   
   # Format code
   black src/ tests/
   
   # Sort imports
   isort src/ tests/
   
   # Lint code
   flake8 src/
   
   # Type checking
   mypy src/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a pull request**

### Commit Message Format

We use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example: `feat: add support for sleep stage analysis`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_whoop_client.py

# Run tests with specific marker
pytest -m unit
```

### Writing Tests

- Write tests for all new features and bug fixes
- Aim for high test coverage (>80%)
- Use descriptive test names
- Mock external API calls
- Test both success and failure scenarios

Example test structure:
```python
def test_feature_description():
    """Test that feature works correctly under normal conditions"""
    # Arrange
    setup_test_data()
    
    # Act
    result = function_under_test()
    
    # Assert
    assert result == expected_value
```

## 📝 Documentation

### Code Documentation

- Use clear, descriptive function and variable names
- Add docstrings to all public functions and classes
- Include type hints for all function parameters and return values
- Comment complex logic and algorithms

### Documentation Files

- Update README.md for user-facing changes
- Update docs/ for detailed documentation changes
- Add examples for new features
- Update troubleshooting guides for known issues

## 🔐 Security Considerations

### Security Guidelines

- Never commit real tokens, API keys, or personal data
- Use mock data in tests
- Follow secure coding practices
- Validate all user inputs
- Handle errors gracefully without exposing sensitive information

### Reporting Security Issues

Please report security vulnerabilities privately to evstigneevromanv@gmail.com rather than opening public issues.

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the project's coding standards
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow conventional commit format
- [ ] No sensitive data is included

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Tests added/updated
- [ ] Manual testing completed
- [ ] Integration tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🏷️ Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):

- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Workflow

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release PR
4. After merge, tag the release
5. GitHub Actions handles the rest

## 🎯 Areas for Contribution

### High Priority
- Bug fixes and stability improvements
- Test coverage improvements
- Documentation enhancements
- Performance optimizations

### Medium Priority
- New WHOOP API endpoints
- Additional data analysis features
- Integration improvements
- Error handling enhancements

### Low Priority
- UI/UX improvements for setup
- Additional export formats
- Advanced configuration options
- Community requested features

## 🤔 Questions and Support

### Getting Help

- **Documentation**: Check README.md and docs/ folder
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive topics

### Issue Templates

When creating issues, please use our templates:

- **Bug Report**: For reporting bugs
- **Feature Request**: For suggesting new features
- **Question**: For asking questions
- **Documentation**: For documentation improvements

## 🏆 Recognition

Contributors are recognized in:

- CHANGELOG.md for significant contributions
- GitHub contributors list
- Release notes for major contributions

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to WHOOP MCP Server! 🙏

Your contributions help make fitness data more accessible and useful for everyone.