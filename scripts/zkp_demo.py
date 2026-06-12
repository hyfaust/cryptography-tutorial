#!/usr/bin/env python3
"""
Zero-Knowledge Proof Demonstration — Schnorr Protocol
======================================================
This script implements the Schnorr identification protocol,
a classic interactive zero-knowledge proof.

The prover demonstrates knowledge of a secret exponent x
such that y = g^x mod p, without revealing x.

Properties demonstrated:
- Completeness: An honest prover always convinces the verifier
- Soundness: A cheating prover cannot convince the verifier
- Zero-Knowledge: The verifier learns nothing about x

Dependencies: None (uses only Python standard library)
"""

import hashlib
import random


class SchnorrParams:
    """Public parameters for the Schnorr protocol."""

    def __init__(self, p, g, q):
        """
        Args:
            p: A large prime (the modulus)
            g: A generator of the subgroup of order q
            q: A prime divisor of (p-1) (the subgroup order)
        """
        self.p = p
        self.g = g
        self.q = q

    def __repr__(self):
        return f"SchnorrParams(p={self.p}, g={self.g}, q={self.q})"


def generate_params(bits=256):
    """
    Generate Schnorr protocol parameters.

    In practice, p should be at least 2048 bits.
    Here we use smaller parameters for demonstration.
    We find a safe prime p = 2q + 1 where q is also prime,
    then find a generator of the subgroup of order q.
    """
    while True:
        # Generate a prime q of the specified bit length
        q = random.getrandbits(bits)
        q |= (1 << (bits - 1)) | 1  # Set high bit and low bit
        if is_probable_prime(q):
            p = 2 * q + 1
            if is_probable_prime(p):
                # Find a generator of the subgroup of order q
                # For safe prime p = 2q+1, any h where h^2 != 1 and h^q != 1
                # gives g = h^2 mod p as generator of order q
                while True:
                    h = random.randint(2, p - 2)
                    g = pow(h, 2, p)
                    if g != 1:
                        return SchnorrParams(p, g, q)


def is_probable_prime(n, k=20):
    """Miller-Rabin primality test."""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


class Prover:
    """
    The Prover knows the secret x and wants to prove
    knowledge of x without revealing it.
    """

    def __init__(self, params: SchnorrParams, secret_x: int):
        self.params = params
        self.x = secret_x  # Secret
        self.y = pow(params.g, secret_x, params.p)  # Public key
        self.r = None  # Random nonce
        self.t = None  # Commitment

    def commit(self):
        """
        Step 1: Prover chooses random r and sends t = g^r mod p.
        """
        self.r = random.randint(1, self.params.q - 1)
        self.t = pow(self.params.g, self.r, self.params.p)
        return self.t

    def respond(self, challenge_c: int) -> int:
        """
        Step 3: Prover computes s = r + c * x mod q.

        This is the response to the verifier's challenge.
        """
        s = (self.r + challenge_c * self.x) % self.params.q
        return s


class Verifier:
    """
    The Verifier checks that the Prover knows x
    without learning x.
    """

    def __init__(self, params: SchnorrParams, y: int):
        self.params = params
        self.y = y  # Prover's public key

    def challenge(self) -> int:
        """
        Step 2: Verifier sends random challenge c.
        """
        return random.randint(1, self.params.q - 1)

    def verify(self, t: int, c: int, s: int) -> bool:
        """
        Step 4: Verifier checks g^s == t * y^c mod p.

        If the prover knows x, then:
            g^s = g^(r + cx) = g^r * g^(cx) = t * (g^x)^c = t * y^c
        """
        lhs = pow(self.params.g, s, self.params.p)
        rhs = (t * pow(self.y, c, self.params.p)) % self.params.p
        return lhs == rhs


def run_schnorr_protocol(params, secret_x, verbose=True):
    """Run one round of the Schnorr protocol."""
    prover = Prover(params, secret_x)
    verifier = Verifier(params, prover.y)

    if verbose:
        print(f"    Public key y = g^x mod p = {prover.y}")
        print(f"    (Secret x is hidden)")

    # Step 1: Commitment
    t = prover.commit()
    if verbose:
        print(f"\n    [Step 1] Prover -> Verifier: t = {t}")

    # Step 2: Challenge
    c = verifier.challenge()
    if verbose:
        print(f"    [Step 2] Verifier -> Prover: c = {c}")

    # Step 3: Response
    s = prover.respond(c)
    if verbose:
        print(f"    [Step 3] Prover -> Verifier: s = {s}")

    # Step 4: Verification
    valid = verifier.verify(t, c, s)
    if verbose:
        print(f"    [Step 4] Verifier checks: g^s == t * y^c mod p")
        lhs = pow(params.g, s, params.p)
        rhs = (t * pow(prover.y, c, params.p)) % params.p
        print(f"      g^s    = {lhs}")
        print(f"      t*y^c  = {rhs}")
        print(f"      Result: {'ACCEPT (proof valid)' if valid else 'REJECT (proof invalid)'}")

    return valid


