"""
RSA Wiener's Attack

When the private key d is small (d < n^(1/4) / 3), the Wiener attack can
recover d by computing the continued fraction expansion of e/n and checking
each convergent as a candidate for k/d.

Mathematical basis:
  e*d = k*phi(n) + 1  for some integer k
  => e/n ≈ k/d (very close approximation)
  => k/d must be a convergent of the continued fraction of e/n

Usage:
    python rsa_wiener.py
"""

import math


def continued_fraction(numerator, denominator):
    """
    Compute the continued fraction expansion of numerator/denominator.

    Returns the list of partial quotients [a0, a1, a2, ...].

    Args:
        numerator: The numerator
        denominator: The denominator

    Returns:
        List of partial quotients.
    """
    result = []
    while denominator != 0:
        q = numerator // denominator
        result.append(q)
        numerator, denominator = denominator, numerator - q * denominator
    return result


def convergents(partial_quotients):
    """
    Compute the convergents from a continued fraction's partial quotients.

    Returns a list of (numerator, denominator) tuples.

    Args:
        partial_quotients: List [a0, a1, a2, ...]

    Returns:
        List of (p_k, q_k) tuples representing convergents p_k/q_k.
    """
    convergents_list = []
    p_prev2, p_prev1 = 0, 1  # p_{-2} = 0, p_{-1} = 1
    q_prev2, q_prev1 = 1, 0  # q_{-2} = 1, q_{-1} = 0

    for a in partial_quotients:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        convergents_list.append((p, q))
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q

    return convergents_list


def wiener_attack(n, e):
    """
    Perform Wiener's attack on RSA with a small private exponent.

    Args:
        n: RSA modulus
        e: Public exponent

    Returns:
        Tuple (d, p, q) if attack succeeds, None otherwise.
    """
    print(f"\n  Computing continued fraction of e/n...")
    cf = continued_fraction(e, n)
    print(f"  Partial quotients: {cf[:15]}{'...' if len(cf) > 15 else ''}")

    convs = convergents(cf)
    print(f"  Number of convergents: {len(convs)}")

    for i, (k, d) in enumerate(convs):
        if d == 0 or k == 0:
            continue

        # Check Wiener condition
        # d < n^(1/4) / 3
        n_quarter = int(n ** 0.25)
        if d > n_quarter // 3 + 1:
            continue

        # Try: phi = (e*d - 1) / k
        # e*d - 1 must be divisible by k
        if (e * d - 1) % k != 0:
            continue

        phi = (e * d - 1) // k

        # phi = n - p - q + 1
        # p + q = n - phi + 1
        s = n - phi + 1  # s = p + q

        # Solve: x^2 - s*x + n = 0
        # discriminant = s^2 - 4*n
        discriminant = s * s - 4 * n

        if discriminant < 0:
            continue

        sqrt_disc = math.isqrt(discriminant)
        if sqrt_disc * sqrt_disc != discriminant:
            continue

        p = (s + sqrt_disc) // 2
        q = (s - sqrt_disc) // 2

        if p * q == n:
            print(f"\n  Found at convergent #{i}: k={k}, d={d}")
            print(f"  phi = {phi}")
            print(f"  p + q = {s}")
            print(f"  p = {p}")
            print(f"  q = {q}")
            return d, p, q

    return None


def verify_decryption(n, d, e, message_int):
    """Verify that encryption and decryption work correctly."""
    c = pow(message_int, e, n)
    m = pow(c, d, n)
    return m == message_int


def int_to_bytes(n):
    """Convert an integer to bytes."""
    if n == 0:
        return b'\x00'
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, 'big')


def demonstrate_continued_fraction():
    """Demonstrate continued fraction basics."""
    print("\n--- Continued Fraction Basics ---")

    # Example: 355/113 (approximation of pi)
    num, den = 355, 113
    cf = continued_fraction(num, den)
    convs = convergents(cf)

    print(f"  {num}/{den} = {num/den:.10f}")
    print(f"  Continued fraction: {cf}")
    print(f"  Convergents:")
    for p, q in convs:
        print(f"    {p}/{q} = {p/q:.10f}")


