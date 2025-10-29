import hashlib


def generate_zk_proof(private_input, public_input):
    """
    A simplified mock of a zk-SNARK proof generation.
    In reality, this involves complex polynomial commitments (e.g., Groth16).
    This simulation just proves knowledge of a private input that hashes to a public input.
    """
    # The "proof" is just a hash of the private and public inputs.
    # A verifier with the public input can't reverse it, but a prover can generate it.
    proof_data = str(private_input).encode() + str(public_input).encode()
    return hashlib.sha256(proof_data).digest()


def verify_zk_proof(proof, public_input, expected_private_input):
    """
    A mock verifier. A real verifier wouldn't need the private input.
    This just shows that the proof is consistent.
    """
    expected_proof = generate_zk_proof(expected_private_input, public_input)
    return proof == expected_proof


if __name__ == "__main__":
    # Scenario: Alice's AI model made a prediction. She wants to prove it was correct
    # without revealing the exact state of her model (private_input).

    ai_model_state = {"param1": 0.123, "param2": -0.456}  # Private input
    prediction_result = 42  # Public input

    # Alice generates a proof
    proof = generate_zk_proof(ai_model_state, prediction_result)
    print(f"Generated ZK Proof: {proof.hex()}")

    # Bob verifies the proof (with knowledge of the model for this simulation)
    is_valid = verify_zk_proof(proof, prediction_result, ai_model_state)
    print(f"Proof is valid: {is_valid}")

    # Eve tries to forge a proof without the correct model state
    fake_model_state = {"param1": 0.999}
    is_fake_valid = verify_zk_proof(proof, prediction_result, fake_model_state)
    print(f"Fake proof is valid: {is_fake_valid}")
