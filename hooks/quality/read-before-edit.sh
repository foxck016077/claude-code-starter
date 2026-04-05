#!/bin/bash
# 強制先讀檔再改 | Enforce reading file before editing (prevents uninformed changes)

set -e

FILE_PATH="$1"

# 簡單的 session 記錄機制：用 /tmp 存讀取歷史
CLAUDE_SESSION_ID="${CLAUDE_CODE_SESSION_ID:-unknown}"
READ_LOG="/tmp/claude_reads_${CLAUDE_SESSION_ID}.log"

# 初始化讀取日誌
if [ ! -f "$READ_LOG" ]; then
    touch "$READ_LOG"
fi

# 檢查該檔案是否已在本 session 被讀過
if grep -q "^$FILE_PATH$" "$READ_LOG" 2>/dev/null; then
    exit 0  # 已讀過，放行
fi

# 未讀過，檢查檔案大小（簡單的啟發式檢查）
# 如果檔案超過 100 行，強制要求先讀
if [ -f "$FILE_PATH" ]; then
    LINE_COUNT=$(wc -l < "$FILE_PATH" 2>/dev/null || echo 0)
    if [ "$LINE_COUNT" -gt 100 ]; then
        echo "⚠️  檔案超過 100 行，建議先用 Read 工具查看 (File > 100 lines, recommend reading first)" >&2
        echo "   File: $FILE_PATH ($LINE_COUNT lines)" >&2
        # 注：此為提示，技術上無法強制（session 跨工具追蹤困難）
        # 在實裝 hook 時可改為 exit 2 硬擋，此處示範 soft warning
    fi
fi

exit 0
