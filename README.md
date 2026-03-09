# SEGPRD — Segurança e Privacidade de Dados

**SEGPRD** = *Segurança e Privacidade de Dados*.  
Repository for the SEGPRD course (practical labs and exercises).

## Structure

```
SEGPRD/
├── README.md           ← you are here
├── .venv/              ← Python virtual environment (create with python3 -m venv .venv)
├── rockyou.txt         ← wordlist (optional; place here or in PL1/Exercise1-DES/)
│
├── PL1/                ← Practical Lab 1
│   ├── README.md
│   ├── Exercise1-DES/  (DES: OpenSSL, brute-force, 3DES)
│   └── Exercise2-AES/  (AES: encrypt/decrypt file, comparison)
│
└── PL2/                ← Practical Lab 2 (Segurança e Privacidade de Dados)
    ├── README.md
    ├── Exercise1-PGP/       (PGP: keys, key server, email, backup design)
    ├── Exercise2-RSA/       (RSA: OpenSSL, hybrid encrypt/decrypt, ransomware/entropy)
    ├── Exercise3-Hashing/   (Hash identification, John/Hashcat, collisions)
    └── Exercise4-FileIntegrity/  (shasum, Shattered, SHA-512 script, AIDE)
```

## Quick start

1. **Python environment** (from repo root):
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install pycryptodome tqdm matplotlib numpy
   ```

2. **Exercise 1 — DES**
   - Part 1 (OpenSSL): `cd PL1/Exercise1-DES && ./openssl_demo.sh`
   - Part 2 (brute-force): `.venv/bin/python PL1/Exercise1-DES/decrypt.py`
   - Part 2 (analysis + plot): `.venv/bin/python PL1/Exercise1-DES/des_analysis.py`
   - See **PL1/Exercise1-DES/README.md** for the full report.

3. **Exercise 2 — AES**
   - Encrypt/decrypt file + timing: `.venv/bin/python PL1/Exercise2-AES/aes_file.py`
   - See **PL1/Exercise2-AES/README.md** for the report and AES vs DES/3DES comparison.

4. **PL2** — See **PL2/README.md** for PGP, RSA, Hashing, and File Integrity exercises.

## Git

If you want this directory to be its own Git repository:

```bash
cd /path/to/SEGPRD
git init
git add .
# Add rockyou.txt only if you want (it is large); or add it to .gitignore
git commit -m "PL1 Exercise 1: DES"
```
