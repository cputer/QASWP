# QASWP Python API Reference

Author: Nikolai Nedovodin (CPUTER Inc.)  
Version: 2.0 • October 2025

This reference documents the core developer surface for the
**Quantum‑Authenticated Neural Semantic Weaving Protocol (QASWP)**.

---

## Overview

A `QASWPSession` manages the complete lifecycle:
handshake (quantum + PQC), encrypted semantic messaging, context
management, and optional proof exchange.

```python
from qaswp import QASWPSession

# Client
cli = QASWPSession(is_client=True, model_id="en-text-v1")
cli.connect("example.org", 4433)
cli.handshake()
cli.send(b"Hello, QASWP!")
print(cli.receive().decode())
cli.close()
```

---

## Class: QASWPSession

```python
class QASWPSession:
    def __init__(self, is_client: bool, model_id: str, config: "SessionConfig|None" = None): ...
    def connect(self, host: str, port: int, timeout: float = 5.0) -> None: ...
    def accept(self, sock) -> None: ...
    def handshake(self) -> None: ...
    def send(self, data: bytes) -> None: ...
    def receive(self, timeout: float | None = None) -> bytes: ...
    def close(self) -> None: ...
    # properties
    @property
    def is_secure(self) -> bool: ...
    @property
    def peer_identity(self): ...
```

**Parameters**
- `is_client`: initiator role if `True`.
- `model_id`: semantic model identifier negotiated in handshake.
- `config`: optional `SessionConfig` (see below).

**Behavior**
- `handshake()` performs QKE integration (if enabled), PQ auth, key
  derivation, model negotiation, optional zk‑proof verification, and
  context initialization.
- `send()` compresses via `CompressionEngine`, protects with AEAD, and
  transmits a QASWP record.
- `receive()` verifies/decaps AEAD, decompresses with current context,
  updates context, and returns plaintext.

**Exceptions**
- `HandshakeError`, `CryptoError`, `ProofError`, `AuthenticationError`,
  `CompressionError`, `DecompressionError`, `TimeoutError`.

---

## Class: KeyExchange

```python
class KeyExchange:
    def __init__(self, is_initiator: bool, quantum_backend=None): ...
    def perform_exchange(self) -> "KeyExchangeResult": ...
    def get_shared_key(self) -> bytes: ...
    def get_handshake_messages(self) -> tuple[bytes, bytes]: ...
```

- Interfaces QKD to obtain `K_q`; performs PQ KEM and signature checks.
- Returns `KeyExchangeResult(master_secret, handshake_hash, params)`.

---

## Class: CompressionEngine

```python
class CompressionEngine:
    def __init__(self, model: "SemanticModel"): ...
    def compress(self, plaintext: bytes, context_state) -> bytes: ...
    def decompress(self, payload: bytes, context_state) -> bytes: ...
```

- Deterministic encode/decode conditioned on `context_state`.
- MUST be inverse up to task fidelity; raise on mismatch.

---

## Class: ContextWeaver

```python
class ContextWeaver:
    def __init__(self, model: "SemanticModel"): ...
    def initial_context(self): ...
    def update_context(self, prev_context, message: bytes): ...
    def merge_remote_context(self, info): ...
```

- Maintains per‑session context; supports resets/checkpoints; may accept
  quantum‑derived seeds via the session’s key schedule.

---

## Class: ProofVerifier (optional)

```python
class ProofVerifier:
    def __init__(self, verifier_key: bytes | None = None): ...
    def verify_model_proof(self, proof: bytes, expected_hash: bytes) -> bool: ...
    def generate_model_proof(self, model: "SemanticModel") -> bytes: ...
    def verify_message_proof(self, proof: bytes, message: bytes) -> bool: ...
```

- Used during handshake to attest model integrity; message proofs are
  reserved for high‑assurance flows.

---

## SessionConfig (suggested fields)

```python
@dataclass
class SessionConfig:
    use_quantum: bool = True
    require_proof: bool = False
    cipher_suites: list[str] = field(default_factory=lambda: ["AES-256-GCM+Dilithium+Kyber"])
    rekey_interval: int = 1_000
    max_context_messages: int = 2_048
    pad_buckets: list[int] | None = None   # optional length padding
    handshake_timeout: float = 5.0
```

---

## Record Layout (reference)

- `seq: uint32`
- `flags: uint8` (bit0 ContextReset, bit1 ProofAttached)
- `ctx_id: uint8`
- `len: uint16`
- `ciphertext: bytes`
- `tag: bytes` (AEAD)

AEAD AAD MUST include header fields. Rekey according to policy.

---

## Usage Notes

- Ensure identical model weights on both endpoints for the selected
  `model_id`. Exchange a hash during handshake.
- Keep inference deterministic (fixed seeds / quantum‑derived seeds).
- Periodically exchange encrypted context hashes; reset on mismatch.
- Bypass compression if `len(Z) >= len(M)`.
- Precompute model proofs if `require_proof=True` to avoid handshake
  stalls.

---

## Minimal Example (pseudo-code)

```python
sess = QASWPSession(is_client=True, model_id="en-text-v1")
sess.connect("127.0.0.1", 4433)
sess.handshake()
sess.send(b"GET /api/v1/profile HTTP/1.1")
resp = sess.receive()
sess.close()
```

---

## Error Handling

- **Decrypt fail / bad tag**: drop record; count; abort after threshold.
- **Decode fail**: request reset or abort.
- **Proof fail**: abort immediately.
- **Timeouts**: surface to caller; allow retry/abort policies.

---

## Versioning

Protocol and model versions are negotiated in the handshake. Implement
graceful refusal when no overlap exists. Keep wire compatibility
stable across minor versions; bump major for breaking changes.
