# PL2 — Exercise 3: Hashing Functions

One-way hashing functions produce a fixed-size digest from input; they are destructive in the sense that the original data cannot be recovered from the hash.

---

## 1. Describe how a hash can be reversed

A hash is not “reversed” in the mathematical sense (no inverse function). In practice, “reversing” means **recovering an input that hashes to a given value**:

- **Brute force:** Try many inputs (passwords, strings) and compare their hash to the target. Feasible only for short or low-entropy inputs (e.g. short passwords, common words).
- **Precomputed tables (rainbow tables / lookup tables):** Precompute hashes for many inputs and store hash → input. Given a hash, look it up. Effective for common passwords and unsalted hashes; mitigated by **salting** and large keyspaces.
- **Dictionary / wordlist attacks:** Hash a list of likely inputs (e.g. rockyou.txt) and compare. Same idea as brute force but with a smarter set of candidates.
- **Collision or preimage attacks:** For weak hash functions (e.g. MD5, SHA-1), cryptanalytic attacks can find collisions or sometimes preimages faster than brute force. That does not “reverse” a single hash in the sense of inverting the function everywhere, but can help find *some* input that hashes to the target.

So “reversing” is really **finding a preimage** (or a second preimage) by guessing, lookup, or cryptanalysis, not inverting the hash function.

---

## 2. Identify the following hashes

**Length and format:**

- **(a) `93319a4441fae08309390fd2e8326002`**  
  - 32 hex characters → **128 bits** → **MD5**.

- **(b) `543b24ecc36f9811f3c6f0ee0e6df6dbe29891bb`**  
  - 40 hex characters → **160 bits** → **SHA-1**.

---

## 3. Crack both hashes using John the Ripper and Hashcat

**John the Ripper**

```bash
# Save hash to a file (one per line)
echo '93319a4441fae08309390fd2e8326002' > hashes.txt
echo '543b24ecc36f9811f3c6f0ee0e6df6dbe29891bb' >> hashes.txt

# John: detect format and run (wordlist or incremental)
john --format=raw-md5 hashes.txt
john --format=raw-sha1 hashes.txt
# Or let John detect: john hashes.txt
john --show hashes.txt
```

**Hashcat**

```bash
# MD5 (mode 0); then SHA1 (mode 100)
hashcat -m 0 -a 0 hashes.txt rockyou.txt
hashcat -m 100 -a 0 hashes.txt rockyou.txt
```

If the hashes are **salted** or in a specific format (e.g. `$1$salt$hash`), use the appropriate John/Hashcat format (e.g. `md5crypt`, `sha1crypt`). For **raw** MD5 and SHA-1 as given, the commands above apply.

---

## 4. What are collisions and why do they occur?

**Collision:** Two different inputs \(M_1 \neq M_2\) such that \(H(M_1) = H(M_2)\).

**Why they occur:**

- **Pigeonhole principle:** The hash has a fixed output size (e.g. 256 bits for SHA-256). Inputs can be arbitrarily long. There are infinitely many inputs and only finitely many outputs, so collisions must exist.
- **Cryptographic requirement:** A good hash function should make finding collisions **computationally infeasible** (e.g. ~2^{128} work for SHA-256). Weak hashes (MD5, SHA-1) have known collision attacks, so collisions can be found in practice.

**Implications:** Collisions undermine integrity guarantees (e.g. two different files with the same hash). That is why MD5 and SHA-1 are deprecated for security-sensitive use; SHA-256/SHA-512 are recommended.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This report |
| `hashes.txt` | Hashes (a) MD5 and (b) SHA-1 for cracking with John/Hashcat |
