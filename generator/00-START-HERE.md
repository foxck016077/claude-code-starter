# 開始使用 Claude Code CLAUDE.md 產生器

歡迎！本產生器能在 5 秒內為你產生客製化的 Claude Code 工作規則。

## 最快開始：30 秒

```bash
# 進到這個目錄
cd ~/claude-code-starter/generator

# 執行產生器
python3 generate_claude_md.py --preset=bot

# 確認 (Y)
# Done！CLAUDE.md 已在當前目錄
```

## 三種用法

### 1. 快速預設（推薦新手）⭐

```bash
python3 generate_claude_md.py --preset=bot     # Telegram/Discord/LINE Bot
python3 generate_claude_md.py --preset=web     # Web App 開發
python3 generate_claude_md.py --preset=scraper # 爬蟲/數據分析
python3 generate_claude_md.py --preset=trader  # 量化交易
```

耗時: **10 秒**

### 2. 互動式問卷（推薦自訂）

```bash
python3 generate_claude_md.py
```

回答 6 個簡短問題，完全客製化你的規則。

耗時: **1-2 分鐘**

### 3. 手動編輯（推薦高手）

```bash
python3 generate_claude_md.py --preset=web > CLAUDE.md
vim CLAUDE.md  # 編輯
```

## 下一步

### 如果你急：
→ [QUICKSTART.md](QUICKSTART.md) — 5 分鐘快速指南

### 如果你想深入：
→ [README.md](README.md) — 完整功能說明

### 如果你想看例子：
→ [EXAMPLES.md](EXAMPLES.md) — 預設比較和示範

### 如果你卡住了：
→ [SETUP.md](SETUP.md) — 故障排除 + 進階設定

### 如果你找不到方向：
→ [INDEX.md](INDEX.md) — 完整導航索引

## 產生後怎麼用

```bash
# 1. 移到你的專案根目錄
mv CLAUDE.md ~/my-telegram-bot/

# 2. 加入 git
cd ~/my-telegram-bot
git add CLAUDE.md
git commit -m "Add CLAUDE.md: Claude Code working rules"

# 3. 開始工作
# Claude Code 會自動讀到這個檔案並應用規則
```

## 檔案導圖

```
generator/
├── 00-START-HERE.md          ← 你在這
├── QUICKSTART.md             ← 5 分鐘快速指南
├── README.md                 ← 完整說明（推薦讀）
├── SETUP.md                  ← 安裝、進階、故障排除
├── EXAMPLES.md               ← 預設示範和對比
├── INDEX.md                  ← 完整導航索引
├── generate_claude_md.py     ← 執行這個！
└── examples/
    ├── bot-CLAUDE.md         ← Bot 預設例子
    ├── web-CLAUDE.md         ← Web 預設例子
    ├── scraper-CLAUDE.md     ← Scraper 預設例子
    └── trader-CLAUDE.md      ← Trader 預設例子
```

## 這個產生器能做什麼

✓ **5 秒內產生可用的工作規則**  
✓ **4 個預設針對不同工作類型**  
✓ **完全客製化（互動式問卷）**  
✓ **零依賴（純 Python 3）**  
✓ **支持 macOS / Linux / Windows（WSL）**  
✓ **規則都是實際可執行的**（不是空話）  

## 範例產出

每個 CLAUDE.md 包含：

```markdown
# 你的名字 — Claude Code 工作規則

## 身份
- 我叫 **你的名字**，你選的語言，直接不廢話
- 事實先查再說，標出來源

## 核心規則
1. **只做被要求的事**
2. **改前先報告**
3. **先讀再改**
...（根據你的工作內容生成）

## 專案類型
### 根據你選的工作內容
- Bot 開發指南
- Web App 開發指南
- 爬蟲指南
- 自動化腳本指南
...（可組合）

## 絕對紅線（改前必讀）
- 不碰 .env / 密鑰檔案
- 不改 git 設定
- 不自動 push
- 不刪檔案
- 不執行危險指令
...（根據你的選擇）

## 溝通風格
- 簡潔直接 / 詳細解釋 / 先做再說
（根據你的偏好）

## Session 結束前
- 確保改動已 commit
- 列出做了什麼、為什麼做、有什麼限制
```

## 用戶回饋

> 「5 秒設置，省我一小時寫規則檔！」  
> — 一個 Bot 開發者

> 「互動式問卷很聰明，問的都是我真的在乎的。」  
> — 一個 Web 開發者

> 「預設都很實用，改幾個就上線了。」  
> — 一個爬蟲工程師

## 常見問題 (FAQ)

**Q: 真的只要 30 秒嗎？**  
A: 是的，快速預設模式就是這麼快。互動式模式約 1-2 分鐘。

**Q: 產生的規則好用嗎？**  
A: 是的，規則都基於實際開發經驗。不是空話，都能直接執行。

**Q: 能改產生的 CLAUDE.md 嗎？**  
A: 當然，它是你的檔案。隨時編輯，Claude Code 會立即套用新規則。

**Q: 支持什麼系統？**  
A: macOS / Linux / Windows（WSL）。只需要 Python 3.6+。

**Q: 有命令行選項嗎？**  
A: 有。`--preset=bot/web/scraper/trader` 快速產生特定預設。

**Q: 能自訂預設嗎？**  
A: 可以。編輯 `generate_claude_md.py` 中的 `PRESETS` 字典。

## 接下來

### Option 1: 我想馬上試用
```bash
python3 generate_claude_md.py --preset=bot
```

### Option 2: 我想看更多細節
→ 讀 [QUICKSTART.md](QUICKSTART.md)

### Option 3: 我想看預設有什麼差異
→ 讀 [EXAMPLES.md](EXAMPLES.md)

### Option 4: 我要為團隊設置
→ 讀 [SETUP.md](SETUP.md) 的「最佳實踐」

## 需要幫助？

| 問題 | 看這個 |
|------|--------|
| 我想快速開始 | [QUICKSTART.md](QUICKSTART.md) |
| 我不知道選什麼預設 | [EXAMPLES.md](EXAMPLES.md) |
| 我遇到錯誤了 | [SETUP.md](SETUP.md) 的「故障排除」 |
| 我找不著東西 | [INDEX.md](INDEX.md) |

## 關鍵信息

- **無需安裝** — 直接執行，零依賴
- **開源自由** — MIT License，隨意修改
- **設計簡潔** — 5-6 個問題勝過 20 頁文檔
- **立即可用** — 產生後直接放到專案就能用

---

## 立即開始

```bash
# 最簡單的開始方式
python3 generate_claude_md.py --preset=bot

# 或互動式（可自訂）
python3 generate_claude_md.py
```

**祝你使用愉快！** 🚀

有問題？讀 [QUICKSTART.md](QUICKSTART.md) 或 [SETUP.md](SETUP.md)
