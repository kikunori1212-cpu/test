# -*- coding: utf-8 -*-
"""
自己紹介スライド v2 - リデザイン版
スライド生成 + Pollinations AI 画像挿入を一括実行

使い方:
  python src/create_slides_v2.py
"""

import os
import sys
import time
import tempfile
import requests as http_requests
from urllib.parse import quote
from pathlib import Path
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv(Path(__file__).parent.parent / ".env")

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
TOKEN_FILE       = Path(__file__).parent / "token.json"

SLIDE_W = 9144000
SLIDE_H = 5143500

# ---- カラーパレット ----
C_NAVY   = {"red": 0.118, "green": 0.161, "blue": 0.235}   # #1E293B
C_BLUE   = {"red": 0.231, "green": 0.510, "blue": 0.965}   # #3B82F6
C_AMBER  = {"red": 0.961, "green": 0.620, "blue": 0.043}   # #F59E0B
C_LIGHT  = {"red": 0.973, "green": 0.980, "blue": 0.988}   # #F8FAFC
C_WHITE  = {"red": 1.0,   "green": 1.0,   "blue": 1.0}
C_GRAY   = {"red": 0.557, "green": 0.600, "blue": 0.647}   # #8E99A5
C_LGRAY  = {"red": 0.878, "green": 0.902, "blue": 0.925}   # #E0E6EC
C_GREEN  = {"red": 0.133, "green": 0.694, "blue": 0.298}   # #22B14C
C_RED    = {"red": 0.859, "green": 0.196, "blue": 0.212}   # #DB3236

def emu(pt): return int(pt * 12700)
def rgb(c):  return {"opaqueColor": {"rgbColor": c}}
def fill(c): return {"rgbColor": c}

def mk_size(w, h):
    return {"width": {"magnitude": w, "unit": "EMU"},
            "height": {"magnitude": h, "unit": "EMU"}}

def mk_tf(x, y):
    return {"scaleX": 1, "scaleY": 1, "shearX": 0, "shearY": 0,
            "translateX": x, "translateY": y, "unit": "EMU"}

def shape_req(obj_id, slide_id, shape, x, y, w, h, color):
    return [
        {"createShape": {
            "objectId": obj_id, "shapeType": shape,
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": mk_size(w, h),
                "transform": mk_tf(x, y),
            }
        }},
        {"updateShapeProperties": {
            "objectId": obj_id,
            "shapeProperties": {
                "shapeBackgroundFill": {"solidFill": {"color": fill(color)}},
                "outline": {"outlineFill": {"solidFill": {"color": fill(color)}}}
            },
            "fields": "shapeBackgroundFill,outline",
        }},
    ]

def text_req(obj_id, slide_id, text, x, y, w, h,
             size_pt, bold=False, color=None, align="START", italic=False):
    if color is None:
        color = C_NAVY
    ALIGN_MAP = {"LEFT": "START", "CENTER": "CENTER", "RIGHT": "END", "START": "START"}
    reqs = [
        {"createShape": {
            "objectId": obj_id, "shapeType": "TEXT_BOX",
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": mk_size(w, h),
                "transform": mk_tf(x, y),
            }
        }},
        {"insertText": {"objectId": obj_id, "text": text}},
        {"updateTextStyle": {
            "objectId": obj_id,
            "style": {
                "foregroundColor": rgb(color),
                "fontSize": {"magnitude": size_pt, "unit": "PT"},
                "bold": bold,
                "italic": italic,
                "fontFamily": "Noto Sans JP",
            },
            "fields": "foregroundColor,fontSize,bold,italic,fontFamily",
        }},
        {"updateParagraphStyle": {
            "objectId": obj_id,
            "style": {
                "alignment": ALIGN_MAP.get(align, "START"),
                "spaceAbove": {"magnitude": 0, "unit": "PT"},
                "spaceBelow": {"magnitude": 2, "unit": "PT"},
            },
            "fields": "alignment,spaceAbove,spaceBelow",
        }},
    ]
    return reqs


# ===========================================================
# スライド定義
# ===========================================================

