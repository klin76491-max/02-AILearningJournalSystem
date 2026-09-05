# AI 學習日誌系統（子彈筆記）(The Bullet Journal Method System)
> **專案代號**：`02_AILearningJournalSystem`  
> **所屬章節**：第 2 章 留下痕跡 (Track & Trace)  
> **核心概念**：「追蹤過去、釐清現在、設計未來」— 依據 Ryder Carroll 原作《子彈思考整理術》之思想盤點、焦點目標、四大核心子彈集合、晨晚省思與遷移機制。

---

## 系統特色與功能亮點

1. **思想盤點精靈 (Mental Inventory Wizard)**：
   - 首次進入系統強制引導完成「正在做 (Doing)」、「應該做 (Should)」、「想做 (Want)」三欄人生清單。
   - **篩選測試 (The Test)**：透過「這重要嗎？這有意義嗎？」雙重測試，果斷劃掉假性負擔。
2. **焦點目標鎖定 (Focus Sprints & 54321)**：
   - 挑選最在意的 1~2 個核心目標，依據 54321 原則拆解為具體衝刺專案。
3. **隨時可動態調整 (Adjustable Anytime)**：
   - 全站導航列隨時可進入「🌿 人生清單」管理中心，隨時增刪項目、重新篩選與切換焦點。
4. **正宗子彈筆記工作區 (Core BuJo Hub)**：
   - **今日日誌 (Daily Log)**：晨間焦點意圖 (AM) + 敏捷速記 Rapid Logging + 晚間省思 (PM) + 狀態自評 (1-5)。
   - **正宗子彈符號**：任務 (`•` 進行中 / `x` 完成 / `>` 遷移 / `<` 未來誌 / `—` 劃掉取消)、筆記 (`-`)、事件 (`○`)、反思 (`★`)、阻礙 (`!`)。
   - **遷移機制 (Migration)**：一鍵將未完成任務遷移至明日、當月月誌、排程至未來誌或放手劃掉。
   - **月誌 (Monthly Log)**：日曆頁 (Calendar Page) + 當月任務頁 (Tasks Page)。
   - **未來誌 (Future Log)**：跨月遠期規劃。
5. **AI 智能教練 (AI BuJo Copilot)**：
   - 整合 Google Gemini API，提供盤點雜訊過濾、每日溫暖微小進展反思與週期覆盤報告。
6. **安全認證**：
   - 強制採用 Google OAuth 2.0 唯一一鍵註冊與登入。

---

## 環境需求與技術棧

- **Python**: 3.13+
- **後端框架**: Django 5.2 LTS
- **前端風格**: Vanilla CSS + Bootstrap 5.3 + Bootstrap Icons (Dot Grid 紙質手帳風格)
- **資料庫**: SQLite (開發) / PostgreSQL (生產)
- **第三方服務**: Google OAuth 2.0, Google Gemini API (`google-genai`)

---

## 快速開始 (PowerShell)

### 1. 建立虛擬環境與安裝依賴
```powershell
# 進入專案目錄
cd App/AILearningJournalSystem

# 建立 Python 虛擬環境
python -m venv .venv

# 暫時放寬限制：
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 啟用虛擬環境 (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# 安裝依賴套件
pip install -r requirements.txt
```

### 2. 環境變數配置 (`.env`)
複製 `.env.example` 為 `.env`：
```powershell
Copy-Item .env.example .env
```
並在 `.env` 中填入你的憑證：
- `SECRET_KEY`: Django 密鑰
- `GOOGLE_OAUTH_CLIENT_ID`: Google Cloud OAuth Client ID
- `GOOGLE_OAUTH_CLIENT_SECRET`: Google Cloud OAuth Client Secret
- `GEMINI_API_KEY`: Google Gemini API Key

### 3. 資料庫遷移與初始化
```powershell
.\.venv\Scripts\python.exe manage.py makemigrations accounts inventory goals journal reports
.\.venv\Scripts\python.exe manage.py migrate
```

### 4. 啟動開發伺服器
```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```
瀏覽器開啟：`http://127.0.0.1:8000/`

### 5. 🐳 Docker 獨立微服務建置與部署 (獨立容器)

本專案支援獨立 Docker 容器化部署（嚴禁依賴 `docker-compose`，具備獨立生命週期與資料持久化）：

#### 5.1 建立與設定環境變數檔 (`.env`)
啟動容器前請確保目錄下已建立 `.env` 檔案並配置 Google OAuth 與 Gemini API 金鑰：
```powershell
Copy-Item .env.example .env
```

#### 5.2 建置獨立 Docker 映像檔
```bash
docker build -t fwm-ai-journal:latest .
```

#### 5.3 啟動微服務容器 (含 Volume 資料持久化與 Port 映射)
```bash
# 映射主機 8002 Port，並掛載 .env 與 SQLite 資料庫 Volume
docker run -d \
  --name fwm-app-02 \
  -p 8002:8000 \
  --env-file .env \
  -v fwm_journal_data:/app \
  --restart unless-stopped \
  fwm-ai-journal:latest
```
> [!NOTE]
> 容器啟動時，`docker-entrypoint.sh` 會自動執行 `python manage.py migrate --noinput` 資料庫遷移。
> 啟動後可開啟瀏覽器訪問：[http://localhost:8002/](http://localhost:8002/)

#### 5.4 查看即時日誌
```bash
docker logs -f fwm-app-02
```

#### 5.5 建立管理員帳號 (在容器內執行)
```bash
docker exec -it fwm-app-02 python manage.py createsuperuser
```

#### 5.6 執行容器內自動化測試
```bash
docker exec -it fwm-app-02 python manage.py test accounts inventory goals journal ai_engine reports -v 2
```

#### 5.7 停止、重啟與移除容器
```bash
# 停止容器
docker stop fwm-app-02

# 重新啟動容器
docker start fwm-app-02

# 刪除容器 (Volume 資料仍會妥善保留於 fwm_journal_data)
docker rm -f fwm-app-02
```


---

## 執行單元測試

```powershell
.\.venv\Scripts\python.exe manage.py test accounts inventory goals journal ai_engine reports -v 2
```

---

## 📂 專案架構概覽

- `Dockerfile` — 獨立微服務 Docker 映像檔建置規格。
- `docker-entrypoint.sh` — 容器啟動進入點腳本（自動執行資料庫遷移）。
- `.dockerignore` — Docker 建置排除清單。
- `config/` — Django 專案核心設定、環境變數載入與全域路由 (`urls.py`)。
- `accounts/` — 使用者認證與 Google OAuth 2.0 唯一登入服務。
- `inventory/` — 思想盤點模組 (Doing, Should, Want 三欄清單)。
- `goals/` — 核心焦點目標與 54321 衝刺拆解。
- `journal/` — 子彈筆記核心 (今日日誌、月誌、未來誌、Rapid Logging 符號系統)。
- `ai_engine/` — Google Gemini API 智能教練 (覆盤與雜訊過濾)。
- `reports/` — 週期覆盤報告。
- `templates/` — 前端 Dot Grid 紙質手帳風格 HTML 模板。
- `static/` — 前端樣式與 JS 互動腳本。
- `db.sqlite3` — 本地 SQLite 資料庫。

