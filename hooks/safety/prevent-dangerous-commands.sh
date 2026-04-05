#!/bin/bash
# 防止危險 Bash 指令執行 | Prevent dangerous bash commands (rm -rf, git push --force, etc.)

set -e

COMMAND="$1"

# 危險關鍵字 grep pattern
DANGEROUS_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "git push --force"
    "git push -f"
    "DROP TABLE"
    "DELETE FROM.*WHERE"
    "TRUNCATE TABLE"
    ": \(\) { : ; };"  # fork bomb
    "sudo rm"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -iE "$pattern" &>/dev/null; then
        echo "❌ 危險指令被阻止 (Dangerous command blocked): $COMMAND" >&2
        exit 2
    fi
done

exit 0
