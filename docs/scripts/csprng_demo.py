"""
CSPRNG algorithm implementation demo.

Demonstrates HMAC-DRBG (simplified) and OpenSSL random generation.

Usage:
    python csprng_demo.py               # Run all demos
    python csprng_demo.py --hmac        # HMAC-DRBG demo
    python csprng_demo.py --openssl     # OpenSSL integration
    python csprng_demo.py --platform    # Platform CSPRNG info
"""

import argparse
import hashlib
import hmac
import os
import platform
import secrets
import struct
import subprocess
import time


class HMAC_DRBG:
    """Simplified HMAC-DRBG implementation (NIST SP 800-90A).

    This is for educational purposes only. Use the OS CSPRNG in production.
    """

    def __init__(self, entropy, personalization=b""):
        # Instantiate: V = Key, K = 0x00 * hlen
        self.hash_func = hashlib.sha256
        self.hlen = 32
        self.key = b"\x00" * self.hlen
        self.value = b"\x01" * self.hlen
        self._update(entropy + personalization)
        self.reseed_counter = 1

    def _hmac(self, key, data):
        return hmac.new(key, data, self.hash_func).digest()

    def _update(self, provided_data):
        self.key = self._hmac(self.key, self.value + b"\x00" + provided_data)
        self.value = self._hmac(self.key, self.value)

        if provided_data:
            self.key = self._hmac(self.key, self.value + b"\x01" + provided_data)
            self.value = self._hmac(self.key, self.value)

    def generate(self, num_bytes):
        """Generate num_bytes of pseudorandom output."""
        if self.reseed_counter > 2**48:
            raise RuntimeError("Reseed required")

        result = b""
        while len(result) < num_bytes:
            self.value = self._hmac(self.key, self.value)
            result += self.value

        self._update(b"")
        self.reseed_counter += 1
        return result[:num_bytes]

    def reseed(self, new_entropy):
        """Reseed with fresh entropy."""
        self._update(new_entropy)
        self.reseed_counter = 1


def demo_hmac_drbg():
    """Demonstrate HMAC-DRBG operation."""
    print("=" * 60)
    print("HMAC-DRBG (Simplified) Demo")
    print("=" * 60)

    # Initial entropy (in production, from OS CSPRNG)
    entropy = os.urandom(32)
    personalization = b"demo-csprng-v1"

    print(f"\n[1] Instantiation:")
    print(f"  Entropy input:      {entropy.hex()[:40]}...")
    print(f"  Personalization:    {personalization.decode()}")
    print(f"  Hash function:      SHA-256")

    drbg = HMAC_DRBG(entropy, personalization)

    # Generate output
    print(f"\n[2] Generate 64 bytes:")
    output1 = drbg.generate(64)
    print(f"  Output: {output1.hex()[:60]}...")

    # Generate more (state updated internally)
    print(f"\n[3] Generate 64 more bytes (state updated):")
    output2 = drbg.generate(64)
    print(f"  Output: {output2.hex()[:60]}...")
    print(f"  Different from first: {output1 != output2}")

    # Same seed => same output (deterministic)
    print(f"\n[4] Determinism test (same seed):")
    drbg2 = HMAC_DRBG(entropy, personalization)
    output3 = drbg2.generate(64)
    print(f"  Same seed => same output: {output1 == output3}")

    # Reseed
    print(f"\n[5] Reseed with new entropy:")
    new_entropy = os.urandom(32)
    drbg.reseed(new_entropy)
    output4 = drbg.generate(64)
    print(f"  New entropy:    {new_entropy.hex()[:40]}...")
    print(f"  Output:         {output4.hex()[:60]}...")
    print(f"  Different after reseed: {output1 != output4}")

    # Security properties
    print(f"\n[6] Security properties:")
    print(f"  Forward secrecy:  YES (state updated after each generate)")
    print(f"  Backward secrecy: YES (reseed with fresh entropy)")
    print(f"  Output indist.:   YES (computationally indistinguishable)")
    print()


