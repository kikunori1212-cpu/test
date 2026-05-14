# -*- coding: utf-8 -*-
"""
Gemini Imagen 3 で画像を生成して Google Slides に挿入するスクリプト

使い方:
  python src/add_images_to_slides.py <PRESENTATION_ID>

  例:
  python src/add_images_to_slides.py 1Jg3HdRCyNgSe_EeNQkQ_4EdYb72dUALZ6yVrPLAjKiQ
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

# ---- 設定 ----
load_dotenv(Path(__file__).parent.parent / ".env")

SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]
CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
TOKEN_FILE       = Path(__file__).parent / "token.json"

SLIDE_W = 9144000
SLIDE_H = 5143500


# ---- 各スライドの画像設定 ----
IMAGE_CONFIGS = [
    {
        "slide_index": 0,
        "prompt": (
            "A friendly Japanese male engineer in his 40s sitting at a clean desk, "
            "surrounded by bug report documents and multiple monitors showing code and test results. "
            "Warm, approachable expression. Flat illustration style, dark navy and cyan color palette. "
            "No text, no letters."
        ),
        "x_ratio": 0.60, "y_ratio": 0.10,
        "w_ratio": 0.38, "h_ratio": 0.78,
        "label": "Page1: 表紙イラスト",
    },
    {
        "slide_index": 1,
        "prompt": (
            "Split illustration: left panel shows a Japanese student in agricultural school "
            "with green rice fields and a tractor; right panel shows the same person "
            "at a game development school with colorful monitors and game controllers. "
            "Arrow connecting the two panels. Flat illustration, soft pastel colors. "
            "No text, no letters."
        ),
        "x_ratio": 0.52, "y_ratio": 0.52,
        "w_ratio": 0.46, "h_ratio": 0.42,
        "label": "Page2: 農業->ゲーム転換イラスト",
    },
    {
        "slide_index": 2,
        "prompt": (
            "A glowing vertical timeline road winding upward through dark space, "
            "with icons representing game controllers, smartphones, web browsers, "
            "and a QA team along the path. Isometric flat design, dark navy background, "
            "cyan and yellow glowing accents. No text, no letters."
        ),
        "x_ratio": 0.00, "y_ratio": 0.08,
        "w_ratio": 0.13, "h_ratio": 0.88,
        "label": "Page3: キャリアタイムライン装飾",
    },
    {
        "slide_index": 3,
        "prompt": (
            "Two-panel illustration: left side shows one lonely engineer at an empty desk "
            "with minimal setup; right side shows a vibrant team of 20 diverse people "
            "collaborating around dashboards and laptops, celebrating success. "
            "Flat design, warm green tones on the right panel. No text, no letters."
        ),
        "x_ratio": 0.28, "y_ratio": 0.76,
        "w_ratio": 0.44, "h_ratio": 0.21,
        "label": "Page4: 1人->20名チーム成長",
    },
    {
        "slide_index": 4,
        "prompt": (
            "An inspiring flat illustration of a large magnifying glass revealing a bug symbol, "
            "surrounded by floating lightbulbs, question marks, a notebook, and speech bubbles. "
            "Symbolizing curiosity, documentation, and teamwork in software quality assurance. "
            "Dark navy background, cyan and yellow accent colors. No text, no letters."
        ),
        "x_ratio": 0.60, "y_ratio": 0.10,
        "w_ratio": 0.38, "h_ratio": 0.55,
        "label": "Page5: QAメッセージイラスト",
    },
]


# ---- Google 認証 ----
def get_google_credentials():
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


# ---- Pollinations AI で画像生成 ----
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
    print(f"    -> 生成完了 ({len(resp.content)//1024} KB)")
    return tmp.name


# ---- Google Drive にアップロード ----
def upload_to_drive(drive_service, file_path, filename):
    print(f"    -> Drive にアップロード中...")
    file_metadata = {"name": filename, "mimeType": "image/png"}
    media = MediaFileUpload(file_path, mimetype="image/png")
    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    file_id = uploaded["id"]

    drive_service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"}
    ).execute()

    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"    -> Drive URL 取得完了")
    return direct_url, file_id


# ---- スライドに画像を挿入 ----
def insert_image_to_slide(slides_service, presentation_id, slide_id, image_url, config):
    x = int(SLIDE_W * config["x_ratio"])
    y = int(SLIDE_H * config["y_ratio"])
    w = int(SLIDE_W * config["w_ratio"])
    h = int(SLIDE_H * config["h_ratio"])

    img_id = f"img_{slide_id}"
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={"requests": [{
            "createImage": {
                "objectId": img_id,
                "url": image_url,
                "elementProperties": {
                    "pageObjectId": slide_id,
                    "size": {
                        "width":  {"magnitude": w, "unit": "EMU"},
                        "height": {"magnitude": h, "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1, "scaleY": 1,
                        "shearX": 0, "shearY": 0,
                        "translateX": x,
                        "translateY": y,
                        "unit": "EMU",
                    },
                },
            }
        }]}
    ).execute()
    print(f"    -> スライドに挿入完了")


# ---- メイン ----
def main():
    if len(sys.argv) < 2:
        print("使い方: python src/add_images_to_slides.py <PRESENTATION_ID>")
        sys.exit(1)

    presentation_id = sys.argv[1]

    print("Google API 認証中...")
    creds = get_google_credentials()
    slides_service = build("slides", "v1", credentials=creds)
    drive_service  = build("drive",  "v3", credentials=creds)

    print("スライド情報を取得中...")
    presentation = slides_service.presentations().get(
        presentationId=presentation_id
    ).execute()
    slides = presentation["slides"]
    print(f"  {len(slides)} 枚のスライドを確認")

    uploaded_file_ids = []
    tmp_files = []

    for config in IMAGE_CONFIGS:
        idx = config["slide_index"]
        if idx >= len(slides):
            print(f"  スキップ: スライド {idx+1} が存在しません")
            continue

        slide_id = slides[idx]["objectId"]
        print(f"\n[スライド {idx+1}] {config['label']}")

        try:
            tmp_path = generate_image(config["prompt"], config["label"])
            tmp_files.append(tmp_path)

            filename = f"slide_{idx+1:02d}_image.png"
            image_url, file_id = upload_to_drive(drive_service, tmp_path, filename)
            uploaded_file_ids.append(file_id)

            time.sleep(2)
            insert_image_to_slide(slides_service, presentation_id, slide_id, image_url, config)

        except Exception as e:
            print(f"    [エラー] {e}")
            continue

    for f in tmp_files:
        try:
            os.unlink(f)
        except Exception:
            pass

    url = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    print(f"\n[完了]")
    print(f"  URL: {url}")
    print(f"  挿入画像数: {len(uploaded_file_ids)} 枚")


if __name__ == "__main__":
    main()
