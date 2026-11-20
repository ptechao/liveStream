@echo off
chcp 65001 >nul
title LiveTalking AI 直播帶貨與說唱表演展示台

echo ======================================================================
echo    🎙️ LiveTalking AI 直播帶貨與說唱表演展示台
echo ======================================================================
echo.
echo 請選擇啟動模式：
echo   [1] 啟動 AI 擬真主播展示台 (推薦！流暢無卡頓、自動帶貨/說唱/彈幕互動)
echo   [2] 啟動 LiveTalking 原生 WebRTC 數字人服務 (Wav2Lip 深度模型 CPU 推理)
echo   [3] 下載/檢查模型權重與數字人資料包
echo.
set /p mode="請輸入選項 (預設為 1): "
if "%mode%"=="" set mode=1

if "%mode%"=="1" (
    echo.
    echo ----------------------------------------------------------------------
    echo  👉 展示台觀看網址:
    echo     http://localhost:8010/livestream_stage.html
    echo ----------------------------------------------------------------------
    echo.
    .\.venv\Scripts\python.exe stage_server.py --port 8010
) else if "%mode%"=="2" (
    echo.
    echo ----------------------------------------------------------------------
    echo  👉 LiveTalking 原生 WebRTC 網址:
    echo     http://localhost:8010/index.html
    echo  (CPU 推理模式已啟動，batch_size=1)
    echo ----------------------------------------------------------------------
    echo.
    .\.venv\Scripts\python.exe app.py --transport webrtc --model wav2lip --avatar_id wav2lip256_avatar1 --batch_size 1 --listenport 8010
) else if "%mode%"=="3" (
    echo 正在檢查並下載模型權重...
    .\.venv\Scripts\python.exe download_models.py
)
pause
