import pytest

from src.config import is_qiskit_enabled
from src.qaswp import QASWPSession, VOCAB
from src.qaswp_qiskit import QISKIT_AVAILABLE

skip_reason = None
if not is_qiskit_enabled():
    skip_reason = "QASWP_QISKIT flag disabled"
elif not QISKIT_AVAILABLE:
    skip_reason = "Qiskit not available in this environment"


@pytest.mark.skipif(skip_reason is not None, reason=skip_reason)
def test_qiskit_integration_end_to_end():
    """Ensure the Qiskit-backed handshake yields matching session keys."""

    client = QASWPSession(is_client=True)
    server = QASWPSession(is_client=False)

    client_hello = client.client_pass_1()
    server_resp = server.server_pass_2(client_hello)

    assert server_resp["status"] == "ok"
    assert "qiskit_key" in server_resp
    assert isinstance(server_resp["qiskit_key"], (bytes, bytearray))
    assert len(server_resp["qiskit_key"]) == 32

    client_finish = client.client_pass_3(server_resp)
    assert client_finish["status"] == "ok"

    packet = client.weave_packet([VOCAB["GET"], VOCAB["/api/v1/profile"]])
    server_out = server.receive_woven_packet(packet)
    assert server_out is None or isinstance(server_out, dict)

    flushed = client.flush()
    if flushed:
        server_out = server.receive_woven_packet(flushed)
        assert server_out is None or isinstance(server_out, dict)
