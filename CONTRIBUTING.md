# Contributing to QASWP

First off, thanks for your interest in improving QASWP!

## Ground Rules
- Be respectful and constructive.
- Follow the Code of Conduct.
- Discuss significant changes in an issue before opening a PR.

## How to Contribute
1. **Fork** the repo and create a feature branch: `git checkout -b feature/my-change`.
2. **Install dev tools**:
   ```bash
   pip install -r requirements.txt
   pip install pre-commit pytest
   pre-commit install
   ```
3. **Run tests** locally with `pytest`.
4. **Lint/format**: pre-commit hooks will auto-run on commit (black, isort, flake8).
5. **Open a Pull Request** with a clear description and reference any related issues.

## License for Contributions
By contributing, you agree your contributions are licensed to **CPUTER Inc.** under the repository’s
proprietary license (see `LICENSE`). CPUTER Inc. may relicense contributions for commercial use.

## Reporting Security Issues
Please email `security@puter.example` (replace with your address). We’ll respond promptly.
