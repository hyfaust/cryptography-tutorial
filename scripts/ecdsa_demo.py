#!/usr/bin/env python3
"""
ECDSA (Elliptic Curve Digital Signature Algorithm) Demonstration
================================================================
This script demonstrates ECDSA digital signature operations:
- Key pair generation on different curves
- Signing and verification
- Comparison with RSA signatures
- Deterministic vs random nonce

Dependencies: pip install cryptography
"""

import hashlib
import time
from cryptography.hazmat.primitives.asymmetric import ec, utils
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


def generate_ecdsa_keypair(curve=ec.SECP256R1()):
    """Generate an ECDSA key pair on the specified curve."""
    private_key = ec.generate_private_key(curve)
    public_key = private_key.public_key()
    return private_key, public_key


def sign_message(private_key, message: bytes) -> bytes:
    """Sign a message using ECDSA with SHA-256."""
    signature = private_key.sign(
        message,
        ec.ECDSA(hashes.SHA256()),
    )
    return signature


def verify_signature(public_key, message: bytes, signature: bytes) -> bool:
    """Verify an ECDSA signature."""
    try:
        public_key.verify(
            signature,
            message,
            ec.ECDSA(hashes.SHA256()),
        )
        return True
    except InvalidSignature:
        return False


def get_curve_info(private_key):
    """Extract curve information from a private key."""
    public_key = private_key.public_key()
    pub_numbers = public_key.public_numbers()
    curve = pub_numbers.curve
    return {
        "name": curve.name,
        "key_size": curve.key_size,
        "pub_x": pub_numbers.x,
        "pub_y": pub_numbers.y,
    }


def main():
    print("=" * 60)
    print("  ECDSA Digital Signature Demonstration")
    print("=" * 60)

    # Step 1: Generate key pair on P-256 curve
    print("\n[1] Generating ECDSA key pair (secp256r1 / P-256)...")
    private_key, public_key = generate_ecdsa_keypair(ec.SECP256R1())
    info = get_curve_info(private_key)
    print(f"    Curve: {info['name']}")
    print(f"    Key size: {info['key_size']} bits")
    print(f"    Public key X: {hex(info['pub_x'])}")
    print(f"    Public key Y: {hex(info['pub_y'])}")

    # Export keys to PEM
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    print(f"\n    Private key (PEM):")
    for line in private_pem.decode().split('\n')[:3]:
        print(f"      {line}")

    # Step 2: Sign and verify
    message = b"Hello, ECDSA signatures!"
    print(f"\n[2] Signing message: {message.decode()}")

    signature = sign_message(private_key, message)
    print(f"    Signature ({len(signature)} bytes): {signature.hex()}")
    print(f"    Signature is DER-encoded (ASN.1)")

    # Parse DER signature to get (r, s)
    from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
    r, s = decode_dss_signature(signature)
    print(f"    r = {hex(r)}")
    print(f"    s = {hex(s)}")

    is_valid = verify_signature(public_key, message, signature)
    print(f"\n[3] Verification result: {'VALID' if is_valid else 'INVALID'}")

    # Step 3: Tamper detection
    tampered = b"TAMPERED message!"
    is_valid_tampered = verify_signature(public_key, tampered, signature)
    print(f"\n[4] Tampered message verification: {'VALID' if is_valid_tampered else 'INVALID (detected!)'}")

    # Step 4: Compare different curves
    print(f"\n[5] Comparing ECDSA curves:")
    curves = [
        ("secp256r1 (P-256)", ec.SECP256R1()),
        ("secp384r1 (P-384)", ec.SECP384R1()),
        ("secp521r1 (P-521)", ec.SECP521R1()),
    ]

    for name, curve in curves:
        sk, pk = generate_ecdsa_keypair(curve)
        sig = sign_message(sk, message)
        r, s = decode_dss_signature(sig)
        print(f"    {name}:")
        print(f"      Key size: {curve.key_size} bits")
        print(f"      Signature size: {len(sig)} bytes")
        print(f"      r bit length: {r.bit_length()}, s bit length: {s.bit_length()}")

    # Step 5: ECDSA vs RSA comparison
    print(f"\n[6] ECDSA vs RSA comparison:")
    from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding

    # RSA timing
    iterations = 500
    start = time.time()
    rsa_sk = rsa.generate_private_key(65537, 2048)
    rsa_pk = rsa_sk.public_key()
    for _ in range(iterations):
        rsa_sig = rsa_sk.sign(message, rsa_padding.PSS(
            mgf=rsa_padding.MGF1(hashes.SHA256()),
            salt_length=rsa_padding.PSS.MAX_LENGTH,
        ), hashes.SHA256())
    rsa_sign_time = time.time() - start

    start = time.time()
    for _ in range(iterations):
        rsa_pk.verify(rsa_sig, message, rsa_padding.PSS(
            mgf=rsa_padding.MGF1(hashes.SHA256()),
            salt_length=rsa_padding.PSS.MAX_LENGTH,
        ), hashes.SHA256())
    rsa_verify_time = time.time() - start

    # ECDSA timing
    start = time.time()
    ecdsa_sk, ecdsa_pk = generate_ecdsa_keypair(ec.SECP256R1())
    for _ in range(iterations):
        ecdsa_sig = sign_message(ecdsa_sk, message)
    ecdsa_sign_time = time.time() - start

    start = time.time()
    for _ in range(iterations):
        verify_signature(ecdsa_pk, message, ecdsa_sig)
    ecdsa_verify_time = time.time() - start

    print(f"    {'Metric':<25} {'RSA-2048':>12} {'ECDSA P-256':>12}")
    print(f"    {'-'*25} {'-'*12} {'-'*12}")
    print(f"    {'Key size (bits)':<25} {'2048':>12} {'256':>12}")
    print(f"    {'Signature size (bytes)':<25} {len(rsa_sig):>12} {len(ecdsa_sig):>12}")
    print(f"    {'Sign speed (ops/s)':<25} {iterations/rsa_sign_time:>12.0f} {iterations/ecdsa_sign_time:>12.0f}")
    print(f"    {'Verify speed (ops/s)':<25} {iterations/rsa_verify_time:>12.0f} {iterations/ecdsa_verify_time:>12.0f}")
    print(f"    {'Security level (bits)':<25} {'112':>12} {'128':>12}")

    # Summary
    print("\n" + "=" * 60)
    print("  Summary")
    print("=" * 60)
    print("""
    ECDSA Advantages over RSA:
    - Smaller key sizes (256-bit ECDSA ~ 3072-bit RSA)
    - Smaller signatures
    - Faster signing (especially on constrained devices)
    - Same security with less computational overhead

    ECDSA Considerations:
    - Nonce (k) must be truly random and never reused
    - Nonce reuse reveals the private key!
    - Deterministic ECDSA (RFC 6979) mitigates nonce risks
    - Used in Bitcoin, Ethereum, TLS 1.3, SSH
    """)


if __name__ == "__main__":
    main()
