# 🌌 QASWP — Quantum-AI Secure Weaving Protocol

[![Benchmarks](https://github.com/cputer/QASWP/actions/workflows/benchmarks.yml/badge.svg)](../../actions/workflows/benchmarks.yml)
[![Fuzz](https://github.com/cputer/QASWP/actions/workflows/fuzz.yml/badge.svg)](../../actions/workflows/fuzz.yml)
[![Tests](https://github.com/cputer/QASWP/actions/workflows/claim-tests.yml/badge.svg)](https://github.com/cputer/QASWP/actions/workflows/claim-tests.yml)
[![Qiskit Smoke](https://github.com/cputer/QASWP/actions/workflows/qiskit.yml/badge.svg)](../../actions/workflows/qiskit.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: CPUTER Proprietary](https://img.shields.io/badge/license-CPUTER--Proprietary-red.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/cputer/QASWP)](https://github.com/cputer/QASWP)
[![IETF QIRG](https://img.shields.io/badge/IETF-QIRG-blue)](https://datatracker.ietf.org/wg/qirg/)

---

### Overview

**QASWP** is a hybrid **Quantum Key Distribution (QKD)** + **Neural Semantic Transport** framework for the **Quantum Internet**, achieving predictive compression, verifiable AI inference, and context synchronization between distributed agents.

It fuses quantum security primitives with neural-semantic prediction to create a verifiable, low-latency Layer 4 protocol connecting quantum computers and AI systems.

---

### Demo Mode

The **demo-only** path demonstrates ≥ 99 % *semantic compression* on repeated templated flows via batched confirmation bits.  
It uses a shared-key handshake for testability, a deterministic entanglement sync stub, and a succinct “zk-like” proof (commitment + verify).  
Real deployments will vary and require production-grade crypto/ML systems.

---

## 📈 Claims & Validation

**CI:** The `Proofs` workflow in `/proofs/` runs reproducible validation tests:

- **Compression benchmark:** templated flows ≥ 95 % savings (typically ≥ 99 %)  
- **Shared-session keys:** encryption/decryption symmetry confirmed  
- **Entanglement stub:** identical IDs on both ends (0-byte sync)  
- **Succinct verify:** 64-byte proof check passes  

---

## 🚀 Quick Demo (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server in one terminal
python examples/server.py

# 3. Run the client in another terminal
python examples/client.py
```

**Expected Output:**

```text
[QASWP Server] Listening for quantum-neural connections...
[QASWP Client] Handshake successful! QBER=0.00% | Session Key derived.
[QASWP Client] Alice predicts next message: "GET /api/v1/profile"
[QASWP Server] Bob predicts next message:  "GET /api/v1/profile"
[Result] Neural Prediction MATCH! (0 bytes of payload transmitted)
[Stats] Compression Ratio: 99.8% 🚀
```

---

### Packet Semantics & Flushing

* **Placeholders:** non-flushed packets have `flushed=False`, `wire_len=0`, and empty `nonce`/`payload`; receivers must treat them as **no-ops**.
* **Stream boundaries:** call `QASWPSession.flush()` before shutdown to emit trailing confirmations.
* **Schema version:** first byte of encrypted payload is `schema_version=1` for forward compatibility.

---

## 📖 Documentation

* [Overview](/docs/overview.md)
* [API Reference](/docs/api.md)
* [WHITEPAPER.md](WHITEPAPER.md): 20-page technical deep dive
* [IETF-DRAFT.txt](IETF-DRAFT.txt): RFC-style specification
* [API_REFERENCE.md](API_REFERENCE.md): core logic (`QASWPSession(is_client=True)`)

---

## 🛠 Core Features

* ✅ **Hybrid Security:** combines QKD (BB84) for eavesdrop detection with Kyber + Dilithium for post-quantum safety
* ✅ **Neural Semantic Compression:** TinyLLM prediction → single-bit confirmation
* ✅ **Verifiable AI:** zk-proof-like inference verification
* ✅ **Entanglement Simulation:** QuTiP-based shared-state model for zero-latency context sync

---

## 🔮 Future Roadmap

* **Qiskit Integration:** transition QKD to real quantum backends (2026)
* **Federated LoRA Sync:** live on-device model updates for edge nodes
* **Formal IETF Submission:** evolve draft → RFC proposal for QIRG

---

## 🔐 Licensing & Commercial Use

Public for research and collaboration, but **not open-source**.

* Non-commercial research use allowed under the **CPUTER Inc. Proprietary License (Royalty-Bearing)**
* Commercial use requires a paid license and royalties
* Contact **[info@cputer.com](mailto:info@cputer.com)** for licensing

See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE).

---

### Qiskit-Backed QKD (v2.2 Scaffold)

Feature-flagged optional handshake using Qiskit (IBM Quantum).

```bash
export QASWP_QISKIT=1
pip install qiskit
pytest -q tests/test_qiskit_stub.py
pytest -q tests/test_qiskit_integration_optional.py
```

In CI, the **Qiskit Smoke** workflow can be triggered manually; it installs Qiskit best-effort and skips cleanly if unavailable.

> Current scaffold returns a deterministic 32-byte demo key.
> Future revisions will derive real keys from Qiskit circuits (Samplers / Estimators).

---

### ⚖️ Theoretical Limits & Semantic Compression

In classical information theory, the **Shannon limit** defines the lower bound for lossless compression, set by source entropy ( H(X) ).
QASWP does **not** violate that law.
Its “99 % compression” describes **semantic efficiency**—reducing transmitted bits when peers share predictive context.

[
\text{Effective compression} = 1 - \frac{H(Δ|Ψ)}{H(M)}
]

When ( H(Δ|Ψ)\to0 ), apparent compression approaches 100 %, but total entropy remains consistent with Shannon’s theorem.

**References**

* Shannon (1948) *A Mathematical Theory of Communication*
* Zhang et al. (2023) *Semantic Communication Networks*
* Nedovodin (2025) *QASWP v2.1 Technical Report*

---

### Applicability & Limitations

QASWP excels in structured, context-rich exchanges (telemetry, control-plane, federated updates) where TinyLLM predictions minimize payloads.<br>
Unstructured or high-entropy streams gain little benefit, prompting fallback to classical compression or full-payload transfer.<br>
Hybrid QKD+PQC encryption, authenticated sequencing, and model rotation mitigate replay, leakage, and disclosure risks.

---

## 🧪 Testing Matrix

* Local: `pytest`, `coverage`
* CI: GitHub Actions (CI, Coverage, Lint, CodeQL)
* Environments: Python 3.10 – 3.11 (tox/nox)

---

## 🐳 Docker

```bash
docker build -t qaswp .
docker run --rm qaswp
```

---

## 🧰 Dev Container

Open in VS Code → “Dev Containers: Open Folder in Container…”

---

## 📦 Releasing

* Release notes via **Release Drafter**
* Version bump in `CHANGELOG.md` → `git tag v2.3 && git push --tags`

---

Join the future of communication 🌌 — Star this repo, open issues, or submit PRs.