def build_slide_cover(slide_id):
    """Page 1: 左ネイビー / 右ホワイト 分割レイアウト"""
    reqs = []
    n = [0]
    def nid(tag): n[0] += 1; return f"{slide_id}_{tag}_{n[0]:03d}"

    # 左パネル（ネイビー）
    reqs += shape_req(nid("bg_l"), slide_id, "RECTANGLE",
                      0, 0, emu(480), SLIDE_H, C_NAVY)
    # 右パネル（薄グレー）
    reqs += shape_req(nid("bg_r"), slide_id, "RECTANGLE",
                      emu(480), 0, emu(280), SLIDE_H, C_LIGHT)

    # アクセントライン（縦）
    reqs += shape_req(nid("line"), slide_id, "RECTANGLE",
                      emu(477), 0, emu(6), SLIDE_H, C_AMBER)

    # ラベル
    reqs += text_req(nid("label"), slide_id, "第三者検証 若手向け講習",
                     emu(30), emu(50), emu(430), emu(28),
                     12, bold=False, color=C_BLUE, align="LEFT")

    # 名前
    reqs += text_req(nid("name"), slide_id, "菊一 則久",
                     emu(30), emu(100), emu(430), emu(75),
                     42, bold=True, color=C_WHITE, align="LEFT")

    # ふりがな
    reqs += text_req(nid("kana"), slide_id, "きくいち のりひさ",
                     emu(30), emu(178), emu(430), emu(28),
                     14, bold=False, color=C_GRAY, align="LEFT")

    # 区切り線（アンバー）
    reqs += shape_req(nid("sep"), slide_id, "RECTANGLE",
                      emu(30), emu(215), emu(60), emu(4), C_AMBER)

    # 属性
    reqs += text_req(nid("attr"), slide_id, "45歳  ／  QAエンジニア",
                     emu(30), emu(232), emu(430), emu(30),
                     16, bold=False, color=C_LGRAY, align="LEFT")

    # キャッチコピー
    reqs += shape_req(nid("quote_bg"), slide_id, "RECTANGLE",
                      emu(30), emu(280), emu(420), emu(60), C_BLUE)
    reqs += text_req(nid("quote"), slide_id,
                     '"バグを愛して20年、まだまだ現役です"',
                     emu(38), emu(290), emu(404), emu(42),
                     14, bold=False, color=C_WHITE, align="LEFT", italic=True)

    # 所属
    reqs += text_req(nid("org"), slide_id,
                     "東急株式会社 URBAN HACKS",
                     emu(30), emu(360), emu(430), emu(28),
                     12, bold=False, color=C_GRAY, align="LEFT")

    # 右パネル：画像プレースホルダーラベル
    reqs += text_req(nid("img_label"), slide_id, "[ illustration ]",
                     emu(490), emu(180), emu(255), emu(30),
                     12, bold=False, color=C_LGRAY, align="CENTER")

    return reqs


