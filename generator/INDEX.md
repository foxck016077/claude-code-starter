# Claude Code CLAUDE.md 產生器 — 完整索引

快速導航到你需要的文檔。

## 瀏覽路線圖

```
新手      → [QUICKSTART.md](QUICKSTART.md) (5 分鐘)
          ↓
想深入了解 → [README.md](README.md) (15 分鐘)
          ↓
想自訂規則 → [SETUP.md](SETUP.md) (進階設定)
          ↓
想看例子   → [EXAMPLES.md](EXAMPLES.md) (預設比較)
```

## 核心檔案

| 檔案 | 大小 | 內容 | 何時讀 |
|------|------|------|--------|
| **generate_claude_md.py** | ~8KB | 產生器本體（零依賴）| 執行它 |
| **QUICKSTART.md** | ~3KB | 30 秒快速試用 | 第一次用 |
| **README.md** | ~6KB | 完整功能說明 | 想了解全貌 |
| **SETUP.md** | ~12KB | 安裝、設定、進階 | 遇到問題或要自訂 |
| **EXAMPLES.md** | ~8KB | 預設示範 & 比較 | 挑不出適合的預設 |
| **INDEX.md** | 本檔案 | 導航索引 | 你在這 |

## 例子檔案

```
examples/
├── bot-CLAUDE.md      — Bot 開發者預設
├── web-CLAUDE.md      — Web 開發者預設
├── scraper-CLAUDE.md  — 爬蟲/數據分析預設
└── trader-CLAUDE.md   — 交易開發者預設
```

## 快速命令

```bash
# 執行產生器
cd ~/claude-code-starter/generator
python3 generate_claude_md.py              # 互動式
python3 generate_claude_md.py --preset=bot # 快速預設

# 查看預設例子
cat examples/bot-CLAUDE.md

# 比較預設
diff examples/bot-CLAUDE.md examples/web-CLAUDE.md
```

## 按任務找文檔

### 「我要立即開始」
→ [QUICKSTART.md](QUICKSTART.md) — 5 分鐘快速指南

### 「我不知道選什麼預設」
→ [EXAMPLES.md](EXAMPLES.md) — 看預設例子，對比選擇

### 「我要全自訂規則」
→ [SETUP.md](SETUP.md) —「進階設定」章節

### 「我遇到報錯了」
→ [SETUP.md](SETUP.md) —「故障排除」章節

### 「我要給團隊用」
→ [README.md](README.md) —「授權和分享」章節

### 「我想擴展產生器」
→ [SETUP.md](SETUP.md) —「進階：批量產生」章節

### 「我要了解規則設計哲學」
→ [EXAMPLES.md](EXAMPLES.md) —「為什麼不同預設有不同規則」章節

## 按角色找文檔

### Product Manager / Team Lead
- [README.md](README.md) — 了解功能
- [EXAMPLES.md](EXAMPLES.md) — 預設比較
- [SETUP.md](SETUP.md) —「最佳實踐」章節

### 開發者（第一次用）
- [QUICKSTART.md](QUICKSTART.md) — 快速開始
- 執行: `python3 generate_claude_md.py --preset=web`
- 把產生的 CLAUDE.md 加入你的專案

### 開發者（想自訂）
- [SETUP.md](SETUP.md) —「進階設定」章節
- 編輯 `generate_claude_md.py` 加自訂預設

### DevOps / 自動化工程師
- [SETUP.md](SETUP.md) —「進階：批量產生」章節
- 創建 shell 腳本自動產生多個預設
- 整合進 CI/CD pipeline

## 檔案樹狀圖

```
generator/
├── INDEX.md                          ← 你在這
├── README.md                         ← 完整說明
├── QUICKSTART.md                     ← 快速開始
├── SETUP.md                          ← 安裝 & 進階
├── EXAMPLES.md                       ← 預設示範
├── generate_claude_md.py             ← 執行這個
└── examples/
    ├── bot-CLAUDE.md
    ├── web-CLAUDE.md
    ├── scraper-CLAUDE.md
    └── trader-CLAUDE.md
```

## 規則流程圖

```
開始
  ↓
[選擇方式]
  ├→ 互動式 (generate_claude_md.py)
  │   ↓
  │   [回答 6 問題]
  │   ↓
  │   [產生客製化 CLAUDE.md]
  │   ↓
  │   [確認保存]
  │
  ├→ 快速預設 (--preset=bot/web/scraper/trader)
  │   ↓
  │   [產生對應預設]
  │   ↓
  │   [確認保存]
  │
  └→ 手動編輯
      ↓
      [編輯 CLAUDE.md]
      ↓
      [git commit]
      ↓
      [完成]

保存
  ↓
[複製到專案根目錄]
  ↓
[git add / commit]
  ↓
[Claude Code 讀取規則]
  ↓
[應用工作規則]
```

