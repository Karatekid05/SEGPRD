#!/bin/bash
# PL1, Exercise 1, Part 1: DES with OpenSSL
# (a) Plaintext message  →  message.txt
# (b) Key (8 bytes)
# (c) Encrypt            →  encrypted.bin
# (d) Decrypt same key   →  decrypted.txt
# (e) Decrypt wrong key  →  wrong_decrypted.txt
#
# OpenSSL 3.x disables DES by default. We try -provider legacy so DES works.

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

PLAINTEXT="My secret message"
KEY="mykey123"
WRONG_KEY="wrongkey"

# OpenSSL 3.x disables DES; try legacy provider if default fails
OSSL_ARGS=""
CIPHER_TEST=$(echo -n "$PLAINTEXT" | openssl enc -des-ecb -K "$(echo -n "$KEY" | xxd -p)" -base64 2>/dev/null)
if [ -z "$CIPHER_TEST" ]; then
  OSSL_ARGS="-provider default -provider legacy"
fi

echo "=== (a) Plaintext ==="
echo "$PLAINTEXT"
echo -n "$PLAINTEXT" > message.txt
echo "  → saved to message.txt"

echo ""
echo "=== (b) Key (8 bytes for DES) ==="
echo "$KEY"

echo ""
echo "=== (c) Encrypt ==="
CIPHER_B64=$(echo -n "$PLAINTEXT" | openssl enc -des-ecb -K "$(echo -n "$KEY" | xxd -p)" -base64 $OSSL_ARGS 2>/dev/null)
if [ -z "$CIPHER_B64" ]; then
  echo "OpenSSL DES not available. On OpenSSL 3.x enable the legacy provider (e.g. -provider default -provider legacy)."
  exit 1
fi
echo "$CIPHER_B64" | base64 -d > encrypted.bin
echo "Ciphertext (base64): $CIPHER_B64"
echo "  → saved to encrypted.bin"

echo ""
echo "=== (d) Decrypt with same key ==="
cat encrypted.bin | openssl enc -des-ecb -d -K "$(echo -n "$KEY" | xxd -p)" $OSSL_ARGS > decrypted.txt
cat decrypted.txt
echo ""
echo "  → saved to decrypted.txt (matches message.txt)"

echo ""
echo "=== (e) Decrypt with different key ==="
echo "Result (garbage or error):"
cat encrypted.bin | openssl enc -des-ecb -d -K "$(echo -n "$WRONG_KEY" | xxd -p)" $OSSL_ARGS > wrong_decrypted.txt 2>/dev/null || true
cat wrong_decrypted.txt 2>/dev/null | xxd || true
echo "  → saved to wrong_decrypted.txt"
echo ""
echo "Explanation: Decryption with a wrong key produces random-looking output (or padding errors); only the correct key recovers the original plaintext."
