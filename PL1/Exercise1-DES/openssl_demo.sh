#!/bin/bash
# PL1, Exercise 1, Part 1: DES with OpenSSL
# (a) Plaintext message
# (b) Key (DES: 8 bytes; OpenSSL will use first 8 bytes of provided key)
# (c) Encrypt
# (d) Decrypt with same key
# (e) Try to decrypt with different key → garbage / wrong result

PLAINTEXT="My secret message"
KEY="mykey123"
WRONG_KEY="wrongkey"

echo "=== (a) Plaintext ==="
echo "$PLAINTEXT"

echo ""
echo "=== (b) Key (8 bytes for DES) ==="
echo "$KEY"

echo ""
echo "=== (c) Encrypt ==="
CIPHER_B64=$(echo -n "$PLAINTEXT" | openssl enc -des-ecb -K "$(echo -n "$KEY" | xxd -p)" -base64)
echo "Ciphertext (base64): $CIPHER_B64"

echo ""
echo "=== (d) Decrypt with same key ==="
echo "$CIPHER_B64" | base64 -d | openssl enc -des-ecb -d -K "$(echo -n "$KEY" | xxd -p)"
echo ""

echo "=== (e) Decrypt with different key ==="
echo "Result (garbage or error):"
echo "$CIPHER_B64" | base64 -d | openssl enc -des-ecb -d -K "$(echo -n "$WRONG_KEY" | xxd -p)" 2>&1 || true
echo ""
echo "Explanation: Decryption with a wrong key produces random-looking output (or padding errors) because the key schedule and round operations are completely different; there is no meaningful plaintext."
