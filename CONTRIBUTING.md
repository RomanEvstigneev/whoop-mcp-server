# 🤝 Contributing to Whoop MCP Server

Thank you for your interest in contributing to the Whoop MCP Server! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Process](#development-process)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Issue Guidelines](#issue-guidelines)
- [Security Considerations](#security-considerations)
- [Community](#community)

## 🤝 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow:

- **Be respectful**: Treat all community members with respect and kindness
- **Be inclusive**: Welcome contributors from all backgrounds and experience levels
- **Be collaborative**: Work together to improve the project
- **Be patient**: Help others learn and grow
- **Be professional**: Maintain a professional tone in all communications

## 🚀 Getting Started

### Prerequisites

- **Node.js**: Version 18.0.0 or higher
- **Git**: For version control
- **Whoop Device**: For testing (recommended)
- **Claude Desktop**: For integration testing

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/yourusername/whoop-mcp-server.git
   cd whoop-mcp-server
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment**
   ```bash
   cp .env.template .env
   # Edit .env with your test credentials
   ```

4. **Run tests**
   ```bash
   npm test
   ```

5. **Start development server**
   ```bash
   npm start
   ```

## 📝 Types of Contributions

We welcome various types of contributions:

### 🐛 Bug Fixes

- Fix issues with API integration
- Resolve authentication problems
- Address error handling issues
- Fix documentation errors

### ✨ Features

- Add new MCP tools
- Improve data processing
- Enhance error handling
- Add configuration options

### 📚 Documentation

- Improve setup instructions
- Add usage examples
- Create troubleshooting guides
- Translate documentation

### 🧪 Testing

- Add unit tests
- Create integration tests
- Improve test coverage
- Add performance tests

### 🔧 Infrastructure

- Improve CI/CD processes
- Add development tools
- Enhance security measures
- Optimize performance

## 🔄 Development Process

### Branching Strategy

- **main**: Production-ready code
- **develop**: Integration branch for new features
- **feature/***: New features and enhancements
- **bugfix/***: Bug fixes
- **hotfix/***: Critical production fixes

### Branch Naming Convention

```
feature/add-new-metric-tool
bugfix/fix-authentication-error
hotfix/critical-security-fix
docs/improve-setup-guide
```

### Commit Messages

Use conventional commit format:

```
type(scope): description

feat(api): add support for new sleep metrics
fix(auth): resolve token refresh issue
docs(readme): update installation instructions
test(unit): add tests for data processing
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance tasks

## 🔍 Pull Request Guidelines

### Before Submitting

1. **Check existing issues/PRs**: Avoid duplicates
2. **Run tests**: Ensure all tests pass
3. **Update documentation**: Include relevant documentation changes
4. **Follow code style**: Use consistent formatting
5. **Add tests**: Include tests for new functionality

### PR Requirements

- **Clear title**: Descriptive title following conventional commits
- **Description**: Explain what changes were made and why
- **Issue reference**: Link to related issues
- **Screenshots**: Include screenshots for UI changes
- **Breaking changes**: Clearly document any breaking changes

### PR Template

```markdown
## Description
Brief description of changes

## Related Issues
- Fixes #123
- Addresses #456

## Changes Made
- [ ] Feature A
- [ ] Bug fix B
- [ ] Documentation update C

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
(If applicable)

## Breaking Changes
(If any)
```

## 🐛 Issue Guidelines

### Bug Reports

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g. macOS 14.0]
- Node.js: [e.g. 18.17.0]
- Server version: [e.g. 1.0.0]
- Whoop device: [e.g. Whoop 4.0]

## Additional Context
Any other relevant information
```

### Feature Requests

Use the feature request template:

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches were considered?

## Additional Context
Any other relevant information
```

## 🔒 Security Considerations

### Sensitive Data

- **Never commit credentials**: Use environment variables
- **Sanitize logs**: Remove sensitive information from logs
- **Secure APIs**: Follow security best practices
- **Validate inputs**: Always validate user inputs

### Security Reviews

- Security-related changes require additional review
- Include security implications in PR descriptions
- Test for common vulnerabilities
- Follow the [Security Policy](./SECURITY.md)

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── fixtures/       # Test data
└── utils/          # Test utilities
```

### Writing Tests

- **Test coverage**: Aim for >80% coverage
- **Test naming**: Use descriptive test names
- **Test isolation**: Each test should be independent
- **Mock external APIs**: Use mocks for Whoop API calls

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- --grep "auth"

# Run tests in watch mode
npm run test:watch
```

## 📊 Code Quality

### Code Style

- **ESLint**: Follow ESLint configuration
- **Prettier**: Use Prettier for formatting
- **Comments**: Add meaningful comments
- **Documentation**: Include JSDoc for functions

### Quality Checks

```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Format code
npm run format

# Type checking (if using TypeScript)
npm run type-check
```

## 🚀 Release Process

### Version Management

- Follow [Semantic Versioning](https://semver.org/)
- Update CHANGELOG.md
- Tag releases properly

### Release Steps

1. **Create release branch**
2. **Update version number**
3. **Update CHANGELOG.md**
4. **Run full test suite**
5. **Create pull request**
6. **Merge and tag release**

## 🌟 Recognition

### Contributors

All contributors are recognized in:
- GitHub contributors list
- CHANGELOG.md
- Documentation credits

### Levels of Contribution

- **Contributor**: Made accepted contributions
- **Maintainer**: Regular contributor with commit access
- **Admin**: Project administrator

## 📞 Getting Help

### Development Support

- **GitHub Discussions**: For questions and discussions
- **Discord**: Join our development chat
- **Email**: Contact maintainers directly

### Resources

- **Documentation**: Comprehensive guides and tutorials
- **Examples**: Sample code and usage examples
- **Best Practices**: Development guidelines and standards

## 📋 Checklist for Contributors

Before submitting your contribution:

- [ ] Code follows project style guidelines
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Security considerations are addressed
- [ ] Breaking changes are documented
- [ ] Commit messages follow convention
- [ ] PR description is clear and complete

## 🎉 Thank You!

We appreciate your interest in contributing to the Whoop MCP Server! Your contributions help make this project better for everyone in the community.

---

**Questions?** Feel free to ask in our [GitHub discussions](https://github.com/RomanEvstigneev/whoop-mcp-server/discussions) or open an issue!