# Claude Code CLAUDE.md 產生器

快速為你的 Claude Code 專案產生客製化的工作規則檔 `CLAUDE.md`。

## 使用方法

### 互動式模式（推薦新手）

```bash
python3 generate_claude_md.py
```

回答 6-7 個簡短問題，自動產生客製化的 CLAUDE.md：
1. 你叫什麼名字
2. 用什麼語言
3. 主要工作內容（多選）
4. 絕對不能碰的地方（多選）
5. 溝通風格
6. 有其他特殊規則嗎（選填）

### 快速預設模式

```bash
# Bot 開發者
python3 generate_claude_md.py --preset=bot

# Web App 開發者
python3 generate_claude_md.py --preset=web

# 爬蟲/數據分析
python3 generate_claude_md.py --preset=scraper

# 量化交易
python3 generate_claude_md.py --preset=trader
```

## 輸出內容

每個 CLAUDE.md 包含：
- **身份** — AI 如何稱呼你、工作方式
- **核心規則** — 改程式碼前的基本紀律
- **專案類型** — 根據你的工作內容給出具體建議
- **絕對紅線** — 什麼絕對不能碰（密鑰、git 設定、危險指令等）
- **溝通風格** — 定義 AI 與你的互動方式
- **Session 結束** — 保存工作前的檢查清單

## 規則特色

所有規則都是**實際可用的**，不是空話：

✓ 改前先讀文件，不盲目修改  
✓ 批量操作前小跑試手，確認邏輯  
✓ 做壞就 revert，不疊補丁  
✓ 有驗證才動手，先定義怎麼測  
✓ 絕對紅線明確，密鑰/git/危險指令一律拒絕  

## 例子

### 互動式模式對話
```
>> 問題 1：你的名字
你的名字 [Assistant]: Hunter

>> 問題 2：工作語言
1. 繁體中文
選擇 (1-5): 1

>> 問題 3：主要工作內容
你用 Claude Code 主要做什麼？(可多選)
1. 寫網站/Web App
2. 寫 Bot (Telegram/Discord/LINE)
3. 數據分析/爬蟲
選擇 (1-5): 2 3

...（繼續回答幾個問題）
```

### 產生的 CLAUDE.md 片段
```markdown
# Hunter — Claude Code 工作規則

## 身份
- 我叫 **Hunter**，繁體中文，直接不廢話
- 事實先查再說，標出來源 `[查：<來源>]`，不准猜

## 核心規則
1. **只做被要求的事** — 做 A 就只做 A，想改別的先回報
2. **改前先報告** — 說清改什麼、為什麼、影響範圍，確認才動手
...

## 絕對紅線（改前必讀）
- **不碰 .env / 密鑰檔案** — 任何情況都不改，不上傳
- **不改 git 設定** — 不動 `.git/config`
- **不自動 push** — 改完 commit 就停
```

## 技術細節

- **零依賴** — 純 Python 3，不需要額外安裝
- **彩色輸出** — 終端友善的顏色提示
- **容錯設計** — 空選擇有預設值，不會產生無效規則
- **預設模板** — 內建 4 個常用預設，快速上手

## 將 CLAUDE.md 整合到專案

生成後，把 `CLAUDE.md` 放在你的專案根目錄：

```bash
mv CLAUDE.md ~/your-project/
```

Claude Code 啟動時會自動讀取並應用這些規則。

## 常見問題

**Q: 能不能改 CLAUDE.md 裡的規則？**  
A: 當然，文件是你的，隨時可以改。改完後 Claude Code 會直接套用新規則。

**Q: 能不能同時用多個 CLAUDE.md？**  
A: 不行，一個專案只讀一個。如果需要不同的規則，建議：
- 新建不同的專案目錄
- 或用 git branch 隔離
- 或在 CLAUDE.md 最後加備註「不同分支用不同規則」

**Q: 產生的規則看起來不夠詳細？**  
A: 這是故意的。CLAUDE.md 要保持可閱讀性，高度數字化的規則寫在代碼級別（測試、hook、自動化）。CLAUDE.md 是「人類可讀的原則」，不是「機器檢查清單」。

**Q: 怎麼知道規則是否有效？**  
A: Claude Code 啟動時會在終端顯示「讀取 CLAUDE.md」的日誌。改完規則後，問 AI「你讀到什麼規則了」，它應該能複述。

## 進階用法

### 自訂問題流程

編輯 `generate_claude_md.py` 中的 `interactive_mode()` 函數，加入自己的問題。

### 擴展預設

在 `PRESETS` 字典中加新的預設：

```python
PRESETS = {
    'my-custom': {
        'name': '我的自訂預設',
        'language': 'zh-tw',
        'use_cases': ['web', 'automation'],
        'communication': 'direct',
        'safety_rules': ['no_env', 'no_auto_push'],
    }
}
```

然後執行：
```bash
python3 generate_claude_md.py --preset=my-custom
```

### 批量生成多個 CLAUDE.md

```bash
for preset in bot web scraper trader; do
  mkdir -p /tmp/test-$preset
  cd /tmp/test-$preset
  python3 /path/to/generate_claude_md.py --preset=$preset < /dev/null
done
```

## 設計哲學

這個產生器遵循 Claude Code 的核心原則：

1. **簡化選擇** — 5-6 個問題勝過 20 頁文檔
2. **模板即文檔** — CLAUDE.md 本身就是工作指南
3. **預設優於配置** — 預設涵蓋 80% 的用途
4. **可驗證** — 規則清楚到可以被 AI 執行和驗證

## 建議用法

1. 初次設置用快速預設（`--preset=bot` 等）
2. 跑幾個任務，感受一下 AI 的表現
3. 調整 CLAUDE.md 中不合適的規則
4. 逐漸優化，形成適合自己的工作模式

## 授權

MIT License - 自由使用和修改

---

**提示**: 建議每個月檢查一次 CLAUDE.md，看看有沒有規則需要調整。隨著專案演進，工作方式也會變。
