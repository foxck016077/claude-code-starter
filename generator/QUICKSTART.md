# 快速開始

## 30 秒快速試用

```bash
# 1. 進入產生器目錄
cd ~/claude-code-starter/generator

# 2. 執行互動式問卷
python3 generate_claude_md.py

# 3. 回答 6 個簡短問題（每個 < 10 秒）
# 4. 確認產出 (Y)
# Done! CLAUDE.md 已產生在當前目錄
```

## 或者用快速預設（更快）

```bash
# 一行指令，立即生成
python3 generate_claude_md.py --preset=bot

# 選項: bot, web, scraper, trader
```

## 什麼時候用互動式 vs 預設

| 情況 | 用什麼 | 時間 |
|------|--------|------|
| 第一次用，不知道填什麼 | `--preset=bot` | 5 秒 |
| 我的工作有點特殊 | 互動式模式 | 1-2 分鐘 |
| 我想完全自訂 | 編輯 CLAUDE.md | 5 分鐘 |

## 生成後要做什麼

### Option 1: 放到專案根目錄（推薦）

```bash
# 假設你有一個 Bot 專案
mv CLAUDE.md ~/my-telegram-bot/

# Claude Code 啟動時會自動讀到這個檔案
```

### Option 2: 放到全域設定（系統全用）

```bash
# 所有 Claude Code 專案都用同一套規則
mkdir -p ~/.claude
cp CLAUDE.md ~/.claude/

# 或編輯現有的 ~/.claude/CLAUDE.md
```

## 測試規則是否有效

做完上面的步驟後，打開一個 Claude Code session：

```bash
cd ~/my-telegram-bot  # 或任何有 CLAUDE.md 的目錄

# 啟動 Claude Code
code .
```

在終端詢問：
```
問: 你讀到什麼規則了？用三句話總結
```

Claude 應該能複述你寫在 CLAUDE.md 裡的核心規則。

## 常見第一次問卷

### 我是 Bot 開發者

```
問題 1: MyBot
問題 2: 繁體中文 (1)
問題 3: 寫 Bot (2)
問題 4: 不要動 .env / 密鑰, 不要自動 push, 不要執行危險指令 (1 3 5)
問題 5: 簡潔直接 (1)
問題 6: (按 Enter 跳過)
```

預計時間: 1 分鐘

### 我是 Web 開發者

```
問題 1: WebDev
問題 2: 繁體中文 (1)
問題 3: 寫網站 (1), 自動化腳本 (4)
問題 4: 不要動 .env, 不要改 git 設定, 不要自動 push (1 2 3)
問題 5: 詳細解釋 (2)
問題 6: (按 Enter 跳過)
```

預計時間: 1 分鐘

### 我要完全自訂

用互動式模式，在問題 6（自訂規則）寫你的特殊需求：

```
問題 6: 
- 不要改資料庫連線設定
- 先跑單元測試才能 commit
- 改 config 前務必備份
```

預計時間: 2-3 分鐘

## 如果產生的規則不滿意

直接編輯 `CLAUDE.md`：

```bash
# 用你習慣的編輯器編輯
vim CLAUDE.md
# 或
nano CLAUDE.md
# 或用 VS Code
code CLAUDE.md
```

改完存檔，Claude Code 下次啟動就會讀到新規則。

## 故障排除

| 問題 | 解決方案 |
|------|--------|
| 「選擇未正確註冊」 | 重新執行，輸入 1-3 等編號，用空格分隔多選 |
| 「預設不存在」 | 檢查拼寫，有效的預設: bot, web, scraper, trader |
| 「CLAUDE.md 寫入失敗」 | 檢查目錄權限，或改成 `--preset=bot > my-CLAUDE.md` |
| Claude 沒讀到規則 | 確認 CLAUDE.md 在專案根目錄，不是子目錄 |

## 下一步

1. **把 CLAUDE.md 加入 git**（推薦）
   ```bash
   git add CLAUDE.md
   git commit -m "Add CLAUDE.md: custom Claude Code rules"
   ```

2. **讓團隊也用**
   - 把整個 `generator/` 目錄共享給隊友
   - 或放到公司 wiki，讓大家參考

3. **定期更新**
   - 每月檢查一次，看有沒有新的規則要加
   - 隨著專案演進，工作方式也會改

4. **分享你的預設**
   - 如果你創造了很有用的預設，可以貢獻回來
   - 或分享給同事/朋友

---

**提示**: 不要被「完美的規則」追求綁架。最好的 CLAUDE.md 是你真的會讀、真的會用的那個。先產生一個，跑幾個任務，再慢慢優化。
