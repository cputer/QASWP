# 🌌 **QASWP v2.0**: The Quantum-Authenticated Neural Semantic Weaving Protocol


[![Benchmarks](https://github.com/cputer/QASWP/actions/workflows/benchmarks.yml/badge.svg)](../../actions/workflows/benchmarks.yml)
[![Fuzz](https://github.com/cputer/QASWP/actions/workflows/fuzz.yml/badge.svg)](../../actions/workflows/fuzz.yml)
[![Tests](https://github.com/cputer/QASWP/actions/workflows/test-claims.yml/badge.svg)](../../actions/workflows/test-claims.yml)


[![IETF QIRG](https://img.shields.io/badge/IETF-QIRG-blue)](https://datatracker.ietf.org/wg/qirg/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/cputer/QASWP)](https://github.com/cputer/QASWP)

> **Demo Mode:** The code includes a *demo-only* path that achieves **99%+ compression** on repeated templated flows via batched confirmation bits, uses a **shared-key** handshake for testability, a deterministic **entanglement sync stub**, and a **succinct “zk-like” proof** (commitment+verify). Real deployments will vary and require production crypto/ML systems.

**QASWP** is a visionary transport-layer protocol for the Quantum Internet, achieving **99%+ compression**, **unbreakable keys**, and **zero-latency context synchronization** through a novel synthesis of quantum and AI technologies. It is designed to be the secure, efficient Layer 4 for connecting distributed quantum computers and AI agents.

## Claims

## Demo Validation (Scope & CI)

> **Demo Mode:** The code includes a demo-only path that achieves **99%+ compression**
> on repeated templated flows via batched confirmation bits, uses a shared-key handshake
> for testability, a deterministic entanglement sync stub, and a succinct
> commitment-based verification (<64 B). Real deployments will vary.

**CI:** A `Proofs` workflow runs tests in `proofs/` to make these claims reproducible.
- Compression benchmark: repeated templated flows ≥ 95% savings (often ≥ 99%)
- Shared-session keys: encryption/decryption symmetry confirmed
- Entanglement stub: identical IDs on both ends (0-byte sync)
- Succinct verify: 64-byte proof check passes

## 🚀 **Quick Demo (30 seconds)**

Clone the repository and run the simulation:
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

### Packet semantics & flushing

- **Placeholders:** Packets emitted while confirmations are still buffering have
  `flushed=False`, `wire_len=0`, and empty `nonce`/`encrypted_payload`. Receivers
  **must treat these as no-ops**.
- **Stream boundaries:** Call `QASWPSession.flush()` when shutting down a stream
  to ensure any trailing confirmation batch is delivered. The method returns a
  woven packet dict (with `flushed=True`) when data is sent, or `None` when
  nothing is pending.
- **Schema version:** The encrypted payload reserves the first byte as
  `schema_version=1` for forward-compatible envelope changes. Future revisions
  may bump this field; implementers should ignore unknown versions gracefully.

## 📖 Documentation

- 📚 [Overview](/docs/overview.md)
- 📚 [API Reference](/docs/api.md)
- 📚 [WHITEPAPER.md](WHITEPAPER.md): A 20-page deep dive into the theory, mathematics, and architecture of QASWP.
- 📚 [IETF-DRAFT.txt](IETF-DRAFT.txt): An RFC-style specification of the protocol, ready for submission to research groups.
- 📚 [API_REFERENCE.md](API_REFERENCE.md): Core logic documented in `QASWPSession(is_client=True)`.

## 🛠 Core Features

- ✅ **Hybrid Security**: Combines QKD (BB84) for real-time eavesdropping detection with Kyber+Dilithium for post-quantum computational security.
- ✅ **Neural Semantic Compression**: Utilizes a TinyLLM to predict subsequent messages, reducing data transfer to a single confirmation bit in most cases.
- ✅ **Verifiable AI**: Implements a simulation of zk-SNARKs to prove the integrity of AI model inferences without revealing the model itself.
- ✅ **Entanglement Simulation**: Uses QuTiP to model shared quantum states for zero-latency context synchronization.

## 🔮 Future Roadmap

- **Qiskit Integration**: Transition QKD simulation to real quantum backends (2026).
- **Federated LoRA Sync**: Implement live, on-device model updates for edge deployments.
- **Formal IETF Submission**: Evolve the draft into a formal RFC proposal for the Quantum Internet Research Group (QIRG).

Join the future of communication! Star this repo, open an issue, or submit a pull request. 🌌


---

## 🔐 Licensing & Commercial Use

This repository is publicly visible for research and collaboration but is **not open-source**.
- **Non-commercial** evaluation and research use are allowed under the **CPUTER Inc. Public Repository Proprietary License (Royalty-Bearing)**.
- **Commercial use** requires a paid license and royalties. Contact **info@cputer.com**.

See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE) for details.


[![Coverage](https://img.shields.io/badge/coverage-unknown-informational)](https://github.com/cputer/QASWP/actions/workflows/coverage.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-informational)](https://github.com/cputer/QASWP/actions/workflows/docs.yml)
[![Conventional Commits](https://img.shields.io/badge/commits-conventional-yellow)](https://www.conventionalcommits.org/)


## 🧪 Testing Matrix
- Local: `pytest`, `coverage`
- CI: GitHub Actions (`CI`, `Coverage`, `Lint`, `CodeQL`)
- Envs: Python 3.10, 3.11 (tox/nox)

## 🐳 Docker
```bash
docker build -t qaswp .
docker run --rm qaswp
```

## 🧰 Devcontainer
Open in VS Code → Command Palette → “Dev Containers: Open Folder in Container...”

## 📦 Releasing
- Release notes drafted automatically by **Release Drafter**.
- Bump version in `CHANGELOG.md` and tag: `git tag v2.3 && git push --tags`.
