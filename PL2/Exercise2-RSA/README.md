# PL2 — Exercise 2: RSA

RSA (Rivest–Shamir–Adleman) is a public-key cryptosystem based on the hardness of factoring large integers. It enables secure transmission and digital signatures.

---

## 1. Generate a key pair using OpenSSL

```bash
# Private key (e.g. 2048-bit RSA)
openssl genrsa -out private.pem 2048

# Extract public key
openssl rsa -in private.pem -pubout -out public.pem
```

**Larger key (stronger, slower):** e.g. `openssl genrsa -out private.pem 4096`.

---

## 2. Encrypt a file using a key

RSA encrypts only small data (smaller than the key size in bytes). For files, use **hybrid encryption**: encrypt the file with a symmetric key (e.g. AES), then encrypt that key with RSA.

**Encrypt a short message (e.g. symmetric key) with the public key:**

```bash
# RSA can encrypt only limited data; for a key (e.g. 32 bytes for AES-256)
openssl rsautl -encrypt -pubin -inkey public.pem -in symmetric_key.bin -out symmetric_key.enc
```

The script `rsa_file.py` (or the commands in `rsa_openssl.sh`) implement hybrid: generate random AES key, encrypt file with AES, encrypt AES key with RSA public key.

**Using the provided script (hybrid encryption):**

```bash
# From PL2/Exercise2-RSA/ (or pass full paths)
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
echo "Hello RSA" > sample.txt
chmod +x rsa_openssl.sh
./rsa_openssl.sh encrypt sample.txt public.pem
# Produces: sample.txt.enc (IV + AES ciphertext) + sample.txt.key.enc (RSA-encrypted AES key)
```

---

## 3. Decrypt the file using the same key and the corresponding key

**Decrypt the symmetric key with the private key:**

```bash
openssl rsautl -decrypt -inkey private.pem -in symmetric_key.enc -out symmetric_key.bin
```

Then decrypt the file with that symmetric key (AES). The provided script automates this:

```bash
./rsa_openssl.sh decrypt sample.txt.enc sample.txt.key.enc private.pem
# Produces: sample.txt (restored)
```

---

## 4. How can you use this in a simple ransomware program? How many days would it be necessary to crack?

**Simple ransomware idea:**

- Attacker generates an RSA key pair; embeds the **public** key in the malware.
- For each victim file: generate a random AES key, encrypt the file with AES, encrypt the AES key with the **public** key; delete the plaintext and the unencrypted AES key.
- Only the **private** key (held by the attacker) can decrypt the AES keys, hence the files.
- Victim cannot recover files without the private key or paying the ransom.

**How many days to “crack”?**

- “Cracking” here means **factoring** the RSA modulus (or breaking the key). Security depends on the key size.
- **2048-bit RSA:** Current estimates (e.g. NIST, keylength.com) assume 2048-bit RSA is safe until at least 2030; factoring it with general-purpose algorithms (GNFS) is out of reach for today’s technology (would take an enormous number of years with current hardware).
- **1024-bit RSA:** Deprecated; has been factored in the past with large efforts; not recommended.
- So with **2048-bit or 4096-bit RSA**, the answer in practice is: **infeasible** (not “X days” with current technology). Ransomware security relies on the private key never being recovered, not on “days to crack.”

---

## 5. What entropy should you adopt?

- **Key generation:** RSA key pair must be generated from a **cryptographically secure random source** (e.g. OpenSSL’s RNG, which uses OS entropy). No custom low-entropy source.
- **Key size:** For long-term security, use at least **2048 bits**; **3072 or 4096 bits** for higher security or longer validity. NIST recommends 2048 bits until 2030, 3072 for beyond.
- **Entropy source:** Rely on the OS/OpenSSL default (e.g. `/dev/urandom`, CSPRNG). Ensure the system has enough entropy (e.g. on headless servers, consider hardware RNG or delayed first use).
- **Passwords/passphrases** (if you protect the private key with one): Use a high-entropy passphrase (long, random or diceware). Entropy here refers to unpredictability of the passphrase, not the RSA modulus.

**Summary:** Use 2048-bit (minimum) or 3072/4096-bit RSA; generate keys with OpenSSL’s default CSPRNG; protect private keys with high-entropy passphrases if encrypted.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This report |
| `rsa_openssl.sh` | Hybrid encrypt/decrypt file (AES-256-CBC + RSA) with OpenSSL |
