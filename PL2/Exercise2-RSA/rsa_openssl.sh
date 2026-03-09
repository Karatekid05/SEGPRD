#!/bin/bash
# PL2 Exercise 2: RSA — Hybrid encrypt/decrypt a file using OpenSSL.
# Usage:
#   ./rsa_openssl.sh encrypt <file> <public.pem>   → file.enc + file.key.enc
#   ./rsa_openssl.sh decrypt <file.enc> <file.key.enc> <private.pem>  → restored file

set -e
MODE="$1"
if [ "$MODE" = "encrypt" ]; then
  INFILE="$2"
  PUBKEY="$3"
  if [ -z "$INFILE" ] || [ -z "$PUBKEY" ] || [ ! -f "$INFILE" ]; then
    echo "Usage: $0 encrypt <file> <public.pem>"
    exit 1
  fi
  KEYFILE=$(mktemp)
  IVFILE=$(mktemp)
  KEYENC="${INFILE}.key.enc"
  OUTENC="${INFILE}.enc"
  openssl rand -hex 32 | xxd -r -p > "$KEYFILE"
  openssl rand -hex 16 | xxd -r -p > "$IVFILE"
  KEYHEX=$(xxd -p -c 256 < "$KEYFILE")
  IVHEX=$(xxd -p -c 256 < "$IVFILE")
  { cat "$IVFILE"; openssl enc -aes-256-cbc -in "$INFILE" -K "$KEYHEX" -iv "$IVHEX"; } > "$OUTENC"
  openssl rsautl -encrypt -pubin -inkey "$PUBKEY" -in "$KEYFILE" -out "$KEYENC"
  rm -f "$KEYFILE" "$IVFILE"
  echo "Encrypted: $OUTENC (key in $KEYENC)"
elif [ "$MODE" = "decrypt" ]; then
  ENCFILE="$2"
  KEYENCFILE="$3"
  PRIVKEY="$4"
  if [ -z "$ENCFILE" ] || [ -z "$KEYENCFILE" ] || [ -z "$PRIVKEY" ]; then
    echo "Usage: $0 decrypt <file.enc> <file.key.enc> <private.pem>"
    exit 1
  fi
  KEYFILE=$(mktemp)
  OUTBASE="${ENCFILE%.enc}"
  openssl rsautl -decrypt -inkey "$PRIVKEY" -in "$KEYENCFILE" -out "$KEYFILE"
  KEYHEX=$(xxd -p -c 256 < "$KEYFILE")
  IVHEX=$(head -c 16 "$ENCFILE" | xxd -p -c 32)
  tail -c +17 "$ENCFILE" | openssl enc -aes-256-cbc -d -K "$KEYHEX" -iv "$IVHEX" -out "$OUTBASE"
  rm -f "$KEYFILE"
  echo "Decrypted: $OUTBASE"
else
  echo "Usage: $0 encrypt <file> <public.pem> | decrypt <file.enc> <file.key.enc> <private.pem>"
  exit 1
fi
