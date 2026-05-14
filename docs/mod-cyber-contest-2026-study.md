# 防衛省サイバーコンテスト2026 対策メモ

Source:

- Money Forward Developers Blog: https://moneyforward-dev.jp/entry/2026/02/16/142824
- T45K blog: https://t45k.github.io/blog/mod_ctf_2026/

## Contest Snapshot

- Date: 2026-02-01 10:00-18:00
- Format: Online Jeopardy CTF
- Flag format: `flag{...}`
- Categories seen in the writeup: Welcome, Crypto, Forensics, Network, Programming, Pwn, Web, Misc
- Scoring: 10, 20, 30 point challenges
- Important rule: Do not attack the score server or disrupt challenge servers.

## Problems Mentioned

| Challenge | Category | Points | Main skill |
| --- | --- | ---: | --- |
| 突破された認証 | Web | 30 | Tor onion service, client auth confusion, Host header routing |
| 静寂の調べ | Web | 20 | Stored XSS, `iframe srcdoc`, external exfiltration receiver |
| 空中の架け橋 | Network | 30 | Network protocol analysis |
| 運命の数字 | Network | 10 | Packet/protocol clue extraction |
| 怪しい名前解決 | Network | 20 | DNS analysis |
| 断片の記憶 | Forensics | 30 | File/memory fragment reconstruction |
| 囚われの記録 | Forensics | 20 | Artifact/log analysis |
| 刻まれし証 | Forensics | 20 | Evidence extraction |
| 脅威の報告 | Forensics | 10 | Threat report / IOC reading |
| 埋もれし痕跡 | Forensics | 10 | Hidden artifact discovery |
| 細胞の回帰 | Programming | 30 | Data processing / algorithmic reconstruction |
| 認証問合 | Programming | 20 | Automation around auth/query logic |
| 三角の綻び | Programming | 10 | Small algorithmic puzzle |

## Practical Lessons

### AIに任せる前に渡す情報

- 競技ルール、禁止事項、フラグ形式、カテゴリ一覧を最初に共有する。
- ヒントは得点を消費する場合があるため、勝手に開かないルールを明文化する。
- AIには「実装」を任せ、人間は「何を疑うか」を明示する。
- 問題文の違和感、接続先、認証キーの用途、Hostヘッダー、外部通信の可否を必ず確認する。

### Web

Preparation:

- Burp Suite Community, browser DevTools, curl/httpx, Beeceptorなど一時Webhookを準備する。
- XSSでは `<script>` と `on*` が止められても、`iframe srcdoc`、SVG、HTML entity、URL contextを試す。
- 認証バイパスでは Host header、reverse proxy、virtual host、cookie scope、client certificate/key の用途違いを疑う。

Checklist:

- `Host`, `X-Forwarded-Host`, `X-Original-URL`, `X-Rewrite-URL` を確認する。
- Admin bot問題では、外部から受け取れるWebhookを先に用意する。
- Tor問題では Onion URL、client authファイル、対象ドメイン、秘密鍵の対応関係を表にする。

### Network

Preparation:

- Wireshark, tshark, NetworkMiner系の解析環境を準備する。
- DNS, HTTP, TLS SNI, TCP stream, ICMP, unusual port, file carving を素早く見る。

Checklist:

- `tshark -r file.pcapng -q -z conv,tcp`
- `tshark -r file.pcapng -Y dns`
- Wiresharkの Follow TCP Stream / Export Objects を使う。

### Forensics

Preparation:

- CyberChef, binwalk, exiftool, strings, 7-Zip, Python Pillow を準備する。
- ファイル先頭・末尾、マジックバイト、メタデータ、埋め込みアーカイブを確認する。

Checklist:

- `file`, `exiftool`, `strings`, `binwalk`, `xxd`
- 画像は LSB、alpha channel、palette、EXIF、QR を確認する。
- ログは時系列、ユーザー名、IP、User-Agent、失敗/成功イベントを並べる。

### Programming

Preparation:

- Pythonで即席パーサ、探索、復号、整形を作る。
- z3, numpy, regex, itertools, collections をすぐ使える状態にする。

Checklist:

- 入力形式を保存し、最小ケースでスクリプトを作る。
- brute forceは探索空間を見積もってから実行する。
- 結果を `notes.md` にコマンドごと残す。

### Pwn / Rev / Crypto

Preparation:

- Ghidra, gdb/gef, pwntools, ROPgadget, pycryptodome, z3 を準備する。
- Windowsでpwnをやる場合はWSL Ubuntu側に寄せると楽。

Checklist:

- `checksec`, `strings`, `file`, `objdump`, `ltrace/strace`
- Cryptoは RSA parameters, reuse, small exponent, XOR, base64, encoding chain をまず見る。

## Recommended Practice Plan

1. Web: Stored XSS + webhook受信を10分で再現する。
2. Web: Host headerによるvirtual host切り替えをローカルで再現する。
3. Network: pcapからDNSクエリ、HTTP object、TCP streamを抽出する。
4. Forensics: 画像・zip・ログから隠し情報を見つける練習をする。
5. Programming: 入力ファイルを読み、復号・探索・整形してflag形式を出すテンプレを作る。
6. Team ops: 問題ごとに担当、試行、発見、flagを `notes.md` に残す。
