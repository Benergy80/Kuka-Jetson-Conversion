# Contributing Guidelines

## Development Workflow

1. Create a feature branch from `develop`
2. Implement changes with tests
3. Run linters: `make lint`
4. Run formatters: `make format`
5. Run tests: `make test`
6. Submit pull request
7. Address review comments
8. Merge after approval

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (100 char line length)
- Use isort for import sorting
- Add type hints to all functions
- Write docstrings for public APIs

## Testing

- Add unit tests for new functionality
- Maintain >80% code coverage
- Safety-critical code requires >95% coverage

## Commit Messages

Format: `<type>(<scope>): <subject>`

Types: feat, fix, docs, style, refactor, perf, test, chore, safety

Example: `feat(ml): implement ACT model`

## Safety-Critical Changes

Changes to safety-related code require:
- Extra review from safety officer
- Updated safety documentation
- Thorough testing
