# Challenge Notes

## Basic Info

- Name:
- Category: misc
- Difficulty: beginner
- Points: 500
- URL / Host: omikuji.beginners.seccon.games:33457
- Files:
- Status: investigating
- Assigned: Codex
- Started: 2026-06-13

## Goal

What do we need to recover, exploit, prove, or submit?

Predict five consecutive omikuji numbers and recover the flag.

## First 10 Minutes

- [ ] Problem statement copied or summarized
- [ ] Attached files listed
- [x] Service checked with browser / nc / curl
- [ ] Source code, Dockerfile, package files, or binary metadata checked
- [ ] Similar pattern checked in `docs/ctf4b-2025-patterns.md`

## Observations

- Initial prompt asks for a name, then asks for five guesses.
- A wrong first guess immediately prints `wrong` and closes the connection.
- Names up to 64 bytes reach the guess prompt.
- With 65 or more bytes, the remainder is consumed as the first guess and the service prints `wrong`.
- Literal `%p`, `{7*7}`, and `$(id)` names are echoed without evaluation.
- Typical `random.seed(name)` predictions did not match.
- Typical Python `random.seed(int(time.time()))` predictions for small ranges did not match.
- Repeated fixed-name guesses in the range 1-10 did not reach guess 2.

## Hypotheses

- The service likely reads socket input in 64-byte chunks.
- The intended weakness is probably visible in the distributed source or container files.
- Possible remaining areas: PRNG state construction, hash/truncation issue, or multi-read input confusion.

## Next Attempts

- Download the challenge attachment/source from the score site.
- Inspect the exact number generation, range, seed, and input parser.
- Build a local predictor and confirm it reaches `guess 2` before submitting all five.

## Commands

```bash
nc omikuji.beginners.seccon.games 33457
```

## Findings

-

## Submit Check

- [ ] Flag format checked
- [ ] No leading/trailing whitespace
- [ ] Reproducing command/script saved
- [ ] Writeup updated

## Flag

```text

```
