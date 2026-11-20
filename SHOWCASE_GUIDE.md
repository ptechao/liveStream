# liveStream：AI 擬真數字主播帶貨、表演與即時互動直播展示台

本專案基於 **[LiveTalking](https://github.com/lipku/LiveTalking)** 實時流式數字人架構深度定制，專為**無高階 GPU 的本地環境**打造，實現了免裝大型 CUDA 權重即可順暢運行的**「AI 自動帶貨 + 說唱表演 + 智能互動展示台」**。

---

## 📌 一、 需求背景與目標

用戶需求重點：
1. **基於 LiveTalking 架構**：構建 AI 自動帶貨、表演（說唱跳）、智能問答的直播展示系統。
2. **本機快速測試**：優先支援本機輕量流暢運行，無需受限於本地高階顯卡硬體。
3. **展示台與視覺介面**：啟動後顯示清晰步驟，提供視覺化展示台與觀看頁面。
4. **豐富的互動選項與自訂填寫**：支援選擇說話/帶貨/表演模式，支援輸入商品名稱、特點、價格、上傳商品照片、購買 URL。
5. **擬真數字 AI 主播**：提供高擬真度主播形象、自然口型同步、呼吸與眨眼微動作，並支援上傳任意真人肖像照片一鍵驅動。

---

## 🚀 二、 已完成之核心功能

### 1. 🛍️ AI 自動帶貨口播系統
* **一鍵範本帶入**：預設多種熱銷品類（降噪耳機、專業運動錶、精品冷萃咖啡、筋膜按摩槍）。
* **商品資料自訂**：商品名稱、核心亮點、秒殺特價、原價、活動標籤、商品購買網址。
* **商品圖上傳與預覽**：支援本地照片上傳（儲存於 `/uploads/`）或貼上圖片 URL。
* **4 種演繹風格 AI 文案生成**：
  * 💥 **爆款激情叫賣**：熱情高亢、破盤特惠、限時秒殺話術。
  * 🧐 **專業測評開箱**：理性數據、品質解析、痛點分析。
  * 💖 **溫柔知性推坑**：親切真誠、自用回購、生活體驗。
  * ⏱️ **限時倒數秒殺**：緊張刺激、庫存告急、催促下單。
* **直播間商品浮動卡**：開播時動態彈出商品卡片，帶有折扣角標與立即搶購跳轉。
* **3·2·1 上架大字特效**：全螢幕震撼彈出開搶倒數，強化直播間緊迫感。

### 2. 🎤 表演 / 說唱跳大秀模式 (Rap & Dance)
* **押韻說唱詞自動生成**：AI 自動將商品特點改編為節奏感強勁的押韻說唱詞（支援雙押與合轍押韻）。
* **節奏速度切換**：125 BPM（狂暴快嘴）、105 BPM（標準律動）、88 BPM（隨性搖擺）。
* **動態律動表演**：數位人加大肢體擺動幅度與點頭節奏，伴隨背景節拍律動。
* **炫彩舞台燈光**：提供霓虹派對（Neon Club）、賽博紫光（Cyberpunk）、專業暖光（Pro Studio）切換。
* **現場音效觸發板**：內建 Web Audio 合成音效（👏 掌聲歡呼、🛎️ 叮咚上架、🥁 激動戰鼓、📢 派對喇叭）。

### 3. 💬 觀眾互動 & 彈幕問答系統
* **真實感滾動彈幕**：自動模擬粉絲進場、點贊、購買評價（「已拍兩組」、「品質有保固嗎」）。
* **自訂觀眾彈幕提問**：使用者可在控制台模擬任意觀眾發送訊息。
* **AI 智能應對**：針對「現貨/發貨」、「優惠贈品」、「品質保固」、「主播唱歌」等問題自動產生應對話術。
* **主播即時口播解答**：數位人主播即時以語音回覆提問並提及粉絲。

### 4. 🧑‍🎤 擬真數字 AI 主播模組
* **三大預設高擬真主播**：
  * 🌟 **艾蓮娜 (Elena)**：輕奢知性、專業金牌帶貨官。
  * 🎤 **盧卡斯 (Lucas)**：潮流嘻哈、爆款說唱帶貨小生。
  * 🌸 **米亞 (Mia)**：甜美清新、親切鄰家好物分享。
* **📸 真人照片一鍵換臉驅動**：支援本機上傳任意真人肖像照，自動定位面部，即時疊加動態呼吸、自然眨眼與音素嘴型！
* **雙模式舞台展現**：
  * **擬真照片級主播直播間** (`livestream_stage.html`)：細膩膚質、自然打光、即時口型疊加。
  * **3D 擬真主播台** (`realistic_avatar.html`)：Three.js 3D 骨骼角色、光影渲染。

### 5. 🎙️ 擬真語音與口型同步 (Lip-Sync Engine)
* **微軟 Edge-TTS 神經網絡音色**：
  * `zh-TW-HsiaoChenNeural`（台灣甜美女聲）
  * `zh-CN-YunxiNeural`（陽光激情男聲，喊麥首選）
  * `zh-CN-XiaoxiaoNeural`（溫柔自然女聲）
  * `zh-TW-YunJheNeural`（台灣沉穩男聲）
  * `zh-CN-YunjianNeural`（影視解說激情男聲）
  * `en-US-JennyNeural`（國際英語女聲）
* **音素口型實時解析 (Web Audio FFT)**：分析語音頻譜能量，平滑驅動開口幅度、露齒與唇峰微笑，毫無機械卡頓感。

---

## 📂 三、 系統架構與檔案清單

```
d:\peter\liveStream\
├── stage_server.py             # 展示台後端服務 (Edge-TTS 語音流、文案生成 API、上傳處理)
├── run_showcase.bat            # 本機一鍵啟動腳本
├── generate_avatars.py         # 高擬真主播肖像生成腳本
├── assets/
│   └── avatars/                # 擬真主播肖像資源
│       ├── elena_pro.png       # 艾蓮娜主播
│       ├── lucas_hype.png      # 盧卡斯主播
│       └── mia_sweet.png       # 米亞主播
├── web/
│   ├── livestream_stage.html   # 【主要展示台】擬真主播自動帶貨與說唱表演直播間
│   └── realistic_avatar.html   # 【3D展示台】Three.js 3D 擬真主播舞台
├── uploads/                    # 使用者自訂上傳商品照片與主播照片儲存目錄
├── app.py                      # LiveTalking 原生 WebRTC 後端 (GPU 模式預留)
└── README.md                   # 專案主說明文檔
```

---

## 🖥️ 四、 本機快速啟動步驟

### 步驟 1：啟動伺服器
在專案根目錄中雙擊執行：
```bat
run_showcase.bat
```
*(腳本會自動檢測虛擬環境並啟動在 `http://localhost:8010`)*

### 步驟 2：開啟瀏覽器觀看
* **主要展示台（推薦）**：[http://localhost:8010/livestream_stage.html](http://localhost:8010/livestream_stage.html)
* **3D 擬真舞台（備選）**：[http://localhost:8010/realistic_avatar.html](http://localhost:8010/realistic_avatar.html)
* **LiveTalking 原生首頁**：[http://localhost:8010/index.html](http://localhost:8010/index.html)

---

## 🔗 五、 Git 儲存庫

* **GitHub 遠端庫**：[https://github.com/ptechao/liveStream](https://github.com/ptechao/liveStream)
* **上游開源參照**：[https://github.com/lipku/LiveTalking](https://github.com/lipku/LiveTalking)
