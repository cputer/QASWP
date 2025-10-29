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
