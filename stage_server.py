#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LiveTalking AI Live E-Commerce & Performance Showcase Server
提供 AI 自動帶貨、說唱表演、智能問答互動展示台與 Edge-TTS 語音合成後端
"""

import os
import sys
import json
import uuid
import time
import random
import asyncio
from pathlib import Path
from aiohttp import web
import aiohttp_cors
import edge_tts

# 當前目錄設定
BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
ASSETS_DIR = BASE_DIR / "assets"
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# 支援的 Edge-TTS 音色
DEFAULT_VOICES = {
    "yunxi": "zh-CN-YunxiNeural",       # 激情陽光男聲 (帶貨、說唱推薦)
    "xiaoxiao": "zh-CN-XiaoxiaoNeural", # 甜美溫柔女聲 (親切帶貨)
    "hsaiochan": "zh-TW-HsiaoChenNeural", # 台灣甜美女聲 (自然台灣腔)
    "yunjhe": "zh-TW-YunJheNeural",     # 台灣知性男聲
    "yunjian": "zh-CN-YunjianNeural",   # 激情解說男聲
    "yunxia": "zh-CN-YunxiaNeural",     # 活力小生
    "jenny": "en-US-JennyNeural",       # 國際英文女聲
}

# 帶貨話術庫與生成邏輯
SCRIPT_TEMPLATES = {
    "passionate": [
        "家人們！所有直播間的兄弟姐妹們注意了！今天給大家帶來的這款【{name}】，真的不用我多吹！{highlights}！平時在專櫃、在官網原價要【{orig_price}】，今天在我們直播間，品牌方直接放血，限時秒殺只要【{price}】！只有前50組，搶完立刻恢復原價！3、2、1，手慢無，給我火速搶起來！",
        "天吶家人們！看看我手裡的【{name}】！這顏值、這手感，簡直絕了！核心亮點就在於：{highlights}！很多老粉都在後台催我返場，今天終於被我跟品牌方把價格打下來了！不要【{orig_price}】，今天破盤秒殺只要【{price}】！再加送獨家大禮包！準備好了嗎？右上角關注點一點，手速跟上，上連結！",
        "大家屏住呼吸！今天的壓軸王炸爆款——【{name}】登場了！為什麼大家都搶著要？因為它真正做到了{highlights}！今天老闆不在家，主播直接給大家任性放福利！原本【{orig_price}】的頂級規格，今天直播間全網獨家價只要【{price}】！買一盒送一盒，下單還抽免單！衝衝衝，搶到就是賺到！"
    ],
    "review": [
        "哈囉大家好！今天主播為大家做一個深度開箱測評，主角就是這款【{name}】。很多朋友選購時常常踩坑，而這款產品最打動我的地方在於：{highlights}。我們經過長達兩週的實測對比，無論是穩定性還是體驗感都完全超越同級產品。原價【{orig_price}】，今天在直播間爭取到的專屬體驗價是【{price}】。追求品質生活的朋友，閉著眼睛入都不會後悔。",
        "歡迎新進來的朋友！如果你正在尋找一款真正靠譜好用的產品，聽我一句勸，一定要看看這款【{name}】。它的核心技術亮點在於：{highlights}。不僅解決了傳統產品的痛點，而且細節設計非常人性化。目前市場公認定價在【{orig_price}】左右，今天我們直播間特批限量特價【{price}】。下方小黃車可以直接查看詳細參數和測評報告，建議大家盡早鎖定庫存。"
    ],
    "gentle": [
        "哈囉直播間的家人們～今天想跟大家分享的是我自己私藏回購很久的心頭好——【{name}】。每次用它都覺得生活幸福感大大提升，因為它{highlights}，溫柔又省心。平時私訊很多姐妹問我怎麼買最划算，今天特別幫大家談到了直播專屬福利，原價【{orig_price}】，今天只要【{price}】就能帶回家，還加贈專屬體驗裝。喜歡的朋友輕輕點擊下方連結，讓它陪伴你的每一天吧～"
    ],
    "countdown": [
        "最後三十秒倒數！最後三十秒！熱賣榜第一名的【{name}】庫存只剩下最後二十組！{highlights}！再說一遍，今天活動一結束立刻恢復【{orig_price}】！現在只要【{price}】！倒數五個數：5！4！3！2！1！手速快的朋友抓緊付款，右上角紅包雨同步開啟，買到就是大暴賺！"
    ]
}

RAP_TEMPLATES = [
    "Yo check it out！這裡是今日直播間，今天帶來的【{name}】絕對不一般！\n{highlights}，實力強大看得見！\n價格打到骨折，品質頂上天，原價【{orig_price}】猶豫一秒你就慢了一年！\n今天秒殺【{price}】，全場節奏跟著搖！點關注，不迷路，3-2-1 上連結，買到就是大暴富！",
    "來來來，節奏打起來，雙手借給我！\n主播今天不廢話，只說乾貨大實話！\n【{name}】有多神？{highlights}！\n不要九千九，不要九百九，今天直播間福利價只要【{price}】！\n音樂不停，優惠不停，拍下的都是真英雄！Drop the beat，上小黃車！",
    "Mic check one two，今天全場最燃的單品！\n看過來，瞧過來，【{name}】閃亮登台！\n超高顏值超強實力，{highlights}！\n告別焦慮，告別等待，限時狂歡只要【{price}】！\n跟我一起喊：三！二！一！開搶！"
]

QA_TEMPLATES = {
    "現貨": "家人們放心！這款【{name}】我們直接從官方大倉直發，全都是全新現貨！今天下單24小時內極速出庫，保證最快送到大家手上！",
    "優惠": "今天在我們直播間下單就是全網歷史最低價！除了限時特價【{price}】之外，還額外加贈專屬運費險和精美小禮品，收到不滿意包退換，完全零風險！",
    "品質": "品質問題大家一萬個放心！我們的【{name}】具備官方質檢認證，假一賠十！主播自己和團隊全員都在用，品質不過關絕對不敢拿上直播間！",
    "歌": "既然家人們點歌了，主播立刻為大家來一段現場節奏表演！動次打次，音樂起，大家彈幕小小心心刷起來！",
    "default": "感謝這位朋友在彈幕裡的提問！關於【{name}】，大家只要記住：{highlights}，現在特惠只要【{price}】，點擊下方連結就能馬上帶走喔！"
}

# ─── API 端點 ──────────────────────────────────────────────────

async def handle_tts(request):
    """生成 TTS 語音音頻 (MP3)"""
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        voice_key = data.get("voice", "yunxi")
        rate = data.get("rate", "+0%")
        pitch = data.get("pitch", "+0Hz")
        
        if not text:
            return web.json_response({"code": -1, "msg": "text is required"}, status=400)
            
        voice = DEFAULT_VOICES.get(voice_key, voice_key)
        
        # 呼叫 Edge-TTS 生成音訊
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        audio_chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_chunks.append(chunk["data"])
                
        audio_bytes = b"".join(audio_chunks)
        if not audio_bytes:
            return web.json_response({"code": -1, "msg": "TTS generation returned empty audio"}, status=500)
            
        return web.Response(
            body=audio_bytes,
            content_type="audio/mpeg",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        return web.json_response({"code": -1, "msg": str(e)}, status=500)


async def handle_generate_script(request):
    """生成直播帶貨文案、說唱詞或問答"""
    try:
        data = await request.json()
        mode = data.get("mode", "sales") # sales, rap, qa
        name = data.get("name", "爆款智能新品")
        highlights = data.get("highlights", "超長續航、極致輕薄、手感一流")
        price = data.get("price", "NT$ 899")
        orig_price = data.get("orig_price", "NT$ 2,499")
        style = data.get("style", "passionate")
        question = data.get("question", "")

        if mode == "sales":
            tpl_list = SCRIPT_TEMPLATES.get(style, SCRIPT_TEMPLATES["passionate"])
            tpl = random.choice(tpl_list)
            script = tpl.format(name=name, highlights=highlights, price=price, orig_price=orig_price)
        elif mode == "rap":
            tpl = random.choice(RAP_TEMPLATES)
            script = tpl.format(name=name, highlights=highlights, price=price, orig_price=orig_price)
        elif mode == "qa":
            matched = False
            for k, ans in QA_TEMPLATES.items():
                if k in question and k != "default":
                    script = ans.format(name=name, highlights=highlights, price=price)
                    matched = True
                    break
            if not matched:
                script = QA_TEMPLATES["default"].format(name=name, highlights=highlights, price=price)
        else:
            script = f"大家好！歡迎來到直播間，今天為大家推薦【{name}】，{highlights}，特惠只要【{price}】！"

        return web.json_response({"code": 0, "msg": "ok", "script": script})
    except Exception as e:
        return web.json_response({"code": -1, "msg": str(e)}, status=500)


async def handle_upload_image(request):
    """上傳商品照片或自訂主播形象圖片"""
    try:
        reader = await request.multipart()
        field = await reader.next()
        if not field or not field.filename:
            return web.json_response({"code": -1, "msg": "No file uploaded"}, status=400)
            
        ext = os.path.splitext(field.filename)[1].lower() or ".jpg"
        if ext not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
            ext = ".jpg"
            
        filename = f"{uuid.uuid4().hex[:12]}{ext}"
        filepath = UPLOADS_DIR / filename
        
        with open(filepath, "wb") as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
                
        file_url = f"/uploads/{filename}"
        return web.json_response({"code": 0, "msg": "ok", "url": file_url, "filename": filename})
    except Exception as e:
        return web.json_response({"code": -1, "msg": str(e)}, status=500)


async def handle_human(request):
    """相容 LiveTalking /human 介面"""
    try:
        data = await request.json()
        text = data.get("text", "")
        mode = data.get("type", "echo")
        sessionid = data.get("sessionid", "0")
        return web.json_response({"code": 0, "msg": "ok", "received": text, "sessionid": sessionid})
    except Exception as e:
        return web.json_response({"code": -1, "msg": str(e)}, status=500)


async def handle_status(request):
    """檢查服務器狀態"""
    return web.json_response({
        "code": 0,
        "msg": "LiveTalking Showcase Server Running",
        "version": "2.0-Showcase",
        "voices": list(DEFAULT_VOICES.keys()),
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })


async def handle_index_redirect(request):
    """導向展示台首頁"""
    raise web.HTTPFound("/livestream_stage.html")


# ─── 服務器構建與啟動 ──────────────────────────────────────────

def create_app():
    app = web.Application(client_max_size=1024 * 1024 * 50)

    # API 路由 (先加，才套 CORS)
    app.router.add_get("/", handle_index_redirect)
    app.router.add_get("/api/status", handle_status)
    app.router.add_post("/api/tts", handle_tts)
    app.router.add_post("/api/generate_script", handle_generate_script)
    app.router.add_post("/api/upload_image", handle_upload_image)
    app.router.add_post("/human", handle_human)

    # 只對 API 路由套 CORS（靜態檔不套，避免 header 重複 assertion error）
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })
    for route in list(app.router.routes()):
        cors.add(route)

    # 靜態文件路由 (CORS 設定之後再加，避免衝突)
    app.router.add_static("/uploads", path=str(UPLOADS_DIR))
    app.router.add_static("/assets", path=str(ASSETS_DIR))
    app.router.add_static("/", path=str(WEB_DIR))

    return app


def main():
    import argparse
    parser = argparse.ArgumentParser(description="LiveTalking Showcase Server")
    parser.add_argument("--port", type=int, default=8010, help="Listen port (default: 8010)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Listen host (default: 0.0.0.0)")
    args = parser.parse_args()
    
    app = create_app()
    print("=" * 65)
    print(" 🚀 LiveTalking AI 直播帶貨 / 說唱表演展示台已啟動！")
    print(f" 🌐 本地觀看與展示台入口: http://localhost:{args.port}/livestream_stage.html")
    print(f" 📺 LiveTalking 原生首頁:   http://localhost:{args.port}/index.html")
    print(f" 📊 LiveTalking 儀表板:     http://localhost:{args.port}/dashboard.html")
    print("=" * 65)
    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
