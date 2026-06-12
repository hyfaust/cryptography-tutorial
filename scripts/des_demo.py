#!/usr/bin/env python3
"""
DES Encryption Demo Script
Demonstrates DES encryption/decryption using pycryptodome library.

This script is for educational purposes only.
DES is considered insecure and should not be used in production.

Usage:
    python des_demo.py

Requirements:
    pip install pycryptodome
"""

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii
import os

def print_hex(data, label=""):
    """Print data in hexadecimal format."""
    if label:
        print(f"{label}: {binascii.hexlify(data).decode().upper()}")
    else:
        print(binascii.hexlify(data).decode().upper())

def des_ecb_demo():
    """Demonstrate DES encryption in ECB mode."""
    print("\n--- DES-ECB Mode ---")
    
    # Example key (8 bytes = 64 bits, but only 56 bits are effective)
    key = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    
    # Plaintext must be multiple of 8 bytes (DES block size)
    plaintext = b"Hello DES"  # 9 bytes, needs padding
    print(f"Original text: {plaintext.decode()}")
    print(f"Key (hex): {binascii.hexlify(key).decode().upper()}")
    
    # Create DES cipher in ECB mode
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Pad plaintext to multiple of 8 bytes
    padded_plaintext = pad(plaintext, DES.block_size)
    print(f"Padded plaintext (hex): {binascii.hexlify(padded_plaintext).decode().upper()}")
    
    # Encrypt
    ciphertext = cipher.encrypt(padded_plaintext)
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = DES.new(key, DES.MODE_ECB)
    decrypted_padded = cipher_decrypt.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, DES.block_size)
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print("✓ Encryption/decryption successful!")
    
    return ciphertext

def des_cbc_demo():
    """Demonstrate DES encryption in CBC mode."""
    print("\n--- DES-CBC Mode ---")
    
    # Key and IV (Initialization Vector)
    key = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    iv = b'\x12\x34\x56\x78\x90\xAB\xCD\xEF'
    
    plaintext = b"Hello DES CBC Mode!"
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, "Key (hex)")
    print_hex(iv, "IV (hex)")
    
    # Create DES cipher in CBC mode
    cipher = DES.new(key, DES.MODE_CBC, iv)
    
    # Pad and encrypt
    padded_plaintext = pad(plaintext, DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt (need new cipher instance with same IV)
    cipher_decrypt = DES.new(key, DES.MODE_CBC, iv)
    decrypted_padded = cipher_decrypt.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, DES.block_size)
    print(f"Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "Decryption failed!"
    print("✓ CBC mode encryption/decryption successful!")
    
    return ciphertext

def des_key_analysis():
    """Analyze DES key structure."""
    print("\n=== DES Key Analysis ===")
    
    # Example 64-bit key (includes parity bits)
    key_64bit = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    print(f"64-bit key: {binascii.hexlify(key_64bit).decode().upper()}")
    
    # Show binary representation
    key_binary = ''.join(format(byte, '08b') for byte in key_64bit)
    print(f"Key in binary: {key_binary}")
    
    # Extract 56-bit effective key (remove parity bits)
    # Parity bits are the LSB of each byte
    effective_key_bits = []
    for i, byte in enumerate(key_64bit):
        # Get bits 7-1 (MSB to bit 1), skip bit 0 (parity)
        for bit_pos in range(7, 0, -1):
            effective_key_bits.append((byte >> bit_pos) & 1)
    
    print(f"56-bit effective key bits: {''.join(map(str, effective_key_bits))}")
    
    # Show parity bits
    parity_bits = []
    for byte in key_64bit:
        parity_bits.append(byte & 1)
    
    print(f"Parity bits: {''.join(map(str, parity_bits))}")
    
    # Verify parity
    for i, byte in enumerate(key_64bit):
        parity = bin(byte).count('1') % 2
        if parity == 0:
            print(f"  Byte {i}: {hex(byte)} - Parity OK (even)")
        else:
            print(f"  Byte {i}: {hex(byte)} - Parity ERROR (odd)")

def des_security_analysis():
    """Analyze DES security characteristics."""
    print("\n=== DES Security Analysis ===")
    
    # Key space size
    key_space = 2**56
    print(f"Key space size: 2^56 = {key_space:,}")
    print(f"Key space in decimal: {key_space:,}")
    
    # Brute force time estimation
    keys_per_second = 1_000_000_000  # 1 billion keys per second
    seconds_needed = key_space / keys_per_second
    years_needed = seconds_needed / (365.25 * 24 * 3600)
    
    print(f"\nBrute force time estimation:")
    print(f"  Keys per second: {keys_per_second:,}")
    print(f"  Seconds needed: {seconds_needed:,.0f}")
    print(f"  Years needed: {years_needed:,.2f}")
    
    # Historical context
    print("\nHistorical context:")
    print("  1977: DES becomes standard")
    print("  1998: EFF's 'Deep Crack' breaks DES in 56 hours")
    print("  1999: DES broken in 22 hours")
    print("  2024: Modern GPUs can break DES in hours")
    
    # Recommendation
    print("\nRecommendation:")
    print("  ✗ DES is INSECURE and should NOT be used")
    print("  ✗ 3DES is being phased out")
    print("  ✓ Use AES-256 for modern applications")

def triple_des_demo():
    """Demonstrate Triple DES (3DES) encryption."""
    print("\n=== Triple DES (3DES) Demo ===")
    
    # Three different keys for 3DES (key option 1: 168-bit effective)
    key1 = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    key2 = b'\x23\x45\x67\x89\xAB\xCD\xEF\x01'
    key3 = b'\x45\x67\x89\xAB\xCD\xEF\x01\x23'
    
    # Combined key for 3DES (24 bytes)
    key_3des = key1 + key2 + key3
    
    plaintext = b"Hello Triple DES!"
    print(f"Original text: {plaintext.decode()}")
    print_hex(key_3des, "3DES Key (24 bytes)")
    
    # Create 3DES cipher
    from Crypto.Cipher import DES3
    
    # Encrypt
    cipher = DES3.new(key_3des, DES3.MODE_ECB)
    padded_plaintext = pad(plaintext, DES3.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    print_hex(ciphertext, "3DES Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = DES3.new(key_3des, DES3.MODE_ECB)
    decrypted_padded = cipher_decrypt.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, DES3.block_size)
    print(f"3DES Decrypted: {decrypted.decode()}")
    
    # Verify
    assert decrypted == plaintext, "3DES decryption failed!"
    print("✓ 3DES encryption/decryption successful!")
    
    # Show 3DES advantages
    print("\n3DES vs DES:")
    print("  • 3DES uses three 56-bit keys (168-bit effective)")
    print("  • 3DES is 3x slower than DES")
    print("  • 3DES is more secure than single DES")
    print("  • 3DES is being replaced by AES")

def main():
    """Main function to run all DES demos."""
    print("=== DES Encryption Demo ===")
    print("Note: DES is considered INSECURE. Use AES for real applications.")
    
    # Run demos
    des_ecb_demo()
    des_cbc_demo()
    des_key_analysis()
    des_security_analysis()
    triple_des_demo()
    
    print("\n=== Summary ===")
    print("• DES uses 56-bit effective key (64-bit with parity)")
    print("• DES block size is 64 bits (8 bytes)")
    print("• DES is vulnerable to brute force attacks")
    print("• Use AES-256 for modern applications")
    print("• 3DES can be used for backward compatibility")

if __name__ == "__main__":
    main()