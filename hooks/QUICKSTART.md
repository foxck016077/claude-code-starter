# 快速開始 — 5 分鐘上手

## 30 秒的解釋

**Hooks 是什麼？** — 自動執行的小程式，在你執行操作前或後檢查/驗證。比如：
- 防止你執行危險指令（`rm -rf /`）
- 提醒你先讀大檔案再改
- 檢查代碼風格（自動 lint）

---

## 安裝（1 分鐘）

### 方法 1：互動式（推薦新手）

```bash
cd ~/claude-code-starter/hooks/
python3 install.py
```

選擇要裝哪個套裝，按 Enter 確認。

**輸出示例：**
```
Claude Code Hooks Installer
============================================================

Available Hook Packs:

1. 🔒 Safety Pack — 防止危險操作
   • 3 hooks included

2. ✨ Quality Pack — 品質控制
   • 2 hooks included

3. ⚡ Productivity Pack — 效率提升
   • 1 hook included

Options:
  0. All (全裝)
  1. Safety only
  2. Quality only
  3. Productivity only
  Q. Quit

Choose (0/1/2/3/Q): 0

============================================================
Installing 3 hook pack(s)...
============================================================

✓ Installation Complete!
Total hooks registered: 6

Location: ~/.claude/hooks/
Settings: ~/.claude/settings.json
```

### 方法 2：一行指令（進階）

```bash
# 全裝
python3 install.py --all

# 只裝安全防護
python3 install.py --safety

# 只裝品質檢查
python3 install.py --quality

# 只裝效率提升
python3 install.py --productivity
```

---

## 安裝完成後，會發生什麼？（1 分鐘）

### 1. 防止危險指令

```bash
# 你試著執行：
rm -rf /

# Hook 擋住你：
❌ 危險指令被阻止 (Dangerous command blocked): rm -rf /
# 指令沒有執行 ✓
```

### 2. 保護敏感檔案

```bash
# 你試著讀取 .env 檔案：
# [使用 Read 工具讀 ~/.env]

# Hook 擋住你：
⚠️  敏感檔案被保護 (Sensitive file protected): /Users/fox/.env
# 檔案沒有被讀取 ✓
```

### 3. 自動檢查代碼風格

```bash
# 你寫完 test.py：
def hello( ):  # 多餘空格
    return 1

# Hook 自動檢查：
🔍 Running ruff on test.py...
E201 whitespace after '('
⚠️  Ruff found style issues. Fix before committing.
# 但不會擋住你的操作（你可以手動修正）
```

### 4. 提醒 commit

```bash
# 你編輯了 6 個檔案

# Hook 提醒你：
📝 Reminder: 6 files have uncommitted changes (>5). Consider committing.
   Run: git add . && git commit -m 'message'
```

---

## 常用場景（3 分鐘）

### 場景 1：我想用完全最小化的 hooks（只要安全）

```bash
python3 install.py --safety
```

安裝 3 個 hooks：
- ✓ 防止危險指令
- ✓ 保護敏感檔案
- ✓ 禁止自動 push

### 場景 2：我想要最嚴格的品質控制

```bash
python3 install.py --quality
```

安裝 2 個 hooks：
- ✓ 強制先讀後改
- ✓ 自動代碼風格檢查

### 場景 3：我想要所有的（Safety + Quality + Productivity）

```bash
python3 install.py --all
```

安裝全部 6 個 hooks。

### 場景 4：我改主意了，想關掉某個 hook

**不要重新執行 install.py**（會覆蓋設定）。直接編輯：

```bash
vim ~/.claude/settings.json
```

找到要移除的 hook，刪掉那個 entry：

```json
{
  "hooks": {
    "PreToolUse": [
      // 刪除下面這個
      // {
      //   "name": "prevent-dangerous-commands",
      //   ...
      // }
    ]
  }
}
```

儲存，立即生效 ✓

---

## 驗證安裝（1 分鐘）

### 檢查檔案是否存在

```bash
ls -la ~/.claude/hooks/
```

