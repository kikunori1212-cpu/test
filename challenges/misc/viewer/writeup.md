# viewer

## Summary

- Category: misc
- Difficulty: easy
- Solved by: Codex
- Flag: `ctf4b{un1C0dE_N0rMal12a710n_15_7r1CKy}`
- Time spent: about 15 minutes
- Source files / service: `viewer.beginners.seccon.games:33458`

## Problem

The service displays selected files but blocks filenames containing `flag`.

## Approach

Basic traversal, shell metacharacters, URL encoding, and escape sequences did not work. Sending the fullwidth filename `ｆｌａｇ.txt` bypassed the lowercase ASCII substring filter. The service then normalized the filename to `flag.txt` before reading it.

## Reproduction

Run `python solve.py`.

## Solution

```bash
python solve.py
```

## Why It Works

The security check runs before Unicode compatibility normalization. NFKC-style normalization converts fullwidth ASCII characters into ordinary ASCII, so the checked name and opened name differ.

## Lessons Learned

- Normalize input before applying security checks.
- Use the same canonical representation for validation and file lookup.
