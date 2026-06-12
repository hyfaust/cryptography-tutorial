#!/usr/bin/env python3
"""
RSA Digital Signature Demonstration
====================================
This script demonstrates RSA digital signature operations:
- Key pair generation
- Signing a message
- Verifying a signature
- Tamper detection

Dependencies: pip install cryptography
"""

import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


def generate_rsa_keypair(key_size=2048):
    """Generate an RSA key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key, message: bytes) -> bytes:
    """Sign a message using RSA private key with PSS padding."""
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    """Verify an RSA signature. Returns True if valid."""
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


def sign_with_pkcs1v15(private_key, message: bytes) -> bytes:
    """Sign using PKCS#1 v1.5 padding (legacy, less secure)."""
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    return signature


def main():
    print("=" * 60)
    print("  RSA Digital Signature Demonstration")
    print("=" * 60)

    # Step 1: Generate key pair
    print("\n[1] Generating RSA-2048 key pair...")
    private_key, public_key = generate_rsa_keypair(2048)

    # Display key info
    pub_numbers = public_key.public_numbers()
    print(f"    Public exponent (e): {pub_numbers.e}")
    print(f"    Modulus (n) bit length: {pub_numbers.n.bit_length()} bits")

    # Export keys to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    print(f"\n    Private key (PEM, first 2 lines):")
    for line in private_pem.decode().split('\n')[:3]:
        print(f"      {line}")

    print(f"\n    Public key (PEM, first 2 lines):")
    for line in public_pem.decode().split('\n')[:3]:
        print(f"      {line}")

    # Step 2: Sign a message
    message = b"This is a secret message for RSA signature demo."
    print(f"\n[2] Signing message: {message.decode()}")
    print(f"    Message hash (SHA-256): {hashlib.sha256(message).hexdigest()}")

    signature = sign_message(private_key, message)
    print(f"    Signature ({len(signature)} bytes): {signature[:32].hex()}...")
    print(f"    Signature (full hex): {signature.hex()}")

    # Step 3: Verify the signature
    print(f"\n[3] Verifying signature...")
    is_valid = verify_signature(public_key, message, signature)
    print(f"    Verification result: {'VALID' if is_valid else 'INVALID'}")

    # Step 4: Tamper detection
    print(f"\n[4] Tamper detection test...")
    tampered_message = b"This is a TAMPERED message for RSA signature demo."
    print(f"    Tampered message: {tampered_message.decode()}")

    is_valid_tampered = verify_signature(public_key, tampered_message, signature)
    print(f"    Verification result: {'VALID' if is_valid_tampered else 'INVALID (tampered!)'}")

    # Step 5: Wrong key detection
    print(f"\n[5] Wrong key detection test...")
    other_private, other_public = generate_rsa_keypair(2048)
    is_valid_wrong_key = verify_signature(other_public, message, signature)
    print(f"    Verification with wrong key: {'VALID' if is_valid_wrong_key else 'INVALID (wrong key!)'}")

    # Step 6: Compare PSS vs PKCS#1 v1.5
    print(f"\n[6] Comparing signature schemes...")
    sig_pss = sign_message(private_key, message)
    sig_pkcs = sign_with_pkcs1v15(private_key, message)
    print(f"    PSS signature length:      {len(sig_pss)} bytes")
    print(f"    PKCS#1 v1.5 signature length: {len(sig_pkcs)} bytes")
    print(f"    Both produce {len(sig_pss) * 8}-bit signatures for RSA-2048")

    # Step 7: Performance test
    import time
    print(f"\n[7] Performance test (1000 sign/verify operations)...")
    iterations = 1000
    start = time.time()
    for _ in range(iterations):
        sign_message(private_key, message)
    sign_time = time.time() - start

    start = time.time()
    for _ in range(iterations):
        verify_signature(public_key, message, signature)
    verify_time = time.time() - start

    print(f"    Signing:   {iterations} ops in {sign_time:.3f}s ({iterations/sign_time:.0f} ops/s)")
    print(f"    Verifying: {iterations} ops in {verify_time:.3f}s ({iterations/verify_time:.0f} ops/s)")

    # Summary
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print("""
    RSA Digital Signatures provide:
    - Authentication: Only the private key holder can sign
    - Integrity: Any modification invalidates the signature
    - Non-repudiation: Signer cannot deny signing

    Security notes:
    - PSS padding is preferred over PKCS#1 v1.5
    - RSA-2048 is the minimum recommended key size
    - RSA-3072 or RSA-4096 for long-term security
    - Consider ECDSA for better performance with smaller keys
    """)


if __name__ == "__main__":
    main()
