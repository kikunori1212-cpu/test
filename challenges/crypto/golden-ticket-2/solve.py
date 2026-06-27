from __future__ import annotations

import re
import socket


HOST = "golden-ticket-2.beginners.seccon.games"
PORT = 9999
BLOCK_SIZE = 16
SOLVER_COMPLETE = False


def xor_bytes(*values: bytes) -> bytes:
    return bytes(a ^ b ^ c for a, b, c in zip(*values, strict=True))


def recv_until(sock: socket.socket, marker: bytes) -> bytes:
    data = bytearray()
    while not data.endswith(marker):
        chunk = sock.recv(4096)
        if not chunk:
            raise ConnectionError("connection closed")
        data.extend(chunk)
    return bytes(data)


def encrypt(sock: socket.socket, plaintext: bytes) -> bytes:
    sock.sendall(b"1\n")
    recv_until(sock, b"pt> ")
    sock.sendall(plaintext.hex().encode() + b"\n")
    response = recv_until(sock, b"> ")
    match = re.search(rb"ct: ([0-9a-f]+)", response)
    if not match:
        raise RuntimeError(response.decode(errors="replace"))
    return bytes.fromhex(match.group(1).decode())


def decrypt(sock: socket.socket, ciphertext: bytes) -> bytes:
    sock.sendall(b"2\n")
    recv_until(sock, b"ct> ")
    sock.sendall(ciphertext.hex().encode() + b"\n")
    response = recv_until(sock, b"> ")
    match = re.search(rb"pt: ([0-9a-f]*)", response)
    if not match:
        raise RuntimeError(response.decode(errors="replace"))
    return bytes.fromhex(match.group(1).decode())


def get_challenge(sock: socket.socket, answer: bytes) -> tuple[bytes, bytes]:
    sock.sendall(b"3\n")
    response = recv_until(sock, b"answer> ")
    match = re.search(rb"challenge: ([0-9a-f]+)", response)
    if not match:
        raise RuntimeError(response.decode(errors="replace"))
    challenge = bytes.fromhex(match.group(1).decode())
    sock.sendall(answer.hex().encode() + b"\n")
    result = recv_until(sock, b"> ")
    return challenge, result


def main() -> None:
    if not SOLVER_COMPLETE:
        raise SystemExit(
            "Solver is incomplete. Download the Golden Ticket 2 attachment "
            "and inspect the exact decrypt-oracle implementation first."
        )

    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        sock.settimeout(10)
        recv_until(sock, b"> ")

        challenge, _ = get_challenge(sock, b"\x00")
        blocks = [
            challenge[i : i + BLOCK_SIZE]
            for i in range(0, len(challenge), BLOCK_SIZE)
        ]
        if len(blocks) != 6:
            raise RuntimeError(f"unexpected challenge size: {len(challenge)}")

        first = encrypt(sock, blocks[0] + blocks[1])
        c1, c2, padding_block = (
            first[0:16],
            first[16:32],
            first[32:48],
        )

        leaked = decrypt(sock, c2 + padding_block)
        if len(leaked) != BLOCK_SIZE:
            raise RuntimeError(f"unexpected decrypt output: {leaked.hex()}")
        iv = xor_bytes(leaked, blocks[1], c1)

        second_input = xor_bytes(blocks[2], c2, iv) + blocks[3]
        second = encrypt(sock, second_input)
        c3, c4 = second[0:16], second[16:32]

        third_input = xor_bytes(blocks[4], c4, iv) + blocks[5]
        third = encrypt(sock, third_input)
        c5, c6 = third[0:16], third[16:32]

        answer = iv + c1 + c2 + c3 + c4 + c5 + c6
        repeated_challenge, result = get_challenge(sock, answer)
        if repeated_challenge != challenge or b"Correct!" not in result:
            raise RuntimeError(result.decode(errors="replace"))

        sock.sendall(b"4\n")
        response = sock.recv(4096).decode(errors="replace")
        print(response.strip())


if __name__ == "__main__":
    main()
