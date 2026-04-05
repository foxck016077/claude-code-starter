# Hooks 使用示範

本檔案展示各 hooks 的實際行為。

---

## 1. 防止危險指令

### 場景：嘗試執行 `rm -rf /`

```bash
# Claude Code 中執行 Bash 工具
rm -rf /

# 輸出：
# ❌ 危險指令被阻止 (Dangerous command blocked): rm -rf /
# [操作被 exit 2 阻止，無法執行]
```

### 場景：嘗試強制 git push

```bash
git push origin main --force

# 輸出：
# ❌ 自動 push 被阻止，請手動執行 (Auto push blocked, run manually)
#    Reason: To prevent accidental remote changes without review
```

---

## 2. 保護敏感檔案

### 場景：嘗試讀取 `.env` 檔案

```bash
# 使用 Read 工具讀取 ~/.env

# 輸出：
# ⚠️  敏感檔案被保護 (Sensitive file protected): /Users/fox/.env
# Use separate secure credentials management
# [操作被 exit 2 阻止]
```

### 場景：嘗試編輯 credentials.json

```bash
# 使用 Edit 工具修改 ~/config/credentials.json

# 輸出：
# ⚠️  敏感檔案被保護 (Sensitive file protected): /Users/fox/config/credentials.json
# Use separate secure credentials management
```

---

## 3. 自動 Linting

### 場景：寫完 Python 檔案

```python
# 新增一個 test.py 檔案
def hello( ):  # 多餘空格
    x=1  # 沒有空格
    return x
```

**Hook 輸出：**
```
🔍 Running ruff on /Users/fox/project/test.py...
error: 1 error found in /Users/fox/project/test.py:1:11: E201 whitespace after '('
⚠️  Ruff found style issues. Fix before committing.
```

### 場景：寫完 JavaScript 檔案

```javascript
// app.js
var x = 1   // 應該用 const
console.log(x)  // 多餘分號
;
```

**Hook 輸出：**
```
🔍 Running eslint on /Users/fox/project/app.js...
  1:1  error  Unexpected var, use let or const instead  no-var
✨ ESLint found style issues. Fix before committing.
```

---

## 4. 提醒未 Commit 的改動

### 場景：編輯超過 5 個檔案

```bash
# 編輯了 app.py, config.py, utils.py, main.py, helpers.py (5個)
# 再編輯第 6 個檔案時：

# Hook 輸出：
# 📝 Reminder: 6 files have uncommitted changes (>5). Consider committing.
#    Run: git add . && git commit -m 'message'
```

---

## 5. 強制先讀後改

### 場景：編輯大檔案（>100 行）

```bash
# 嘗試編輯 models.py（200 行）

# Hook 輸出（soft warning）：
# ⚠️  檔案超過 100 行，建議先用 Read 工具查看 (File > 100 lines, recommend reading first)
#    File: /Users/fox/project/models.py (200 lines)
```

---

## 自訂 Hook：案例研究

### 案例：禁止使用 eval()

你想確保沒有人在 Python 中使用危險的 `eval()` 函數。

**步驟 1：建立 hook 腳本**

```bash
#!/bin/bash
# 禁止在 Python 中使用 eval() | Prevent eval() in Python

set -e

FILE_PATH="$1"

# 只檢查 .py 檔案
if [[ "$FILE_PATH" != *.py ]]; then
    exit 0
fi

# 檢查是否含有 eval(
if grep -nE "eval\s*\(" "$FILE_PATH" &>/dev/null; then
    echo "❌ eval() is dangerous in $FILE_PATH" >&2
    echo "   Use ast.literal_eval() for safe JSON/string parsing" >&2
    exit 2
fi

exit 0
```

**步驟 2：存到 ~/.claude/hooks/**

```bash
chmod +x ~/.claude/hooks/no-eval.sh
```

**步驟 3：在 settings.json 註冊**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "name": "no-eval",
        "handler": "~/.claude/hooks/no-eval.sh",
        "tools": ["Write", "Edit"]
      }
    ]
  }
}
```

**步驟 4：測試**

```python
# bad_code.py
result = eval(user_input)  # 危險!

# 保存時的 hook 輸出：
# ❌ eval() is dangerous in /Users/fox/bad_code.py
#    Use ast.literal_eval() for safe JSON/string parsing
# [操作被阻止]
```

修正後：

```python
# good_code.py
import ast
result = ast.literal_eval(user_input)  # 安全

# 保存時無警告 ✓
```

---

## 進階：條件式 Hook

### 案例：只有在 commit message 時才檢查

```bash
#!/bin/bash
# 確保 commit message 至少有 10 個字 | Enforce commit message length

set -e

# 這個 hook 需要更複雜的參數傳遞
# 目前的框架支援度有限，但可以透過檢查環境變數

if [ -n "$GIT_COMMIT_MESSAGE" ]; then
    if [ ${#GIT_COMMIT_MESSAGE} -lt 10 ]; then
        echo "❌ Commit message too short (minimum 10 characters)" >&2
        exit 2
    fi
fi

exit 0
```

---

## Troubleshooting 案例

### 問題：Hook 執行失敗，提示 "command not found"

```bash
# lint-after-write.sh 報錯：ruff: command not found

# 解決：安裝 ruff
pip install ruff

# 或使用已安裝的其他工具（如 pylint）
# 修改 ~/.claude/hooks/lint-after-write.sh，改用 pylint
```

### 問題：Hook 阻止了合法操作

```bash
# 我真的需要強制 push，但 no-auto-push hook 擋住了

# 臨時解決：編輯 settings.json，移除這個 hook entry
# 或修改 hook 邏輯，加上例外條件

# 進階：新增環境變數旗標
# 在 hook 中檢查：
if [ "$FORCE_PUSH_ALLOWED" = "true" ]; then
    exit 0
fi
```

---

## 效能考量

所有內建 hooks 都設計為 **<500ms** 執行時間：

| Hook | 平均執行時間 |
|------|------------|
| prevent-dangerous-commands | ~50ms |
| protect-env-files | ~100ms |
| no-auto-push | ~50ms |
| read-before-edit | ~30ms |
| lint-after-write | ~1000ms (需要外部工具) |
| auto-commit-reminder | ~100ms |

**注**：lint-after-write 較慢是因為要執行外部 linter。如果不需要，可停用。

---

## Best Practices

1. **簡單優於完整** — Hook 應該快速執行，複雜邏輯放在外部工具
2. **明確的提示** — 用 emoji 和清楚的錯誤訊息，讓使用者知道發生什麼
3. **易於禁用** — 使用者應該能輕易移除或改動 hook
4. **向下相容** — 新增 hook 時，不應該破壞現有工作流
5. **測試充分** — 新的 hook 應該在實裝前測試好

---

**想要更多範例？歡迎貢獻！** 📚
