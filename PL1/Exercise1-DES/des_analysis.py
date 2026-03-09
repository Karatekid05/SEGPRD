"""
PL1, Exercise 1, Part 2: Key complexity (b), symbol domain (c), plot (d), 3DES comparison (e).
Run from repo root: .venv/bin/python PL1/Exercise1-DES/des_analysis.py
Or from this folder: ../../.venv/bin/python des_analysis.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

SYMBOL_DOMAINS = {
    "lowercase (26)": 26,
    "alpha (52)": 52,
    "alphanumeric (62)": 62,
    "printable ASCII (95)": 95,
}

def keyspace_by_length(max_len=12, alphabet_size=26):
    lengths = list(range(1, max_len + 1))
    spaces = [alphabet_size ** n for n in lengths]
    return lengths, spaces

def plot_key_complexity():
    fig, ax = plt.subplots(figsize=(10, 6))
    lengths = np.arange(1, 11)
    for label, size in SYMBOL_DOMAINS.items():
        spaces = [size ** n for n in lengths]
        ax.semilogy(lengths, spaces, "o-", label=label)
    ax.set_xlabel("Key length (characters)")
    ax.set_ylabel("Keyspace size (log scale)")
    ax.set_title("(d) Key complexity: keyspace vs key length and symbol domain")
    ax.legend()
    ax.grid(True, which="both")
    import os
    out_dir = os.path.dirname(os.path.abspath(__file__))
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "des_complexity_plot.png"), dpi=150)
    print("Saved des_complexity_plot.png")
    plt.close()

def demo_3des():
    from Crypto.Cipher import DES3
    from Crypto.Random import get_random_bytes

    key_des = b"8bytes!!"
    for _ in range(10):
        try:
            key_3des_24 = DES3.adjust_key_parity(get_random_bytes(24))
            break
        except ValueError:
            continue
    else:
        key_3des_24 = DES3.adjust_key_parity(bytes(range(24)))

    plain = b"secret"
    pt_padded = pad(plain, DES.block_size)
    c_des = DES.new(key_des, DES.MODE_ECB)
    enc_des = c_des.encrypt(pt_padded)
    dec_des = unpad(DES.new(key_des, DES.MODE_ECB).decrypt(enc_des), DES.block_size)
    assert dec_des == plain

    c_3des = DES3.new(key_3des_24, DES3.MODE_ECB)
    enc_3des = c_3des.encrypt(pt_padded)
    dec_3des = unpad(DES3.new(key_3des_24, DES3.MODE_ECB).decrypt(enc_3des), DES3.block_size)
    assert dec_3des == plain

    print("\n(e) 3DES vs DES comparison")
    print("-" * 50)
    print("DES:   key 8 bytes  → 56-bit effective; 2^56 keys → brute-force feasible with hardware.")
    print("3DES:  key 24 bytes → 168-bit effective; 2^168 keys → brute-force infeasible.")
    print("3DES applies DES three times (encrypt-decrypt-encrypt) with 2 or 3 keys.")
    print("Conclusion: DES is obsolete; 3DES improves security but is being phased out for AES.")
    print("-" * 50)
    print("Demo: DES and 3DES encrypt/decrypt OK (different ciphertexts).")

def main():
    print("(b) Key complexity (alphabet size = 26)")
    lengths, spaces = keyspace_by_length(10, 26)
    for n, s in zip(lengths, spaces):
        print(f"  Length {n}: keyspace = {s:,}")
    print("  → Increasing key length → exponential growth → brute force quickly infeasible.\n")

    print("(c) Symbol domain (key length = 8)")
    for label, size in SYMBOL_DOMAINS.items():
        print(f"  {label}: keyspace = {size**8:,}")
    print("  → Larger symbol set → much larger keyspace for same length.\n")

    print("(d) Plot: saving des_complexity_plot.png")
    plot_key_complexity()
    print("  Conclusions: (1) Key length dominates (exponential). (2) Symbol domain also increases keyspace. (3) DES 8-byte key with 95 symbols ≈ 6.6e15, still brute-forceable with dedicated hardware; 3DES 168-bit is not.\n")
    demo_3des()

if __name__ == "__main__":
    main()
