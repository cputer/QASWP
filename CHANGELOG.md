# Changelog

All notable changes to this project will be documented in this file.

## v2.1.0 — 2025-10-29
- FIX: receiver no longer errors on placeholder packets (safe no-op)
- FEAT: public `QASWPSession.flush()` to emit trailing confirmations
- TEST: all demo compression tests use flush(); Benchmarks confirm ≥ 99%
- CI: added Benchmarks and Fuzz workflows; offline-tolerant robustness suite

## [2.2] - 2025-10-29
### Added
- Proprietary royalty-bearing license and NOTICE (CPUTER Inc.).
- Pre-commit (black, isort, flake8), CodeQL workflow.
- CONTRIBUTING, CODE_OF_CONDUCT, docs site scaffold.

## [2.1] - 2025-10-29
### Added
- MIT license (initial), CI workflow for tests.

## [2.0] - 2025-10-29
### Added
- Initial QASWP simulation, examples, tests, and docs.
