#!/usr/bin/env python3
"""
XOR Cipher Demo Script
Demonstrates XOR encryption, One-Time Pad (OTP), and key reuse attacks.

This script shows:
- Basic XOR encryption/decryption
- XOR properties demonstration
- One-Time Pad (OTP) implementation
- Key reuse attack demonstration
- RC4 stream cipher (broken) warning
- ChaCha20 modern stream cipher

Usage:
    python xor_cipher.py
    python xor_cipher.py --attack-demo

Requirements:
    pip install cryptography
"""

import os
import binascii
import base64
from typing import List, Tuple

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR two byte sequences together."""
    # Repeat key to match data length
    key_stream = (key * (len(data) // len(key) + 1))[:len(data)]
    return bytes(a ^ b for a, b in zip(data, key_stream))

def print_hex(data: bytes, label: str = ""):
    """Print data in hexadecimal format."""
    if label:
        print(f"{label}: {binascii.hexlify(data).decode().upper()}")
    else:
        print(binascii.hexlify(data).decode().upper())

def basic_xor_demo():
    """Demonstrate basic XOR encryption/decryption."""
    print("\n=== Basic XOR Encryption Demo ===")
    
    plaintext = b"Hello, XOR Encryption!"
    key = b"SECRETKEY"
    
    print(f"Original text: {plaintext.decode()}")
    print(f"Key: {key.decode()}")
    
    # Encrypt
    ciphertext = xor_bytes(plaintext, key)
    print_hex(ciphertext, "Encrypted (hex)")
    print(f"Encrypted (base64): {base64.b64encode(ciphertext).decode()}")
    
    # Decrypt (same operation as encryption)
    decrypted = xor_bytes(ciphertext, key)
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print("✓ XOR encryption/decryption successful!")

def xor_properties_demo():
    """Demonstrate XOR mathematical properties."""
    print("\n=== XOR Properties Demo ===")
    
    # Property 1: Self-inverse (A XOR K XOR K = A)
    print("\n1. Self-inverse property:")
    A = 0x41  # 'A'
    K = 0x13
    result1 = A ^ K
    result2 = result1 ^ K
    print(f"   A = 0x{A:02X} ({A})")
    print(f"   K = 0x{K:02X} ({K})")
    print(f"   A XOR K = 0x{result1:02X} ({result1})")
    print(f"   (A XOR K) XOR K = 0x{result2:02X} ({result2}) = A ✓")
    
    # Property 2: Identity with zero (A XOR 0 = A)
    print("\n2. Identity property:")
    A = 0x41
    result = A ^ 0
    print(f"   A = 0x{A:02X} ({A})")
    print(f"   A XOR 0 = 0x{result:02X} ({result}) = A ✓")
    
    # Property 3: Commutative (A XOR B = B XOR A)
    print("\n3. Commutative property:")
    A = 0x41
    B = 0x13
    result1 = A ^ B
    result2 = B ^ A
    print(f"   A = 0x{A:02X}, B = 0x{B:02X}")
    print(f"   A XOR B = 0x{result1:02X}")
    print(f"   B XOR A = 0x{result2:02X}")
    print(f"   A XOR B = B XOR A ✓")
    
    # Property 4: Associative ((A XOR B) XOR C = A XOR (B XOR C))
    print("\n4. Associative property:")
    A = 0x41
    B = 0x13
    C = 0x57
    result1 = (A ^ B) ^ C
    result2 = A ^ (B ^ C)
    print(f"   A = 0x{A:02X}, B = 0x{B:02X}, C = 0x{C:02X}")
    print(f"   (A XOR B) XOR C = 0x{result1:02X}")
    print(f"   A XOR (B XOR C) = 0x{result2:02X}")
    print(f"   (A XOR B) XOR C = A XOR (B XOR C) ✓")
    
    # Property 5: XOR with self gives zero (A XOR A = 0)
    print("\n5. Self-cancellation:")
    A = 0x41
    result = A ^ A
    print(f"   A = 0x{A:02X}")
    print(f"   A XOR A = 0x{result:02X} = 0 ✓")

def one_time_pad_demo():
    """Demonstrate One-Time Pad (OTP) encryption."""
    print("\n=== One-Time Pad (OTP) Demo ===")
    print("OTP provides perfect secrecy when used correctly.")
    
    plaintext = b"ATTACK AT DAWN"
    
    # Generate truly random key (same length as plaintext)
    key = os.urandom(len(plaintext))
    
    print(f"Plaintext: {plaintext.decode()}")
    print(f"Plaintext length: {len(plaintext)} bytes")
    print_hex(key, "Random Key (same length as plaintext)")
    
    # Encrypt
    ciphertext = xor_bytes(plaintext, key)
    print_hex(ciphertext, "Ciphertext")
    
    # Decrypt
    decrypted = xor_bytes(ciphertext, key)
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "OTP decryption failed!"
    print("✓ OTP encryption/decryption successful!")
    
    # Show OTP properties
    print("\nOTP Security Properties:")
    print("✓ Key length = Plaintext length (14 bytes)")
    print("✓ Key is truly random (from os.urandom)")
    print("✓ Key is used only once")
    print("✓ Key should be destroyed after use")
    
    print("\nWhy OTP is Perfectly Secure:")
    print("• For any ciphertext C and any plaintext P, there exists a key K = P XOR C")
    print("• Since all keys are equally likely, all plaintexts are equally likely")
    print("• Ciphertext reveals nothing about plaintext")
    
    print("\nWhy OTP is Impractical:")
    print("✗ Key must be as long as the message")
    print("✗ Key must be truly random")
    print("✗ Key must be used only once")
    print("✗ Key distribution and storage is difficult")

def key_reuse_attack_demo():
    """Demonstrate the key reuse attack (two-time pad)."""
    print("\n=== Key Reuse Attack Demo ===")
    print("Demonstrating why reusing a key stream is catastrophic.")
    
    # Two messages
    message1 = b"HELLO WORLD"
    message2 = b"GOODBYE NOW"
    
    print(f"Message 1: {message1.decode()}")
    print(f"Message 2: {message2.decode()}")
    
    # Generate a single key stream (mistake: reusing it)
    key_stream = os.urandom(max(len(message1), len(message2)))
    
    # Encrypt both messages with the SAME key stream
    cipher1 = xor_bytes(message1, key_stream)
    cipher2 = xor_bytes(message2, key_stream[:len(message2)])
    
    print("\nBoth messages encrypted with the SAME key stream:")
    print_hex(cipher1, "Cipher 1")
    print_hex(cipher2, "Cipher 2")
    
    # Attack: XOR the two ciphertexts
    # C1 XOR C2 = (P1 XOR K) XOR (P2 XOR K) = P1 XOR P2
    xor_result = xor_bytes(cipher1, cipher2[:len(cipher1)])
    print_hex(xor_result, "C1 XOR C2 = P1 XOR P2")
    
    # Now if we know one plaintext, we can recover the other
    print("\n--- Known-Plaintext Attack ---")
    print("If attacker knows P1 = 'HELLO WORLD'")
    
    # Recover P2 using known P1
    recovered_p2 = xor_bytes(xor_result, message1)
    print(f"Recovered P2: {recovered_p2.decode()}")
    
    # Verify
    assert recovered_p2 == message2, "Attack failed!"
    print("✓ Key reuse attack successful!")
    
    # Show why this works
    print("\nWhy this attack works:")
    print("• C1 = P1 XOR K")
    print("• C2 = P2 XOR K")
    print("• C1 XOR C2 = (P1 XOR K) XOR (P2 XOR K) = P1 XOR P2")
    print("• The key K cancels out!")
    print("• If we know P1, we can find P2 = (P1 XOR P2) XOR P1")

def rc4_demo():
    """Demonstrate RC4 stream cipher (showing it's broken)."""
    print("\n=== RC4 Stream Cipher Demo ===")
    print("WARNING: RC4 is BROKEN and should NOT be used!")
    
    # Simple RC4 implementation (for demonstration only)
    def rc4_init(key: bytes) -> List[int]:
        """RC4 Key Scheduling Algorithm (KSA)."""
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        return S
    
    def rc4_generate(S: List[int], length: int) -> bytes:
        """RC4 Pseudo-Random Generation Algorithm (PRGA)."""
        i = j = 0
        keystream = []
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            keystream.append(S[(S[i] + S[j]) % 256])
        return bytes(keystream)
    
    key = b"SecretKey"
    plaintext = b"Hello, RC4!"
    
    print(f"Key: {key.decode()}")
    print(f"Plaintext: {plaintext.decode()}")
    
    # Generate keystream
    S = rc4_init(key)
    keystream = rc4_generate(S, len(plaintext))
    print_hex(keystream, "RC4 Keystream (first 11 bytes)")
    
    # Encrypt
    ciphertext = xor_bytes(plaintext, keystream)
    print_hex(ciphertext, "Encrypted")
    
    # Decrypt
    S = rc4_init(key)
    keystream = rc4_generate(S, len(plaintext))
    decrypted = xor_bytes(ciphertext, keystream)
    print(f"Decrypted: {decrypted.decode()}")
    
    # Show RC4 weaknesses
    print("\nRC4 Security Issues:")
    print("✗ Initial bytes have statistical biases")
    print("✗ Related key attacks possible")
    print("✗ Fluhrer-Mantin-Shamir attack (2001)")
    print("✗ Klein attack (2005)")
    print("✗ RFC 7465 prohibits RC4 in TLS")
    
    print("\nAlternatives:")
    print("✓ ChaCha20 (used in TLS 1.3)")
    print("✓ AES-CTR (with AES-NI hardware acceleration)")

def chacha20_demo():
    """Demonstrate ChaCha20 modern stream cipher."""
    print("\n=== ChaCha20 Modern Stream Cipher ===")
    print("ChaCha20 is secure and used in TLS 1.3.")
    
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, ChaCha20
        
        # Generate random key and nonce
        key = os.urandom(32)  # 256-bit key
        nonce = os.urandom(12)  # 96-bit nonce
        
        plaintext = b"Hello, ChaCha20 Encryption!"
        
        print(f"Plaintext: {plaintext.decode()}")
        print_hex(key, "Key (256 bits)")
        print_hex(nonce, "Nonce (96 bits)")
        
        # Encrypt
        cipher = Cipher(ChaCha20(key, nonce), mode=None)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        print_hex(ciphertext, "Encrypted")
        
        # Decrypt
        cipher_decrypt = Cipher(ChaCha20(key, nonce), mode=None)
        decryptor = cipher_decrypt.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        
        print(f"Decrypted: {decrypted.decode()}")
        
        # Verify
        assert decrypted == plaintext, "ChaCha20 decryption failed!"
        print("✓ ChaCha20 encryption/decryption successful!")
        
        print("\nChaCha20 Properties:")
        print("✓ 256-bit key")
        print("✓ 96-bit nonce (must be unique)")
        print("✓ High performance (especially without AES-NI)")
        print("✓ Used in TLS 1.3, SSH, WireGuard")
        print("✓ Designed by Daniel J. Bernstein")
        
    except ImportError:
        print("ChaCha20 not available. Install cryptography: pip install cryptography")

def frequency_analysis_demo():
    """Demonstrate how XOR encryption can be broken with frequency analysis."""
    print("\n=== Frequency Analysis Attack ===")
    print("Simple XOR encryption can be broken using statistical analysis.")
    
    # English letter frequencies (approximate)
    english_freq = {
        ' ': 18.3, 'e': 10.3, 't': 7.5, 'a': 6.5, 'o': 6.1,
        'n': 5.7, 'i': 5.7, 's': 5.1, 'r': 4.9, 'h': 4.8,
        'l': 3.7, 'd': 3.1, 'c': 2.7, 'u': 2.3, 'm': 2.2,
        'f': 2.0, 'p': 1.8, 'g': 1.7, 'w': 1.6, 'y': 1.5,
        'b': 1.3, 'v': 0.9, 'k': 0.5, 'x': 0.2, 'j': 0.1,
        'q': 0.1, 'z': 0.1
    }
    
    # Simple XOR encryption with single-byte key
    plaintext = b"The quick brown fox jumps over the lazy dog"
    key_byte = 0x42  # Single byte key
    
    print(f"Plaintext: {plaintext.decode()}")
    print(f"Single-byte key: 0x{key_byte:02X}")
    
    # Encrypt
    key = bytes([key_byte])
    ciphertext = xor_bytes(plaintext, key)
    print_hex(ciphertext, "Ciphertext")
    
    # Attack: try all possible single-byte keys
    print("\nBrute-force attack on single-byte key:")
    
    best_key = None
    best_score = -1
    
    for possible_key in range(256):
        # Decrypt with this key
        key_try = bytes([possible_key])
        decrypted = xor_bytes(ciphertext, key_try)
        
        # Check if result is printable ASCII
        try:
            text = decrypted.decode('ascii')
            if not all(32 <= ord(c) < 127 for c in text):
                continue
        except UnicodeDecodeError:
            continue
        
        # Score based on English letter frequency
        score = 0
        for char in text.lower():
            if char in english_freq:
                score += english_freq[char]
        
        if score > best_score:
            best_score = score
            best_key = possible_key
    
    # Recover plaintext
    recovered = xor_bytes(ciphertext, bytes([best_key]))
    print(f"Recovered key: 0x{best_key:02X}")
    print(f"Recovered plaintext: {recovered.decode()}")
    
    # Verify
    assert recovered == plaintext, "Attack failed!"
    print("✓ Frequency analysis attack successful!")
    
    print("\nWhy this attack works:")
    print("• Single-byte key has only 256 possibilities")
    print("• English text has predictable letter frequencies")
    print("• The correct key produces text with highest frequency score")
    print("• This is why XOR with short keys is insecure!")

def main():
    """Main function to run all XOR demos."""
    print("=== XOR Cipher Demo ===")
    print("Demonstrating XOR encryption properties and attacks.")
    
    # Run demos
    basic_xor_demo()
    xor_properties_demo()
    one_time_pad_demo()
    key_reuse_attack_demo()
    rc4_demo()
    chacha20_demo()
    frequency_analysis_demo()
    
    print("\n=== Summary ===")
    print("• XOR is the basis of stream cipher encryption")
    print("• XOR has important mathematical properties:")
    print("  - Self-inverse: A XOR K XOR K = A")
    print("  - Identity: A XOR 0 = A")
    print("  - Commutative: A XOR B = B XOR A")
    print("• One-Time Pad provides perfect secrecy but is impractical")
    print("• Key reuse (two-time pad) is catastrophic")
    print("• RC4 is broken - use ChaCha20 or AES-CTR instead")
    print("• Single-byte XOR can be broken with frequency analysis")

if __name__ == "__main__":
    import sys
    
    if "--attack-demo" in sys.argv:
        # Run only attack demonstrations
        key_reuse_attack_demo()
        frequency_analysis_attack_demo()
    else:
        main()