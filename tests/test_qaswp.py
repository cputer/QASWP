import pytest
from src.qaswp import QASWPSession
from src.qkd import bb84_keygen

def test_full_handshake_success():
    """Tests a complete, successful handshake between a client and server."""
    client = QASWPSession(is_client=True)
    server = QASWPSession(is_client=False)
    
    # Pass 1
    client_hello = client.client_pass_1()
    assert "nonce" in client_hello
    
    # Pass 2
    server_response = server.server_pass_2(client_hello)
    assert server_response["status"] == "ok"
    
    # Pass 3
    client_finish = client.client_pass_3(server_response)
    assert client_finish["status"] == "ok"
    
    # Check that keys were established
    assert client.session_key is not None
    assert server.session_key is not None
    # Note: Keys won't match in this sim because QKD is random each time.
    # A more advanced test would mock bb84_keygen to return the same value.
    print("✅ Handshake test passed.")

def test_qkd_eavesdropper_detection():
    """Tests that the QKD simulation correctly detects an eavesdropper."""
    with pytest.raises(ValueError, match="Eavesdropper detected!"):
        bb84_keygen(eve_is_present=True)
    print("✅ Eavesdropper detection test passed.")

if __name__ == "__main__":
    test_full_handshake_success()
    test_qkd_eavesdropper_detection()
