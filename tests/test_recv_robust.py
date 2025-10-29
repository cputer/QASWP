from hypothesis import given, strategies as st

from src.qaswp import QASWPSession


def _handshake_server() -> QASWPSession:
    server = QASWPSession(is_client=False)
    hello = server.client_pass_1()
    response = server.server_pass_2(hello)
    assert response["status"] == "ok"
    finish = server.client_pass_3(response)
    assert finish["status"] == "ok"
    return server


@given(
    nonce=st.binary(min_size=0, max_size=24),
    payload=st.binary(min_size=0, max_size=256),
    flushed=st.booleans(),
    wire_len=st.integers(min_value=0, max_value=512),
)
def test_receive_woven_packet_never_raises(nonce, payload, flushed, wire_len):
    """
    Robustness property:
      - receive_woven_packet() MUST NOT raise on placeholder or malformed frames.
      - It should return None (no-op) or a dict (well-formed decoded payload).
    """
    server = _handshake_server()
    packet = {
        "nonce": nonce,
        "encrypted_payload": payload,
        "flushed": flushed,
        "wire_len": wire_len,
    }
    try:
        output = server.receive_woven_packet(packet)
    except Exception as exc:  # Any exception is a failure of robustness
        raise AssertionError(
            "receive_woven_packet raised unexpectedly: "
            f"{type(exc).__name__}: {exc}"
        ) from exc
    assert (output is None) or isinstance(output, dict)
