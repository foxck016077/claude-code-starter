# 產生器輸出例子

本目錄包含 4 個預設的示範輸出，展示不同工作類型會產生什麼規則。

## 文件清單

- `bot-CLAUDE.md` — Telegram/Discord/LINE Bot 開發者
- `web-CLAUDE.md` — Web App 開發者
- `scraper-CLAUDE.md` — 爬蟲/數據分析師
- `trader-CLAUDE.md` — 量化交易開發者

## 快速比較

### Bot 開發者 (`bot-CLAUDE.md`)

**重點規則:**
```markdown
### Bot 開發
- 改 Bot 邏輯前先讀現有的 message handlers
- 測試改動不部署，確認不會炸才上線
- 改 schedule/cron 前確認現有的排程依賴
- 不改 Bot token 或環境設定，一律請示
```

**適合:**
- Telegram Bot 開發
- Discord Bot 開發
- LINE Bot 開發
- 即時通訊相關

**關鍵限制:**
- 不碰 Bot token / API key
- 改排程前要確認
- 測試環境先試

---

### Web App 開發者 (`web-CLAUDE.md`)

**重點規則:**
```markdown
### Web App 開發
- 改 code 前讀整個檔案結構 (`ls -la src/`)
- 小改先跑本地測試再 commit
- 改 config 檔先備份原版
- 不自動安裝新套件，先確認版本相容性

### 自動化腳本
- 改 cron/排程前確認現有依賴和影響
- 自動化指令要有乾淨的 rollback 方案
- 批量操作前小跑試手，確認無誤再全量
```

**適合:**
- React/Vue/Next.js 應用
- Node.js 後端
- 自動化工具
- 部署腳本

**關鍵限制:**
- 版本相容性要檢查
- 新套件裝前確認
- Config 改前備份

---

### 爬蟲/數據分析 (`scraper-CLAUDE.md`)

**重點規則:**
```markdown
### 爬蟲/數據分析
- 大量爬取前先小跑 2-3 筆驗證邏輯
- 改 Selector 前先手動測試一次
- 爬蟲改動不自動執行，先看輸出確認
- 遇到 IP ban/限流，先停下來報告，不盲目重試
```

**適合:**
- 數據爬蟲開發
- 市場分析
- 數據提取
- 自動化數據處理

**關鍵限制:**
- 爬取前小跑測試
- IP ban 會停止
- Selector 改要驗證

---

### 量化交易 (`trader-CLAUDE.md`)

**重點規則:**
```markdown
### 自動化腳本
- 改 cron/排程前確認現有依賴和影響
- 自動化指令要有乾淨的 rollback 方案
- 批量操作前小跑試手，確認無誤再全量
```

**適合:**
- 量化交易策略
- 自動化交易
- 交易監控系統
- 金融數據處理

**關鍵限制:**
- 高風險操作必備 rollback
- 排程干擾檢查
- 模擬測試後才上線

---

## 內容對比表

| 項目 | Bot | Web | Scraper | Trader |
|------|-----|-----|---------|--------|
| 語言 | 繁體中文 | 繁體中文 | 繁體中文 | 繁體中文 |
| 核心規則 | 通用 6 點 | 通用 6 點 | 通用 6 點 | 通用 6 點 |
| 專案類型段 | Bot 開發 | Web App + 自動化 | 爬蟲 + 分析 | 自動化腳本 |
| 紅線數量 | 5 條 | 3 條 | 5 條 | 5 條 |
| 溝通風格 | 簡潔直接 | 簡潔直接 | 詳細解釋 | 簡潔直接 |

---

## 如何使用這些例子

### 1. 作為參考
```bash
# 查看 Bot 開發者的完整規則
cat examples/bot-CLAUDE.md

# 和 Web 開發者比較
diff examples/bot-CLAUDE.md examples/web-CLAUDE.md
```

### 2. 複製作為模板
```bash
# 複製 Bot 預設作為起點，然後自訂
cp examples/bot-CLAUDE.md my-project/CLAUDE.md

# 編輯裡面的規則
vim my-project/CLAUDE.md
```

### 3. 分享給團隊
```bash
# 讓團隊看看有哪些選項
cat examples/README.md

# 各自選擇適合的預設
python3 generate_claude_md.py --preset=web
```

---

## 自訂規則的例子

如果預設不完全符合，可以用互動式模式並在最後加自訂規則：

### 例子 1: Bot + 額外的數據庫限制
```
問題 6: 不要改資料庫 migration 檔案，新 migration 必須在開發環境測試通過
```

→ 產出會包含這條規則

### 例子 2: Web 開發 + 效能要求
```
問題 6: 
- 改完要跑 lighthouse 檢查
- 性能指標下降 > 10% 要報告
- 新圖片格式要用 webp
```

→ 產出會包含所有這些規則

---

## 常見組合

### 1. Full Stack 開發者

用互動式模式，選擇:
- 問題 3: Web App (1) + 自動化腳本 (4)
- 問題 4: 所有紅線 (1 2 3 4 5)

結果: 兼有 Web 和自動化規則

### 2. 數據科學家 + DevOps

用互動式模式，選擇:
- 問題 3: 數據分析 (3) + 自動化腳本 (4)
- 問題 5: 詳細解釋 (2)

結果: 爬蟲 + 自動化 + 詳細說明

### 3. Bot 農場維護者

用 Bot 預設，加自訂規則:
```
問題 6:
- 一次只改一個 Bot，不同時改多個
- Bot 改動前備份 bot_config.json
- 大於 10 個 Bot 的改動要逐個測試
```

---

## 為什麼不同預設有不同規則

設計哲學：**規則應該符合風險等級**

| 預設 | 風險等級 | 為什麼 |
|------|----------|--------|
| Bot | 中等 | 宕機影響即時通訊，但通常可快速恢復 |
| Web | 中等 | 用戶體驗影響，但可回滾 |
| Scraper | 高 | IP ban 很難恢復，速率控制重要 |
| Trader | 超高 | 金錢損失，必須模擬+驗證 |

所以:
- **Bot** 強調 schedule 隔離和環境分離
- **Web** 強調版本相容性和本地測試
- **Scraper** 強調速率控制和小跑測試
- **Trader** 強調 rollback 和模擬驗證

---

## 進階：創建自己的預設

如果你多次生成相同的規則，可以在 `generate_claude_md.py` 中加新預設：

```python
PRESETS = {
    # ... existing presets ...
    'my-ai-course': {
        'name': 'AI 課程開發者',
        'language': 'zh-tw',
        'use_cases': ['web', 'learning'],
        'communication': 'detailed',
        'safety_rules': ['no_env', 'no_delete', 'no_auto_push'],
    }
}
```

然後執行:
```bash
python3 generate_claude_md.py --preset=my-ai-course
```

---

## 驗證規則的有效性

拿到一個 CLAUDE.md 後，問 Claude Code：

```
「根據你的規則檔，我改 .env 的時候會怎樣？」

預期回答: 「不能改，.env 是絕對紅線...」
```

如果 Claude 能正確引用規則，表示讀取成功。

---

**提示**: 這些例子會隨著產生器更新而更新。如果你發現某個預設不夠實用，可以：
1. 編輯本地的 CLAUDE.md
2. 提交 feedback 或 PR 改進產生器
3. 自己擴展新的預設
