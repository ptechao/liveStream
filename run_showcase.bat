@echo off
chcp 65001 >nul
title LiveTalking AI 直播帶貨與說唱表演展示台

echo ======================================================================
echo    🎙️ LiveTalking AI 直播帶貨與說唱表演展示台
echo ======================================================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/2] 正在檢測並初始化虛擬環境...
    uv venv .venv
    .\.venv\Scripts\python.exe -m pip install aiohttp aiohttp-cors edge-tts
)

echo [2/2] 啟動展示台伺服器中...
echo.
echo ----------------------------------------------------------------------
echo  👉 觀看地方 (在瀏覽器打開):
echo     http://localhost:8010/livestream_stage.html
echo ----------------------------------------------------------------------
echo.

.\.venv\Scripts\python.exe stage_server.py --port 8010
pause
