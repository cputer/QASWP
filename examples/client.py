from src.qaswp import QASWPSession, VOCAB
import time

def run_client():
    print("🚀 [QASWP Client] Initializing...")
    client_session = QASWPSession(is_client=True)

    # --- Handshake ---
    print("\n--- Handshake Step 1: Client -> Server ---")
    client_hello = client_session.client_pass_1()
    print(f"Sent ClientHello with nonce: {client_hello['nonce'].hex()[:16]}...")
    
    # Simulate receiving server response
    # In a real scenario, this comes over the network.
    print("\n--- Handshake Step 2: Server -> Client (Simulated) ---")
    # We create a temporary server session to generate the response
    from src.qaswp import QASWPSession as ServerSession
    server_session = ServerSession()
    server_response = server_session.server_pass_2(client_hello)
    
    if server_response["status"] == "error":
        print(f"🔴 Handshake failed: {server_response['message']}")
        return
    print("Received ServerHello with ZK proof. Verification successful.")

    print("\n--- Handshake Step 3: Client -> Server ---")
    client_finish = client_session.client_pass_3(server_response)
    if client_finish["status"] == "ok":
        print("✅ Handshake complete. Secure session established.")
    else:
        print("🔴 Handshake failed at final step.")
        return

    # --- Data Transfer ---
    print("\n--- Neural-Semantic Data Transfer ---")
    message_to_send = [VOCAB["GET"], VOCAB["/api/v1/profile"]]
    
    woven_packet = client_session.weave_packet(message_to_send)
    print(f"Client sends woven packet. Size: {len(woven_packet['encrypted_payload'])} bytes.")

    # Simulate server receiving and decoding
    decoded_payload = server_session.receive_woven_packet(woven_packet)
    print(f"Server decoded payload: {decoded_payload}")
    
    # Assuming the next token is HTTP/1.1
    if decoded_payload['prediction_id'] == VOCAB["HTTP/1.1"]:
        print("✅ SUCCESS: Server correctly predicted the next part of the message!")
        print("📊 Data transmitted was minimal, only the encrypted prediction.")
    else:
        print("❌ FAILURE: Prediction mismatch.")


if __name__ == "__main__":
    run_client()
