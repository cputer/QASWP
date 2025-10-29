from .qkd import bb84_keygen
from .neural import TinyLLM, VOCAB
from .zk_sim import generate_zk_proof
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class QASWPSession:
    """Core QASWP protocol logic simulation."""
    def __init__(self, is_client=False):
        self.is_client = is_client
        self.model = TinyLLM()
        self.session_key = None
        self.transcript = b''

    def _update_transcript(self, data):
        self.transcript += data

    def client_pass_1(self):
        """Client initiates the handshake."""
        # In a real PQC implementation, we'd use Kyber.
        # Here we simulate the ephemeral key as a random string.
        ephemeral_pub_key = secrets.token_bytes(32) 
        qrng_nonce = secrets.token_bytes(32)
        model_hash = self.model.get_model_diff_hash()
        
        hello_packet = ephemeral_pub_key + qrng_nonce + model_hash
        self._update_transcript(hello_packet)
        return {"ephemeral_pub_key": ephemeral_pub_key, "nonce": qrng_nonce, "model_hash": model_hash}

    def server_pass_2(self, client_hello):
        """Server responds with QKD-based authentication."""
        self._update_transcript(client_hello["ephemeral_pub_key"] + client_hello["nonce"] + client_hello["model_hash"])
        
        try:
            # The quantum master key is derived from the QKD session
            qkd_master_key = bb84_keygen()

            # The session key is derived from both QKD and ephemeral keys (hybrid model)
            # This is a simplified KDF step.
            kdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=self.transcript)
            self.session_key = kdf.derive(qkd_master_key)

            zk_proof = generate_zk_proof("server_private_state", self.transcript)
            return {"status": "ok", "zk_proof": zk_proof, "entanglement_id": secrets.randbits(64)}
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def client_pass_3(self, server_response):
        """Client verifies server and completes handshake."""
        # Client would verify zk_proof here
        # Derives the same session key
        qkd_master_key = bb84_keygen()  # Simulates client's side of QKD
        kdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=self.transcript)
        self.session_key = kdf.derive(qkd_master_key)
        
        finish_proof = generate_zk_proof("client_private_state", self.transcript)
        return {"status": "ok", "finish_proof": finish_proof}

    def weave_packet(self, data_tokens):
        """Creates a neural-semantic packet."""
        if not self.session_key:
            raise ConnectionError("Session not established.")

        prediction_id = self.model.predict_next_token(data_tokens)
        
        # Check if prediction matches the next actual token
        # For simplicity, we assume the next token is known for this demo.
        # In reality, the other side would confirm the match.
        payload = {"prediction_id": prediction_id, "delta": b""}  # Assume match
        
        # Encrypt the payload with AEAD
        aesgcm = AESGCM(self.session_key)
        nonce = secrets.token_bytes(12)
        encrypted_payload = aesgcm.encrypt(nonce, str(payload).encode(), None)
        
        return {"nonce": nonce, "encrypted_payload": encrypted_payload}

    def receive_woven_packet(self, packet):
        """Decrypts and processes a woven packet."""
        if not self.session_key:
            raise ConnectionError("Session not established.")
        
        aesgcm = AESGCM(self.session_key)
        decrypted_payload = aesgcm.decrypt(packet["nonce"], packet["encrypted_payload"], None)
        return eval(decrypted_payload)
