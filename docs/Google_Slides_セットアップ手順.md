# Google Slides 自動生成 セットアップ手順

## 概要

`src/create_slides.py` を使って、自己紹介スライドを Google Slides に自動生成します。

---

## 事前準備（初回のみ）

### Step 1: Google Cloud Console でAPIを有効化

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 左上のプロジェクト選択 → **「新しいプロジェクト」** を作成（または既存を選択）
3. 左メニュー → **「APIとサービス」→「ライブラリ」**
4. 以下の2つを検索して **「有効にする」** をクリック
   - `Google Slides API`
   - `Google Drive API`

---

### Step 2: OAuth クライアントIDを作成

1. 左メニュー → **「APIとサービス」→「認証情報」**
2. 上部の **「認証情報を作成」→「OAuth クライアントID」** をクリック
3. 初回は「同意画面を設定」が求められる場合あり
   - ユーザーの種類：**「外部」** を選択
   - アプリ名・メールアドレスを入力して保存
4. アプリケーションの種類：**「デスクトップアプリ」** を選択
5. 名前は任意（例：`slides-creator`）
6. **「作成」** をクリック
7. ダウンロードボタン（⬇️）をクリックして JSON をダウンロード

---

### Step 3: credentials.json を配置

ダウンロードした JSON ファイルを以下の場所に保存：

```
testpj/
└── src/
    └── credentials.json   ← ここに置く
```

> ⚠️ `credentials.json` は絶対に Git にコミットしないでください。
> `.gitignore` に `src/credentials.json` と `src/token.json` を追加してください。

---

## 実行方法

```bash
cd c:\Users\Airin\testpj
python src/create_slides.py
```

### 初回実行時

1. ブラウザが自動で開きます
2. Google アカウントでログイン
3. 「このアプリを信頼しますか？」→ **「続行」**
4. 認証完了後、ターミナルに戻ります
5. `src/token.json` が自動生成されます（次回から不要）

### 実行結果

```
Google API 認証中...
プレゼンテーションを作成中...
  スライド 1/5 を作成中: cover
  スライド 2/5 を作成中: profile
  スライド 3/5 を作成中: career
  スライド 4/5 を作成中: current
  スライド 5/5 を作成中: message

✅ 完成！
   URL: https://docs.google.com/presentation/d/XXXXXXXXXX/edit
```

表示された URL をブラウザで開けばスライドが確認できます。

---

## スライド構成

| ページ | 内容 |
|--------|------|
| 1 | 表紙（名前・キャッチコピー） |
| 2 | プロフィール（基本情報・経歴の意外性） |
| 3 | キャリア年表（2002〜2025） |
| 4 | 今やっていること（URBAN HACKS での挑戦） |
| 5 | 伝えたいこと（QAの面白さ・3つのポイント） |

---

## トラブルシューティング

| エラー | 対処 |
|--------|------|
| `credentials.json が見つかりません` | Step 3 を確認 |
| `Access blocked` | 同意画面でテストユーザーに自分のアカウントを追加 |
| `quota exceeded` | しばらく待ってから再実行 |
| フォントが崩れる | Google Slides 上で手動調整（Noto Sans JP 使用） |
