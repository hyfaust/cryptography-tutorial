"""
Randomness attack simulations.

Demonstrates real-world consequences of weak random number generation:
1. ECDSA nonce reuse => private key leakage (Sony PS3 style)
2. Weak seed => predictable keys

Usage:
    python randomness_attack.py                # Run all demos
    python randomness_attack.py --ecdsa        # ECDSA nonce reuse attack
    python randomness_attack.py --weakseed     # Weak seed attack
"""

import argparse
import hashlib
import os
import random as insecure_random
import secrets
import time

try:
    from sympy import mod_inverse, isprime, nextprime
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False
    print("[!] sympy not installed; some demos will use fallback implementations.")


# ---------- Fallback number theory (if sympy not available) ----------

def _mod_inverse(a, m):
    """Extended Euclidean algorithm for modular inverse."""
    if HAS_SYMPY:
        return int(mod_inverse(a, m))
    g, x, _ = _extended_gcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse")
    return x % m


def _extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = _extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


# ---------- Simplified ECDSA for demo ----------

class SimpleECDSA:
    """Simplified ECDSA over a small prime field for educational demo.

    NOT a real elliptic curve implementation. Uses modular arithmetic
    to illustrate the nonce-reuse attack mathematically.
    """

    def __init__(self, n=None):
        # Use a large prime (simplified: we work in Z_n* instead of on a curve)
        if n is None:
            # A 256-bit prime (simplified)
            self.n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
        else:
            self.n = n

    def keygen(self):
        """Generate a private key x and public key y = g^x mod n (simplified)."""
        x = secrets.randbelow(self.n - 1) + 1  # private key
        g = 2  # generator (simplified)
        y = pow(g, x, self.n)  # public key
        return x, y

    def _hash_message(self, msg):
        """Hash message to integer."""
        h = hashlib.sha256(msg.encode() if isinstance(msg, str) else msg).digest()
        return int.from_bytes(h, "big") % self.n

    def sign(self, msg, private_key, k=None):
        """Sign message. If k is provided, use it (for demo of reuse attack)."""
        z = self._hash_message(msg)
        if k is None:
            k = secrets.randbelow(self.n - 1) + 1
        g = 2
        r = pow(g, k, self.n) % self.n
        k_inv = _mod_inverse(k, self.n)
        s = (k_inv * (z + private_key * r)) % self.n
        return r, s, k

    def verify(self, msg, signature, public_key):
        """Verify signature (simplified)."""
        r, s = signature
        z = self._hash_message(msg)
        g = 2
        s_inv = _mod_inverse(s, self.n)
        u1 = (z * s_inv) % self.n
        u2 = (r * s_inv) % self.n
        v = (pow(g, u1, self.n) * pow(public_key, u2, self.n)) % self.n
        return v % self.n == r


def demo_ecdsa_nonce_reuse():
    """
    Demonstrate the Sony PS3 ECDSA nonce-reuse attack.

    If the same k is used in two ECDSA signatures:
      s1 = k^{-1} * (z1 + x*r) mod n
      s2 = k^{-1} * (z2 + x*r) mod n

    Then:
      s1 - s2 = k^{-1} * (z1 - z2) mod n
      k = (z1 - z2) / (s1 - s2) mod n
      x = (s1*k - z1) / r mod n
    """
    print("=" * 60)
    print("ECDSA Nonce Reuse Attack (Sony PS3 Style)")
    print("=" * 60)

    ecdsa = SimpleECDSA()

    # Key generation
    private_key, public_key = ecdsa.keygen()
    print(f"\n[1] Key Generation:")
    print(f"  Private key x: {hex(private_key)[:40]}...")
    print(f"  Public key y:  {hex(public_key)[:40]}...")

    # Sign two messages with the SAME k (the vulnerability!)
    msg1 = "Transaction: Send 100 coins to Alice"
    msg2 = "Transaction: Send 50 coins to Bob"
    fixed_k = secrets.randbelow(ecdsa.n - 1) + 1  # Fixed k (the bug!)

    print(f"\n[2] Signing two messages with SAME k (the vulnerability!):")
    print(f"  Fixed k: {hex(fixed_k)[:40]}...")

    r1, s1, _ = ecdsa.sign(msg1, private_key, k=fixed_k)
    r2, s2, _ = ecdsa.sign(msg2, private_key, k=fixed_k)

    print(f"\n  Signature 1 (msg1):")
    print(f"    r = {hex(r1)[:40]}...")
    print(f"    s = {hex(s1)[:40]}...")
    print(f"\n  Signature 2 (msg2):")
    print(f"    r = {hex(r2)[:40]}...")
    print(f"    s = {hex(s2)[:40]}...")

    # Attack: recover private key
    print(f"\n[3] ATTACK: Recovering private key from two signatures...")

    z1 = ecdsa._hash_message(msg1)
    z2 = ecdsa._hash_message(msg2)

    # k = (z1 - z2) / (s1 - s2) mod n
    k_recovered = ((z1 - z2) * _mod_inverse((s1 - s2) % ecdsa.n, ecdsa.n)) % ecdsa.n

    # x = (s1*k - z1) / r mod n
    x_recovered = ((s1 * k_recovered - z1) * _mod_inverse(r1, ecdsa.n)) % ecdsa.n

    print(f"  Recovered k: {hex(k_recovered)[:40]}...")
    print(f"  Recovered x: {hex(x_recovered)[:40]}...")

    # Verify
    match = (x_recovered == private_key)
    print(f"\n[4] Verification:")
    print(f"  Recovered key == Original key: {match}")

    if match:
        print(f"\n  [!] PRIVATE KEY LEAKED!")
        print(f"  The attacker can now forge signatures for any message.")
        print(f"  This is exactly what happened to Sony PS3 in 2010.")

    # Show the math
    print(f"\n[5] The Math Behind the Attack:")
    print(f"""
  ECDSA signature:
    s = k^(-1) * (z + x*r) mod n

  Two signatures with same k, same r:
    s1 = k^(-1) * (z1 + x*r) mod n
    s2 = k^(-1) * (z2 + x*r) mod n

  Subtract:
    s1 - s2 = k^(-1) * (z1 - z2) mod n

  Solve for k:
    k = (z1 - z2) * (s1 - s2)^(-1) mod n

  Solve for x (private key):
    x = (s1*k - z1) * r^(-1) mod n
""")


