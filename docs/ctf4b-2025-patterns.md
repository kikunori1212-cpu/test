# CTF4B 2025 Pattern Notes

SECCON Beginners CTF 2025 の writeup から、2026 本番で初動を速くするための観察ポイントを抽出したメモ。

## Web

### Header / Path tricks

- まずソースコード、README、Dockerfile、ルーティングを見る。
- `curl -v` でレスポンスヘッダ、リダイレクト、拒否理由を見る。
- `/flag` が拒否される場合、カスタムヘッダ、メソッド変更、パス正規化を試す。

Useful commands:

```bash
curl -v http://HOST/
curl -v -H 'x-ctf4b-request: ctf4b' http://HOST/flag
curl -v -X POST http://HOST/flag
```

### Directory traversal / proc leaks

- ログビューアやファイル名指定がある場合は traversal を疑う。
- Linux コンテナでは `/proc/self/cmdline`、`/proc/self/environ`、`/app`、`/flag` を候補にする。
- エラーログ内の typo やファイル名のヒントをそのまま信じすぎない。

Useful payloads:

```text
../.env
../../proc/self/cmdline
../../proc/self/environ
../../app/app.py
```

### LLM / RAG function misuse

- AI が tool/function calling できる問題では、関数名、引数名、フィルタ条件を探す。
- 禁止語フィルタは分割、置換指示、出力変換で回避できる場合がある。
- 「検索して」「secret を含めて」「特定 user id で」など、権限境界を明示して試す。

### XSS

- サニタイズ後に URL 化、絵文字変換、Markdown 変換、リンク化が走る場合は危険。
- コロン、引用符、スラッシュが制限される場合は Base64、`atob`、イベント属性、別構文を検討する。
- bot/admin が読む問題では `/flag` 取得と外部送信の両方を設計する。

## Crypto

### RSA with weak parameters

- `p` と `q` のビット長が偏っていないかを見る。
- 小さい素因数、近い素数、共通因数、低指数、同一 modulus を先に試す。

```python
from Crypto.Util.number import long_to_bytes

for q in range(2, 2**20):
    if n % q == 0:
        p = n // q
        phi = (p - 1) * (q - 1)
        d = pow(e, -1, phi)
        print(long_to_bytes(pow(c, d, n)))
        break
```

### ECB / block oracle

- 同じ平文ブロックが同じ暗号文ブロックになるなら ECB を疑う。
- 入力できる文字列を 16 バイト境界に揃え、0/1 や候補文字をブロック単位で対応付ける。

## Reversing

### Native binaries

- `file`、`strings`、実行、Ghidra の順で見る。
- 逆コンパイルが崩れる場合は Ghidra のバージョン更新、関数境界修正、アセンブリ確認を試す。
- 文字比較の羅列は、手で読むよりスクリプトで回収する。

### WASM

- `wasm2wat` で WAT に戻し、`i32.const` と比較命令の組を抽出する。
- 位置変換や XOR がある場合、チェック式を Python に移して flag 配列を復元する。

## Pwn

- まず `checksec`、実行、入出力、クラッシュ条件を確認する。
- beginner/easy では ret2win、BOF、format string、整数境界、固定 seed を優先して見る。
- リモート総当たりに寄せない。問題文やソースに必ず短い道がある前提で探す。

## Misc / Forensics

- `file`、`strings`、`exiftool`、`binwalk`、`7z l`、`xxd` を初動セットにする。
- 画像、pcap、zip、ログはメタデータと埋め込みを先に見る。
- パスワード付き zip は問題文、ファイル名、既知文字列、弱い形式から探す。

## Fast Triage

1. 問題文から「入力できるもの」「出力されるもの」「添付ファイル」「接続先」を分ける。
2. beginner/easy は 15 分で初動チェックを終える。
3. medium 以上は、解法候補を 2-3 個に絞ってから深掘りする。
4. 迷ったら `notes.md` の `Next Attempts` に残して別問題へ移る。

## Source

- https://qiita.com/kusano_k/items/e06defb55cdd3e4e4631