## 常見路徑

### 場景 1: 新專案，要快速規則
```
1. python3 generate_claude_md.py --preset=web
2. cp CLAUDE.md ~/my-project/
3. cd ~/my-project && git add CLAUDE.md && git commit
4. 開始工作
```

### 場景 2: 想自訂規則
```
1. python3 generate_claude_md.py (互動式)
2. 檢查預覽
3. Y 保存
4. vim CLAUDE.md (微調)
5. git commit
```

### 場景 3: 團隊共用規則
```
1. python3 generate_claude_md.py --preset=web
2. cp CLAUDE.md company-template/
3. 分享給團隊
4. 每人複製到自己的專案
```

### 場景 4: 已有 CLAUDE.md，要更新
```
1. cat existing-CLAUDE.md (看目前規則)
2. python3 generate_claude_md.py (重新產生)
3. diff CLAUDE.md existing-CLAUDE.md
4. 手動合併改動
5. git commit
```

## 功能速查表

| 功能 | 命令 | 文檔 |
|------|------|------|
| 互動式產生 | `python3 generate_claude_md.py` | QUICKSTART |
| Bot 預設 | `python3 generate_claude_md.py --preset=bot` | EXAMPLES |
| Web 預設 | `python3 generate_claude_md.py --preset=web` | EXAMPLES |
| Scraper 預設 | `python3 generate_claude_md.py --preset=scraper` | EXAMPLES |
| Trader 預設 | `python3 generate_claude_md.py --preset=trader` | EXAMPLES |
| 自訂預設 | 編輯 `PRESETS` 字典 | SETUP |
| 自訂問題 | 編輯 `interactive_mode()` | SETUP |
| 批量產生 | 寫 shell 腳本 | SETUP |
| 查看例子 | `cat examples/bot-CLAUDE.md` | EXAMPLES |
| 比較預設 | `diff examples/*.md` | EXAMPLES |

## 關鍵概念

### 預設 (Preset)
預先配置的規則組合，針對不同工作類型優化：
- **Bot**: 排程隔離、環境保護
- **Web**: 版本相容性、本地測試
- **Scraper**: 批量驗證、速率控制
- **Trader**: 模擬驗證、Rollback 方案

### CLAUDE.md
你的 Claude Code 工作規則檔。放在專案根目錄，Claude 會自動讀取。

### 絕對紅線
不能碰的地方：.env、git 設定、危險指令等。嚴格執行。

### 溝通風格
定義 Claude 與你互動的方式：簡潔直接 / 詳細解釋 / 先做再說

## 進階主題

### 為團隊建立標準

1. 產生一個基礎 CLAUDE.md
2. 放到公司範本 repo
3. 讓每個專案複製並微調
4. 版本控制追蹤演變

### 整合進 CI/CD

```yaml
# .github/workflows/claude-setup.yml
- run: python3 generator/generate_claude_md.py --preset=web > CLAUDE.md
- run: git add CLAUDE.md && git commit -m "Auto: update CLAUDE.md"
```

### 自動規則驗證

```bash
# 確認 Claude 讀到規則
claude "根據 CLAUDE.md，我改 .env 時會怎樣？"
# 應該回答：「不能改，因為...」
```

## 版本資訊

| 版本 | 發佈日 | 更新 |
|------|--------|------|
| v1.0 | 2026-04 | 首次發佈 |

---

## 需要幫助？

按順序試試：

1. **翻閱文檔**
   - [QUICKSTART.md](QUICKSTART.md) — 快速問題
   - [SETUP.md](SETUP.md) — 詳細問題
   - [EXAMPLES.md](EXAMPLES.md) — 預設問題

2. **查看例子**
   ```bash
   cat examples/bot-CLAUDE.md
   diff examples/bot-CLAUDE.md examples/web-CLAUDE.md
   ```

3. **試執行**
   ```bash
   python3 generate_claude_md.py --preset=web
   ```

4. **檢查終端輸出**
   大多數問題都會有清楚的錯誤提示

5. **查看源代碼**
   `generate_claude_md.py` 有詳細註解

---

**快速開始:** `python3 generate_claude_md.py --preset=bot` ← 試試這個

**深入學習:** 讀 [README.md](README.md)

**遇到問題:** 查 [SETUP.md](SETUP.md) 的「故障排除」
