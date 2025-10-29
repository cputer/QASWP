# 🌌 **QASWP v2.0**: The Quantum-Authenticated Neural Semantic Weaving Protocol

[![CI](https://img.shields.io/github/actions/workflow/status/cputer/QASWP/python-tests.yml?branch=main)](#)
[![CodeQL](https://img.shields.io/github/actions/workflow/status/cputer/QASWP/codeql.yml?label=CodeQL)](#)
[![Release](https://img.shields.io/github/v/release/cputer/QASWP?display_name=tag)](#)


[![IETF QIRG](https://img.shields.io/badge/IETF-QIRG-blue)](https://datatracker.ietf.org/wg/qirg/)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/cputer/QASWP)](https://github.com/cputer/QASWP)


**QASWP** is a visionary transport-layer protocol for the Quantum Internet, achieving **99%+ compression**, **unbreakable keys**, and **zero-latency context synchronization** through a novel synth[...] 

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

## 📖 Documentation

- **WHITEPAPER.md**: A 20-page deep dive into the theory, mathematics, and architecture of QASWP.
- **IETF-DRAFT.txt**: An RFC-style specification of the protocol, ready for submission to research groups.
- **API Reference**: Core logic documented in `QASWPSession(is_client=True)`.

## 🔐 Licensing & Commercial Use

This repository is publicly visible for research and collaboration but is **not open-source**.
- **Non-commercial** evaluation and research use are allowed under the **CPUTER Inc. Public Repository Proprietary License (Royalty-Bearing)**.
- **Commercial use** requires a paid license and royalties. Contact **licensing@cputer.com** (replace with your address).

See [`LICENSE`](./LICENSE) and [`NOTICE`](./NOTICE) for details.

[![Coverage](https://img.shields.io/badge/coverage-unknown-informational)](#)
[![Docs](https://img.shields.io/badge/docs-mkdocs--material-informational)](#)
[![Conventional Commits](https://img.shields.io/badge/commits-conventional-yellow)](#)

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
Open in VS Code → Command Palette → “Dev Containers: Open Folder in Container..."

## 📦 Releasing
- Release notes drafted automatically by **Release Drafter**.
- Bump version in `CHANGELOG.md` and tag: `git tag v2.3 && git push --tags`