def build_slide_profile(slide_id):
    """Page 2: プロフィール - カード2枚レイアウト"""
    reqs = []
    n = [0]
    def nid(tag): n[0] += 1; return f"{slide_id}_{tag}_{n[0]:03d}"

    # 背景
    reqs += shape_req(nid("bg"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H, C_LIGHT)

    # ヘッダーバー
    reqs += shape_req(nid("hdr"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, emu(62), C_NAVY)
    reqs += shape_req(nid("hdr_acc"), slide_id, "RECTANGLE", 0, emu(59), SLIDE_W, emu(4), C_AMBER)

    # タイトル
    reqs += text_req(nid("title"), slide_id, "私って何者？",
                     emu(28), emu(10), emu(400), emu(45),
                     26, bold=True, color=C_WHITE, align="LEFT")

    # 左カード（白）
    reqs += shape_req(nid("card_l"), slide_id, "RECTANGLE",
                      emu(28), emu(78), emu(340), emu(260), C_WHITE)
    # 左カード上部ライン
    reqs += shape_req(nid("card_l_top"), slide_id, "RECTANGLE",
                      emu(28), emu(78), emu(340), emu(5), C_BLUE)

    reqs += text_req(nid("card_l_ttl"), slide_id, "基本スペック",
                     emu(40), emu(90), emu(316), emu(28),
                     14, bold=True, color=C_NAVY, align="LEFT")

    profile_text = (
        "出身　茨城県（つくばみらい市）\n"
        "年齢　45歳（昭和55年生まれ）\n"
        "最寄　みらい平駅（TX）\n"
        "趣味　車 — WRX STI 乗ってます\n"
        "資格　トレース技能検定3級\n"
        "　　　小型特殊建設機械免許"
    )
    reqs += text_req(nid("card_l_body"), slide_id, profile_text,
                     emu(40), emu(124), emu(316), emu(205),
                     13, bold=False, color=C_NAVY, align="LEFT")

    # 右カード（白）
    reqs += shape_req(nid("card_r"), slide_id, "RECTANGLE",
                      emu(388), emu(78), emu(360), emu(260), C_WHITE)
    reqs += shape_req(nid("card_r_top"), slide_id, "RECTANGLE",
                      emu(388), emu(78), emu(360), emu(5), C_AMBER)

    reqs += text_req(nid("card_r_ttl"), slide_id, "ちょっと変わった経歴です",
                     emu(400), emu(90), emu(336), emu(28),
                     14, bold=True, color=C_NAVY, align="LEFT")

    career_text = (
        "茨城県立水戸農業高校\n"
        "【土木科】卒業\n"
        "\n"
        "　　　　↓  なぜか…\n"
        "\n"
        "東京コミュニケーションアート\n"
        "専門学校【ゲームクリエーター科\n"
        "プログラミング専攻】卒業"
    )
    reqs += text_req(nid("card_r_body"), slide_id, career_text,
                     emu(400), emu(124), emu(336), emu(205),
                     12, bold=False, color=C_NAVY, align="LEFT")

    # ボトムメモ
    reqs += text_req(nid("note"), slide_id,
                     "農業・土木  →  ゲームクリエーター  →  QAエンジニア",
                     emu(28), emu(355), emu(720), emu(28),
                     12, bold=False, color=C_GRAY, align="CENTER")

    return reqs


def build_slide_career(slide_id):
    """Page 3: キャリア年表 - タイムライン"""
    reqs = []
    n = [0]
    def nid(tag): n[0] += 1; return f"{slide_id}_{tag}_{n[0]:03d}"

    reqs += shape_req(nid("bg"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H, C_NAVY)
    reqs += shape_req(nid("hdr"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, emu(62), C_BLUE)
    reqs += shape_req(nid("hdr_acc"), slide_id, "RECTANGLE", 0, emu(59), SLIDE_W, emu(4), C_AMBER)

    reqs += text_req(nid("title"), slide_id, "キャリア年表",
                     emu(28), emu(10), emu(500), emu(45),
                     26, bold=True, color=C_WHITE, align="LEFT")

    # タイムライン縦線
    reqs += shape_req(nid("tl_line"), slide_id, "RECTANGLE",
                      emu(148), emu(72), emu(4), emu(315), C_BLUE)

    entries = [
        ("2002", "ポールトゥウィン入社",     "PS/PS2/Xbox バグ取りでキャリアスタート"),
        ("2005", "株式会社 SEGA 入社",       "ゲーム企画・仕様書作成を担当"),
        ("2009", "第三者検証 本格参入",       "携帯・スマホ・Web・AIアプリ → リーダーへ"),
        ("2012", "会社立ち上げに参画",        "30名 → 200名規模。最高検証責任者に就任"),
        ("2022〜", "東急 URBAN HACKS 入社",  "QA 1人目 → チームを 20名 に拡大！"),
    ]

    for i, (year, title, desc) in enumerate(entries):
        y = emu(76 + i * 62)
        # ドット
        reqs += shape_req(nid(f"dot{i}"), slide_id, "ELLIPSE",
                          emu(136), y + emu(4), emu(28), emu(28), C_AMBER)
        # 年
        reqs += text_req(nid(f"year{i}"), slide_id, year,
                         emu(10), y, emu(122), emu(36),
                         12, bold=True, color=C_AMBER, align="RIGHT")
        # タイトル
        reqs += text_req(nid(f"ttl{i}"), slide_id, title,
                         emu(168), y, emu(560), emu(26),
                         15, bold=True, color=C_WHITE, align="LEFT")
        # 説明
        reqs += text_req(nid(f"desc{i}"), slide_id, desc,
                         emu(168), y + emu(26), emu(560), emu(24),
                         11, bold=False, color=C_GRAY, align="LEFT")

    reqs += text_req(nid("foot"), slide_id,
                     "気づいたら20年以上、バグを追いかけていました。",
                     emu(28), emu(390), emu(700), emu(28),
                     12, bold=False, color=C_BLUE, align="CENTER", italic=True)

    return reqs


def build_slide_current(slide_id):
    """Page 4: 今やっていること - Before/After"""
    reqs = []
    n = [0]
    def nid(tag): n[0] += 1; return f"{slide_id}_{tag}_{n[0]:03d}"

    reqs += shape_req(nid("bg"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H, C_LIGHT)
    reqs += shape_req(nid("hdr"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, emu(62), C_NAVY)
    reqs += shape_req(nid("hdr_acc"), slide_id, "RECTANGLE", 0, emu(59), SLIDE_W, emu(4), C_AMBER)

    reqs += text_req(nid("title"), slide_id, "今やっていること",
                     emu(28), emu(10), emu(500), emu(45),
                     26, bold=True, color=C_WHITE, align="LEFT")

    reqs += text_req(nid("sub"), slide_id,
                     "東急株式会社 URBAN HACKS — QA 1人目として参画",
                     emu(28), emu(70), emu(700), emu(24),
                     13, bold=False, color=C_GRAY, align="LEFT")

    # BEFORE カード
    before_bg = {"red": 0.996, "green": 0.937, "blue": 0.937}
    reqs += shape_req(nid("b_card"), slide_id, "RECTANGLE",
                      emu(28), emu(102), emu(300), emu(230), before_bg)
    reqs += shape_req(nid("b_top"), slide_id, "RECTANGLE",
                      emu(28), emu(102), emu(300), emu(6), C_RED)
    reqs += text_req(nid("b_ttl"), slide_id, "BEFORE  2022年",
                     emu(40), emu(115), emu(276), emu(28),
                     13, bold=True, color=C_RED, align="LEFT")
    reqs += text_req(nid("b_body"), slide_id,
                     "QA担当：自分 1人\n品質基準：なし\nテスト自動化：なし\nドキュメント：なし",
                     emu(40), emu(148), emu(276), emu(178),
                     13, bold=False, color=C_NAVY, align="LEFT")

    # 矢印
    reqs += text_req(nid("arrow"), slide_id, "→",
                     emu(338), emu(188), emu(72), emu(50),
                     32, bold=True, color=C_AMBER, align="CENTER")

    # AFTER カード
    after_bg = {"red": 0.914, "green": 0.980, "blue": 0.929}
    reqs += shape_req(nid("a_card"), slide_id, "RECTANGLE",
                      emu(420), emu(102), emu(330), emu(230), after_bg)
    reqs += shape_req(nid("a_top"), slide_id, "RECTANGLE",
                      emu(420), emu(102), emu(330), emu(6), C_GREEN)
    reqs += text_req(nid("a_ttl"), slide_id, "AFTER  2025年",
                     emu(432), emu(115), emu(306), emu(28),
                     13, bold=True, color=C_GREEN, align="LEFT")
    reqs += text_req(nid("a_body"), slide_id,
                     "チーム：20名（内製9名＋外部11名）\n自動化：MagicPod＋Appium\nQAプロセス：ゼロから策定\n品質基準：全社展開済み",
                     emu(432), emu(148), emu(306), emu(178),
                     13, bold=False, color=C_NAVY, align="LEFT")

    # ボトム実績
    reqs += shape_req(nid("achv_bg"), slide_id, "RECTANGLE",
                      emu(28), emu(345), emu(722), emu(42), C_NAVY)
    reqs += text_req(nid("achv"), slide_id,
                     "JaSST東京 2024 登壇  ／  社内脆弱性診断担当  ／  防衛省セキュリティコンテスト出場",
                     emu(36), emu(353), emu(706), emu(28),
                     12, bold=False, color=C_AMBER, align="CENTER")

    return reqs


def build_slide_message(slide_id):
    """Page 5: 伝えたいこと - メッセージスライド"""
    reqs = []
    n = [0]
    def nid(tag): n[0] += 1; return f"{slide_id}_{tag}_{n[0]:03d}"

    reqs += shape_req(nid("bg"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, SLIDE_H, C_LIGHT)
    reqs += shape_req(nid("hdr"), slide_id, "RECTANGLE", 0, 0, SLIDE_W, emu(62), C_NAVY)
    reqs += shape_req(nid("hdr_acc"), slide_id, "RECTANGLE", 0, emu(59), SLIDE_W, emu(4), C_AMBER)

    reqs += text_req(nid("title"), slide_id, "今日、皆さんに伝えたいこと",
                     emu(28), emu(10), emu(700), emu(45),
                     26, bold=True, color=C_WHITE, align="LEFT")

    # サブタイトル
    reqs += shape_req(nid("sub_bg"), slide_id, "RECTANGLE",
                      emu(28), emu(72), emu(722), emu(38), C_BLUE)
    reqs += text_req(nid("sub"), slide_id,
                     "QA って、実はめちゃくちゃ面白い仕事です",
                     emu(36), emu(79), emu(706), emu(26),
                     16, bold=True, color=C_WHITE, align="LEFT")

    # 3つのポイント
    points = [
        ("01", "「なぜ？」を問い続ける習慣",
         "バグは現象ではなく、原因を探ることが大事"),
        ("02", "記録する力",
         "再現手順・環境・状況を正確に言語化できると一気に信頼される"),
        ("03", "報告・連絡・相談を怖がらない",
         "問題を早く共有した人が、チームのヒーローになれる"),
    ]
    for i, (num, ttl, desc) in enumerate(points):
        y = emu(122 + i * 70)
        reqs += shape_req(nid(f"num_bg{i}"), slide_id, "RECTANGLE",
                          emu(28), y, emu(52), emu(52), C_AMBER)
        reqs += text_req(nid(f"num{i}"), slide_id, num,
                         emu(28), y + emu(8), emu(52), emu(36),
                         16, bold=True, color=C_NAVY, align="CENTER")
        reqs += text_req(nid(f"ttl{i}"), slide_id, ttl,
                         emu(92), y + emu(4), emu(658), emu(26),
                         15, bold=True, color=C_NAVY, align="LEFT")
        reqs += text_req(nid(f"desc{i}"), slide_id, desc,
                         emu(92), y + emu(28), emu(658), emu(22),
                         12, bold=False, color=C_GRAY, align="LEFT")

    # 締めの言葉
    reqs += shape_req(nid("close_bg"), slide_id, "RECTANGLE",
                      emu(28), emu(338), emu(722), emu(52), C_NAVY)
    reqs += text_req(nid("close"), slide_id,
                     "きれいなキャリアじゃなくていい。深掘りし続ければ、気づいたら専門家になっています。",
                     emu(36), emu(348), emu(706), emu(34),
                     13, bold=False, color=C_WHITE, align="CENTER", italic=True)

    return reqs


# ===========================================================
# Google 認証
# ===========================================================
def get_credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


# ===========================================================
# Pollinations AI 画像生成
# ===========================================================
IMAGE_PROMPTS = [
    {
        "slide_index": 0,
        "prompt": (
            "Professional flat illustration of a friendly Japanese male QA engineer in his 40s, "
            "sitting at a modern desk with multiple monitors showing code and test dashboards. "
            "Clean, minimal style, white and light blue background. No text."
        ),
        "x_ratio": 0.535, "y_ratio": 0.04, "w_ratio": 0.455, "h_ratio": 0.92,
    },
    {
        "slide_index": 1,
        "prompt": (
            "Flat illustration showing career transition: left side rice fields and tractor "
            "(agriculture school), center a glowing arrow, right side colorful game controller "
            "and monitors (game school). Clean white background, minimal design. No text."
        ),
        "x_ratio": 0.52, "y_ratio": 0.20, "w_ratio": 0.46, "h_ratio": 0.56,
    },
    {
        "slide_index": 2,
        "prompt": (
            "Minimal vertical timeline decoration: glowing dots connected by a vertical line, "
            "small icons for game controller, smartphone, laptop, team silhouette along the line. "
            "Dark navy background, cyan and amber glowing accents. Very narrow tall composition. No text."
        ),
        "x_ratio": 0.84, "y_ratio": 0.12, "w_ratio": 0.15, "h_ratio": 0.76,
    },
    {
        "slide_index": 3,
        "prompt": (
            "Simple flat illustration: one small figure alone at a desk on the left, "
            "a large happy team of diverse people collaborating on the right, "
            "connected by a large upward arrow. Clean white background. No text."
        ),
        "x_ratio": 0.53, "y_ratio": 0.12, "w_ratio": 0.45, "h_ratio": 0.55,
    },
    {
        "slide_index": 4,
        "prompt": (
            "Inspiring flat illustration: large magnifying glass discovering a bug symbol, "
            "surrounded by lightbulbs, question marks, a notebook and chat bubbles. "
            "Light gray background, blue and amber accent colors. Clean minimal style. No text."
        ),
        "x_ratio": 0.55, "y_ratio": 0.12, "w_ratio": 0.43, "h_ratio": 0.62,
    },
]

def generate_image(prompt, label):
    print(f"  Pollinations AI 生成中: {label}")
    encoded = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=1024&height=1024&model=flux&nologo=true&seed={abs(hash(label)) % 99999}"
    )
    resp = http_requests.get(url, timeout=120)
    resp.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.write(resp.content)
    tmp.close()
    print(f"    -> 完了 ({len(resp.content)//1024} KB)")
    return tmp.name

def upload_to_drive(drive_service, file_path, filename):
    media = MediaFileUpload(file_path, mimetype="image/png")
    uploaded = drive_service.files().create(
        body={"name": filename, "mimeType": "image/png"},
        media_body=media, fields="id"
    ).execute()
    file_id = uploaded["id"]
    drive_service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"}
    ).execute()
    return f"https://drive.google.com/uc?export=download&id={file_id}", file_id

def insert_image(slides_service, prs_id, slide_id, url, cfg):
    x = int(SLIDE_W * cfg["x_ratio"])
    y = int(SLIDE_H * cfg["y_ratio"])
    w = int(SLIDE_W * cfg["w_ratio"])
    h = int(SLIDE_H * cfg["h_ratio"])
    slides_service.presentations().batchUpdate(
        presentationId=prs_id,
        body={"requests": [{"createImage": {
            "objectId": f"img_{slide_id}",
            "url": url,
            "elementProperties": {
                "pageObjectId": slide_id,
                "size": mk_size(w, h),
                "transform": mk_tf(x, y),
            },
        }}]}
    ).execute()


# ===========================================================
# メイン
# ===========================================================
def main():
    print("Google API 認証中...")
    creds = get_credentials()
    slides_service = build("slides", "v1", credentials=creds)
    drive_service  = build("drive",  "v3", credentials=creds)

    print("プレゼンテーション作成中...")
    prs = slides_service.presentations().create(body={
        "title": "自己紹介スライド v2｜第三者検証 若手向け講習"
    }).execute()
    prs_id = prs["presentationId"]

    # デフォルトスライド削除
    default_id = prs["slides"][0]["objectId"]
    slides_service.presentations().batchUpdate(
        presentationId=prs_id,
        body={"requests": [{"deleteObject": {"objectId": default_id}}]}
    ).execute()

    # スライド定義
    slide_builders = [
        ("cover",   build_slide_cover),
        ("profile", build_slide_profile),
        ("career",  build_slide_career),
        ("current", build_slide_current),
        ("message", build_slide_message),
    ]

    slide_ids = []
    for i, (name, builder) in enumerate(slide_builders):
        print(f"  スライド {i+1}/5 作成: {name}")
        slide_id = f"slide_v2_{i:02d}"
        slide_ids.append(slide_id)

        slides_service.presentations().batchUpdate(
            presentationId=prs_id,
            body={"requests": [{"createSlide": {
                "objectId": slide_id,
                "insertionIndex": i,
                "slideLayoutReference": {"predefinedLayout": "BLANK"},
            }}]}
        ).execute()

        reqs = builder(slide_id)
        if reqs:
            slides_service.presentations().batchUpdate(
                presentationId=prs_id,
                body={"requests": reqs}
            ).execute()

    # 画像生成・挿入
    print("\n画像生成・挿入中...")
    labels = ["Page1:表紙", "Page2:プロフィール", "Page3:キャリア", "Page4:現在", "Page5:メッセージ"]
    tmp_files = []

    for cfg in IMAGE_PROMPTS:
        idx = cfg["slide_index"]
        slide_id = slide_ids[idx]
        label = labels[idx]
        try:
            tmp = generate_image(cfg["prompt"], label)
            tmp_files.append(tmp)
            img_url, _ = upload_to_drive(drive_service, tmp, f"v2_slide_{idx+1:02d}.png")
            time.sleep(2)
            insert_image(slides_service, prs_id, slide_id, img_url, cfg)
            print(f"    -> スライド {idx+1} に挿入完了")
        except Exception as e:
            print(f"    [スキップ] {e}")

    for f in tmp_files:
        try: os.unlink(f)
        except: pass

    url = f"https://docs.google.com/presentation/d/{prs_id}/edit"
    print(f"\n[完了]")
    print(f"  URL: {url}")


if __name__ == "__main__":
    main()
