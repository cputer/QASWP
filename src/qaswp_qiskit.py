"""Qiskit-backed QKD handshake scaffold for QASWP."""
from __future__ import annotations

from typing import Tuple, Union
import hashlib
import os

try:
    import qiskit  # type: ignore  # noqa: F401

    QISKIT_AVAILABLE = True
except Exception:  # pragma: no cover - availability check
    QISKIT_AVAILABLE = False


def perform_qkd_session() -> Tuple[str, Union[bytes, str]]:
    """Attempt to derive a demo key using Qiskit when enabled."""
    flag = os.getenv("QASWP_QISKIT", "0").strip().lower() in ("1", "true", "yes", "y")
    if not flag:
        return ("skipped", "QASWP_QISKIT flag not enabled")
    if not QISKIT_AVAILABLE:
        return ("skipped", "Qiskit not installed/available in this environment")

    seed = (os.getenv("QISKIT_DEMO_SEED", "qaswp") + os.getenv("GITHUB_RUN_ID", "local")).encode()
    demo_key = hashlib.sha256(seed).digest()[:32]
    return ("ok", demo_key)
