# Claude Code Hooks Installer

> 讓小白一鍵安裝常用 hooks，無需手工寫 shell script

**Hooks 是什麼？**

Claude Code 的 hooks 是在特定事件觸發時自動執行的腳本——比如在 Bash 執行前檢查指令是否安全，或在 Write 後自動執行 linter。通過 hooks，你可以：

- 🔒 **防止危險操作**（rm -rf, git push --force 等）
- 🛡️ **保護敏感檔案**（.env, credentials 等）
- ✨ **自動品質檢查**（執行 linter、強制先讀後改）
- ⚡ **提升工作效率**（自動提醒 commit）

---

## 快速安裝

### 1. 互動模式（推薦新手）

```bash
python3 install.py
```

會列出可用套裝，你選擇要裝哪些。

### 2. 一行指令安裝特定套裝

```bash
# 全裝（三個套裝都裝）
python3 install.py --all

# 只裝安全相關
python3 install.py --safety

# 只裝品質相關
python3 install.py --quality

# 只裝效率相關
python3 install.py --productivity
```

### 3. 安裝完成

```
✓ Installation Complete!
Total hooks registered: 6
  PreToolUse:
    • prevent-dangerous-commands
    • protect-env-files
    • no-auto-push
    • read-before-edit
  PostToolUse:
    • lint-after-write
    • auto-commit-reminder

Location: ~/.claude/hooks/
Settings: ~/.claude/settings.json
```

---

## 內含的 Hooks

### 🔒 Safety Pack（安全防護）

#### `prevent-dangerous-commands.sh`
- **觸發事件**: PreToolUse (Bash)
- **功能**: 攔截危險指令，包括：
  - `rm -rf /`, `rm -rf ~`（誤刪根目錄/家目錄）
  - `git push --force`, `git push -f`（強制推送）
  - `DROP TABLE`, `TRUNCATE TABLE`（資料庫危險操作）
  - Fork bomb（`:() { : ; };`）
- **行為**: 偵測到危險指令時 **exit 2** 阻止執行

#### `protect-env-files.sh`
- **觸發事件**: PreToolUse (Read, Edit, Write)
- **功能**: 禁止讀取/修改敏感檔案，包括：
  - `.env`, `credentials`, `token`, `secret`
  - `password`, `private_key`, `.aws`, `.gcp`, `.ssh`
  - `config.json`, `apikey`, `.vault`
- **行為**: 偵測到敏感檔案時 **exit 2** 阻止操作

#### `no-auto-push.sh`
- **觸發事件**: PreToolUse (Bash)
- **功能**: 禁止自動執行 `git push`
- **原因**: 防止未審查的代碼意外推送到遠端
- **行為**: exit 2 阻止，提醒手動執行

---

### ✨ Quality Pack（品質控制）

#### `read-before-edit.sh`
- **觸發事件**: PreToolUse (Edit)
- **功能**: 強制先讀檔再改（檔案超過 100 行時警告）
- **目的**: 防止盲目編輯導致邏輯錯誤
- **行為**: soft warning（目前；可改為 exit 2 硬擋）

#### `lint-after-write.sh`
- **觸發事件**: PostToolUse (Write, Edit)
- **功能**: 寫完後自動執行 linter
  - **`.py` 檔案**: 使用 `ruff` 或 `pylint`
  - **`.js/.jsx/.ts/.tsx` 檔案**: 使用 `eslint`
- **行為**: 顯示風格問題，但不阻止（可改為 exit 2 擋住不符合的代碼）
- **前置條件**: 需要已安裝對應的 linter（ruff/pylint 或 eslint）

---

### ⚡ Productivity Pack（效率提升）

#### `auto-commit-reminder.sh`
- **觸發事件**: PostToolUse (Edit, Write)
- **功能**: 監測改動檔案數，超過 5 個時提醒 commit
- **目的**: 避免大量改動堆積未提交
- **行為**: 顯示提醒和建議指令 `git add . && git commit -m 'message'`

---

## Hook 系統架構

### 檔案位置

```
~/.claude/hooks/
├── prevent-dangerous-commands.sh
├── protect-env-files.sh
├── no-auto-push.sh
├── read-before-edit.sh
├── lint-after-write.sh
└── auto-commit-reminder.sh

~/.claude/settings.json
```

### Settings.json 結構

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "prevent-dangerous-commands",
        "handler": "~/.claude/hooks/prevent-dangerous-commands.sh",
        "tools": ["Bash"]
      },
      {
        "name": "protect-env-files",
        "handler": "~/.claude/hooks/protect-env-files.sh",
        "tools": ["Read", "Edit", "Write"]
      }
    ],
    "PostToolUse": [
      {
        "name": "lint-after-write",
        "handler": "~/.claude/hooks/lint-after-write.sh",
        "tools": ["Write", "Edit"]
      }
    ]
  }
}
```

### Exit Code 約定

- **exit 0**: Hook 通過，允許操作繼續
- **exit 1**: 警告（提示，不阻止）
- **exit 2**: 阻止操作（硬擋，操作被取消）

---

## 常見問題 (FAQ)

### Q: 安裝後什麼時候生效？
**A**: 立即生效。無需重啟 Claude Code 或終端，hooks 在下一次操作時自動觸發。

### Q: 我怎麼知道 hook 被觸發了？
**A**: Hook 會輸出訊息到 stderr（標準錯誤流）。你會看到 emoji 提示：
- ❌ 危險操作被阻止
- ⚠️  警告或敏感檔案
- 🔍 linter 執行中
- 📝 提醒 commit

### Q: 我想自己新增一個 hook，怎麼做？

1. 在 `~/.claude/hooks/` 建立一個新的 `.sh` 檔案，比如 `my-custom-hook.sh`
2. 加上這個模板：

```bash
#!/bin/bash
# 簡短說明 | Short description

