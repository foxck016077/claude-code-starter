#!/bin/bash
# 寫完後自動 lint | Auto-lint .py/.js files after write (catch style issues early)

set -e

FILE_PATH="$1"
TOOL="$2"

# 只在 Write/Edit 後檢查
if [[ "$TOOL" != "Write" ]] && [[ "$TOOL" != "Edit" ]]; then
    exit 0
fi

if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# 根據副檔名執行對應的 linter
case "$FILE_PATH" in
    *.py)
        # 檢查 pylint 或 ruff 是否存在
        if command -v ruff &>/dev/null; then
            echo "🔍 Running ruff on $FILE_PATH..." >&2
            if ! ruff check "$FILE_PATH" 2>&1; then
                echo "⚠️  Ruff found style issues. Fix before committing." >&2
                # exit 2 會擋住，此處示範 soft warning；實裝可改為 exit 2
            fi
        elif command -v pylint &>/dev/null; then
            echo "🔍 Running pylint on $FILE_PATH..." >&2
            pylint "$FILE_PATH" --disable=all --enable=syntax-error 2>&1 || true
        fi
        ;;
    *.js|*.jsx|*.ts|*.tsx)
        # 檢查 eslint
        if command -v eslint &>/dev/null; then
            echo "🔍 Running eslint on $FILE_PATH..." >&2
            if ! eslint "$FILE_PATH" 2>&1; then
                echo "⚠️  ESLint found style issues. Fix before committing." >&2
            fi
        fi
        ;;
    *)
        # 其他副檔名不 lint
        ;;
esac

exit 0
