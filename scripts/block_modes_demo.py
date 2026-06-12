#!/usr/bin/env python3
"""
Block Cipher Modes Demo Script
Demonstrates different block cipher modes: ECB, CBC, CTR, GCM.

This script shows:
- How each mode works
- Security differences between modes
- ECB mode weakness demonstration
- Padding demonstration
- Performance comparison

Usage:
    python block_modes_demo.py

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

def ecb_mode_demo():
    """Demonstrate ECB mode and its weaknesses."""
    print("\n=== ECB Mode (Electronic Codebook) ===")
    print("WARNING: ECB mode is INSECURE for most applications!")
    
    # Fixed key for demonstration
    key = os.urandom(16)  # 128-bit key
    plaintext = b"This is a test message for block cipher modes demonstration."
    
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, "Key (128 bits)")
    
    # Create AES cipher in ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad plaintext
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    
    # Encrypt
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    
    # Demonstrate ECB weakness: same blocks produce same ciphertext
    print("\n--- ECB Weakness Demonstration ---")
    
    # Create messages with repeated blocks
    block_size = 16  # AES block size
    repeated_block = b"AAAAAAAAAAAAAAAA"  # 16 'A's
    message_with_repeat = repeated_block * 3  # 3 identical blocks
    
    print(f"Message with repeated blocks: {message_with_repeat}")
    print(f"Number of blocks: {len(message_with_repeat) // block_size}")
    
    # Encrypt with ECB
    cipher_ecb = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor_ecb = cipher_ecb.encryptor()
    ciphertext_ecb = encryptor_ecb.update(message_with_repeat) + encryptor_ecb.finalize()
    
    # Show that identical blocks produce identical ciphertext
    print("\nECB encrypted blocks:")
    for i in range(0, len(ciphertext_ecb), block_size):
        block = ciphertext_ecb[i:i+block_size]
        print(f"  Block {i//block_size}: {binascii.hexlify(block).decode().upper()}")
    
    # Check if blocks are identical
    block1 = ciphertext_ecb[0:block_size]
    block2 = ciphertext_ecb[block_size:block_size*2]
    block3 = ciphertext_ecb[block_size*2:block_size*3]
    
    if block1 == block2 == block3:
        print("\n✓ CONFIRMED: All three blocks are IDENTICAL!")
        print("  This is the security weakness of ECB mode.")
        print("  Attackers can see patterns in the encrypted data.")
    else:
        print("\n✗ Unexpected: Blocks are different (shouldn't happen with ECB)")

def cbc_mode_demo():
    """Demonstrate CBC mode."""
    print("\n=== CBC Mode (Cipher Block Chaining) ===")
    
    key = os.urandom(16)
    iv = os.urandom(16)  # Initialization Vector
    plaintext = b"Hello, CBC mode! This message will be encrypted with chaining."
    
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, "Key (128 bits)")
    print_hex(iv, "IV (128 bits)")
    
    # Create AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad and encrypt
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    print_hex(ciphertext, "Encrypted (hex)")
    
    # Decrypt
    cipher_decrypt = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    
    # Show that same plaintext with different IV produces different ciphertext
    print("\n--- CBC with Different IVs ---")
    iv2 = os.urandom(16)
    cipher2 = Cipher(algorithms.AES(key), modes.CBC(iv2), backend=default_backend())
    encryptor2 = cipher2.encryptor()
    ciphertext2 = encryptor2.update(padded_plaintext) + encryptor2.finalize()
    
    print_hex(iv, "IV 1")
    print_hex(ciphertext[:32], "Ciphertext 1 (first 32 bytes)")
    print_hex(iv2, "IV 2")
    print_hex(ciphertext2[:32], "Ciphertext 2 (first 32 bytes)")
    
    if ciphertext != ciphertext2:
        print("✓ Different IVs produce different ciphertext (even with same plaintext and key)")

def ctr_mode_demo():
    """Demonstrate CTR mode."""
    print("\n=== CTR Mode (Counter) ===")
    print("CTR mode turns a block cipher into a stream cipher.")
    
    key = os.urandom(16)
    nonce = os.urandom(16)  # 128-bit nonce
    plaintext = b"Hello, CTR mode! No padding needed for stream cipher mode."
    
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, "Key (128 bits)")
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
    
    # Show that CTR mode doesn't need padding
    print("\n--- CTR Mode Properties ---")
    print(f"Plaintext length: {len(plaintext)} bytes")
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"No padding needed: Ciphertext length = Plaintext length")

def gcm_mode_demo():
    """Demonstrate GCM mode (Authenticated Encryption)."""
    print("\n=== GCM Mode (Galois/Counter Mode) ===")
    print("GCM provides both encryption AND authentication.")
    
    key = os.urandom(16)
    nonce = os.urandom(12)  # 96-bit nonce recommended for GCM
    plaintext = b"Hello, GCM mode! This message is authenticated."
    associated_data = b"Additional authenticated data (AAD)"
    
    print(f"Original text: {plaintext.decode()}")
    print_hex(key, "Key (128 bits)")
    print_hex(nonce, "Nonce (96 bits)")
    print(f"Associated data: {associated_data.decode()}")
    
    # Create AES cipher in GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Authenticate additional data (not encrypted)
    encryptor.authenticate_additional_data(associated_data)
    
    # Encrypt
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag  # Authentication tag
    
    print_hex(ciphertext, "Encrypted (hex)")
    print_hex(tag, "Authentication Tag (128 bits)")
    
    # Decrypt and verify
    cipher_decrypt = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher_decrypt.decryptor()
    decryptor.authenticate_additional_data(associated_data)
    
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    
    print(f"Decrypted: {decrypted.decode()}")
    print("✓ Authentication tag verified!")
    
    # Demonstrate authentication failure
    print("\n--- Authentication Failure Demonstration ---")
    print("Attempting to decrypt with tampered ciphertext...")
    
    # Tamper with ciphertext
    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[0] ^= 0x01  # Flip one bit
    tampered_ciphertext = bytes(tampered_ciphertext)
    
    try:
        cipher_tampered = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor_tampered = cipher_tampered.decryptor()
        decryptor_tampered.authenticate_additional_data(associated_data)
        decrypted_tampered = decryptor_tampered.update(tampered_ciphertext) + decryptor_tampered.finalize()
        print("✗ Should not reach here - decryption should fail!")
    except Exception as e:
        print(f"✓ Decryption failed with error: {type(e).__name__}")
        print("  This is expected - tampered ciphertext is detected!")

def padding_demo():
    """Demonstrate PKCS7 padding."""
    print("\n=== Padding Demonstration ===")
    print("PKCS7 padding ensures plaintext is multiple of block size.")
    
    block_size = 16  # AES block size
    
    test_cases = [
        b"Hello",           # 5 bytes, needs 11 bytes padding
        b"123456789012345", # 15 bytes, needs 1 byte padding
        b"1234567890123456",# 16 bytes, needs full block padding
        b"This is a test message for padding demonstration",  # 48 bytes
    ]
    
    for plaintext in test_cases:
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        
        padding_needed = len(padded) - len(plaintext)
        padding_byte = bytes([padding_needed]) if padding_needed > 0 else b''
        
        print(f"\nOriginal: '{plaintext.decode()}' ({len(plaintext)} bytes)")
        print(f"Padded: {binascii.hexlify(padded).decode().upper()}")
        print(f"Padding added: {padding_needed} bytes of value {hex(padding_needed) if padding_needed > 0 else '0x00'}")
        
        # Verify unpadding
        unpadder = padding.PKCS7(128).unpadder()
        unpadded = unpadder.update(padded) + unpadder.finalize()
        assert unpadded == plaintext, "Unpadding failed!"
        print(f"✓ Unpadding successful: '{unpadded.decode()}'")

def performance_comparison():
    """Compare performance of different modes."""
    print("\n=== Performance Comparison ===")
    
    # Test data
    data = os.urandom(1024 * 1024)  # 1 MB of random data
    iterations = 100
    
    modes_config = [
        ("ECB", lambda: modes.ECB()),
        ("CBC", lambda: modes.CBC(os.urandom(16))),
        ("CTR", lambda: modes.CTR(os.urandom(16))),
        ("GCM", lambda: modes.GCM(os.urandom(12))),
    ]
    
    results = []
    
    for mode_name, mode_factory in modes_config:
        key = os.urandom(16)  # 128-bit key
        mode = mode_factory()
        cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
        
        # Pad for modes that need it
        if mode_name in ["ECB", "CBC"]:
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
        else:
            padded_data = data
        
        # Measure encryption time
        start_time = time.time()
        for _ in range(iterations):
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            if mode_name == "GCM":
                _ = encryptor.tag
        end_time = time.time()
        
        elapsed = end_time - start_time
        speed = (len(data) * iterations) / elapsed / (1024 * 1024)  # MB/s
        
        results.append((mode_name, elapsed, speed))
        print(f"{mode_name}: {elapsed:.3f} seconds for {iterations} encryptions ({speed:.2f} MB/s)")
    
    # Show comparison
    print("\nPerformance Summary:")
    baseline = results[0][2]  # ECB as baseline
    for mode_name, _, speed in results:
        ratio = speed / baseline
        print(f"  {mode_name}: {ratio:.2f}x relative to ECB")

def mode_comparison_table():
    """Print a comparison table of block cipher modes."""
    print("\n=== Block Cipher Modes Comparison ===")
    
    header = "| Mode | Security | Parallel Enc | Parallel Dec | Padding | IV/Nonce | Authentication |"
    separator = "|------|----------|--------------|--------------|---------|----------|----------------|"
    
    rows = [
        "| ECB  | Low      | Yes          | Yes          | Yes     | No       | No             |",
        "| CBC  | Medium   | No           | Yes          | Yes     | Yes      | No             |",
        "| CTR  | High     | Yes          | Yes          | No      | Yes      | No             |",
        "| GCM  | High     | Yes          | Yes          | No      | Yes      | Yes            |",
    ]
    
    print(header)
    print(separator)
    for row in rows:
        print(row)
    
    print("\nRecommendations:")
    print("• ECB: NEVER use for real applications")
    print("• CBC: Legacy applications, requires careful IV management")
    print("• CTR: High-performance applications without authentication")
    print("• GCM: Modern standard for authenticated encryption")

def main():
    """Main function to run all block mode demos."""
    print("=== Block Cipher Modes Demo ===")
    print("Demonstrating AES encryption with different block cipher modes.")
    
    # Run demos
    ecb_mode_demo()
    cbc_mode_demo()
    ctr_mode_demo()
    gcm_mode_demo()
    
    # Additional demonstrations
    padding_demo()
    performance_comparison()
    mode_comparison_table()
    
    print("\n=== Summary ===")
    print("• ECB mode is insecure - same plaintext blocks produce same ciphertext")
    print("• CBC mode requires IV and padding, but is more secure than ECB")
    print("• CTR mode turns block cipher into stream cipher, no padding needed")
    print("• GCM mode provides authenticated encryption (encryption + integrity)")
    print("• Always use authenticated encryption (GCM) when possible")
    print("• Never reuse IV/Nonce with the same key")

if __name__ == "__main__":
    main()