import importlib

import pytest


def _has(module: str) -> bool:
    try:
        importlib.import_module(module)
        return True
    except Exception:
        return False


HYPOTHESIS_AVAILABLE = _has("hypothesis")


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "robust: robustness tests")
    config.addinivalue_line("markers", "hypothesis: requires Hypothesis")
