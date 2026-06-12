#!/usr/bin/env python3
"""
AES Encryption Demo Script
Demonstrates AES encryption/decryption using cryptography library.

This script shows:
- AES-128, AES-192, AES-256 encryption
- CBC, CTR, GCM modes
- Key schedule demonstration
- Performance comparison

Usage:
    python aes_demo.py

Requirements:
    pip install cryptography
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import binascii
import time

def print_hex(data, label=""):
    """Print data in hexadecimal format."""
    if label:
        print(f"{label}: {binascii.hexlify(data).decode().upper()}")
    else:
        print(binascii.hexlify(data).decode().upper())

def aes_cbc_demo(key_size=128):
    """Demonstrate AES encryption in CBC mode."""
    print(f"\n--- AES-{key_size}-CBC ---")
    
    # Generate random key and IV
    key = os.urandom(key_size // 8)  # Convert bits to bytes
    iv = os.urandom(16)  # 128 bits = 16 bytes
    
    plaintext = b"Hello, AES Encryption! This is a secret message."
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, f"Key ({key_size} bits)")
    print_hex(iv, "IV (128 bits)")
    
    # Create AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad plaintext to multiple of 16 bytes (AES block size)
    padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    
    # Encrypt
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print(f"✓ AES-{key_size}-CBC encryption/decryption successful!")
    
    return key, iv, ciphertext

def aes_ctr_demo(key_size=256):
    """Demonstrate AES encryption in CTR mode."""
    print(f"\n--- AES-{key_size}-CTR ---")
    
    # Generate random key and nonce
    key = os.urandom(key_size // 8)
    nonce = os.urandom(16)  # 128 bits for CTR mode
    
    plaintext = b"Hello, AES CTR mode! CTR mode is a stream cipher."
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, f"Key ({key_size} bits)")
    print_hex(nonce, "Nonce (128 bits)")
    
    # Create AES cipher in CTR mode
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # No padding needed for CTR mode
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print(f"✓ AES-{key_size}-CTR encryption/decryption successful!")
    
    return key, nonce, ciphertext

def aes_gcm_demo(key_size=256):
    """Demonstrate AES encryption in GCM mode (Authenticated Encryption)."""
    print(f"\n--- AES-{key_size}-GCM (Authenticated Encryption) ---")
    
    # Generate random key and nonce
    key = os.urandom(key_size // 8)
    nonce = os.urandom(12)  # 96 bits recommended for GCM
    
    plaintext = b"Hello, AES-GCM! This message is authenticated."
    associated_data = b"Additional authenticated data (AAD)"
    
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, f"Key ({key_size} bits)")
    print_hex(nonce, "Nonce (96 bits)")
    print(f"Associated data: {associated_data.decode()}")
    
    # Create AES cipher in GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Add associated data (authenticated but not encrypted)
    encryptor.authenticate_additional_data(associated_data)
    
    # Encrypt
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag  # Authentication tag
    
    print_hex(ciphertext, "Encrypted (hex)")
    print_hex(tag, "Authentication Tag (128 bits)")
    
    # Decrypt and verify authentication
    cipher_decrypt = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decryptor.authenticate_additional_data(associated_data)
    
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print(f"✓ AES-{key_size}-GCM encryption/decryption successful!")
    print("✓ Authentication tag verified!")
    
    return key, nonce, ciphertext, tag

def aes_key_schedule_demo():
    """Demonstrate AES key schedule (simplified)."""
    print("\n=== AES Key Schedule Demo ===")
    
    # This is a simplified demonstration
    # Real AES key schedule is more complex
    
    key = os.urandom(16)  # 128-bit key
    print(f"AES-128 Master Key: {binascii.hexlify(key).decode().upper()}")
    
    # Show key expansion concept
    print("\nKey Schedule Concept:")
    print("• AES-128: 128-bit key → 11 round keys (128 bits each)")
    print("• AES-192: 192-bit key → 13 round keys")
    print("• AES-256: 256-bit key → 15 round keys")
    
    # Demonstrate simple key expansion (not real AES)
    print("\nSimplified Key Expansion (XOR demonstration):")
    round_keys = [key]
    for i in range(1, 11):
        # Simple XOR with round constant (not real AES)
        round_const = bytes([i, 0, 0, 0]) + b'\x00' * 12
        new_key = bytes(a ^ b for a, b in zip(round_keys[-1], round_const))
        round_keys.append(new_key)
        print(f"Round Key {i}: {binascii.hexlify(new_key).decode().upper()}")
    
    print("\nNote: This is a simplified demonstration.")
    print("Real AES key schedule uses Rcon, RotWord, SubWord operations.")

def performance_comparison():
    """Compare performance of different AES configurations."""
    print("\n=== Performance Comparison ===")
    
    # Test data
    data = os.urandom(1024 * 1024)  # 1 MB of random data
    iterations = 100
    
    configs = [
        ("AES-128-CBC", 128, "CBC"),
        ("AES-256-CBC", 256, "CBC"),
        ("AES-256-CTR", 256, "CTR"),
        ("AES-256-GCM", 256, "GCM"),
    ]
    
    results = []
    
    for name, key_size, mode in configs:
        key = os.urandom(key_size // 8)
        
        if mode == "CBC":
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        elif mode == "CTR":
            nonce = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        elif mode == "GCM":
            nonce = os.urandom(12)
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        
        # Pad for CBC mode
        if mode == "CBC":
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
        else:
            padded_data = data
        
        # Measure encryption time
        start_time = time.time()
        for _ in range(iterations):
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            if mode == "GCM":
                _ = encryptor.tag
        end_time = time.time()
        
        elapsed = end_time - start_time
        speed = (len(data) * iterations) / elapsed / (1024 * 1024)  # MB/s
        
        results.append((name, elapsed, speed))
        print(f"{name}: {elapsed:.3f} seconds for {iterations} encryptions ({speed:.2f} MB/s)")
    
    # Show comparison
    print("\nPerformance Summary:")
    baseline = results[0][2]  # AES-128-CMB as baseline
    for name, _, speed in results:
        ratio = speed / baseline
        print(f"  {name}: {ratio:.2f}x relative to AES-128-CBC")

def main():
    """Main function to run all AES demos."""
    print("=== AES Encryption Demo ===")
    print("AES is the current standard for symmetric encryption.")
    
    # Run demos for different key sizes
    aes_cbc_demo(128)
    aes_cbc_demo(192)
    aes_cbc_demo(256)
    
    # Run different modes
    aes_ctr_demo(256)
    aes_gcm_demo(256)
    
    # Key schedule demonstration
    aes_key_schedule_demo()
    
    # Performance comparison
    performance_comparison()
    
    print("\n=== Summary ===")
    print("• AES key sizes: 128, 192, 256 bits")
    print("• AES block size: 128 bits (16 bytes)")
    print("• Recommended modes:")
    print("  - AES-256-GCM for authenticated encryption")
    print("  - AES-256-CBC + HMAC for general encryption")
    print("  - AES-256-CTR for high-performance stream encryption")
    print("• AES is secure for all practical purposes")
    print("• No known practical attacks against properly implemented AES")

if __name__ == "__main__":
    main()