# old-virus

## Summary

- Category: rev
- Difficulty: hard
- Solved by: Codex
- Flag: `ctf4b{Y2K_n05t419ic_viru5_6ut_G2G}`
- Time spent: about 10 minutes
- Source files / service: `old-virus`, `flag.txt.hacked`

## Problem

The archive contains a fake ransomware ELF and an encrypted flag file. The binary is unstripped and retains both cryptographic function names and keys.

## Approach

Static inspection with `file`, `strings`, `readelf`, and `objdump` identified an AES-128-ECB encryption function followed by an RC4 function. The AES and RC4 keys were stored in `.rodata`. Reversing the operation order decrypts the supplied file.

## Reproduction

Install PyCryptodome if needed and run the solver.

## Solution

```bash
python solve.py
```

## Why It Works

The encryption keys are embedded as plaintext constants in the executable. The program applies AES-128-ECB with PKCS#7 padding and then RC4, so the ciphertext can be decrypted using the exposed keys in reverse order.

## Lessons Learned

- Do not execute malware-like samples before static inspection.
- Symbols and `.rodata` can reveal most of an unstripped binary's design immediately.
- Layered encryption must be undone in reverse order.