def demo_weak_seed():
    """Demonstrate predictable keys from weak seeding."""
    print("=" * 60)
    print("Weak Seed Attack: Predictable Random Keys")
    print("=" * 60)

    # Simulate a vulnerable system using time-based seed
    print("\n[1] Scenario: A server generates AES keys using random.seed(time)")
    print("    This was the Netscape SSL vulnerability (1995).\n")

    # "Server" generates a key with weak seed
    server_seed = int(time.time())
    insecure_random.seed(server_seed)

    # Generate a 128-bit AES key
    key_bytes = bytes([insecure_random.randint(0, 255) for _ in range(16)])
    print(f"  Server generated AES-128 key:")
    print(f"  Key (hex): {key_bytes.hex()}")
    print(f"  Seed (epoch): {server_seed}")

    # Attacker brute-forces the seed
    print(f"\n[2] Attack: Brute-forcing the time-based seed...")
    found = False
    # Simulate: attacker knows the approximate time (within 60 seconds)
    for trial_seed in range(server_seed - 60, server_seed + 61):
        insecure_random.seed(trial_seed)
        trial_key = bytes([insecure_random.randint(0, 255) for _ in range(16)])
        if trial_key == key_bytes:
            print(f"  [+] FOUND! Seed = {trial_seed}")
            print(f"  [+] Key recovered: {trial_key.hex()}")
            found = True
            break

    if not found:
        print("  [-] Not found in this demo (timing window too narrow)")

    # Compare with secure approach
    print(f"\n[3] Comparison: Secure key generation")
    secure_key = secrets.token_bytes(16)
    print(f"  Secure key (hex): {secure_key.hex()}")
    print(f"  Generated by: OS CSPRNG (no predictable seed)")
    print(f"  Brute-force difficulty: 2^128 = {2**128:.2e} possibilities")

    # Show the impact
    print(f"\n[4] Impact Summary:")
    print(f"  Weak seed search space:   ~2^16 (65536 seconds ~ 18 hours)")
    print(f"  Secure key search space:  2^128 = 3.4 x 10^38")
    print(f"  Ratio: 2^112 times harder to crack secure keys")
    print()

    # Debian OpenSSL bug simulation
    print("[5] Debian OpenSSL Bug (2008) Simulation:")
    print("  A developer removed two lines of entropy-collection code.")
    print("  Result: only PID (15 bits) was used as entropy.")
    print(f"  Search space: 2^15 = {2**15} = {2**15} possibilities")
    print("  All SSH keys generated on affected systems were crackable.\n")

    # Simulate: only PID as seed
    simulated_pid = 12345
    insecure_random.seed(simulated_pid)
    debian_key = bytes([insecure_random.randint(0, 255) for _ in range(16)])
    print(f"  Simulated Debian key (PID={simulated_pid}):")
    print(f"  Key (hex): {debian_key.hex()}")

    print(f"\n  Attacker only needs to try {2**15} PIDs to find the key!")
    print(f"  That takes less than 1 second on modern hardware.")


def main():
    parser = argparse.ArgumentParser(description="Randomness attack demos")
    parser.add_argument("--ecdsa", action="store_true",
                        help="ECDSA nonce reuse attack")
    parser.add_argument("--weakseed", action="store_true",
                        help="Weak seed attack")
    args = parser.parse_args()

    run_all = not any([args.ecdsa, args.weakseed])

    if run_all or args.ecdsa:
        demo_ecdsa_nonce_reuse()
    if run_all or args.weakseed:
        demo_weak_seed()


if __name__ == "__main__":
    main()
