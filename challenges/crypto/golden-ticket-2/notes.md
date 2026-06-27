# Challenge Notes

## Basic Info

- Name: Golden Ticket 2
- Category: crypto
- Difficulty: hard
- Points: 500
- URL / Host: golden-ticket-2.beginners.seccon.games:9999
- Files: `golden-ticket-2.zip`, `golden-ticket-2.py`
- Status: blocked by probable challenge issue
- Assigned: Codex
- Started: 2026-06-13

## Goal

What do we need to recover, exploit, prove, or submit?

Forge a CBC encryption of the server's 96-byte challenge and obtain a golden ticket.

## First 10 Minutes

- [x] Problem statement copied or summarized
- [ ] Attached files listed
- [x] Service checked with browser / nc / curl
- [ ] Source code, Dockerfile, package files, or binary metadata checked
- [x] Similar pattern checked in `docs/ctf4b-2025-patterns.md`

## Observations

- Initial tickets: 3 encryption, 10000 decryption.
- `Encrypt` accepts at most 16 plaintext bytes.
- Encrypting 1-16 bytes returns one 16-byte ciphertext block.
- Encrypting exactly 16 bytes returns two blocks due to PKCS#7 padding.
- `Decrypt` accepts at most 32 ciphertext bytes and removes padding.
- Invalid ciphertext/padding closes the session.
- `Get ticket` returns a random 96-byte challenge.
- The expected answer length is 112 bytes: a 16-byte IV plus six ciphertext blocks.
- Keys/IVs are connection-local. Identical plaintexts encrypt differently across connections.
- A valid ciphertext from one connection fails padding validation in another, confirming the key is not shared.
- The 2025 official challenge used AES-CBC and a broken decrypt oracle that padded ciphertext before decrypting.
- The 2025 official solver no longer works because the sequel changed input limits/decryption behavior.
- Distributed archive SHA-256: `91C9A1E74A77E9A97D33D0E0807B9C9C5B11AB2314D184E2336924C7AFA5D2BE`.
- The distributed source matches the observed remote behavior.
- Each correct ticket answer adds only `0.25` golden tickets.
- Each correct answer immediately replaces the AES key with a fresh `os.urandom(16)` key.
- The IV and challenge remain fixed, but AES oracle transcripts from the previous key become unusable.
- Four successful forgeries under four independent AES keys are therefore required.
- Encryption tickets are not replenished and only three are available for the whole connection.
- Invalid CBC length or invalid PKCS#7 padding raises an uncaught `ValueError`.
- Docker runs `socat ... fork ... EXEC:"python golden-ticket-2.py"`, so the exception terminates the per-connection Python process and loses its key, ticket balance, and accumulated golden tickets.

## Hypotheses

- The sequel appears intended to use a CBC padding/decryption oracle.
- As distributed, a failed padding guess destroys the only process holding the current AES key.
- Even a successful first padding guess does not resolve the mismatch between four independent keys and three total encryption tickets.
- No user-controlled input reaches `GOLDEN_TICKET`, `key`, or `ENC_TICKET` except through the fixed menu operations.
- This strongly suggests a missing exception handler, missing ticket reset, incorrect `0.25`, or another deployment/source bug.

## Next Attempts

- Check official announcements for a patch.
- Ask the organizer whether `ValueError` termination, `GOLDEN_TICKET += 0.25`, and non-resetting `ENC_TICKET` are intended.
- Re-download the attachment and re-test the service after any update.
- Complete the solver once the intended state transition is confirmed.

## Commands

```bash
nc golden-ticket-2.beginners.seccon.games 9999
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