def demonstrate_wiener_basic():
    """Demonstrate Wiener attack with basic example."""
    print("=" * 50)
    print("  RSA Wiener's Attack")
    print("=" * 50)

    print("\n--- Basic Example ---")

    # Construct RSA with small d
    # Choose small d first, then compute e
    p = 9440477
    q = 9446071
    n = p * q
    phi = (p - 1) * (q - 1)

    d = 13  # Small private key! (must be coprime with phi)
    e = pow(d, -1, phi)  # Compute public key

    print(f"  p = {p}")
    print(f"  q = {q}")
    print(f"  n = {n}")
    print(f"  phi(n) = {phi}")
    print(f"  d = {d} (small!)")
    print(f"  e = {e}")

    # Check Wiener condition
    n_quarter = n ** 0.25
    print(f"\n  Wiener condition: d < n^(1/4) / 3")
    print(f"    n^(1/4) / 3 = {n_quarter / 3:.2f}")
    print(f"    d = {d}")
    print(f"    Condition met? {d < n_quarter / 3}")

    # Verify encryption/decryption
    m = 42
    c = pow(m, e, n)
    m_dec = pow(c, d, n)
    print(f"\n  Encryption test: m={m}, c={c}, decrypted={m_dec}, correct={m == m_dec}")

    # Perform attack
    print("\n  Performing Wiener attack...")
    result = wiener_attack(n, e)

    if result:
        d_rec, p_rec, q_rec = result
        print(f"\n  Attack successful!")
        print(f"  Recovered d = {d_rec}")
        print(f"  Recovered p = {p_rec}, q = {q_rec}")
        print(f"  d correct? {d_rec == d}")
        print(f"  Factorization correct? {p_rec * q_rec == n}")
    else:
        print("\n  Attack failed.")


def demonstrate_wiener_larger():
    """Demonstrate with larger parameters."""
    print("\n--- Larger Parameters Example ---")

    # 512-bit RSA with small d
    # Using actual primes for this demo
    p = 16157387885063800092468972531095442600227637936690303362357377535130907802167
    q = 68374361576449959379811878238702970795767227995234058958640265755013581201943
    n = p * q
    phi = (p - 1) * (q - 1)

    d = 123456789012349  # Relatively small d (coprime with phi)
    e = pow(d, -1, phi)

    print(f"  n: {n.bit_length()} bits")
    print(f"  d = {d} ({d.bit_length()} bits)")
    print(f"  e: {e.bit_length()} bits")

    # Check condition
    n_quarter = int(n ** 0.25)
    print(f"  n^(1/4) / 3 ≈ {n_quarter // 3}")
    print(f"  d < n^(1/4) / 3? {d < n_quarter // 3}")

    if d >= n_quarter // 3:
        print("  Wiener condition not met. Attack may fail.")
        return

    # Attack
    result = wiener_attack(n, e)
    if result:
        d_rec, p_rec, q_rec = result
        print(f"\n  Recovered d = {d_rec}")
        print(f"  Correct? {d_rec == d}")

        # Verify with a message
        m = 314159265358979
        c = pow(m, e, n)
        m_dec = pow(c, d_rec, n)
        print(f"  Decryption test: m={m}, decrypted={m_dec}, correct={m == m_dec}")


def demonstrate_ctf_scenario():
    """Demonstrate a typical CTF scenario."""
    print("\n--- CTF Scenario Simulation ---")
    print("""
  Scenario: You receive an RSA ciphertext with:
    - n (large number)
    - e (unusually large, close to n)
    - c (ciphertext)
    
  The large e suggests d might be small (since e*d ≈ k*phi(n)).
  This is a classic Wiener attack setup.
    """)

    # Simulate CTF setup
    p = 97092073796983986774381980821144125571907651350894568788100992512256398308261
    q = 39461738708185018703673131751378652946181973007918800179659849755381938321847
    n = p * q
    phi = (p - 1) * (q - 1)

    d = 98767  # Very small d (coprime with phi)
    e = pow(d, -1, phi)

    flag = "flag{w1ener_4ttack_is_c00l}"
    m = int.from_bytes(flag.encode(), 'big')
    c = pow(m, e, n)

    print(f"  Given:")
    print(f"    n = {n}")
    print(f"    e = {e}")
    print(f"    c = {c}")

    # Attack
    print("\n  Analyzing...")
    print(f"  e is very large ({e.bit_length()} bits vs n {n.bit_length()} bits)")
    print(f"  This suggests d might be small. Trying Wiener attack...")

    result = wiener_attack(n, e)
    if result:
        d_rec, p_rec, q_rec = result
        m_rec = pow(c, d_rec, n)
        flag_rec = int_to_bytes(m_rec).decode()
        print(f"\n  Decrypted flag: {flag_rec}")
        print(f"  Correct? {flag_rec == flag}")


def main():
    demonstrate_continued_fraction()
    demonstrate_wiener_basic()
    demonstrate_wiener_larger()
    demonstrate_ctf_scenario()

    print("\n" + "=" * 50)
    print("  Summary")
    print("=" * 50)
    print("""
  Wiener's attack works when:
    1. d < n^(1/4) / 3
    2. Can be detected by unusually large e

  Defense:
    - Use standard RSA key generation (d will be large)
    - Use e = 65537
    - Never choose small d for "performance"
    - Use OAEP padding for encryption
    """)


if __name__ == '__main__':
    main()
