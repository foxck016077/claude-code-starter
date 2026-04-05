# Claude Code Hooks 文檔索引

整理本專案的所有檔案和資源。

---

## 📖 文檔導航

### 新手開始
1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ — 5 分鐘快速上手
   - 30 秒了解 hooks 是什麼
   - 安裝步驟
   - 常見問題速查

### 完整參考
2. **[README.md](README.md)** — 官方完整文檔
   - Hooks 系統詳解
   - 三大套裝介紹（Safety/Quality/Productivity）
   - 安裝和使用指南
   - FAQ 常見問題
   - 自訂 hook 教學

3. **[EXAMPLES.md](EXAMPLES.md)** — 實際使用案例
   - 每個 hook 的行為演示
   - 自訂 hook 案例研究（禁止 eval）
   - 進階條件式 hook
   - Troubleshooting 常見問題

### 進階開發
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** — 系統架構深入
   - Hook 事件系統
   - Settings.json 詳細結構
   - Shell script 模板
   - 執行流程詳解
   - 效能優化
   - 調試技巧
   - Hook 間通信

### 快速參考
5. **[INSTALL_REFERENCE.md](#)** (本檔案) — 什麼在哪裡？

---

## 🗂️ 目錄結構

```
~/claude-code-starter/hooks/
├── install.py                  # 安裝工具
├── README.md                   # 主文檔
├── QUICKSTART.md               # 快速開始（新手）
├── EXAMPLES.md                 # 使用案例
├── ARCHITECTURE.md             # 架構設計
├── INDEX.md                    # 本檔案
│
├── safety/                     # 安全防護 hooks
│   ├── prevent-dangerous-commands.sh
│   ├── protect-env-files.sh
│   └── no-auto-push.sh
│
├── quality/                    # 品質控制 hooks
│   ├── read-before-edit.sh
│   └── lint-after-write.sh
│
└── productivity/               # 效率提升 hooks
    └── auto-commit-reminder.sh
```

### 安裝後生成的檔案

```
~/.claude/
├── settings.json               # Hook 組態（install.py 生成）
├── settings.backup_*.json      # 備份（install.py 自動備份）
└── hooks/                      # Hook scripts
    ├── prevent-dangerous-commands.sh
    ├── protect-env-files.sh
    ├── no-auto-push.sh
    ├── read-before-edit.sh
    ├── lint-after-write.sh
    └── auto-commit-reminder.sh
```

---

## 🎯 按目的找資料

### 我想...

#### 快速安裝
→ [QUICKSTART.md](QUICKSTART.md) — 30 秒安裝

#### 了解 hooks 是什麼
→ [README.md#什麼是-hooks](README.md#什麼是-hooks) 或 [QUICKSTART.md#30-秒的解釋](QUICKSTART.md#30-秒的解釋)

#### 選擇安裝哪個套裝
→ [README.md#內含的-hooks](README.md#內含的-hooks) — 詳細描述各 hook 功能

#### 看各個 hook 的實際行為
→ [EXAMPLES.md](EXAMPLES.md) — 含執行結果示範

#### 自訂或新增 hook
→ [README.md#我想自己新增一個-hook-怎麼做](README.md) 或 [ARCHITECTURE.md](#shell-script-模板) — 模板和最佳實踐

#### 調試 hook 問題
→ [ARCHITECTURE.md#調試-hooks](ARCHITECTURE.md#調試-hooks) 或 [README.md#hook-沒有執行](README.md#hook-沒有執行)

#### 了解 hook 如何運作的
→ [ARCHITECTURE.md#hook-事件類型](ARCHITECTURE.md#hook-事件類型) — 事件系統詳解

#### 優化 hook 效能
→ [ARCHITECTURE.md#效能最佳化](ARCHITECTURE.md#效能最佳化)

#### 查看某個 hook 的完整程式碼
→ `~/claude-code-starter/hooks/safety/` 或 `quality/` 或 `productivity/`

#### 修改 settings.json
→ [ARCHITECTURE.md#settingsjson-結構](ARCHITECTURE.md#settingsjson-結構) — 欄位說明

---

## 📋 功能速查表

### PreToolUse Hooks（執行前檢查）

| Hook 名稱 | 檔案 | 功能 | 何時觸發 |
|-----------|------|------|--------|
| prevent-dangerous-commands | safety/ | 防止危險 Bash 指令 | 執行 Bash 前 |
| protect-env-files | safety/ | 保護敏感檔案 | Read/Edit/Write 前 |
| no-auto-push | safety/ | 禁止自動 git push | 執行 Bash 前 |
| read-before-edit | quality/ | 警告大檔案未讀 | Edit 前 |

### PostToolUse Hooks（執行後檢查）

| Hook 名稱 | 檔案 | 功能 | 何時觸發 |
|-----------|------|------|--------|
| lint-after-write | quality/ | 自動代碼風格檢查 | Write/Edit 後 |
| auto-commit-reminder | productivity/ | 提醒 commit | Edit/Write 後 |

---

## 🔧 工具參考

### install.py 使用

```bash
# 互動模式
python3 install.py

# 命令行模式
python3 install.py --all        # 全裝
python3 install.py --safety     # 只裝安全
python3 install.py --quality    # 只裝品質
python3 install.py --productivity  # 只裝效率
```

### Hook script 參數格式

```bash
# PreToolUse
./my-hook.sh <tool> <param1> [param2] ...

# PostToolUse
./my-hook.sh <tool> <return_code> [param] ...
```

### 常用指令

```bash
# 查看安裝的 hooks
cat ~/.claude/settings.json | jq '.hooks'

# 測試 hook
bash -x ~/.claude/hooks/my-hook.sh "Bash" "test-param"

# 檢查語法
bash -n ~/.claude/hooks/my-hook.sh

# 查看備份
ls -la ~/.claude/settings.backup_*.json
```

---

## 📚 內容層級

### Level 1: 新手（無經驗）
- 讀 [QUICKSTART.md](QUICKSTART.md)
- 執行 `python3 install.py`
- 完成！

### Level 2: 使用者（已安裝）
- 讀 [README.md](README.md)
- 了解各 hook 做什麼
- 需要時關掉某個 hook（編輯 settings.json）

### Level 3: 進階用戶（自訂 hook）
- 讀 [EXAMPLES.md](EXAMPLES.md) — 看自訂案例
- 讀 [ARCHITECTURE.md](ARCHITECTURE.md) — 深入系統設計
- 新增自己的 hook

### Level 4: 開發者（貢獻者）
- 讀完所有文檔
- 改進現有 hooks
- 提交新 hook 套裝

---

## 🔗 相關資源

### Claude Code 官方
- [Claude Code 文檔](https://claude.ai/docs)
- [Claude Code Hooks 系統](https://claude.ai/docs/hooks) (待補充)

### 社群
- [GitHub Issues](https://github.com/anthropic-ai/claude-code/issues)
- [社群討論](https://github.com/anthropic-ai/claude-code/discussions)

### Shell 相關
- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [Shell Script Best Practices](https://mywiki.wooledge.org/BashGuide)

---

## ❓ 快速 FAQ

**Q: 哪個文檔最適合我？**
- 新手 → QUICKSTART.md
- 想了解功能 → README.md
- 想看例子 → EXAMPLES.md
- 想自訂 hook → ARCHITECTURE.md

**Q: 文檔版本？**
- v1.0 (2026-04-05)
- 對應 install.py v1.0

**Q: 有視頻教學嗎？**
- 目前沒有，歡迎貢獻！

---

## 📊 文檔統計

| 檔案 | 行數 | 內容 |
|------|------|------|
| QUICKSTART.md | ~300 | 快速入門 |
| README.md | ~600 | 完整參考 |
| EXAMPLES.md | ~400 | 使用案例 |
| ARCHITECTURE.md | ~700 | 深入設計 |
| INDEX.md | ~400 | 本檔案 |

總計：~2400 行文檔

---

## 🚀 開始使用

```bash
# 1. 進入目錄
cd ~/claude-code-starter/hooks/

# 2. 執行安裝
python3 install.py

# 3. 選擇套裝
# (互動菜單會出現)

# 4. 完成！
# 下次操作時 hooks 會自動觸發
```

---

**最後更新**: 2026-04-05

**貢獻者**: Hope

**授權**: 自由修改和分享
