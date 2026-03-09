# PL1 — Exercise 1: DES

Symmetric keys and DES (Data Encryption Standard): OpenSSL tasks and brute-force tool with analysis.

---

## Part 1: DES with OpenSSL

Using the OpenSSL command-line tool:

| Task | Description |
|------|-------------|
| **(a)** | Choose a plain-text message |
| **(b)** | Choose a key (DES uses 8-byte keys) |
| **(c)** | Encrypt the payload |
| **(d)** | Decrypt the same payload with the same key |
| **(e)** | Try to decrypt using a different key and explain the result |

### How to run Part 1

```bash
cd PL1/Exercise1-DES
chmod +x openssl_demo.sh
./openssl_demo.sh
```

On OpenSSL 3.x, DES is disabled by default. The script tries the legacy provider (`-provider default -provider legacy`) automatically. If DES still fails, enable the legacy provider in your OpenSSL configuration.

The script produces the following files (artifacts of the exercise):

| File | Description |
|------|-------------|
| `message.txt` | (a) The chosen plaintext message |
| `encrypted.bin` | (c) The encrypted payload (binary) |
| `decrypted.txt` | (d) Result of decrypting with the **same** key (should equal `message.txt`) |
| `wrong_decrypted.txt` | (e) Result of decrypting with a **different** key (garbage) |

**Explanation for (e):** Decrypting with a wrong key yields random-looking output (or padding errors). The cipher is deterministic: only the correct key reproduces the original plaintext; any other key produces effectively random bytes.

---

## Part 2: Brute-force tool and analysis

Target ciphertext (base64): `s8knpxKRpJ3JDd+UJqCupw==`

### 2(a) Procedure and results

**Procedure:**

1. Decode the ciphertext from base64 and treat it as DES-ECB with PKCS7 padding.
2. For each password in the wordlist (e.g. rockyou.txt):
   - Derive an 8-byte key (truncate or zero-pad the password).
   - Decrypt and unpad; if decryption succeeds, re-encrypt the candidate plaintext with the same key.
3. Only report success when the re-encrypted result matches the original ciphertext (avoids false positives).

**Results (using rockyou.txt):**

| Item | Value |
|------|--------|
| **Key found** | `w421peh` |
| **Decrypted message** | `0[I<pvHKtD` |
| **Attempts** | ~2.84M |
| **Time** | ~37 s |

**How to reproduce:**

From the repo root (with `rockyou.txt` in repo root or in `PL1/Exercise1-DES/`):

```bash
.venv/bin/python PL1/Exercise1-DES/decrypt.py
# Or with explicit wordlist:
.venv/bin/python PL1/Exercise1-DES/decrypt.py /path/to/rockyou.txt
```

---

### 2(b) Key complexity — increasing key length

- Keyspace for keys of length *n* over an alphabet of size *A* is **A^n**.
- As key length increases, keyspace grows **exponentially**; brute force becomes infeasible even for moderate *n*.

Example (alphabet size 26):

| Length | Keyspace |
|--------|----------|
| 1 | 26 |
| 4 | 456,976 |
| 8 | 208,827,064,576 |
| 10 | 141,167,095,653,376 |

**Conclusion:** Increasing key length makes brute-force search impractical without a constrained wordlist.

---

### 2(c) Symbol domain — increasing the set of symbols

- For a fixed key length (e.g. 8), a larger symbol set increases the keyspace.

Example (length 8):

| Domain | Size | Keyspace (8 chars) |
|--------|------|--------------------|
| Lowercase | 26 | 208,827,064,576 |
| Alphanumeric | 62 | 218,340,105,584,896 |
| Printable ASCII | 95 | 6,634,204,312,890,625 |

**Conclusion:** Increasing the domain of symbols (e.g. adding digits, uppercase, symbols) greatly increases the keyspace and makes exhaustive search harder.

---

### 2(d) Graph and conclusions

Run the analysis script to generate the plot:

```bash
.venv/bin/python PL1/Exercise1-DES/des_analysis.py
```

This creates **`des_complexity_plot.png`** in this folder: key length (x) vs keyspace (y, log scale) for several symbol domains.

**Conclusions:**

1. **Key length** has an exponential effect on keyspace; small increases in length quickly make brute force infeasible.
2. **Symbol domain** also increases keyspace significantly for the same length.
3. DES uses an 8-byte key; with 95 symbols the theoretical keyspace is ~95^8 ≈ 6.6×10^15, which is still attackable with dedicated hardware; 3DES with 168-bit keys is not.

---

### 2(e) 3DES vs DES

| | DES | 3DES |
|---|-----|------|
| **Key size** | 8 bytes (64 bits, 56 effective) | 16 or 24 bytes (112 or 168 bits effective) |
| **Structure** | Single block cipher | DES applied three times (E-D-E) with 2 or 3 keys |
| **Brute force** | 2^56 keys → feasible with hardware | 2^168 keys → infeasible |
| **Status** | Obsolete, weak | Stronger, but being phased out in favour of AES |

The script `des_analysis.py` runs a short DES and 3DES encrypt/decrypt demo and prints this comparison.

**Conclusion:** DES should not be used in up-to-date systems; 3DES improves security but AES is the current standard.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This report |
| `openssl_demo.sh` | Part 1: OpenSSL DES demo (a)–(e) |
| `message.txt` | Part 1: (a) plaintext message |
| `encrypted.bin` | Part 1: (c) encrypted payload |
| `decrypted.txt` | Part 1: (d) decryption with correct key |
| `wrong_decrypted.txt` | Part 1: (e) decryption with wrong key (garbage) |
| `decrypt.py` | Part 2a: DES brute-force tool |
| `des_analysis.py` | Part 2b–e: Key complexity, plot, 3DES demo |
| `des_complexity_plot.png` | Part 2d: Generated by `des_analysis.py` |

**Requirements:** Python 3 with `pycryptodome`, `tqdm`, `matplotlib`, `numpy`. Use the repo’s `.venv` or install these in your environment. For Part 1, OpenSSL must be installed.
