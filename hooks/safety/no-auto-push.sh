#!/bin/bash
# 禁止自動 git push | Prevent accidental auto git push (manual only)

set -e

COMMAND="$1"

# 檢查是否含有 git push
if echo "$COMMAND" | grep -iE "git push" &>/dev/null; then
    echo "❌ 自動 push 被阻止，請手動執行 (Auto push blocked, run manually)" >&2
    echo "   Reason: To prevent accidental remote changes without review" >&2
    exit 2
fi

exit 0
