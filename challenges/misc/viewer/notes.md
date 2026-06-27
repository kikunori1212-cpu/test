# Challenge Notes

## Basic Info

- Name: viewer
- Category: misc
- Difficulty: easy
- Points: 500
- URL / Host: viewer.beginners.seccon.games:33458
- Files:
- Status: solved
- Assigned: Codex
- Started: 2026-06-13

## Goal

What do we need to recover, exploit, prove, or submit?

Read the blocked `flag.txt` file.

## First 10 Minutes

- [ ] Problem statement copied or summarized
- [ ] Attached files listed
- [x] Service checked with browser / nc / curl
- [ ] Source code, Dockerfile, package files, or binary metadata checked
- [x] Similar pattern checked in `docs/ctf4b-2025-patterns.md`

## Observations

- `readme.txt` and `hello.txt` are listed and readable.
- Input containing lowercase `flag` is rejected with `blocked`.
- Slash-containing paths are rejected with `invalid path`.
- URL and backslash escape forms are not decoded.
- Fullwidth `ｆｌａｇ.txt` bypasses the substring check and is later normalized to `flag.txt`.

## Hypotheses

- Filtering occurs before Unicode normalization.
- Compatibility normalization such as NFKC converts fullwidth ASCII letters to normal ASCII.

## Next Attempts

- Send UTF-8 encoded `ｆｌａｇ.txt`.

## Commands

```bash
python solve.py
```

## Findings

- The filter and the filesystem lookup must operate on the same normalized representation.

## Submit Check

- [x] Flag format checked
- [x] No leading/trailing whitespace
- [x] Reproducing command/script saved
- [ ] Writeup updated

## Flag

```text
ctf4b{un1C0dE_N0rMal12a710n_15_7r1CKy}
```
