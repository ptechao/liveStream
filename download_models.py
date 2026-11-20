#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LiveTalking Model & Avatar Downloader
一鍵自動下載 Wav2Lip 模型權重與數字人形象包
"""

import os
import sys
import zipfile
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
AVATARS_DIR = BASE_DIR / "data" / "avatars"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
AVATARS_DIR.mkdir(parents=True, exist_ok=True)

def download_file(url, target_path, label=""):
    target_path = Path(target_path)
    if target_path.exists() and target_path.stat().st_size > 1000:
        print(f"✅ {label or target_path.name} 已存在 ({target_path.stat().st_size / (1024*1024):.1f} MB)，跳過下載。")
        return target_path

    print(f"⬇️ 正在下載 {label or target_path.name}...")
    print(f"   來源: {url}")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)

    tmp_path = target_path.with_suffix(".tmp")
    with urllib.request.urlopen(req) as resp, open(tmp_path, "wb") as f:
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 512
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if total > 0:
                pct = downloaded / total * 100
                mb_down = downloaded / (1024 * 1024)
                mb_tot = total / (1024 * 1024)
                sys.stdout.write(f"\r   進度: {mb_down:.1f} MB / {mb_tot:.1f} MB ({pct:.1f}%)")
                sys.stdout.flush()
    print()
    tmp_path.rename(target_path)
    print(f"✅ 下載完成: {target_path.name} ({target_path.stat().st_size / (1024*1024):.1f} MB)")
    return target_path

def main():
    print("=" * 65)
    print(" 🚀 開始下載 LiveTalking Wav2Lip 模型權重與 Avatar 資料包")
    print("=" * 65)

    # 1. 下載 wav2lip.pth
    wav2lip_url = "https://huggingface.co/shibing624/ai-avatar-wav2lip/resolve/main/wav2lip.pth"
    model_path = MODELS_DIR / "wav2lip.pth"
    download_file(wav2lip_url, model_path, "Wav2Lip256 模型權重 (wav2lip.pth)")

    # 2. 下載數字人形象包 (glass_man 適合快速測試 88MB，亦可選 female_model)
    avatar_url = "https://huggingface.co/shibing624/ai-avatar-wav2lip/resolve/main/wav2lip_avatar_glass_man.zip"
    zip_path = AVATARS_DIR / "wav2lip_avatar_glass_man.zip"
    download_file(avatar_url, zip_path, "數字人形象包 (wav2lip256_avatar1)")

    # 3. 下載 s3fd 人臉檢測模型 (s3fd.pth)
    s3fd_dir = BASE_DIR / "avatars" / "wav2lip" / "face_detection" / "detection" / "sfd"
    s3fd_dir.mkdir(parents=True, exist_ok=True)
    s3fd_path = s3fd_dir / "s3fd.pth"
    s3fd_url = "https://huggingface.co/spaces/hysts/face-detection-with-SCRFD/resolve/main/s3fd.pth"
    download_file(s3fd_url, s3fd_path, "人臉檢測模型 (s3fd.pth)")

    # 4. 解壓縮形象包到 data/avatars/wav2lip256_avatar1
    target_avatar_dir = AVATARS_DIR / "wav2lip256_avatar1"
    target_avatar_dir.mkdir(parents=True, exist_ok=True)

    print(f"📦 正在解壓縮形象包至: {target_avatar_dir}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # 檢查 zip 結構
        names = zf.namelist()
        prefix = ""
        for n in names:
            if n.endswith("coords.pkl"):
                prefix = n[:-len("coords.pkl")]
                break
        
        for member in zf.infolist():
            filename = member.filename
            if prefix and filename.startswith(prefix):
                rel_name = filename[len(prefix):]
            else:
                rel_name = filename
            
            if not rel_name:
                continue
            dest_file = target_avatar_dir / rel_name
            if member.is_dir():
                dest_file.mkdir(parents=True, exist_ok=True)
            else:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, open(dest_file, "wb") as dst:
                    dst.write(src.read())

    print(f"✅ 解壓縮完成！")
    print(f"   coords.pkl 是否存在: {(target_avatar_dir / 'coords.pkl').exists()}")
    print(f"   full_imgs 是否存在: {(target_avatar_dir / 'full_imgs').exists()}")
    print(f"   face_imgs 是否存在: {(target_avatar_dir / 'face_imgs').exists()}")
    print("=" * 65)
    print(" 🎉 所有模型與形象包準備就緒！")
    print("=" * 65)

if __name__ == "__main__":
    main()
