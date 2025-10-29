import numpy as np

def bb84_keygen(length=256, eve_is_present=False, noise_level=0.01):
    """
    Simulates the BB84 Quantum Key Distribution protocol.
    Returns a shared secret key or raises a ValueError if an eavesdropper is detected.
    
    Args:
        length (int): The initial number of qubits to be sent.
        eve_is_present (bool): If True, simulates an intercept-resend attack.
        noise_level (float): The intrinsic error rate of the quantum channel.

    Returns:
        bytes: The derived shared secret key.
    
    Raises:
        ValueError: If the Quantum Bit Error Rate (QBER) exceeds the security threshold.
    """
    # 1. Alice generates her bits and bases
    alice_bits = np.random.randint(0, 2, length)
    alice_bases = np.random.randint(0, 2, length)  # 0 for rectilinear, 1 for diagonal

    # 2. Bob generates his bases
    bob_bases = np.random.randint(0, 2, length)

    # 3. Eve's attack (if present)
    transmitted_bits = alice_bits.copy()
    if eve_is_present:
        eve_bases = np.random.randint(0, 2, length)
        # Eve measures and resends, introducing errors where bases don't match
        error_mask = alice_bases != eve_bases
        transmitted_bits[error_mask] = np.random.randint(0, 2, length)[error_mask]

    # 4. Bob measures
    # Bob gets the correct bit only if his basis matches Alice's (or Eve's resend)
    bob_bits = transmitted_bits.copy()
    
    # 5. Sifting: Alice and Bob publicly compare bases and keep only matching ones
    sift_mask = alice_bases == bob_bases
    
    # 6. Parameter Estimation: They compare a subset of sifted bits to estimate QBER
    alice_sifted = alice_bits[sift_mask]
    bob_sifted = bob_bits[sift_mask]
    
    # Add channel noise
    noise_errors = np.random.random(len(bob_sifted)) < noise_level
    bob_sifted[noise_errors] = 1 - bob_sifted[noise_errors]

    # Calculate QBER
    if len(alice_sifted) == 0:
        raise ValueError("No sifted bits; channel unusable.")
    qber = np.mean(alice_sifted != bob_sifted)
    
    # Security check
    security_threshold = 0.11  # Theoretical threshold for BB84
    if qber > security_threshold:
        raise ValueError(f"Eavesdropper detected! QBER of {qber:.2%} exceeds threshold of {security_threshold:.2%}.")
    
    # 7. Key Generation: Use the remaining sifted bits as the key
    # In a real protocol, error correction and privacy amplification would follow.
    # For simulation, we'll assume the remaining bits form the key.
    final_key_bits = alice_sifted[: len(alice_sifted) // 2]  # Use half for key, half for testing
    
    return np.packbits(final_key_bits).tobytes()

if __name__ == "__main__":
    try:
        # Scenario 1: No eavesdropper
        secure_key = bb84_keygen(length=4096, eve_is_present=False)
        print(f"✅ Secure key established successfully. Length: {len(secure_key)} bytes.")
        
        # Scenario 2: With an eavesdropper
        print("\nSimulating with an eavesdropper...")
        insecure_key = bb84_keygen(length=4096, eve_is_present=True)
    except ValueError as e:
        print(f"🔴 {e}")
