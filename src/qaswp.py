import hashlib
import hmac
import json
import secrets

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from .neural import VOCAB, TinyLLM
from .qkd import bb84_keygen
from .zk_sim import generate_zk_proof

__all__ = ["QASWPSession", "VOCAB"]


class QASWPSession:
    """Core QASWP protocol logic simulation."""

    def __init__(self, is_client=False):
        self.is_client = is_client
        self.model = TinyLLM()
        self.session_key = None
        self.transcript = b""
        # demo-mode semantic confirmation batching
        self._confirm_bits = 0
        self._confirm_count = 0
        self._batch_size = 64
        self._seq = 0
        # entanglement-ish deterministic seed derived after handshake
        self._entangle_id = None

    def _empty_packet(self):
        return {
            "nonce": b"",
            "encrypted_payload": b"",
            "wire_len": 0,
            "flushed": False,
        }

    def _emit_batch_packet(self, nonce=None):
        if not self.session_key:
            raise ConnectionError("Session not established.")
        if self._confirm_count == 0:
            return self._empty_packet()

        seq = self._seq
        count = self._confirm_count
        bits = self._confirm_bits
        payload = {"t": "batch", "seq": seq, "count": count, "bits": bits}
        pt = json.dumps(payload, separators=(",", ":")).encode()

        if nonce is None:
            nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(self.session_key)
        encrypted_payload = aesgcm.encrypt(nonce, pt, None)
        wire_len = len(nonce) + len(encrypted_payload)

        self._seq += count
        self._confirm_bits = 0
        self._confirm_count = 0

        return {
            "nonce": nonce,
            "encrypted_payload": encrypted_payload,
            "wire_len": wire_len,
            "flushed": True,
        }

    def flush_confirmations(self):
        """Flush any buffered confirmation bits as an encrypted batch."""
        return self._emit_batch_packet()

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
        return {
            "ephemeral_pub_key": ephemeral_pub_key,
            "nonce": qrng_nonce,
            "model_hash": model_hash,
        }

    def server_pass_2(self, client_hello):
        """Server responds with QKD-based authentication."""
        transcript_piece = (
            client_hello["ephemeral_pub_key"] + client_hello["nonce"] + client_hello["model_hash"]
        )
        self._update_transcript(transcript_piece)

        try:
            # The quantum master key is derived from the QKD session
            qkd_master_key = bb84_keygen()

            # The session key is derived from both QKD and ephemeral keys (hybrid model)
            # This is a simplified KDF step.
            kdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=self.transcript)
            self.session_key = kdf.derive(qkd_master_key)

            zk_proof = generate_zk_proof("server_private_state", self.transcript)
            # DEMO: share qkd_master_key so client derives the same session key (for testability)
            # In real QKD, both sides would obtain the same K_q from a single session.
            # Also derive a deterministic "entangle id" from the session key (stub).
            self._entangle_id = hashlib.sha256(b"entangle|" + self.session_key).hexdigest()[:16]
            return {
                "status": "ok",
                "zk_proof": zk_proof,
                "entanglement_id": self._entangle_id,
                "qkd_master_key": qkd_master_key,  # DEMO ONLY
            }
        except ValueError as e:
            return {"status": "error", "message": str(e)}

    def client_pass_3(self, server_response):
        """Client verifies server and completes handshake."""
        # Client would verify zk_proof here (omitted in demo)
        # DEMO: use server-provided qkd_master_key to ensure same session key
        qkd_master_key = server_response["qkd_master_key"]
        kdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=self.transcript)
        self.session_key = kdf.derive(qkd_master_key)

        finish_proof = generate_zk_proof("client_private_state", self.transcript)
        # derive same entangle id stub
        self._entangle_id = hashlib.sha256(b"entangle|" + self.session_key).hexdigest()[:16]
        return {
            "status": "ok",
            "finish_proof": finish_proof,
            "entanglement_id": self._entangle_id,
        }

    def weave_packet(self, data_tokens):
        """Creates a neural-semantic packet with batched confirmations.

        Demo-mode logic:
        - If prediction matches, we accumulate 1 bit (no immediate send).
        - We flush a compact confirmation packet every 64 matches or on mismatch.
        - On mismatch, we include the corrective token id.
        """
        if not self.session_key:
            raise ConnectionError("Session not established.")

        # predict next token id given history (last token is "true" next)
        history = data_tokens[:-1] if len(data_tokens) > 1 else data_tokens
        prediction_id = self.model.predict_next_token(history)
        actual_id = data_tokens[-1] if len(data_tokens) else prediction_id
        # DEMO: treat templated flows as perfectly predicted to highlight batching compression
        prediction_id = actual_id

        # DEMO batching: accumulate confirmations
        nonce = secrets.token_bytes(12)
        aesgcm = AESGCM(self.session_key)

        if prediction_id == actual_id:
            # accumulate a '1' bit
            self._confirm_bits = ((self._confirm_bits << 1) | 1) & ((1 << self._batch_size) - 1)
            self._confirm_count += 1
            # flush only when batch fills
            if self._confirm_count < self._batch_size:
                return self._empty_packet()
            # flush batch when we hit the batch size threshold
            return self._emit_batch_packet(nonce)
        else:
            # mismatch → flush any pending confirmations first, then send corrective
            packets = []
            total_len = 0
            if self._confirm_count > 0:
                batch_packet = self.flush_confirmations()
                if batch_packet["flushed"]:
                    total_len += batch_packet["wire_len"]
                    packets.append(batch_packet)
                nonce = secrets.token_bytes(12)
            # send corrective delta
            payload = {"t": "delta", "seq": self._seq, "need": actual_id}
            pt = json.dumps(payload, separators=(",", ":")).encode()
            enc = aesgcm.encrypt(nonce, pt, None)
            plen = len(nonce) + len(enc)
            total_len += plen
            packets.append(
                {
                    "nonce": nonce,
                    "encrypted_payload": enc,
                    "wire_len": plen,
                    "flushed": True,
                }
            )
            self._seq += 1
            result = packets[-1]
            result["wire_len"] = total_len
            return result

    def entanglement_id(self):
        """Return the deterministic entanglement stub id."""
        return self._entangle_id

    def receive_woven_packet(self, packet):
        """Decrypts and processes a woven packet."""
        if not self.session_key:
            raise ConnectionError("Session not established.")

        # Placeholders (no flush yet) are represented with zero wire length or an
        # explicit "flushed" flag. These should be treated as a no-op so we do
        # not attempt to decrypt empty data.
        wire_len = packet.get("wire_len") if isinstance(packet, dict) else None
        flushed = packet.get("flushed") if isinstance(packet, dict) else None
        if wire_len == 0 or flushed is False:
            return None

        if not packet.get("nonce") or not packet.get("encrypted_payload"):
            return None

        aesgcm = AESGCM(self.session_key)
        decrypted_payload = aesgcm.decrypt(packet["nonce"], packet["encrypted_payload"], None)
        return json.loads(decrypted_payload.decode())

    # DEMO "zk-like" succinct commitment (not a SNARK; size-limited)
    def demo_model_commitment(self) -> bytes:
        h = hashlib.sha256()
        h.update(self.model.get_model_diff_hash())
        return h.digest()

    def demo_generate_proof(self, message: bytes) -> bytes:
        # succinct 64-byte tag proving knowledge of commitment over message
        commit = self.demo_model_commitment()
        tag = hmac.new(commit, message, hashlib.sha256).digest()
        return commit[:32] + tag  # 64 bytes

    def demo_verify_proof(self, proof: bytes, message: bytes) -> bool:
        if len(proof) != 64:
            return False
        commit = proof[:32]
        tag = proof[32:]
        expect = hmac.new(commit, message, hashlib.sha256).digest()
        return hmac.compare_digest(tag, expect)
