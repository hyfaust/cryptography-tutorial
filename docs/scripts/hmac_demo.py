#!/usr/bin/env python3
"""
HMAC Generation and Verification Demo
Demonstrates HMAC (Hash-based Message Authentication Code) usage.

Covers:
- Basic HMAC generation with different hash algorithms
- HMAC verification (correct key, wrong key, tampered message)
- Timing attack demonstration
- API authentication simulation

Usage:
    python hmac_demo.py              # Full demo
    python hmac_demo.py --basic      # Basic HMAC operations
    python hmac_demo.py --verify     # Verification demo
    python hmac_demo.py --timing     # Timing attack demo
"""

import hmac
import hashlib
import time
import sys
import os
import secrets


def generate_hmac(key: str, message: str, algorithm: str = "sha256") -> str:
    """
    Generate an HMAC for the given message using the specified algorithm.

    Args:
        key: Secret key for HMAC
        message: Message to authenticate
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)

    Returns:
        Hex-encoded HMAC value
    """
    return hmac.new(
        key.encode("utf-8"),
        message.encode("utf-8"),
        getattr(hashlib, algorithm),
    ).hexdigest()


def verify_hmac(
    key: str, message: str, received_mac: str, algorithm: str = "sha256"
) -> bool:
    """
    Verify an HMAC value using constant-time comparison.

    Args:
        key: Secret key
        message: Original message
        received_mac: HMAC value to verify
        algorithm: Hash algorithm used

    Returns:
        True if HMAC is valid, False otherwise
    """
    computed_mac = generate_hmac(key, message, algorithm)
    return hmac.compare_digest(computed_mac, received_mac)


def insecure_verify_hmac(
    key: str, message: str, received_mac: str, algorithm: str = "sha256"
) -> bool:
    """
    INSECURE HMAC verification using regular string comparison.

    WARNING: This is vulnerable to timing attacks. Never use in production!
    """
    computed_mac = generate_hmac(key, message, algorithm)
    return computed_mac == received_mac


def demonstrate_basic_hmac():
    """Show basic HMAC operations with different algorithms."""
    print("=" * 56)
    print("  HMAC Basic Operations")
    print("=" * 56)
    print()

    message = "Hello, this is a secret message."
    key = "my_secret_key"

    print(f"Message: {message}")
    print(f"Key:     {key}")
    print()

    algorithms = ["md5", "sha1", "sha256", "sha512"]
    print("--- HMAC with Different Algorithms ---")
    print()
    for algo in algorithms:
        mac = generate_hmac(key, message, algo)
        print(f"HMAC-{algo.upper():<7}: {mac}")

    print()
    print("--- Same Message, Different Keys ---")
    print()
    keys = ["key_A", "key_B", "key_C"]
    for k in keys:
        mac = generate_hmac(k, message, "sha256")
        print(f"Key '{k}': {mac}")

    print()
    print("--- Same Key, Different Messages ---")
    print()
    messages = [
        "Transfer $100 to Alice",
        "Transfer $100 to Bob",
        "Transfer $1000 to Alice",
    ]
    for m in messages:
        mac = generate_hmac(key, m, "sha256")
        print(f"'{m}': {mac[:40]}...")


def demonstrate_verification():
    """Show HMAC verification scenarios."""
    print("=" * 56)
    print("  HMAC Verification Demo")
    print("=" * 56)
    print()

    key = "my_secret_key"
    message = "Transfer $1000 to account #12345"

    # Generate HMAC
    mac = generate_hmac(key, message)
    print(f"Message: {message}")
    print(f"HMAC:    {mac}")
    print()

    # Scenario 1: Correct verification
    print("--- Scenario 1: Correct Key, Correct Message ---")
    result = verify_hmac(key, message, mac)
    print(f"Result: {'PASS' if result else 'FAIL'}")
    print()

    # Scenario 2: Wrong key
    print("--- Scenario 2: Wrong Key ---")
    result = verify_hmac("wrong_key", message, mac)
    print(f"Result: {'PASS' if result else 'FAIL'}")
    print()

    # Scenario 3: Tampered message
    print("--- Scenario 3: Tampered Message ---")
    tampered = "Transfer $9999 to account #99999"
    result = verify_hmac(key, tampered, mac)
    print(f"Original:  {message}")
    print(f"Tampered:  {tampered}")
    print(f"Result:    {'PASS' if result else 'FAIL'}")
    print()

    # Scenario 4: Tampered HMAC
    print("--- Scenario 4: Tampered HMAC ---")
    tampered_mac = mac[:-4] + "0000"
    result = verify_hmac(key, message, tampered_mac)
    print(f"Original HMAC: {mac}")
    print(f"Tampered HMAC: {tampered_mac}")
    print(f"Result:        {'PASS' if result else 'FAIL'}")


