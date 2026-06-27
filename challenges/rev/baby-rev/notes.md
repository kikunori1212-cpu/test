# Challenge Notes

## Basic Info

- Name: baby-rev
- Category: rev
- Difficulty: beginner
- Points: 467
- URL / Host:
- Files: `baby-rev.c`
- Status: solved
- Assigned: Codex
- Started: 2026-06-13

## Goal

What do we need to recover, exploit, prove, or submit?

Recover the 34-byte input accepted by the provided C verifier.

## First 10 Minutes

- [x] Problem statement copied or summarized
- [x] Attached files listed
- [ ] Service checked with browser / nc / curl
- [x] Source code, Dockerfile, package files, or binary metadata checked
- [ ] Similar pattern checked in `docs/ctf4b-2025-patterns.md`

## Observations

- The verifier requires exactly 34 bytes.
- For every position, it checks `(inp[i] ^ 0x88) == xorFlag[i]`.
- XOR is its own inverse, so `inp[i] = xorFlag[i] ^ 0x88`.
- Source SHA-256: `1E895429C547A9C4BB9C62F8B723B59DCC7F962FFE6F21DCC8F878B336BF1E98`

## Hypotheses

- Directly XOR every byte in `xorFlag` with `0x88`.

## Next Attempts

- Run `solve.py` and submit the resulting string.

## Commands

```bash
python solve.py
```

## Findings

- Recovered a valid 34-byte ASCII flag.

## Submit Check

- [x] Flag format checked
- [x] No leading/trailing whitespace
- [x] Reproducing command/script saved
- [x] Writeup updated

## Flag

```text
ctf4b{l00k_m0m_n0_h4nds_just_x0r!}
```