set -e

# 你的邏輯
TOOL="$1"
PARAM="$2"

# ... 處理邏輯 ...

if [ some_condition ]; then
    echo "❌ Error message" >&2
    exit 2  # 硬擋
fi

exit 0  # 通過
```

3. 設定執行權限：`chmod +x ~/.claude/hooks/my-custom-hook.sh`
4. 編輯 `~/.claude/settings.json`，在 `hooks.PreToolUse` 或 `hooks.PostToolUse` 加入：

```json
{
  "name": "my-custom-hook",
  "handler": "~/.claude/hooks/my-custom-hook.sh",
  "tools": ["Bash"]  // or ["Edit", "Write", "Read"]
}
```

### Q: 某個 hook 太嚴格了，我想關掉它？

編輯 `~/.claude/settings.json`，找到對應的 hook entry，刪除那一行。比如：

```json
"PreToolUse": [
  // 刪除下面這個 entry
  // {
  //   "name": "prevent-dangerous-commands",
  //   "handler": "...",
  //   "tools": ["Bash"]
  // }
]
```

或直接用 install.py 重新安裝（會覆蓋設定，但會自動備份原檔）。

### Q: 我在 MacOS/Linux 上安裝，會有問題嗎？
**A**: 不會。所有 shell script 都用標準 bash，相容 macOS/Linux/WSL。

### Q: Hook 執行失敗怎麼辦？
**A**: 檢查：
1. 檔案是否有執行權限：`ls -l ~/.claude/hooks/`
2. Shell script 是否有語法錯誤：`bash -n ~/.claude/hooks/my-hook.sh`
3. 依賴工具是否安裝（如 ruff、eslint）：`which ruff` / `which eslint`

### Q: 我能看到 hook 執行的日誌嗎？
**A**: 目前 hooks 輸出到 Claude Code 的 stderr。未來可改為寫到日誌檔案（如 `~/.claude/hooks.log`）。

### Q: 我想改 hook 的邏輯，怎麼做？
**A**: 直接編輯 `~/.claude/hooks/` 底下的 `.sh` 檔案。修改會立即生效，無需重啟。

---

## 進階用法

### 自訂 Hook 邏輯

比如，你想自訂「防止危險指令」的黑名單：

1. 編輯 `~/.claude/hooks/prevent-dangerous-commands.sh`
2. 改動 `DANGEROUS_PATTERNS` 陣列：

```bash
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "your-custom-pattern"
    "another-dangerous-thing"
)
```

3. 儲存，立即生效

### 新增工具特定的 Hook

比如，針對 Python 檔案的特殊檢查：

```bash
#!/bin/bash
# 禁止在 Python 中使用 eval | Prevent eval() in Python

set -e

FILE_PATH="$1"

if [[ "$FILE_PATH" == *.py ]]; then
    if grep -n "eval(" "$FILE_PATH" &>/dev/null; then
        echo "❌ eval() is dangerous, use ast.literal_eval() instead" >&2
        exit 2
    fi
fi

exit 0
```

---

## 故障排除

### Hook 沒有執行

**檢查清單：**
1. `~/.claude/settings.json` 是否包含該 hook？
2. Hook 腳本檔案是否存在且有執行權限？
   ```bash
   ls -la ~/.claude/hooks/
   ```
3. 檢查語法：
   ```bash
   bash -n ~/.claude/hooks/your-hook.sh
   ```

### Hook 執行太慢

**優化建議：**
- 避免複雜的邏輯或外部命令呼叫（比如 curl）
- 使用快速工具（grep, sed）而不是重型工具
- 如果 hook 超過 1 秒，考慮改為異步

### Hook 阻止了我想要的操作

**解決方案：**
1. 臨時禁用：編輯 settings.json，註解掉該 hook
2. 調整邏輯：編輯 hook script，改寬鬆條件
3. 完全移除：刪除 settings.json 中的 hook entry

---

## 版本歷史

- **v1.0** (2026-04-05): 初版發布
  - 3 個套裝（Safety, Quality, Productivity）
  - 6 個預製 hooks
  - Python 安裝工具

---

## 授權與貢獻

本項目為 Claude Code 社群資源，開放自由修改與分享。

**貢獻方式：**
1. 開發新 hook
2. 改進現有 hook 的邏輯或效能
3. 補充文檔或 FAQ

---

## 連結

- Claude Code 官方文檔: https://claude.ai/docs
- Hooks 系統說明: (待補充)
- 社群討論: (待補充)

---

**Happy coding! 🚀**
