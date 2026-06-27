# baby-rev

## Summary

- Category: rev
- Difficulty: beginner
- Solved by: Codex
- Flag: `ctf4b{l00k_m0m_n0_h4nds_just_x0r!}`
- Time spent: under 5 minutes
- Source files / service: `baby-rev.c`

## Problem

The provided C program accepts a 34-byte input and compares each input byte after XOR with a fixed key against a constant byte array.

## Approach

The check is `(inp[i] ^ 0x88) != xorFlag[i]`. Since XOR is reversible with the same key, each original input byte is `xorFlag[i] ^ 0x88`.

## Reproduction

Run the included Python solver.

## Solution

```bash
python solve.py
```

## Why It Works

XOR with a known fixed key provides no secrecy. Applying the same XOR operation to the stored bytes recovers the original input.

## Lessons Learned

- Constant XOR verification can be reversed directly.
- Reading the comparison expression carefully is enough; no debugger or decompiler is needed.
