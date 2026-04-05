# Hooks 系統架構

本檔案說明 Claude Code hooks 系統的內部設計。

---

## 系統概覽

```
Claude Code 執行
    ↓
PreToolUse Hook
    ↓ (驗證/阻止)
    ├─ exit 0: 繼續
    └─ exit 2: 阻止操作
    ↓
工具執行 (Bash, Edit, Write, etc.)
    ↓
PostToolUse Hook
    ↓ (日誌/建議)
    └─ exit 0: 完成
```

---

## Hook 事件類型

### 1. PreToolUse

**觸發時機**: 使用者執行工具前

**用途**:
- 驗證操作的安全性
- 檢查前置條件
- 防止危險動作

**參數傳遞**:
```bash
$1 = 工具名稱 (Bash, Read, Edit, Write)
$2 = 第一個參數（通常是檔案路徑或指令）
```

**Exit Code**:
- `0`: 允許操作
- `2`: 阻止操作（工具執行被取消）

**範例**:
```bash
# 防止危險指令
if echo "$COMMAND" | grep "rm -rf"; then
    exit 2  # 阻止
fi
exit 0  # 通過
```

### 2. PostToolUse

**觸發時機**: 工具執行後

**用途**:
- 後處理結果
- 驗證輸出
- 自動化後續動作

**參數傳遞**:
```bash
$1 = 工具名稱
$2 = 返回狀態 (0 = 成功, 非 0 = 失敗)
$3 = 執行時間（毫秒）
```

**Exit Code**:
- `0`: 接受結果
- `1`: 警告（通知但不阻止）
- `2`: 拒絕結果（需要使用者修正）

**範例**:
```bash
# Linting 後檢查結果
if ! ruff check "$FILE"; then
    exit 2  # 要求修正代碼
fi
exit 0
```

---

## Settings.json 結構

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "unique-hook-id",
        "handler": "~/.claude/hooks/script.sh",
        "tools": ["Bash", "Edit", "Write"],
        "timeout": 5000,
        "enabled": true
      }
    ],
    "PostToolUse": [
      {
        "name": "lint-check",
        "handler": "~/.claude/hooks/lint.sh",
        "tools": ["Write", "Edit"],
        "timeout": 10000,
        "enabled": true
      }
    ]
  }
}
```

### 欄位說明

| 欄位 | 型態 | 說明 | 預設 |
|------|------|------|------|
| `name` | string | Hook 唯一識別符 | 必需 |
| `handler` | string | Shell script 路徑 | 必需 |
| `tools` | array | 觸發的工具名稱 | `["Bash"]` |
| `timeout` | number | 執行超時（毫秒） | 5000 |
| `enabled` | boolean | 是否啟用 | true |

---

## Shell Script 模板

### 基本模板

```bash
#!/bin/bash
# 用途說明 | English description

set -e  # 任何命令失敗時停止

# 讀取參數
TOOL="$1"
PARAM="$2"

# 驗證邏輯
if [ some_condition ]; then
    echo "❌ Error message" >&2
    exit 2  # 阻止
fi

# 通過
exit 0
```

### 詳細模板（含日誌）

```bash
#!/bin/bash
# Hook 完整模板 | Comprehensive hook template

set -e

TOOL="$1"
PARAM="$2"
RETURN_CODE="$3"  # 僅 PostToolUse 有

# 日誌函數
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

warn() {
    echo "⚠️  $*" >&2
}

error() {
    echo "❌ $*" >&2
}

# 邏輯處理
log "Hook executed: $TOOL"

if [ some_error ]; then
    error "Something went wrong"
    exit 2
fi

log "Hook passed"
exit 0
```

---

## 執行流程詳解

### 案例 1：編輯檔案（Edit Tool）

```
1. 使用者點擊 Edit 工具，輸入檔案路徑 /tmp/test.py

2. Claude Code 觸發 PreToolUse hooks
   ├─ read-before-edit.sh 執行
   │  └─ 檢查檔案是否已讀過
   │     → exit 0（已讀或 <100 行）
   │
   └─ protect-env-files.sh 執行
      └─ 檢查是否敏感檔案
         → exit 0（不是敏感檔案）

3. 所有 PreToolUse hooks 通過
   → Edit 工具執行

4. Edit 完成後，觸發 PostToolUse hooks
   ├─ lint-after-write.sh 執行
   │  └─ ruff check /tmp/test.py
   │     → exit 0（風格正確）
   │
   └─ auto-commit-reminder.sh 執行
      └─ git diff --name-only | wc -l
         → exit 0（<5 個檔案）

5. 所有 hooks 完成
   → 編輯成功 ✓
```

### 案例 2：執行危險指令（Bash Tool）

```
1. 使用者執行 Bash: rm -rf /

2. Claude Code 觸發 PreToolUse hooks
   └─ prevent-dangerous-commands.sh 執行
      └─ grep "rm -rf /"
         → 匹配到危險指令
         → exit 2（阻止）

3. Hook 返回 exit 2
   → Claude Code 阻止 Bash 工具執行
   → 顯示錯誤訊息
   → 操作取消 ✗
   
4. PostToolUse hooks 不執行（因為工具未執行）
```

---

## 環境變數和上下文

Hook 執行時可以存取的環境變數：

```bash
# Claude Code 系統
CLAUDE_CODE_VERSION          # e.g., "2.1.90"
CLAUDE_CODE_SESSION_ID       # 當前 session ID

# 使用者資訊
HOME                         # 使用者家目錄
USER                         # 使用者名稱

# Git（如果在 repo）
GIT_DIR                      # .git 目錄路徑
GIT_WORK_TREE                # 工作目錄

