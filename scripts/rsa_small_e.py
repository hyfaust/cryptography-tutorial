"""
RSA Small Public Exponent Attack

When the public exponent e is small (e.g., e=3) and the plaintext m is also
small such that m^e < n, the ciphertext C = m^e mod n equals m^e without
any modular reduction. In this case, we can simply compute the e-th root of C
to recover the plaintext.

Attack condition: m < n^(1/e)

Usage:
    python rsa_small_e.py
"""

import math


def integer_nth_root(n_val, e):
    """
    Compute the integer e-th root of n_val using Newton's method.

    Returns the exact root if n_val is a perfect e-th power,
    otherwise returns None.

    Args:
        n_val: The value to take the root of (must be non-negative)
        e: The root degree (must be >= 2)

    Returns:
        Integer e-th root if exact, None otherwise.
    """
    if n_val < 0:
        raise ValueError("Cannot compute root of negative number")
    if n_val == 0:
        return 0
    if e == 1:
        return n_val

    # Newton's method for integer nth root
    # Initial guess using floating point (may be slightly off for large numbers)
    if n_val.bit_length() < 53:  # Small enough for float
        x = int(round(n_val ** (1.0 / e)))
    else:
        # For large numbers, use bit-length based initial guess
        x = 1 << ((n_val.bit_length() + e - 1) // e)

    # Newton's iteration: x_{k+1} = ((e-1)*x_k + n_val // x_k^(e-1)) / e
    while True:
        x_prev = x
        x_pow = pow(x, e - 1)
        x = ((e - 1) * x + n_val // x_pow) // e
        if x >= x_prev:
            break

    # Verify and adjust
    if pow(x, e) == n_val:
        return x
    if pow(x + 1, e) == n_val:
        return x + 1

    return None  # Not a perfect e-th power


def integer_nth_root_floor(n_val, e):
    """
    Compute the floor of the integer e-th root of n_val.

    Args:
        n_val: The value to take the root of (must be non-negative)
        e: The root degree (must be >= 2)

    Returns:
        Floor of the integer e-th root.
    """
    if n_val < 0:
        raise ValueError("Cannot compute root of negative number")
    if n_val == 0:
        return 0
    if e == 1:
        return n_val

    # Fast path: if e is very large compared to n_val's bit length,
    # the root is 1 (since 2^e >> n_val)
    if e > n_val.bit_length():
        return 1

    # Newton's method for integer nth root
    if n_val.bit_length() < 53:
        x = int(round(n_val ** (1.0 / e)))
    else:
        x = 1 << ((n_val.bit_length() + e - 1) // e)

    while True:
        x_prev = x
        x_pow = pow(x, e - 1)
        x = ((e - 1) * x + n_val // x_pow) // e
        if x >= x_prev:
            break

    # Adjust: ensure x^e <= n_val < (x+1)^e
    while pow(x, e) > n_val:
        x -= 1
    while pow(x + 1, e) <= n_val:
        x += 1

    return x


def int_to_bytes(n):
    """Convert an integer to bytes (big-endian)."""
    if n == 0:
        return b'\x00'
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, 'big')


def small_e_attack(n, e, c):
    """
    Perform the small public exponent attack.

    Args:
        n: RSA modulus
        e: Public exponent (should be small, e.g., 3)
        c: Ciphertext (as integer)

    Returns:
        Plaintext integer if attack succeeds, None otherwise.
    """
    # Check if m^e < n is likely
    # If c itself is small compared to n, the attack likely works
    if c >= n:
        print("  Warning: C >= n, modular reduction definitely occurred.")
        print("  The attack may still work if m^e happened to equal C + k*n for some k.")
        # Try: maybe m^e = c, or m^e = c + n, c + 2n, etc.
        for k in range(0, 10000):
            candidate = c + k * n
            root = integer_nth_root(candidate, e)
            if root is not None:
                return root
        return None
    else:
        # C < n, so m^e = C (no modular reduction)
        root = integer_nth_root(c, e)
        return root


def demonstrate_basic():
    """Demonstrate the attack with basic numbers."""
    print("=" * 50)
    print("  RSA Small Public Exponent Attack")
    print("=" * 50)

    print("\n--- Basic Example ---")
    # Small RSA parameters for demonstration
    # p-1 and q-1 must both be coprime to e=3, so neither can be divisible by 3
    p, q = 101, 107
    n = p * q  # n = 10807
    phi_n = (p - 1) * (q - 1)  # 10600
    e = 3
    d = pow(e, -1, phi_n)

    m = 13  # Plaintext
    c = pow(m, e, n)  # Ciphertext

    print(f"  p = {p}, q = {q}")
    print(f"  n = {n}")
    print(f"  e = {e}")
    print(f"  d = {d}")
    print(f"  m = {m}")
    print(f"  C = m^e mod n = {c}")
    print(f"  m^e = {m**e}")
    print(f"  m^e < n? {m**e < n}")

    if m ** e < n:
        print(f"\n  Since m^e = {m**e} < n = {n}, no modular reduction occurred.")
        print(f"  C = m^e = {m**e}")
        print(f"  Therefore: m = C^(1/e) = {m**e}^(1/3) = {integer_nth_root(c, e)}")

    # Attack
    recovered = small_e_attack(n, e, c)
    print(f"\n  Attack result: m = {recovered}")
    print(f"  Correct? {recovered == m}")


def demonstrate_text():
    """Demonstrate the attack with a text message."""
    print("\n--- Text Message Example ---")

    # Generate RSA parameters
    # Using small primes for demonstration
    p = 104729  # A prime
    q = 104723  # Another prime
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 3

    # Ensure gcd(e, phi_n) = 1
    assert math.gcd(e, phi_n) == 1, f"gcd({e}, {phi_n}) = {math.gcd(e, phi_n)}"

    # Encode message as integer
    message = "Hi"
    m = int.from_bytes(message.encode(), 'big')
    print(f"  Message: '{message}'")
    print(f"  Encoded as integer: m = {m}")
    print(f"  n = {n} ({n.bit_length()} bits)")
    print(f"  e = {e}")

    # Encrypt
    c = pow(m, e, n)
    print(f"  C = m^e mod n = {c}")
    print(f"  m^e = {m**e}")
    print(f"  m^e < n? {m**e < n}")

    if m ** e < n:
        print(f"\n  Attack applicable: m^e < n")
        recovered_m = integer_nth_root(c, e)
        recovered_msg = int_to_bytes(recovered_m).decode()
        print(f"  Recovered m = {recovered_m}")
        print(f"  Recovered message: '{recovered_msg}'")
        print(f"  Correct? {recovered_msg == message}")
    else:
        print(f"\n  Attack NOT applicable: m^e >= n")
        print(f"  Would need to try: m = (C + k*n)^(1/e) for k = 0, 1, 2, ...")


def demonstrate_large():
    """Demonstrate with larger RSA parameters."""
    print("\n--- Large RSA Parameters Example ---")

    # 2048-bit RSA modulus (simplified: using a number close to 2^2048)
    n = 2 ** 2048 - 1  # Simplified; real n = p*q
    e = 3

    # Small message
    message = "Hello"
    m = int.from_bytes(message.encode(), 'big')

    print(f"  Message: '{message}'")
    print(f"  m = {m}")
    print(f"  n: {n.bit_length()}-bit number")
    print(f"  e = {e}")

    # Encrypt (m^3 < n since m is very small)
    c = pow(m, e, n)
    print(f"  C = {c}")
    print(f"  m^3 = {m**3}")
    print(f"  m^3 < n? {m**3 < n}")
    print(f"  C == m^3? {c == m**3}")

    if m ** e < n:
        recovered = integer_nth_root(c, e)
        recovered_msg = int_to_bytes(recovered).decode()
        print(f"\n  Recovered m = {recovered}")
        print(f"  Recovered message: '{recovered_msg}'")
        print(f"  Correct? {recovered_msg == message}")


def demonstrate_edge_cases():
    """Demonstrate edge cases and limitations."""
    print("\n--- Edge Cases & Limitations ---")

    n = 2 ** 2048 - 1
    e = 3

    # Case 1: Message just barely fits
    max_m = integer_nth_root_floor(n, e)
    print(f"  Max m for e=3 attack: {max_m}")
    print(f"  Max m in bytes: ~{max_m.bit_length() // 8} bytes")
    print(f"  (This means messages up to ~{max_m.bit_length() // 8} bytes can be attacked)")

    # Case 2: Message too large
    print(f"\n  If message is larger than {max_m.bit_length()} bits:")
    print(f"  m^e will exceed n, and modular reduction will occur.")
    print(f"  The attack will fail (need other methods).")

    # Case 3: Larger e
    e = 65537
    max_m_e65537 = integer_nth_root_floor(n, e)
    if max_m_e65537 is not None:
        print(f"\n  For e=65537: max m ≈ {max_m_e65537.bit_length()} bits")
        print(f"  This is only {max_m_e65537.bit_length() // 8} bytes — attack window is tiny!")
    else:
        print(f"\n  For e=65537: m^e < n only for extremely tiny m (a few bits)")
        print(f"  This is why e=65537 is safe against this attack.")


def main():
    demonstrate_basic()
    demonstrate_text()
    demonstrate_large()
    demonstrate_edge_cases()

    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
  Small public exponent attack works when:
    1. e is small (typically e=3)
    2. m^e < n (no modular reduction)
    
  Defense:
    - Use e = 65537 (standard practice)
    - Use OAEP padding (ensures m is large)
    - Never use raw RSA without padding
    """)


if __name__ == '__main__':
    main()