def demo_openssl():
    """Show OpenSSL random generation commands."""
    print("=" * 60)
    print("OpenSSL CSPRNG Demo")
    print("=" * 60)

    print("\n[1] openssl rand - generate random bytes:")
    print("  Commands:")
    print("    openssl rand -hex 16       # 16 bytes as hex (32 chars)")
    print("    openssl rand -base64 32    # 32 bytes as base64")
    print("    openssl rand -out file.bin 1024  # 1024 bytes to file")

    # Actually run openssl rand
    print("\n[2] Live output from openssl rand:")
    commands = [
        ("openssl rand -hex 16", "16 bytes hex"),
        ("openssl rand -hex 32", "32 bytes hex (AES-256 key)"),
        ("openssl rand -base64 24", "24 bytes base64"),
    ]

    for cmd, desc in commands:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True,
                                    timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"  {desc}:")
                print(f"    $ {cmd}")
                print(f"    {output}")
            else:
                print(f"  {desc}: openssl error - {result.stderr.strip()}")
        except FileNotFoundError:
            print(f"  {desc}: openssl not found in PATH")
        except Exception as e:
            print(f"  {desc}: {e}")

    # Performance
    print("\n[3] Performance comparison:")
    n = 10000
    start = time.perf_counter()
    for _ in range(n):
        os.urandom(32)
    t_os = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(n):
        secrets.token_bytes(32)
    t_secrets = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(n):
        hashlib.sha256(b"test").digest()
    t_hash = time.perf_counter() - start

    print(f"  {n} iterations:")
    print(f"    os.urandom(32):       {t_os:.3f}s")
    print(f"    secrets.token_bytes:  {t_secrets:.3f}s")
    print(f"    hashlib.sha256:       {t_hash:.3f}s  (for reference)")
    print()


def demo_platform():
    """Show platform-specific CSPRNG information."""
    print("=" * 60)
    print("Platform CSPRNG Information")
    print("=" * 60)

    print(f"\n  OS:          {platform.system()} {platform.release()}")
    print(f"  Python:      {platform.python_version()}")
    print(f"  Architecture:{platform.machine()}")

    system = platform.system()
    if system == "Linux":
        print(f"\n  CSPRNG:      ChaCha20-based (kernel 4.8+)")
        print(f"  Device:      /dev/urandom")
        try:
            with open("/proc/sys/kernel/random/entropy_avail") as f:
                print(f"  Entropy:     {f.read().strip()} bits available")
        except:
            pass
    elif system == "Windows":
        print(f"\n  CSPRNG:      BCryptGenRandom (AES-CTR based)")
        print(f"  API:         CryptGenRandom / BCryptGenRandom")
    elif system == "Darwin":
        print(f"\n  CSPRNG:      Yarrow / Fortuna")
        print(f"  Device:      /dev/urandom")

    print(f"\n  Python backends:")
    print(f"    secrets       -> os.urandom() -> OS CSPRNG")
    print(f"    os.urandom()  -> direct OS CSPRNG call")
    print(f"    random.SystemRandom -> os.urandom()")

    # Verify all backends produce different output
    print(f"\n  Verification (each call produces unique output):")
    for name, func in [
        ("os.urandom(16)", lambda: os.urandom(16).hex()),
        ("secrets.token_hex(16)", lambda: secrets.token_hex(16)),
        ("secrets.token_bytes(16).hex()", lambda: secrets.token_bytes(16).hex()),
    ]:
        vals = [func() for _ in range(3)]
        all_unique = len(set(vals)) == 3
        print(f"    {name}:")
        for v in vals:
            print(f"      {v}")
        print(f"      All unique: {all_unique}")

    print()


def main():
    parser = argparse.ArgumentParser(description="CSPRNG algorithm demo")
    parser.add_argument("--hmac", action="store_true",
                        help="HMAC-DRBG demo")
    parser.add_argument("--openssl", action="store_true",
                        help="OpenSSL integration demo")
    parser.add_argument("--platform", action="store_true",
                        help="Platform CSPRNG info")
    args = parser.parse_args()

    run_all = not any([args.hmac, args.openssl, args.platform])

    if run_all or args.hmac:
        demo_hmac_drbg()
    if run_all or args.openssl:
        demo_openssl()
    if run_all or args.platform:
        demo_platform()


if __name__ == "__main__":
    main()