# 自訂變數（可在 settings.json 設定）
CUSTOM_VAR                   # 任何自訂設定
```

**在 hook 中使用**:

```bash
#!/bin/bash
# 存取環境變數示範

if [ -n "$GIT_DIR" ]; then
    # 在 git repo 中
    git status --short
fi

SESSION_LOG="/tmp/claude_${CLAUDE_CODE_SESSION_ID}.log"
echo "Hook executed at $(date)" >> "$SESSION_LOG"
```

---

## 錯誤處理和日誌

### 標準錯誤（stderr）

所有 hook 訊息應輸出到 stderr（不是 stdout），以便與工具輸出分離：

```bash
# 正確 ✓
echo "❌ Error" >&2
echo "📝 Info" >&2

# 錯誤 ✗
echo "❌ Error"  # 這會混入工具輸出
```

### 日誌檔案

可選：寫入 hook 執行日誌：

```bash
#!/bin/bash
# 帶日誌的 hook

set -e

HOOK_LOG="${HOME}/.claude/hooks.log"

{
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Hook started"
    
    # ... hook 邏輯 ...
    
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] Hook completed with exit code 0"
} >> "$HOOK_LOG" 2>&1

exit 0
```

---

## 效能最佳化

### 1. 減少子程序調用

```bash
# 慢 (多個 grep/sed)
if grep "pattern1" "$FILE" | grep "pattern2"; then
    echo "Match"
fi

# 快 (單次 grep)
if grep -E "pattern1.*pattern2" "$FILE"; then
    echo "Match"
fi
```

### 2. 提早退出

```bash
# 慢 (檢查所有條件)
ERROR=0
if [ condition1 ]; then ERROR=1; fi
if [ condition2 ]; then ERROR=1; fi
if [ condition3 ]; then ERROR=1; fi
[ $ERROR -eq 0 ]

# 快 (條件滿足即退出)
[ condition1 ] || [ condition2 ] || [ condition3 ] || exit 0
exit 2
```

### 3. 使用內建命令

```bash
# 慢
for file in $(find . -name "*.py"); do
    ...
done

# 快
find . -name "*.py" | while read file; do
    ...
done
```

### 4. 設定合理的 timeout

在 settings.json 中設定 timeout（毫秒）：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "name": "quick-check",
        "handler": "~/.claude/hooks/quick.sh",
        "timeout": 1000  // 1 秒
      },
      {
        "name": "slow-check",
        "handler": "~/.claude/hooks/slow.sh",
        "timeout": 10000  // 10 秒
      }
    ]
  }
}
```

---

## 調試 Hooks

### 1. 測試 Hook 腳本

```bash
# 直接執行，測試參數
bash -x ~/.claude/hooks/my-hook.sh "Bash" "rm -rf /"

# 檢查語法
bash -n ~/.claude/hooks/my-hook.sh

# 逐行執行（調試模式）
bash -x ~/.claude/hooks/my-hook.sh
```

### 2. 檢查 settings.json

```bash
# 驗證 JSON 格式
python3 -m json.tool ~/.claude/settings.json

# 確認 hook 路徑存在
ls -la ~/.claude/hooks/
```

### 3. 啟用詳細日誌

在 hook 中加入 debug 模式：

```bash
#!/bin/bash
# Debug 模式 Hook

set -e

DEBUG="${DEBUG:-false}"

if [ "$DEBUG" = "true" ]; then
    set -x  # 列印所有執行的命令
fi

# ... hook 邏輯 ...

exit 0
```

執行時：

```bash
DEBUG=true claude-code  # 啟用 debug
```

---

## Hook 間的通信

### 使用臨時檔案共享狀態

```bash
# Hook A: 記錄檔案被讀過
~/.claude/hooks/read-tracker.sh
#!/bin/bash
if [ "$1" = "Read" ]; then
    echo "$2" >> /tmp/claude_reads_${CLAUDE_CODE_SESSION_ID}.log
fi
exit 0

# Hook B: 檢查檔案是否被讀過
~/.claude/hooks/check-read.sh
#!/bin/bash
if grep -q "^$2$" /tmp/claude_reads_${CLAUDE_CODE_SESSION_ID}.log; then
    exit 0  # 已讀
fi
exit 2  # 未讀
```

### 使用環境變數

```bash
# 在 settings.json 中設定
{
  "hooks": {
    "PreToolUse": [{
      "name": "check-var",
      "handler": "~/.claude/hooks/check.sh",
      "env": {
        "CUSTOM_THRESHOLD": "100"
      }
    }]
  }
}

# Hook 中使用
#!/bin/bash
THRESHOLD=${CUSTOM_THRESHOLD:-50}
if [ $FILE_SIZE -gt $THRESHOLD ]; then
    echo "File too large"
    exit 2
fi
```

---

## 與 Claude Code 核心的整合點

- **settings.json**: Hook 組態存儲位置
- **~/.claude/hooks/**: Hook script 目錄
- **Session context**: 存取目前編輯的檔案、工具等
- **Exit codes**: 標準化的信號機制

---

## 限制和已知問題

1. **無法跨 Hook 共享狀態** — Hook 間通信需要透過檔案或環境變數
2. **超時無法自訂** — 每個 hook 有全域 timeout 上限
3. **無法查詢工具輸出** — PreToolUse hook 無法看到工具執行結果
4. **Session 持久化困難** — 每個 session 的狀態隔離

---

## 未來擴展方向

- [ ] Hook 依賴關係（Hook A 執行後才執行 Hook B）
- [ ] 非同步 Hook 執行
- [ ] Hook 結果快取
- [ ] Web UI 管理 Hook
- [ ] Hook 套件市場

---

**想貢獻架構改進？** 歡迎提案！ 🚀
