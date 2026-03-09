# PL2 — Exercise 1: PGP

Pretty Good Privacy provides cryptographic privacy and authentication for data communication (e.g. email, files).

---

## 1. Create a PGP key pair

**Using GnuPG (gpg):**

```bash
gpg --full-generate-key
```

- Choose key type: RSA and RSA (default) or ECC.
- Key size: 4096 bits recommended for RSA.
- Set expiration (or 0 = no expiry).
- Enter your name, email, and optional comment.
- Set a **passphrase** to protect the private key.

List keys:

```bash
gpg --list-secret-keys --keyid-format=long
gpg --list-keys
```

Export public key (to share):

```bash
gpg --armor --export YOUR_EMAIL@example.com > my_public.asc
```

---

## 2. Upload your PGP key to a key server

```bash
gpg --keyserver keys.openpgp.org --send-keys YOUR_KEY_ID
```

Replace `YOUR_KEY_ID` with the long key ID (e.g. from `gpg --list-keys`). Other key servers: `keyserver.ubuntu.com`, `pgp.mit.edu`.

---

## 3. Integrate your key with your email client

**Thunderbird**

- Install **OpenPGP** (or Enigmail legacy): Add-ons → search “OpenPGP” / “Thunderbird OpenPGP”.
- Settings → Privacy & Security → OpenPGP: enable and select “Use a separate key”.
- Import your key or generate one in Thunderbird; attach your key to your account.
- Compose: you can then sign and/or encrypt messages.

**Outlook**

- Use a plugin that supports PGP (e.g. **Gpg4win** with **GpgOL**, or **p≡p**), or use a bridge/add-in that integrates GnuPG with Outlook.

---

## 4. Send an encrypted and signed message to your teacher

- Import the **teacher’s public key**: `gpg --import teacher_public.asc`.
- Compose the message in your client (Thunderbird/Outlook with PGP).
- **Sign** with your private key (proves identity).
- **Encrypt** with the teacher’s public key (only they can decrypt).
- Send the message. The teacher decrypts with their private key and verifies the signature with your public key.

---

## 5. Encrypt a file using a colleague’s key and send it to them

```bash
gpg --encrypt --recipient colleague@example.com --output document.pdf.gpg document.pdf
```

Send `document.pdf.gpg` to your colleague (email, USB, etc.). Only someone with the private key for `colleague@example.com` can decrypt it.

---

## 6. Decrypt your received file

```bash
gpg --decrypt received_file.gpg --output received_file
```

You will be prompted for your passphrase if the file was encrypted to your public key.

---

## 7. Design a system for system backups using PGP; what could you gain?

**Design (high level):**

- **Backup flow:** Periodically (e.g. cron) run a backup job that creates archives (e.g. tar + compression) of selected directories/files, then encrypt each archive with PGP using a **dedicated backup public key**.
- **Key management:** Use a key pair only for backups: public key on the backup server/script; private key stored offline or in a HSM/vault, only used when restoring.
- **Storage:** Store only the encrypted blobs (e.g. on NAS, cloud, or tape). No need to trust storage with plaintext.

**What you gain:**

- **Confidentiality:** Backups are useless to anyone who steals or finds the media without the private key.
- **Integrity + authentication:** Optionally sign backups with a second key so you can verify that the backup was produced by your system and was not tampered with.
- **Compliance:** Helps meet requirements for encryption of sensitive data at rest.
- **Separation of roles:** Restore only where the backup private key is available, reducing risk of accidental or malicious exposure.

**Practical note:** Key and passphrase recovery must be planned (e.g. secure escrow); losing the backup decryption key means losing the backups.
