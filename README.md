# CTF Workspace

CTF に向けた調査、解法メモ、スクリプト、writeup をまとめるための作業用リポジトリです。

## Structure

- `challenges/`: 問題ごとの作業フォルダ
- `templates/`: writeup や調査メモのテンプレート
- `tools/`: 使い回す補助スクリプト
- `docs/`: 学習メモ、講習資料、参考情報

## Recommended Flow

1. `challenges/<category>/<challenge-name>/` を作る
2. `templates/challenge-notes.md` をコピーして調査メモを書く
3. exploit や解析スクリプトを同じ問題フォルダに置く
4. 解けたら `templates/writeup.md` をもとに writeup を作る

## Categories

- `web`
- `pwn`
- `crypto`
- `rev`
- `forensics`
- `misc`
