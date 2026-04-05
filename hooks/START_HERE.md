# Claude Code Hooks 安裝包 — 從這裡開始

> 讓小白一鍵安裝常用 hooks，無需手工寫 shell script

---

## 🎯 30 秒簡介

**Hooks 是什麼？**

在你執行操作前或後自動執行的檢查腳本。比如：
- 防止危險指令：`rm -rf /` 被攔截
- 保護敏感檔案：`.env` 無法讀取
- 自動代碼檢查：寫完 Python 自動跑 linter

**為什麼需要？**

因為手工寫 shell script + 設定 hooks 很麻煩。本安裝包替你做好，一鍵安裝。

---

## ⚡ 馬上開始（2 分鐘）

### 步驟 1：執行安裝

```bash
python3 install.py
```

### 步驟 2：選擇套裝

```
Claude Code Hooks Installer
============================================================

Available Hook Packs:

1. 🔒 Safety Pack — 防止危險操作 (3 hooks)
2. ✨ Quality Pack — 品質控制 (2 hooks)  
3. ⚡ Productivity Pack — 效率提升 (1 hook)

Choose (0/1/2/3/Q): 
```

選擇 **0** 全裝（推薦），或選擇 1/2/3 分別安裝。

### 步驟 3：完成！

```
✓ Installation Complete!
Total hooks registered: 6

Location: ~/.claude/hooks/
Settings: ~/.claude/settings.json

Hooks will activate automatically on next session
```

Hooks 立即生效，無需重啟。

---

## 📚 找你需要的文檔

| 你是... | 讀這份 | 時間 |
|--------|--------|------|
| 完全新手 | **[QUICKSTART.md](QUICKSTART.md)** | 5 min |
| 想了解詳細 | **[README.md](README.md)** | 15 min |
| 想看實例 | **[EXAMPLES.md](EXAMPLES.md)** | 10 min |
| 想自訂 hooks | **[ARCHITECTURE.md](ARCHITECTURE.md)** | 30 min |
| 想找特定內容 | **[INDEX.md](INDEX.md)** | 5 min |
| 想看專案總結 | **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | 5 min |

---

## 🎁 你會安裝什麼？

### 🔒 Safety Pack（安全防護 — 3 個）
- **prevent-dangerous-commands** — 擋住 `rm -rf /`, `git push --force` 等
- **protect-env-files** — 禁止讀取 `.env`, `credentials` 等敏感檔案
- **no-auto-push** — 禁止自動 git push（必須手動）

### ✨ Quality Pack（品質控制 — 2 個）
- **read-before-edit** — 大檔案 (>100 行) 要求先讀再改
- **lint-after-write** — 寫完代碼自動檢查風格（Python/JavaScript）

### ⚡ Productivity Pack（效率提升 — 1 個）
- **auto-commit-reminder** — 改動 >5 個檔案時提醒 commit

**總計：6 個 hooks，開箱即用**

---

## 🚀 馬上測試

安裝完後，試試看：

### 測試 1：防止危險指令

```bash
# 在 Claude Code 的 Bash 工具中執行：
rm -rf /

# 結果：
# ❌ 危險指令被阻止 (Dangerous command blocked): rm -rf /
# [操作被攔截]
```

### 測試 2：編輯大檔案

```
# 用 Edit 工具修改 >100 行的檔案

# 結果：
# ⚠️  檔案超過 100 行，建議先用 Read 工具查看
```

### 測試 3：改動多個檔案

```
# 編輯 6 個檔案

# 結果：
# 📝 Reminder: 6 files have uncommitted changes (>5). Consider committing.
#    Run: git add . && git commit -m 'message'
```

---

## ❓ 常見問題（快速版）

**Q: 安裝後什麼時候生效？**  
A: 立即生效。無需重啟，下次操作時自動觸發。

**Q: 我想關掉某個 hook？**  
A: 編輯 `~/.claude/settings.json`，刪除該 hook 的 entry。

**Q: 我想自己新增 hook？**  
A: 見 [ARCHITECTURE.md](ARCHITECTURE.md) 的「Shell Script 模板」段落。

**Q: 安裝會覆蓋我的設定嗎？**  
A: 不會。原有的 `settings.json` 會被備份（`settings.backup_*.json`），然後新 hooks 會被合併進去。

**Q: 支援 macOS/Linux/Windows 嗎？**  
A: 支援 macOS 和 Linux（包含 WSL）。Windows 需要 WSL 或 Git Bash。

---

## 🎯 常用指令

```bash
# 安裝（互動式）
python3 install.py

# 安裝全部
python3 install.py --all

# 只裝安全相關
python3 install.py --safety

# 只裝品質相關
python3 install.py --quality

# 只裝效率相關
python3 install.py --productivity

# 查看已安裝的 hooks
cat ~/.claude/settings.json | jq '.hooks'

# 測試某個 hook
bash -x ~/.claude/hooks/prevent-dangerous-commands.sh "Bash" "test"
```

---

## 📖 文檔結構

```
START_HERE.md              ← 你在這裡
├── QUICKSTART.md          ← 5 分鐘快速上手
├── README.md              ← 完整參考
├── EXAMPLES.md            ← 實際案例
├── ARCHITECTURE.md        ← 技術深入
├── INDEX.md               ← 文檔索引
└── PROJECT_SUMMARY.md     ← 專案總結
```

**推薦路徑**：
1. 新手 → START_HERE.md → QUICKSTART.md → 安裝 → 完成 ✓
2. 進階 → README.md → EXAMPLES.md → 自訂 ✓
3. 開發 → ARCHITECTURE.md → 貢獻 ✓

---

## ✨ 主要特性

✅ **一鍵安裝** — 無需手寫 shell script  
✅ **6 個預製 hooks** — 開箱即用  
✅ **3 個套裝** — Safety / Quality / Productivity  
✅ **即時生效** — 無需重啟  
✅ **易於禁用** — 編輯 settings.json 即可  
✅ **完整文檔** — 從新手到開發者  
✅ **安全備份** — 自動備份原有設定  
✅ **支援自訂** — 可擴展和修改  

---

## 🚀 現在就開始

```bash
cd ~/claude-code-starter/hooks/
python3 install.py
```

選擇一個套裝，按 Enter，完成！

---

## 📞 需要幫助？

- **找文檔** → [INDEX.md](INDEX.md)
- **新手教學** → [QUICKSTART.md](QUICKSTART.md)
- **詳細說明** → [README.md](README.md)
- **使用案例** → [EXAMPLES.md](EXAMPLES.md)
- **技術細節** → [ARCHITECTURE.md](ARCHITECTURE.md)

---

**版本**: v1.0  
**建立**: 2026-04-05  
**狀態**: ✅ 完成，可投入使用

---

**讓我們開始吧！** 🎉
