# CTF Workspace

CTF に向けた調査、解法メモ、スクリプト、writeup をまとめるための作業用リポジトリです。

## Structure

- `challenges/`: 問題ごとの作業フォルダ
- `templates/`: writeup や調査メモのテンプレート
- `tools/`: 使い回す補助スクリプト
- `docs/`: 学習メモ、講習資料、参考情報
- `requirements.txt`: CTFでよく使うPython補助ライブラリ

## Recommended Flow

1. `challenges/<category>/<challenge-name>/` を作る
2. `templates/challenge-notes.md` をコピーして調査メモを書く
3. exploit や解析スクリプトを同じ問題フォルダに置く
4. 解けたら `templates/writeup.md` をもとに writeup を作る

SECCON Beginners CTF 2026 に向けた準備は、以下を起点にします。

- `docs/seccon-beginners-2026.md`: 大会概要、本番前チェック、当日運用
- `docs/ctf4b-2025-patterns.md`: 過去問 writeup から抽出した解法パターン
- `tools/prepare_seccon_beginners_2026.ps1`: 2026 用のカテゴリ別作業フォルダを作成

```powershell
powershell -ExecutionPolicy Bypass -File tools\prepare_seccon_beginners_2026.ps1
```

## Categories

- `web`
- `pwn`
- `crypto`
- `rev`
- `forensics`
- `network`
- `programming`
- `misc`

## Setup

Windows 環境では、まず導入候補を確認します。

```powershell
powershell -ExecutionPolicy Bypass -File tools\check_environment.ps1
```

CTF用ツールをまとめて導入する場合は、内容を確認してから以下を実行します。

```powershell
powershell -ExecutionPolicy Bypass -File tools\setup_ctf_windows.ps1
```

## Pre-Contest Checklist

本番前に、以下を確認しておきます。

SECCON Beginners CTF 2026 は、2026/6/13 14:00 JST から 2026/6/14 14:00 JST までの 24 時間開催予定です。参加登録は 2026/6/6 開始予定です。

### 基本情報

- [ ] 参加予定CTFの名前、URL、開始時刻、終了時刻を確認した
- [ ] 競技形式（Jeopardy / Attack & Defense / King of the Hill など）を確認した
- [ ] ルール、禁止事項、スコアリング方式、提出回数制限を確認した
- [ ] チーム名、メンバー、役割分担、連絡手段を確認した
- [ ] タイムゾーンを日本時間に直して、開始・終了時刻を共有した

### アカウントと通信

- [ ] CTFプラットフォームにログインできる
- [ ] チーム参加、招待、登録情報が完了している
- [ ] Discord / Slack / IRC / Mattermost などの連絡先に入れる
- [ ] VPN、OpenVPN設定、接続先、認証情報を確認した
- [ ] 必要なプロキシ、Tor、ブラウザ拡張、証明書を確認した

### 環境

- [ ] `tools\check_environment.ps1` を実行して主要ツールを確認した
- [ ] Python仮想環境を作成し、`requirements.txt` を導入した
- [ ] Git、Python、Node.js、curl、7-Zip、Wireshark/tshark が使える
- [ ] pwn / rev 用に WSL、GDB、Ghidra、Binary Ninja、radare2 などを準備した
- [ ] forensics 用に exiftool、binwalk、Volatility、strings、file などを準備した
- [ ] よく使うエディタ、ターミナル、ブラウザのプロファイルを準備した

### リポジトリ運用

- [ ] `git status` が意図した状態になっている
- [ ] `challenges/<category>/<challenge-name>/` の作成ルールをチームで共有した
- [ ] 新規問題は `tools\new_challenge.py` で作る運用を確認した
- [ ] `notes.md` に観察、仮説、試したコマンド、発見を残す方針を確認した
- [ ] exploit、解析スクリプト、入手ファイル、writeup の置き場所を確認した
- [ ] Flagや認証情報を公開リポジトリへ誤ってpushしない運用を確認した

### 当日運用

- [ ] 開始直後に全カテゴリをざっと見て、解けそうな問題を優先順位付けする
- [ ] 問題ごとに担当者、状況、詰まりポイントを記録する
- [ ] 30〜60分詰まった問題は、一度共有して別視点を入れる
- [ ] Flag提出前に形式、余分な空白、改行、エスケープを確認する
- [ ] 解けた問題は最低限の再現手順を残す
- [ ] スコアボードと残り時間を定期的に確認する

### 終了後

- [ ] 解けた問題のwriteupを整理する
- [ ] 解けなかった問題の公式writeup、他チームwriteupを確認する
- [ ] 使えた手法、足りなかった知識、追加すべきツールを `docs/` に残す
- [ ] 次回に向けた改善タスクを `tasks/current.md` に追加する
