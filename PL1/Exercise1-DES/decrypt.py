"""
DES Brute-Force Tool (PL1, Exercise 1, Part 2)

Procedure and results for ciphertext s8knpxKRpJ3JDd+UJqCupw== are documented
in the README.md of this folder.
"""
import base64
import sys
from pathlib import Path
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad, pad
import time
from tqdm import tqdm

# Default wordlist: same dir, or repo root (two levels up)
def _default_wordlist():
    here = Path(__file__).resolve().parent
    for p in (here / "rockyou.txt", here.parent.parent / "rockyou.txt"):
        if p.exists():
            return str(p)
    return "rockyou.txt"

class DESBruteForcer:
    def __init__(self, ciphertext_b64):
        """Initialize with base64 encoded ciphertext"""
        self.ciphertext = base64.b64decode(ciphertext_b64)

    def decrypt_des(self, key_bytes, ciphertext):
        """Attempt to decrypt with given key"""
        try:
            cipher = DES.new(key_bytes, DES.MODE_ECB)
            decrypted = cipher.decrypt(ciphertext)
            plaintext = unpad(decrypted, DES.block_size)
            return plaintext.decode("utf-8", errors="ignore")
        except (ValueError, KeyError):
            return None

    def try_key(self, key_str):
        """Try a single key (DES: 8 bytes, truncate or zero-pad)."""
        key_bytes = key_str.encode("utf-8")[:8]
        if len(key_bytes) < 8:
            key_bytes = key_bytes.ljust(8, b"\0")
        return self.decrypt_des(key_bytes, self.ciphertext)

    def _verify_key(self, key_bytes, plaintext_str):
        """Re-encrypt and check if we get the same ciphertext (true positive)."""
        try:
            cipher = DES.new(key_bytes, DES.MODE_ECB)
            padded = pad(plaintext_str.encode("utf-8"), DES.block_size)
            return cipher.encrypt(padded) == self.ciphertext
        except Exception:
            return False

    def brute_force_wordlist(self, wordlist_path=None, max_attempts=None):
        wordlist_path = wordlist_path or _default_wordlist()
        print(f"Wordlist: {wordlist_path}")
        print("Starting brute force attack...")
        attempts = 0
        start_time = time.time()
        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in tqdm(f, desc="Trying passwords"):
                    key = line.strip()
                    attempts += 1
                    if max_attempts and attempts > max_attempts:
                        break
                    result = self.try_key(key)
                    if result is not None:
                        key_bytes = key.encode("utf-8")[:8].ljust(8, b"\0")
                        if self._verify_key(key_bytes, result):
                            elapsed = time.time() - start_time
                            print(f"\n✅ SUCCESS (verified)! Key: '{key}'")
                            print(f"Decrypted message: '{result}'")
                            print(f"Attempts: {attempts}, Time: {elapsed:.2f}s")
                            return key, result, attempts, elapsed
        except FileNotFoundError:
            print(f"Wordlist not found: {wordlist_path}")
            print("Download rockyou.txt and place it in this folder or in the repo root.")
        print("No valid key found in wordlist")
        return None, None, attempts, time.time() - start_time


if __name__ == "__main__":
    ciphertext = "s8knpxKRpJ3JDd+UJqCupw=="
    wordlist = sys.argv[1] if len(sys.argv) > 1 else None
    bruteforcer = DESBruteForcer(ciphertext)
    bruteforcer.brute_force_wordlist(wordlist)