def demonstrate_timing_attack():
    """Demonstrate timing difference between secure and insecure verification."""
    print("=" * 56)
    print("  Timing Attack Demonstration")
    print("=" * 56)
    print()

    key = "my_secret_key"
    message = "secret data"
    correct_mac = generate_hmac(key, message)

    # Test with different wrong MACs
    wrong_macs = [
        correct_mac[:-1] + ("0" if correct_mac[-1] != "0" else "1"),  # 1 char wrong
        "0" + correct_mac[1:],  # First char wrong
        "0" * len(correct_mac),  # Completely wrong
    ]

    num_trials = 10000

    print("Comparing timing for different verification methods:")
    print(f"(Each measurement is {num_trials:,} trials)")
    print()

    for i, wrong_mac in enumerate(wrong_macs):
        desc = ["Last char wrong", "First char wrong", "Completely wrong"][i]

        # Insecure comparison
        start = time.perf_counter()
        for _ in range(num_trials):
            insecure_verify_hmac(key, message, wrong_mac)
        insecure_time = time.perf_counter() - start

        # Secure comparison
        start = time.perf_counter()
        for _ in range(num_trials):
            verify_hmac(key, message, wrong_mac)
        secure_time = time.perf_counter() - start

        print(f"  {desc}:")
        print(f"    String '==':   {insecure_time:.4f}s")
        print(f"    compare_digest: {secure_time:.4f}s")
        print()

    print("NOTE: The timing difference is usually very small and hard to")
    print("measure reliably, but attackers with network access can amplify")
    print("the difference through repeated measurements.")


def demonstrate_api_authentication():
    """Simulate HMAC-based API authentication."""
    print("=" * 56)
    print("  API Authentication Simulation")
    print("=" * 56)
    print()

    # Server side: store API keys and secrets
    api_keys = {
        "user_alice": "alice_super_secret_key_256bit",
        "user_bob": "bob_super_secret_key_256bit",
    }

    # Client side: Alice wants to make an API request
    api_key = "user_alice"
    api_secret = api_keys[api_key]
    timestamp = str(int(time.time()))
    request_body = '{"action": "transfer", "amount": 1000}'

    # Construct the message to sign
    sign_message = f"{api_key}:{timestamp}:{request_body}"

    # Generate HMAC signature
    signature = generate_hmac(api_secret, sign_message)

    print(f"API Key:     {api_key}")
    print(f"Timestamp:   {timestamp}")
    print(f"Request:     {request_body}")
    print(f"Sign Message: {sign_message}")
    print(f"Signature:   {signature}")
    print()

    # Server side: verify the request
    print("--- Server Verification ---")

    # Reconstruct the message
    server_message = f"{api_key}:{timestamp}:{request_body}"
    server_secret = api_keys[api_key]
    server_signature = generate_hmac(server_secret, server_message)

    if hmac.compare_digest(signature, server_signature):
        print("Request authenticated: ACCEPTED")
    else:
        print("Authentication failed: REJECTED")

    print()

    # Test with forged request
    print("--- Forged Request (wrong secret) ---")
    forged_message = f"{api_key}:{timestamp}:{request_body}"
    forged_signature = generate_hmac("wrong_secret", forged_message)

    if hmac.compare_digest(forged_signature, server_signature):
        print("Request authenticated: ACCEPTED (should not happen!)")
    else:
        print("Authentication failed: REJECTED (correct behavior)")

    print()
    print("--- Expired Request (replay attack simulation) ---")
    old_timestamp = str(int(time.time()) - 600)  # 10 minutes ago
    old_message = f"{api_key}:{old_timestamp}:{request_body}"
    old_signature = generate_hmac(api_secret, old_message)
    print(f"Old timestamp: {old_timestamp} (10 minutes ago)")
    print("Server would reject this if timestamp validation is implemented.")


def main():
    if "--basic" in sys.argv:
        demonstrate_basic_hmac()
    elif "--verify" in sys.argv:
        demonstrate_verification()
    elif "--timing" in sys.argv:
        demonstrate_timing_attack()
    else:
        demonstrate_basic_hmac()
        print()
        demonstrate_verification()
        print()
        demonstrate_timing_attack()
        print()
        demonstrate_api_authentication()


if __name__ == "__main__":
    main()
