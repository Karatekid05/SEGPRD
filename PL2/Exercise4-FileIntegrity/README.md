# PL2 — Exercise 4: File Integrity

Checksums (e.g. from hash functions) act as digital fingerprints to verify that data has not been modified.

---

## 1. Take a file and generate a shasum

**Using `shasum` (or `sha256sum` / `sha512sum`):**

```bash
shasum -a 256 myfile.txt
# or
sha256sum myfile.txt
```

Output format: **hex digest** followed by the filename (or `-` for stdin). Example:

```
a1b2c3...  myfile.txt
```

To check later:

```bash
shasum -a 256 -c checksums.txt
```

Where `checksums.txt` contains lines like `hexdigest  filename`.

---

## 2. Investigate problematic collisions

**Shattered (https://shattered.io/):** Google demonstrated a **SHA-1 collision**: two different PDF files with the same SHA-1 hash. This shows that SHA-1 is no longer safe for collision resistance (e.g. certificates, integrity in adversarial settings).

**Takeaways:**

- A single byte change in the file changes the hash (avalanche effect).
- For **weak** hashes (MD5, SHA-1), attackers can craft two different inputs with the same hash (collision attack).
- Such collisions break trust in “same hash ⇒ same file”; an attacker could substitute a malicious file that has the same hash as a benign one.
- **Recommendation:** Use SHA-256 or SHA-512 for integrity and security-sensitive applications; avoid MD5 and SHA-1 for new designs.

---

## 3. What changes in SHA-256 and SHA-512?

| Aspect | SHA-256 | SHA-512 |
|--------|---------|---------|
| **Output size** | 256 bits (32 bytes, 64 hex chars) | 512 bits (64 bytes, 128 hex chars) |
| **Internal state / block size** | 32-bit words, 512-bit block | 64-bit words, 1024-bit block |
| **Security (collision resistance)** | ~2^{128} effort | ~2^{256} effort |
| **Speed (on 64-bit)** | Often faster on 32-bit or when output size matters | Often faster on 64-bit CPUs (larger word size) |
| **Use** | Very common (certs, TLS, Git) | When stronger security or 64-bit optimizations are desired |

Both are in the SHA-2 family; SHA-512 is not “twice as secure” than SHA-256 in terms of practical security (both are strong), but it has a larger output and different internal design (64-bit operations).

---

## 4. Create a script to generate SHA-512 of all files on your hard drive and time it

See **`sha512_all.sh`** in this folder. It walks a directory (by default the current directory; can be set to `/` for “whole drive”) and prints `sha512sum`-style lines and optionally writes them to a file. **Warning:** Running on the whole drive can take a long time and stress the disk.

**Usage:**

```bash
chmod +x sha512_all.sh
./sha512_all.sh                    # current directory only
./sha512_all.sh /path/to/dir       # specific directory
time ./sha512_all.sh /path/to/dir  # time the run
```

**Example of timing:** Depends on disk speed and number/size of files. The script reports start/end and can be run under `time` for total elapsed time. Conclusions: hashing many files is I/O-bound; full-disk scans are slow and may interfere with other workloads (consider AIDE or similar for scheduled integrity checking).

---

## 5. Conclusions considering tools such as AIDE

- **Behavior of full-disk hashing:** Generating SHA-512 (or any hash) of every file is **expensive**: lots of I/O and CPU. Doing it on the whole drive is slow and not something you do constantly; it is typically run periodically (e.g. nightly) or on demand.
- **AIDE (Advanced Intrusion Detection Environment):** Maintains a **database** of file metadata and hashes (e.g. SHA-256/SHA-512). After an initial scan, you run **`aide --check`** to recompute hashes and compare with the database; it reports added, removed, or changed files. So you do not recompute hashes of “all files” every time; you update the DB occasionally and then run fast checks.
- **Conclusions:** (1) Full-disk hashing is a heavy operation; timing it shows it’s not suitable for real-time use. (2) Integrity monitoring in practice uses a **stored baseline** (like AIDE’s database) and periodic re-checks. (3) SHA-256 or SHA-512 provide strong integrity; avoid MD5/SHA-1 for new systems. (4) Tools like AIDE automate baseline creation, scheduling, and reporting, making integrity checking feasible for production systems.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This report |
| `sha512_all.sh` | Script to generate SHA-512 of all files under a directory; run with `time` to measure duration |
