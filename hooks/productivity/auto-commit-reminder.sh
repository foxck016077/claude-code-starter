#!/bin/bash
# 大量改動未 commit 時提醒 | Remind to commit when >5 files changed

set -e

TOOL="$1"

# 只在 Edit/Write 後檢查
if [[ "$TOOL" != "Write" ]] && [[ "$TOOL" != "Edit" ]]; then
    exit 0
fi

# 檢查是否在 git repo
if ! git rev-parse --git-dir &>/dev/null; then
    exit 0
fi

# 統計改動檔案數
CHANGED_FILES=$(git diff --name-only 2>/dev/null | wc -l)

if [ "$CHANGED_FILES" -gt 5 ]; then
    echo "📝 Reminder: $CHANGED_FILES files have uncommitted changes (>5). Consider committing." >&2
    echo "   Run: git add . && git commit -m 'message'" >&2
fi

exit 0