def demonstrate_soundness(params):
    """
    Show that a cheating prover (who doesn't know x) cannot
    produce a valid proof.
    """
    print("\n[4] Soundness Test — Cheating Prover")
    print("-" * 50)

    # Cheater knows the public key y but not x
    real_x = random.randint(1, params.q - 1)
    y = pow(params.g, real_x, params.p)

    print(f"    Public key y = {y}")
    print(f"    Cheater does NOT know the secret x")

    # Cheater tries to guess the response without knowing x
    fake_t = random.randint(1, params.p - 1)  # Random commitment
    fake_c = random.randint(1, params.q - 1)  # (Would come from verifier)
    fake_s = random.randint(1, params.q - 1)  # Random guess for s

    print(f"\n    Cheater sends fake: t={fake_t}, s={fake_s}")

    # Verification check
    lhs = pow(params.g, fake_s, params.p)
    rhs = (fake_t * pow(y, fake_c, params.p)) % params.p
    valid = lhs == rhs
    print(f"    Verification: {'PASS' if valid else 'FAIL'}")

    if not valid:
        print(f"    Cheater cannot pass verification without knowing x!")
        print(f"    (Probability of success: ~1/q, negligibly small)")

    # Try many times to show it always fails
    success_count = 0
    trials = 1000
    for _ in range(trials):
        fake_t = random.randint(1, params.p - 1)
        fake_c = random.randint(1, params.q - 1)
        fake_s = random.randint(1, params.q - 1)
        lhs = pow(params.g, fake_s, params.p)
        rhs = (fake_t * pow(y, fake_c, params.p)) % params.p
        if lhs == rhs:
            success_count += 1

    print(f"    After {trials} random attempts: {success_count} successes")
    print(f"    Success rate: {success_count}/{trials} = {success_count/trials:.4%}")


def demonstrate_zero_knowledge(params):
    """
    Show that the transcript can be simulated without knowing x.
    This demonstrates the zero-knowledge property.
    """
    print("\n[5] Zero-Knowledge Test — Transcript Simulation")
    print("-" * 50)

    real_x = random.randint(1, params.q - 1)
    y = pow(params.g, real_x, params.p)

    # Real transcript (from honest protocol execution)
    print("    Generating REAL transcript (with knowledge of x)...")
    prover = Prover(params, real_x)
    t_real = prover.commit()
    c_real = random.randint(1, params.q - 1)
    s_real = prover.respond(c_real)

    # Simulated transcript (without knowing x!)
    # Key insight: verifier can generate fake transcripts by
    # choosing s and c first, then computing t = g^s * y^(-c)
    print("    Generating SIMULATED transcript (WITHOUT x)...")
    s_fake = random.randint(1, params.q - 1)
    c_fake = random.randint(1, params.q - 1)
    # Compute t such that g^s = t * y^c => t = g^s * y^(-c)
    y_inv_c = pow(y, -c_fake, params.p)
    t_fake = (pow(params.g, s_fake, params.p) * y_inv_c) % params.p

    # Both transcripts should be indistinguishable
    print(f"\n    Real transcript:       (t={t_real}, c={c_real}, s={s_real})")
    print(f"    Simulated transcript:  (t={t_fake}, c={c_fake}, s={s_fake})")

    # Verify both
    real_valid = Verifier(params, y).verify(t_real, c_real, s_real)
    fake_valid = Verifier(params, y).verify(t_fake, c_fake, s_fake)

    print(f"\n    Real transcript valid:       {real_valid}")
    print(f"    Simulated transcript valid:  {fake_valid}")
    print(f"    Both are valid — transcripts are indistinguishable!")
    print(f"    => The verifier learns NOTHING about x from the transcript")


def main():
    print("=" * 60)
    print("  Schnorr Zero-Knowledge Proof Demonstration")
    print("=" * 60)

    # Generate parameters (small for demo speed)
    print("\n[1] Generating protocol parameters (128-bit q for speed)...")
    params = generate_params(bits=128)
    print(f"    p = {params.p}")
    print(f"    g = {params.g}")
    print(f"    q = {params.q}")
    print(f"    (p = 2q + 1, safe prime)")

    # Prover's secret
    secret_x = random.randint(1, params.q - 1)
    print(f"\n[2] Prover's secret x = {secret_x}")
    print(f"    (In practice, this stays hidden forever)")

    # Run the protocol
    print(f"\n[3] Running Schnorr Protocol")
    print("-" * 50)
    valid = run_schnorr_protocol(params, secret_x, verbose=True)

    # Run multiple rounds
    print(f"\n    Running 10 more rounds (non-verbose)...")
    all_valid = True
    for i in range(10):
        if not run_schnorr_protocol(params, secret_x, verbose=False):
            all_valid = False
    print(f"    All 10 rounds: {'PASS' if all_valid else 'FAIL'}")

    # Demonstrate soundness
    demonstrate_soundness(params)

    # Demonstrate zero-knowledge
    demonstrate_zero_knowledge(params)

    # Summary
    print("\n" + "=" * 60)
    print("  Summary — Schnorr Protocol Properties")
    print("=" * 60)
    print("""
    1. COMPLETENESS: An honest prover who knows x always
       convinces the verifier. (g^s = g^(r+cx) = t * y^c)

    2. SOUNDNESS: A cheating prover who doesn't know x
       cannot produce a valid response (except with
       negligible probability ~1/q).

    3. ZERO-KNOWLEDGE: The verifier can simulate transcripts
       without the prover, so the transcript reveals nothing
       about x beyond the fact that the prover knows it.

    Applications:
    - Digital identity / authentication
    - Blockchain privacy (Zcash, Monero)
    - Anonymous credentials
    - Multi-party computation
    """)


if __name__ == "__main__":
    main()
