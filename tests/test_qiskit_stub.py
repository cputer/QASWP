"""Smoke test for the Qiskit scaffold."""
import pytest

from src.qaswp_qiskit import QISKIT_AVAILABLE, perform_qkd_session
from src.config import is_qiskit_enabled


skip_reason = None
if not is_qiskit_enabled():
    skip_reason = "QASWP_QISKIT flag disabled"
elif not QISKIT_AVAILABLE:
    skip_reason = "Qiskit not available in this environment"


@pytest.mark.skipif(skip_reason is not None, reason=skip_reason)
def test_qiskit_qkd_smoke() -> None:
    status, out = perform_qkd_session()
    assert status == "ok", f"Unexpected status: {status}"
    assert isinstance(out, (bytes, bytearray))
    assert len(out) == 32
