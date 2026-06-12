"""
RSA Common Modulus Attack

When the same plaintext m is encrypted with the same modulus n but different
public exponents e1 and e2 (where gcd(e1, e2) = 1), the plaintext can be
recovered without knowing the private key.

Attack:
  C1 = m^e1 mod n
  C2 = m^e2 mod n

  Using Extended GCD: s*e1 + t*e2 = 1
  Then: m = C1^s * C2^t mod n

Usage:
    python rsa_common_modulus.py
"""

import math


def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.

    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).

    Args:
        a: First integer
        b: Second integer

    Returns:
        Tuple (gcd, x, y)
    """
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def mod_inverse(a, m):
    """
    Compute the modular multiplicative inverse of a modulo m.

    Args:
        a: The number to find inverse of
        m: The modulus

    Returns:
        The modular inverse, or raises ValueError if it doesn't exist.
    """
    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist: gcd({a}, {m}) = {gcd}")
    return x % m


def common_modulus_attack(n, e1, e2, c1, c2):
    """
    Perform the common modulus attack.

    Given:
      - n: shared RSA modulus
      - e1, e2: two different public exponents (gcd(e1, e2) = 1)
      - c1: ciphertext encrypted with (e1, n)
      - c2: ciphertext encrypted with (e2, n)

    Returns:
      The plaintext m.

    Raises:
      ValueError: If gcd(e1, e2) != 1 (attack not applicable).
    """
    # Step 1: Extended GCD to find s, t such that s*e1 + t*e2 = 1
    gcd, s, t = extended_gcd(e1, e2)

    if gcd != 1:
        raise ValueError(
            f"gcd(e1, e2) = {gcd} != 1. "
            f"The common modulus attack requires gcd(e1, e2) = 1."
        )

    print(f"  Extended GCD: {s}*{e1} + {t}*{e2} = {gcd}")
    print(f"  s = {s}, t = {t}")

    # Step 2: Compute m = C1^s * C2^t mod n
    # Handle negative exponents by computing modular inverse
    m = 1

    if s >= 0:
        m = (m * pow(c1, s, n)) % n
    else:
        # C1^(-|s|) mod n = (C1^(-1))^|s| mod n
        c1_inv = mod_inverse(c1, n)
        m = (m * pow(c1_inv, -s, n)) % n
        print(f"  C1^(-1) mod n = {c1_inv}")

    if t >= 0:
        m = (m * pow(c2, t, n)) % n
    else:
        c2_inv = mod_inverse(c2, n)
        m = (m * pow(c2_inv, -t, n)) % n
        print(f"  C2^(-1) mod n = {c2_inv}")

    return m


def int_to_bytes(n):
    """Convert an integer to bytes (big-endian)."""
    if n == 0:
        return b'\x00'
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, 'big')


def demonstrate_basic():
    """Demonstrate with basic numbers."""
    print("=" * 50)
    print("  RSA Common Modulus Attack")
    print("=" * 50)

    print("\n--- Basic Example ---")

    # Small RSA parameters
    p, q = 61, 53
    n = p * q  # 3233
    e1 = 17
    e2 = 3
    m = 123  # Plaintext

    print(f"  p = {p}, q = {q}")
    print(f"  n = {n}")
    print(f"  e1 = {e1}, e2 = {e2}")
    print(f"  m = {m}")

    # Encrypt with both public keys
    c1 = pow(m, e1, n)
    c2 = pow(m, e2, n)
    print(f"\n  C1 = m^e1 mod n = {m}^{e1} mod {n} = {c1}")
    print(f"  C2 = m^e2 mod n = {m}^{e2} mod {n} = {c2}")

    # Verify gcd condition
    gcd_e = math.gcd(e1, e2)
    print(f"\n  gcd(e1, e2) = gcd({e1}, {e2}) = {gcd_e}")
    if gcd_e != 1:
        print("  Attack NOT applicable (gcd != 1)")
        return

    # Attack
    print("\n  Performing common modulus attack...")
    recovered_m = common_modulus_attack(n, e1, e2, c1, c2)

    print(f"\n  Recovered m = {recovered_m}")
    print(f"  Original m  = {m}")
    print(f"  Correct? {recovered_m == m}")


def demonstrate_text():
    """Demonstrate with a text message."""
    print("\n--- Text Message Example ---")

    # Larger parameters
    p = 104729
    q = 104723
    n = p * q  # 10,967,446,867
    e1 = 65537
    e2 = 3

    # Verify gcd condition
    assert math.gcd(e1, e2) == 1, f"gcd({e1}, {e2}) = {math.gcd(e1, e2)}"

    # Encode message
    message = "CTF"
    m = int.from_bytes(message.encode(), 'big')

    print(f"  Message: '{message}'")
    print(f"  m = {m}")
    print(f"  n = {n} ({n.bit_length()} bits)")
    print(f"  e1 = {e1}, e2 = {e2}")

    # Encrypt twice
    c1 = pow(m, e1, n)
    c2 = pow(m, e2, n)
    print(f"\n  C1 = {c1}")
    print(f"  C2 = {c2}")

    # Attack
    print("\n  Performing common modulus attack...")
    recovered_m = common_modulus_attack(n, e1, e2, c1, c2)
    recovered_msg = int_to_bytes(recovered_m).decode()

    print(f"\n  Recovered m = {recovered_m}")
    print(f"  Recovered message: '{recovered_msg}'")
    print(f"  Correct? {recovered_msg == message}")


def demonstrate_large():
    """Demonstrate with large RSA parameters."""
    print("\n--- Large RSA Parameters (1024-bit) Example ---")

    # Simulate 1024-bit RSA
    # Using product of two large primes (simplified)
    p = 2 ** 512 + 105  # Not actually prime, for demo purposes
    q = 2 ** 512 + 583  # Not actually prime, for demo purposes
    n = p * q
    e1 = 65537
    e2 = 17

    # For demo, use a small message
    message = "Secret"
    m = int.from_bytes(message.encode(), 'big')

    print(f"  Message: '{message}'")
    print(f"  m = {m}")
    print(f"  n: {n.bit_length()}-bit number")
    print(f"  e1 = {e1}, e2 = {e2}")

    # Encrypt
    c1 = pow(m, e1, n)
    c2 = pow(m, e2, n)
    print(f"  C1 = {c1}")
    print(f"  C2 = {c2}")

    # Verify gcd
    print(f"  gcd({e1}, {e2}) = {math.gcd(e1, e2)}")

    # Attack
    print("\n  Performing common modulus attack...")
    recovered_m = common_modulus_attack(n, e1, e2, c1, c2)
    recovered_msg = int_to_bytes(recovered_m).decode()

    print(f"\n  Recovered m = {recovered_m}")
    print(f"  Recovered message: '{recovered_msg}'")
    print(f"  Correct? {recovered_msg == message}")


def demonstrate_math_details():
    """Show the detailed mathematical derivation."""
    print("\n--- Mathematical Details ---")
    print("""
  The Common Modulus Attack relies on the following:

  Given:
    C1 = m^e1 mod n
    C2 = m^e2 mod n
    gcd(e1, e2) = 1

  By the Extended Euclidean Algorithm, find s, t such that:
    s * e1 + t * e2 = 1

  Then:
    C1^s * C2^t mod n
    = (m^e1)^s * (m^e2)^t mod n
    = m^(s*e1) * m^(t*e2) mod n
    = m^(s*e1 + t*e2) mod n
    = m^1 mod n
    = m

  Note: If s < 0, compute C1^(-1) mod n first, then raise to |s|.
  Similarly for t < 0.
    """)

    # Concrete example
    print("  Concrete Example:")
    e1, e2 = 17, 3
    gcd, s, t = extended_gcd(e1, e2)
    print(f"    e1 = {e1}, e2 = {e2}")
    print(f"    Extended GCD: {s}*{e1} + {t}*{e2} = {s*e1 + t*e2}")
    print(f"    s = {s}, t = {t}")

    # Show the step-by-step computation
    n = 3233
    m = 123
    c1 = pow(m, e1, n)
    c2 = pow(m, e2, n)
    print(f"\n    n = {n}, m = {m}")
    print(f"    C1 = {c1}, C2 = {c2}")

    if s >= 0:
        print(f"    C1^{s} = {pow(c1, s, n)}")
    else:
        c1_inv = mod_inverse(c1, n)
        print(f"    C1^(-1) mod n = {c1_inv}")
        print(f"    (C1^(-1))^{abs(s)} mod n = {pow(c1_inv, abs(s), n)}")

    if t >= 0:
        print(f"    C2^{t} = {pow(c2, t, n)}")
    else:
        c2_inv = mod_inverse(c2, n)
        print(f"    C2^(-1) mod n = {c2_inv}")
        print(f"    (C2^(-1))^{abs(t)} mod n = {pow(c2_inv, abs(t), n)}")


def main():
    demonstrate_basic()
    demonstrate_text()
    demonstrate_large()
    demonstrate_math_details()

    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
  Common modulus attack works when:
    1. Same plaintext m encrypted with same n
    2. Two different public exponents e1, e2
    3. gcd(e1, e2) = 1

  Defense:
    - Never reuse the same modulus n for different key pairs
    - Always generate fresh primes for each RSA key
    - Use standard RSA libraries that prevent this
    """)


if __name__ == '__main__':
    main()
