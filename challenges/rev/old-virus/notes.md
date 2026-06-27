# Challenge Notes

## Basic Info

- Name: old-virus
- Category: rev
- Difficulty: hard
- Points: 498
- URL / Host:
- Files: `old-virus`, `flag.txt.hacked`
- Status: solved
- Assigned: Codex
- Started: 2026-06-13

## Goal

What do we need to recover, exploit, prove, or submit?

Reverse the fake ransomware and decrypt `flag.txt.hacked`.

## First 10 Minutes

- [x] Problem statement copied or summarized
- [x] Attached files listed
- [ ] Service checked with browser / nc / curl
- [x] Source code, Dockerfile, package files, or binary metadata checked
- [x] Similar pattern checked in `docs/ctf4b-2025-patterns.md`

## Observations

- `old-virus` is an unstripped x86-64 PIE ELF linked with OpenSSL 3.
- Archive SHA-256: `5C3C98AC16FE61A1434C764803DCF5DDEC12B0CA3B48911E9E5DEB69B6CE3166`.
- Symbols expose `rc4`, `aes_ecb_encrypt`, `AES_KEY`, and `RC4_KEY`.
- `.rodata` contains AES key `THISISNOTAESKEY!`.
- `.rodata` contains RC4 key `ImashyKey!Dontlookme!!!`.
- `main` encrypts the input using AES-128-ECB with padding, then applies RC4.
- The encrypted file is 48 bytes.

## Hypotheses

- Reverse the operations: RC4 decrypt, AES-128-ECB decrypt, then PKCS#7 unpad.

## Next Attempts

- Run `solve.py`.

## Commands

```bash
python solve.py
```

## Findings

- Recovered an ASCII flag followed by a newline.

## Submit Check

- [x] Flag format checked
- [x] No leading/trailing whitespace
- [x] Reproducing command/script saved
- [x] Writeup updated

## Flag

```text
ctf4b{Y2K_n05t419ic_viru5_6ut_G2G}
```