應該看到：
```
-rwxr-xr-x  prevent-dangerous-commands.sh
-rwxr-xr-x  protect-env-files.sh
-rwxr-xr-x  no-auto-push.sh
-rwxr-xr-x  read-before-edit.sh
-rwxr-xr-x  lint-after-write.sh
-rwxr-xr-x  auto-commit-reminder.sh
```

### 檢查 settings.json

```bash
cat ~/.claude/settings.json | jq '.hooks'
```

應該看到：
```json
{
  "PreToolUse": [
    {"name": "prevent-dangerous-commands", ...},
    {"name": "protect-env-files", ...},
    ...
  ],
  "PostToolUse": [...]
}
```

### 測試 Hook（選用）

```bash
# 測試「防止危險指令」hook
bash ~/.claude/hooks/prevent-dangerous-commands.sh "Bash" "rm -rf /"

# 預期輸出：
# ❌ 危險指令被阻止...
# 預期 exit code: 2

echo $?  # 應該輸出 2
```

---

## 常見問題速查

### Q: Hook 什麼時候生效？
**A**: 立即生效。無需重啟 Claude Code 或終端，下一次操作時自動觸發。

### Q: 我看不到 hook 的訊息？
**A**: Hook 輸出到 stderr（標準錯誤）。在 Claude Code 的工具輸出面板應該能看到。

### Q: 我想禁用某個 hook？
**A**: 編輯 `~/.claude/settings.json`，刪除該 hook 的 entry（見上方「場景 4」）。

### Q: 我想增加自己的 hook？
**A**: 見下方「進階」段落。

### Q: Hook 太嚴格了，擋住了我想要的操作？
**A**: 
1. 臨時禁用：編輯 settings.json，註解掉該 hook
2. 調整邏輯：編輯 `~/.claude/hooks/` 底下的 `.sh` 檔案，改寬鬆條件
3. 完全移除：刪除 hook entry

### Q: 安裝期間出錯怎麼辦？
**A**: 
1. 檢查 Python 版本：`python3 --version`（需要 3.6+）
2. 檢查目錄權限：`ls -la ~/.claude/`
3. 重新執行 install.py：`python3 install.py`

### Q: 我有舊的 settings.json，會被覆蓋嗎？
**A**: 不會。install.py 會備份原檔（名稱如 `settings.backup_20260405_120000.json`），然後合併新 hooks。

---

## 進階：新增自己的 Hook（可選）

### 例子：禁止使用 eval()

**第 1 步：建立 hook 腳本**

```bash
cat > ~/.claude/hooks/no-eval.sh << 'EOF'
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
EOF

chmod +x ~/.claude/hooks/no-eval.sh
```

**第 2 步：在 settings.json 註冊**

```bash
# 編輯 settings.json（用你習慣的編輯器）
vim ~/.claude/settings.json
```

在 `hooks.PostToolUse` 陣列加入：

```json
{
  "name": "no-eval",
  "handler": "~/.claude/hooks/no-eval.sh",
  "tools": ["Write", "Edit"]
}
```

完整示例：

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

**第 3 步：測試**

```python
# 寫個 test.py
result = eval(user_input)  # 危險!
```

保存時，hook 會擋住你：

```
❌ eval() is dangerous in test.py
   Use ast.literal_eval() for safe JSON/string parsing
```

修正後保存，通過 ✓

---

## 下一步

- 📚 詳細文檔：[README.md](README.md)
- 🎯 使用案例：[EXAMPLES.md](EXAMPLES.md)
- 🏗️  架構深入：[ARCHITECTURE.md](ARCHITECTURE.md)
- 🔧 自訂 hooks：[README.md#如何自己新增-hook](README.md)

---

**有問題？** 檢查 README.md 的 FAQ 段落。

**想貢獻？** 歡迎提交新 hooks 或改進現有 hooks！

---

**現在就安裝吧！** 🚀

```bash
cd ~/claude-code-starter/hooks/
python3 install.py
```
