"""Configuration helpers for QASWP feature flags."""
import os


def is_demo_mode() -> bool:
    """Return True when demo mode flag (QASWP_DEMO) is enabled."""
    val = os.getenv("QASWP_DEMO", "1").strip().lower()
    return val in ("1", "true", "yes", "y")


def is_qiskit_enabled() -> bool:
    """Return True when the Qiskit integration flag (QASWP_QISKIT) is enabled."""
    val = os.getenv("QASWP_QISKIT", "0").strip().lower()
    return val in ("1", "true", "yes", "y")
