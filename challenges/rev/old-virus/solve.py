from __future__ import annotations

from pathlib import Path

from Crypto.Cipher import AES, ARC4
from Crypto.Util.Padding import unpad


AES_KEY = b"THISISNOTAESKEY!"
RC4_KEY = b"ImashyKey!Dontlookme!!!"
CIPHERTEXT = Path(__file__).with_name("artifact") / "flag.txt.hacked"


def main() -> None:
    encrypted = CIPHERTEXT.read_bytes()
    aes_ciphertext = ARC4.new(RC4_KEY).decrypt(encrypted)
    padded_plaintext = AES.new(AES_KEY, AES.MODE_ECB).decrypt(aes_ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    print(plaintext.decode("ascii").strip())


if __name__ == "__main__":
    main()
