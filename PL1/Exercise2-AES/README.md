# PL1 — Exercise 2: AES

AES (Advanced Encryption Standard) is a symmetric encryption algorithm established by NIST in 2001, widely used for securing sensitive data and communications.

---

## Tasks

### 1. Encrypt a file using AES

The script `aes_file.py` encrypts a file with **AES-256-CBC**: 256-bit key, CBC mode, random IV prepended to the ciphertext.

```bash
.venv/bin/python PL1/Exercise2-AES/aes_file.py
```

- **Input:** `sample.txt` (created automatically if missing; you can replace it with any file and edit the script to use it).
- **Output:** `sample.aes` (encrypted file: 16-byte IV + ciphertext).

### 2. Decrypt a file using AES

The same script decrypts `sample.aes` with the key used for encryption and writes the result to `sample_decrypted.txt`. The IV is read from the first 16 bytes of the encrypted file.

### 3. How much time does it take to complete?

The script measures and prints:

- Time for **encrypt** (seconds).
- Time for **decrypt** (seconds).
- **Total time** (encrypt + decrypt).
- **Throughput** (MB/s) for encrypt and decrypt.

Example output (run on your machine for your own timings):

```
1. Encrypt:  0.009663 s  →  sample.aes
2. Decrypt:  0.000119 s  →  sample_decrypted.txt

3. Total time:  0.009782 s  (encrypt + decrypt)
   Throughput (encrypt): 0.66 MB/s
   Throughput (decrypt): 53.50 MB/s
```

Times depend on file size, CPU, and system load. Run the script to obtain results for your environment.

### 4. Comparison: AES vs DES vs 3DES (performance and strength)

| Criterion | DES | 3DES | AES |
|-----------|-----|------|-----|
| **Key size** | 56 bits (64 with parity) | 112 or 168 bits | 128, 192, or 256 bits |
| **Block size** | 64 bits (8 bytes) | 64 bits | 128 bits (16 bytes) |
| **Rounds** | 16 | 48 (3×16) | 10 / 12 / 14 (128/192/256-bit key) |
| **Security** | Broken (56-bit brute-force feasible) | Deprecated; slow and only 112-bit effective in 2-key variant | Strong; no practical full-key attacks; NIST standard |
| **Performance** | Fast but obsolete | ~3× slower than DES (three passes) | Typically faster than 3DES on modern CPUs (hardware AES-NI); often comparable or faster than DES per block |
| **Standard / status** | FIPS 46-3 (withdrawn) | FIPS 46-3 (withdrawn); legacy only | FIPS 197; current standard |

**Strength**

- **DES:** 56-bit key is too short; exhaustive search is feasible with dedicated hardware. Not suitable for new systems.
- **3DES:** Improves security over DES (112 or 168 effective bits) but is slow (three DES operations) and being phased out (NIST disallows for new applications after 2023).
- **AES:** 128/192/256-bit keys; no practical attacks on the full algorithm; supports hardware acceleration (AES-NI), making it both strong and fast.

**Performance**

- **DES:** Fast in software but obsolete.
- **3DES:** About one third the throughput of DES for the same block count (three DES operations per block).
- **AES:** On modern processors with AES-NI, AES can be faster than DES and much faster than 3DES per byte; without AES-NI, speed is still competitive and AES is the recommended choice.

**Conclusion:** AES offers better security and typically better or comparable performance than DES and 3DES, and is the standard for symmetric encryption in current systems.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This report |
| `aes_file.py` | Encrypt/decrypt a file with AES-256-CBC and report timing |
| `sample.txt` | Sample input file (created by script if missing) |
| `sample.aes` | Encrypted file (created by script) |
| `sample_decrypted.txt` | Decrypted file (created by script) |

**Requirements:** Python 3 and `pycryptodome` (use the repo’s `.venv`).
