# SECCON Beginners CTF 2026 Preparation

## Event

- Name: SECCON Beginners CTF 2026
- Format: Jeopardy
- Schedule: 2026/6/13 14:00 JST - 2026/6/14 14:00 JST
- Duration: 24 hours
- Registration: 2026/6/6 start予定
- Communication: 公式 Discord のアナウンスを確認する
- Flag format: `ctf4b{...}` が基本想定

## Goals

- 開始 30 分以内に全問題を眺め、beginner/easy を優先して着手する。
- 解けそうな問題は `tools/new_challenge.py` で即座に作業フォルダ化する。
- 各問題で `notes.md` に観察、仮説、試したコマンド、flag提出結果を残す。
- 30-60 分詰まったら、いったんメモを整理して別問題へ移る。

## Before Contest

### 1 week before

- [ ] 参加登録、チーム登録、Discord 参加を完了する。
- [ ] `tools/check_environment.ps1` を実行し、不足ツールを埋める。
- [ ] Python 仮想環境を作成し、`pip install -r requirements.txt` を通す。
- [ ] Ghidra、Wireshark/tshark、7-Zip、curl、Node.js、WSL を起動確認する。
- [ ] 2025 writeup のパターンを `docs/ctf4b-2025-patterns.md` で復習する。

### Day before

- [ ] `tools/prepare_seccon_beginners_2026.ps1` を実行する。
- [ ] ブラウザ、Burp Suite / DevTools、curl、Python REPL を開ける状態にする。
- [ ] チーム連絡用のメモ場所を決める。
- [ ] ルールと禁止事項を読み直す。外部への攻撃や過度な負荷は禁止。

## Contest Startup

1. 全問題のカテゴリ、難易度、添付ファイル、URL/Host を一覧化する。
2. beginner/easy から着手し、解けたらすぐ再現手順を書く。
3. web は DevTools、curl、ソースコード、ログ、ヘッダ、パスを先に見る。
4. crypto はパラメータ、鍵長、乱数、モード、同一ブロック、既知平文を先に見る。
5. rev は `file`、`strings`、Ghidra、WASM/WAT、実行時入力を先に見る。
6. pwn は `checksec`、実行、入出力、境界値、format string、整数を先に見る。

## Directory Plan

大会用フォルダは以下の形に揃える。

```text
challenges/
  web/
  crypto/
  rev/
  pwn/
  misc/
  forensics/
```

新規問題を作る例:

```powershell
python tools\new_challenge.py web skipping-like
python tools\new_challenge.py crypto small-prime-rsa
python tools\new_challenge.py rev wasm-checker
```

## Flag Submission Checklist

- [ ] `ctf4b{...}` の形になっている。
- [ ] 前後に空白、改行、引用符が混ざっていない。
- [ ] URL デコード、HTML エスケープ、Base64 デコード漏れがない。
- [ ] 同じ flag を別問題に提出していない。
- [ ] 提出後、`notes.md` と `writeup.md` に再現手順を残した。

## References

- Official: https://www.seccon.jp/15/seccon_beginners/ctf.html
- 2025 writeup used for pattern study: https://qiita.com/kusano_k/items/e06defb55cdd3e4e4631
