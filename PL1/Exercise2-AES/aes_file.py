#!/usr/bin/env python3
"""
PL1, Exercise 2: AES — Encrypt and decrypt a file, measure time.
Uses AES-256-CBC with a random IV (prepended to ciphertext).
"""
import os
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

BLOCK_SIZE = AES.block_size  # 16 bytes
KEY_SIZE = 32  # AES-256


def encrypt_file(input_path: str, output_path: str, key: bytes) -> float:
    """Encrypt file with AES-256-CBC. Returns time taken in seconds."""
    with open(input_path, "rb") as f:
        plaintext = f.read()
    iv = get_random_bytes(BLOCK_SIZE)
    t0 = time.perf_counter()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext, BLOCK_SIZE)
    ciphertext = iv + cipher.encrypt(padded)
    elapsed = time.perf_counter() - t0
    with open(output_path, "wb") as f:
        f.write(ciphertext)
    return elapsed


def decrypt_file(input_path: str, output_path: str, key: bytes) -> float:
    """Decrypt file (IV is first 16 bytes). Returns time taken in seconds."""
    with open(input_path, "rb") as f:
        data = f.read()
    iv = data[:BLOCK_SIZE]
    ciphertext = data[BLOCK_SIZE:]
    t0 = time.perf_counter()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)
    elapsed = time.perf_counter() - t0
    with open(output_path, "wb") as f:
        f.write(plaintext)
    return elapsed


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, "sample.txt")
    encrypted_file = os.path.join(script_dir, "sample.aes")
    decrypted_file = os.path.join(script_dir, "sample_decrypted.txt")

    # Create sample file if it doesn't exist
    if not os.path.exists(sample_file):
        content = b"AES (Advanced Encryption Standard) is a symmetric block cipher.\n"
        content += b"NIST selected it in 2001. It supports 128, 192, and 256-bit keys.\n" * 100
        with open(sample_file, "wb") as f:
            f.write(content)
        print(f"Created sample file: {sample_file} ({len(content)} bytes)")

    key = get_random_bytes(KEY_SIZE)
    size = os.path.getsize(sample_file)

    print("=== Exercise 2: AES — Encrypt / Decrypt file ===\n")
    print(f"Input file: {sample_file} ({size} bytes)")
    print(f"Key: AES-256 (32 bytes)\n")

    # 1. Encrypt
    t_enc = encrypt_file(sample_file, encrypted_file, key)
    print(f"1. Encrypt:  {t_enc:.6f} s  →  {encrypted_file}")

    # 2. Decrypt
    t_dec = decrypt_file(encrypted_file, decrypted_file, key)
    print(f"2. Decrypt:  {t_dec:.6f} s  →  {decrypted_file}")

    # 3. Time
    print(f"\n3. Total time:  {t_enc + t_dec:.6f} s  (encrypt + decrypt)")
    print(f"   Throughput (encrypt): {size / (1024*1024) / t_enc:.2f} MB/s" if t_enc > 0 else "")
    print(f"   Throughput (decrypt): {size / (1024*1024) / t_dec:.2f} MB/s" if t_dec > 0 else "")

    # Verify
    with open(sample_file, "rb") as f:
        orig = f.read()
    with open(decrypted_file, "rb") as f:
        dec = f.read()
    assert orig == dec, "Decrypted content does not match original!"
    print("\nVerification: decrypted file matches original.")


if __name__ == "__main__":
    main()
