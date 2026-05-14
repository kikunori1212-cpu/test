"""
自己紹介スライド自動生成スクリプト
docs/自己紹介_第三者検証講習用.md の内容を Google Slides に変換する

事前準備:
  1. Google Cloud Console で「Slides API」「Drive API」を有効化
  2. OAuth 2.0 クライアントID（デスクトップアプリ）を作成しダウンロード
  3. ダウンロードしたファイルを src/credentials.json として保存
  4. python src/create_slides.py を実行
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ---- 設定 ----
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

# スライドのテーマカラー（RGB 0.0〜1.0）
COLOR_BG_DARK = {"red": 0.11, "green": 0.13, "blue": 0.18}       # 濃紺
COLOR_ACCENT   = {"red": 0.20, "green": 0.60, "blue": 0.86}       # 水色
COLOR_WHITE    = {"red": 1.0,  "green": 1.0,  "blue": 1.0}
COLOR_YELLOW   = {"red": 1.0,  "green": 0.85, "blue": 0.20}
COLOR_LIGHT_BG = {"red": 0.95, "green": 0.97, "blue": 1.0}        # 薄青白

SLIDE_W = 9144000   # EMU (約25.4cm)
SLIDE_H = 5143500   # EMU (約14.3cm)


# ---- 認証 ----
def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"\n[ERROR] {CREDENTIALS_FILE} が見つかりません。\n"
                    "Google Cloud Console から OAuth クライアントIDをダウンロードして\n"
                    "src/credentials.json として保存してください。\n"
                    "詳細: docs/Google_Slides_セットアップ手順.md"
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


# ---- ヘルパー ----
def emu(pt):
    """ポイント → EMU 変換 (1pt = 12700 EMU)"""
    return int(pt * 12700)

def pt(px):
    """pt をそのまま返す（可読性のため）"""
    return px

def rgb(color):
    """テキスト色用（opaqueColor ラッパーあり）"""
    return {"opaqueColor": {"rgbColor": color}}

def rgb_fill(color):
    """シェイプ塗りつぶし用（rgbColor 直接）"""
    return {"rgbColor": color}

def size(w_emu, h_emu):
    return {
        "width":  {"magnitude": w_emu, "unit": "EMU"},
        "height": {"magnitude": h_emu, "unit": "EMU"},
    }

def translate(x_emu, y_emu):
    return {
        "translateX": x_emu,
        "translateY": y_emu,
        "scaleX": 1, "scaleY": 1,
        "shearX": 0, "shearY": 0,
        "unit": "EMU",
    }


# ---- スライド定義 ----
SLIDES = [
    # Page 1: 表紙
    {
        "title": "cover",
        "elements": [
            # 全面背景
            {
                "type": "shape", "shape": "RECTANGLE",
                "x": 0, "y": 0, "w": SLIDE_W, "h": SLIDE_H,
                "fill": COLOR_BG_DARK,
            },
            # アクセントバー（左）
            {
                "type": "shape", "shape": "RECTANGLE",
                "x": 0, "y": 0, "w": emu(8), "h": SLIDE_H,
                "fill": COLOR_ACCENT,
            },
            # メインタイトル
            {
                "type": "text",
                "text": "はじめまして！",
                "x": emu(80), "y": emu(60), "w": emu(660), "h": emu(80),
                "font_size": pt(40), "bold": True,
                "color": COLOR_WHITE,
                "align": "CENTER",
            },
            # 名前
            {
                "type": "text",
                "text": "菊一 則久（きくいち のりひさ）",
                "x": emu(80), "y": emu(155), "w": emu(660), "h": emu(50),
                "font_size": pt(28), "bold": True,
                "color": COLOR_ACCENT,
                "align": "CENTER",
            },
            # 属性
            {
                "type": "text",
                "text": "45歳 ／ QAエンジニア",
                "x": emu(80), "y": emu(215), "w": emu(660), "h": emu(40),
                "font_size": pt(20), "bold": False,
                "color": COLOR_WHITE,
                "align": "CENTER",
            },
            # キャッチコピー枠
            {
                "type": "shape", "shape": "ROUND_RECTANGLE",
                "x": emu(140), "y": emu(270), "w": emu(540), "h": emu(55),
                "fill": COLOR_ACCENT,
            },
            {
                "type": "text",
                "text": '"バグを愛して20年、まだまだ現役です"',
                "x": emu(140), "y": emu(275), "w": emu(540), "h": emu(45),
                "font_size": pt(16), "bold": False,
                "color": COLOR_WHITE,
                "align": "CENTER",
            },
            # サブタイトル
            {
                "type": "text",
                "text": "第三者検証 若手向け講習",
                "x": emu(80), "y": emu(345), "w": emu(660), "h": emu(30),
                "font_size": pt(14), "bold": False,
                "color": {"red": 0.7, "green": 0.7, "blue": 0.7},
                "align": "CENTER",
            },
        ],
    },
    # Page 2: プロフィール
    {
        "title": "profile",
        "elements": [
            # 背景
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": SLIDE_H, "fill": COLOR_LIGHT_BG},
            # ヘッダーバー
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": emu(55), "fill": COLOR_BG_DARK},
            # タイトル
            {"type": "text", "text": "私って何者？── プロフィール",
             "x": emu(30), "y": emu(8), "w": emu(700), "h": emu(40),
             "font_size": pt(22), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            # 左カラム：基本情報
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(30), "y": emu(70), "w": emu(340), "h": emu(230),
             "fill": COLOR_WHITE},
            {"type": "text",
             "text": "📋 基本スペック\n\n出身：茨城県（つくばみらい市）\n年齢：45歳（昭和55年生まれ）\n最寄：みらい平駅\n趣味：車 🚗（WRX STI）\n資格：トレース技能検定3級\n    小型特殊建設機械免許",
             "x": emu(40), "y": emu(78), "w": emu(320), "h": emu(215),
             "font_size": pt(13), "bold": False, "color": COLOR_BG_DARK, "align": "LEFT"},
            # 右カラム：経歴ギャップ
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(390), "y": emu(70), "w": emu(340), "h": emu(230),
             "fill": COLOR_WHITE},
            {"type": "text",
             "text": "⚡ ちょっと待って、経歴がおかしい人です\n\n茨城県立水戸農業高校\n【土木科】卒業\n        ↓  なぜか…\n東京コミュニケーションアート専門学校\n【ゲームクリエーター科\n  プログラミング専攻】卒業\n\n農業・土木 → ゲームクリエーター 笑",
             "x": emu(400), "y": emu(78), "w": emu(320), "h": emu(215),
             "font_size": pt(12), "bold": False, "color": COLOR_BG_DARK, "align": "LEFT"},
        ],
    },
    # Page 3: キャリア年表
    {
        "title": "career",
        "elements": [
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": SLIDE_H, "fill": COLOR_BG_DARK},
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": emu(55), "fill": COLOR_ACCENT},
            {"type": "text", "text": 'キャリア年表 ── "ゲーム少年がQAの道へ"',
             "x": emu(30), "y": emu(8), "w": emu(700), "h": emu(40),
             "font_size": pt(22), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            # タイムライン縦線
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(115), "y": emu(65), "w": emu(4), "h": emu(310),
             "fill": COLOR_ACCENT},
            # 各イベント
            *[
                item
                for year, title, desc, y_pos in [
                    ("2002", "ポールトゥウィン入社",
                     "PS/PS2/Xbox のバグ取りでスタート\n「ゲームしながら仕事できる！」← 甘かった", 70),
                    ("2005", "株式会社 SEGA 入社",
                     "ゲームの企画・仕様書作成へ\n「SEGA SPLASH! GOLF」など担当", 130),
                    ("2009", "第三者検証の世界へ本格参入",
                     "携帯・スマホ・Web・AIアプリまで\nリーダー → マネージャーへ", 190),
                    ("2012", "会社立ち上げに参画",
                     "30名 → 200名規模へ拡大\n最高検証責任者に就任", 240),
                    ("2022\n↓\n2025", "東急 URBAN HACKS 入社",
                     "QA 1人目として参画\nチームを 1名 → 20名 に拡大！", 295),
                ]
                for item in [
                    {"type": "shape", "shape": "ELLIPSE",
                     "x": emu(103), "y": emu(y_pos+4), "w": emu(28), "h": emu(28),
                     "fill": COLOR_YELLOW},
                    {"type": "text", "text": year,
                     "x": emu(10), "y": emu(y_pos), "w": emu(88), "h": emu(50),
                     "font_size": pt(11), "bold": True, "color": COLOR_YELLOW, "align": "RIGHT"},
                    {"type": "text", "text": title,
                     "x": emu(145), "y": emu(y_pos), "w": emu(580), "h": emu(25),
                     "font_size": pt(14), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
                    {"type": "text", "text": desc,
                     "x": emu(145), "y": emu(y_pos+24), "w": emu(580), "h": emu(35),
                     "font_size": pt(11), "bold": False,
                     "color": {"red": 0.8, "green": 0.8, "blue": 0.8}, "align": "LEFT"},
                ]
            ],
        ],
    },
    # Page 4: 今やっていること
    {
        "title": "current",
        "elements": [
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": SLIDE_H, "fill": COLOR_LIGHT_BG},
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": emu(55), "fill": COLOR_BG_DARK},
            {"type": "text", "text": '今やっていること ── "0から20名のチームを作った話"',
             "x": emu(30), "y": emu(8), "w": emu(700), "h": emu(40),
             "font_size": pt(20), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            # BEFORE カード
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(30), "y": emu(70), "w": emu(310), "h": emu(240),
             "fill": {"red": 0.95, "green": 0.85, "blue": 0.85}},
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(30), "y": emu(70), "w": emu(310), "h": emu(35),
             "fill": {"red": 0.8, "green": 0.2, "blue": 0.2}},
            {"type": "text", "text": "📌 スタート時の状況",
             "x": emu(35), "y": emu(74), "w": emu(300), "h": emu(28),
             "font_size": pt(14), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            {"type": "text",
             "text": "・QA担当：自分1人\n・品質基準：何もない\n・テスト自動化：何もない",
             "x": emu(40), "y": emu(112), "w": emu(290), "h": emu(190),
             "font_size": pt(14), "bold": False, "color": COLOR_BG_DARK, "align": "LEFT"},
            # 矢印
            {"type": "text", "text": "→",
             "x": emu(348), "y": emu(165), "w": emu(50), "h": emu(50),
             "font_size": pt(30), "bold": True, "color": COLOR_ACCENT, "align": "CENTER"},
            # AFTER カード
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(408), "y": emu(70), "w": emu(320), "h": emu(240),
             "fill": {"red": 0.85, "green": 0.95, "blue": 0.88}},
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(408), "y": emu(70), "w": emu(320), "h": emu(35),
             "fill": {"red": 0.1, "green": 0.6, "blue": 0.3}},
            {"type": "text", "text": "✅ 今（2025年4月時点）",
             "x": emu(413), "y": emu(74), "w": emu(310), "h": emu(28),
             "font_size": pt(14), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            {"type": "text",
             "text": "・チーム：20名\n  （内製9名 + 外部11名）\n・自動化：MagicPod + Appium\n  ハイブリッド設計\n・品質基準・QAプロセス\n  ゼロから策定",
             "x": emu(418), "y": emu(112), "w": emu(300), "h": emu(190),
             "font_size": pt(13), "bold": False, "color": COLOR_BG_DARK, "align": "LEFT"},
            # その他
            {"type": "text",
             "text": "🎤 JaSST東京（2024）登壇  ／  🔐 社内脆弱性診断担当  ／  🛡️ 防衛省セキュリティコンテスト出場",
             "x": emu(30), "y": emu(325), "w": emu(700), "h": emu(30),
             "font_size": pt(12), "bold": False, "color": COLOR_BG_DARK, "align": "CENTER"},
        ],
    },
    # Page 5: 伝えたいこと
    {
        "title": "message",
        "elements": [
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": SLIDE_H, "fill": COLOR_BG_DARK},
            {"type": "shape", "shape": "RECTANGLE",
             "x": 0, "y": 0, "w": SLIDE_W, "h": emu(55), "fill": COLOR_ACCENT},
            {"type": "text", "text": "今日、皆さんに伝えたいこと",
             "x": emu(30), "y": emu(8), "w": emu(700), "h": emu(40),
             "font_size": pt(24), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
            # QA is fun
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(30), "y": emu(65), "w": emu(700), "h": emu(45),
             "fill": {"red": 0.15, "green": 0.18, "blue": 0.25}},
            {"type": "text", "text": "🎯  QAって、実はめちゃくちゃ面白い仕事です",
             "x": emu(40), "y": emu(72), "w": emu(680), "h": emu(32),
             "font_size": pt(18), "bold": True, "color": COLOR_YELLOW, "align": "LEFT"},
            # 3つ
            {"type": "text", "text": "若いうちに身につけてほしいこと 3つ",
             "x": emu(30), "y": emu(120), "w": emu(700), "h": emu(28),
             "font_size": pt(15), "bold": True, "color": COLOR_ACCENT, "align": "LEFT"},
            *[
                item
                for i, (num, title, desc) in enumerate([
                    ("1", "「なぜ？」を問い続ける習慣",
                     "バグは現象ではなく、原因を探ることが大事"),
                    ("2", "記録する力",
                     "再現手順・環境・状況を正確に言語化できると一気に信頼される"),
                    ("3", "報告・連絡・相談を怖がらない",
                     "問題を早く共有した人が、チームのヒーローになれる"),
                ])
                for item in [
                    {"type": "shape", "shape": "ELLIPSE",
                     "x": emu(30), "y": emu(155 + i*65), "w": emu(35), "h": emu(35),
                     "fill": COLOR_ACCENT},
                    {"type": "text", "text": num,
                     "x": emu(30), "y": emu(157 + i*65), "w": emu(35), "h": emu(32),
                     "font_size": pt(18), "bold": True, "color": COLOR_WHITE, "align": "CENTER"},
                    {"type": "text", "text": title,
                     "x": emu(80), "y": emu(155 + i*65), "w": emu(650), "h": emu(28),
                     "font_size": pt(15), "bold": True, "color": COLOR_WHITE, "align": "LEFT"},
                    {"type": "text", "text": desc,
                     "x": emu(80), "y": emu(180 + i*65), "w": emu(650), "h": emu(25),
                     "font_size": pt(12), "bold": False,
                     "color": {"red": 0.75, "green": 0.75, "blue": 0.75}, "align": "LEFT"},
                ]
            ],
            # 締め
            {"type": "shape", "shape": "RECTANGLE",
             "x": emu(30), "y": emu(355), "w": emu(700), "h": emu(55),
             "fill": {"red": 0.15, "green": 0.18, "blue": 0.25}},
            {"type": "text",
             "text": "きれいなキャリアじゃなくていい。やってみて、面白いと思ったことを深掘りすれば、気づいたら「専門家」になっています。",
             "x": emu(40), "y": emu(360), "w": emu(680), "h": emu(45),
             "font_size": pt(13), "bold": False, "color": COLOR_WHITE, "align": "CENTER"},
        ],
    },
]


# ---- リクエスト構築 ----
def build_requests(slide_id, elements):
    requests = []
    for el in elements:
        el_id = f"{slide_id}_{len(requests):03d}"

        if el["type"] == "shape":
            requests.append({
                "createShape": {
                    "objectId": el_id,
                    "shapeType": el["shape"],
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": size(el["w"], el["h"]),
                        "transform": translate(el["x"], el["y"]),
                    },
                }
            })
            requests.append({
                "updateShapeProperties": {
                    "objectId": el_id,
                    "shapeProperties": {
                        "shapeBackgroundFill": {
                            "solidFill": {"color": rgb_fill(el["fill"])}
                        }
                    },
                    "fields": "shapeBackgroundFill",
                }
            })

        elif el["type"] == "text":
            requests.append({
                "createShape": {
                    "objectId": el_id,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": slide_id,
                        "size": size(el["w"], el["h"]),
                        "transform": translate(el["x"], el["y"]),
                    },
                }
            })
            requests.append({
                "insertText": {
                    "objectId": el_id,
                    "text": el["text"],
                }
            })
            style = {
                "foregroundColor": rgb(el["color"]),
                "fontSize": {"magnitude": el["font_size"], "unit": "PT"},
                "bold": el.get("bold", False),
                "fontFamily": "Noto Sans JP",
            }
            requests.append({
                "updateTextStyle": {
                    "objectId": el_id,
                    "style": style,
                    "fields": "foregroundColor,fontSize,bold,fontFamily",
                }
            })
            _align_map = {"LEFT": "START", "RIGHT": "END", "CENTER": "CENTER", "START": "START"}
            requests.append({
                "updateParagraphStyle": {
                    "objectId": el_id,
                    "style": {
                        "alignment": _align_map.get(el.get("align", "START"), "START"),
                        "spaceAbove": {"magnitude": 0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 0, "unit": "PT"},
                    },
                    "fields": "alignment,spaceAbove,spaceBelow",
                }
            })

    return requests


# ---- メイン ----
def main():
    print("Google API 認証中...")
    creds = get_credentials()
    slides_service = build("slides", "v1", credentials=creds)
    drive_service  = build("drive",  "v3", credentials=creds)

    print("プレゼンテーションを作成中...")
    presentation = slides_service.presentations().create(body={
        "title": "自己紹介スライド｜第三者検証 若手向け講習"
    }).execute()
    prs_id = presentation["presentationId"]

    # デフォルトスライドを削除
    default_slide_id = presentation["slides"][0]["objectId"]
    slides_service.presentations().batchUpdate(
        presentationId=prs_id,
        body={"requests": [{"deleteObject": {"objectId": default_slide_id}}]}
    ).execute()

    # 各スライドを追加
    for i, slide_def in enumerate(SLIDES):
        print(f"  スライド {i+1}/{len(SLIDES)} を作成中: {slide_def['title']}")
        slide_id = f"slide_{i:02d}"

        # スライド追加
        slides_service.presentations().batchUpdate(
            presentationId=prs_id,
            body={"requests": [{
                "createSlide": {
                    "objectId": slide_id,
                    "insertionIndex": i,
                    "slideLayoutReference": {"predefinedLayout": "BLANK"},
                }
            }]}
        ).execute()

        # 要素を追加
        reqs = build_requests(slide_id, slide_def["elements"])
        if reqs:
            slides_service.presentations().batchUpdate(
                presentationId=prs_id,
                body={"requests": reqs}
            ).execute()

    # Drive でリンクを取得
    drive_service.permissions().create(
        fileId=prs_id,
        body={"type": "anyone", "role": "reader"}
    ).execute()

    url = f"https://docs.google.com/presentation/d/{prs_id}/edit"
    print("\n[完成]")
    print(f"   URL: {url}")
    return url


if __name__ == "__main__":
    main()
