#!/bin/bash
# 禁止讀取/修改敏感檔案 | Protect .env, credentials, token files from read/edit/delete

set -e

TOOL="$1"
FILE_PATH="$2"

# 敏感檔名 pattern
SENSITIVE_PATTERNS=(
    ".env"
    "credentials"
    "token"
    "secret"
    "password"
    "private_key"
    ".aws"
    ".gcp"
    ".ssh"
    "config.json"
    "apikey"
    ".vault"
)

# 檔案存在檢查
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# 提取檔案名稱（去路徑）
FILENAME=$(basename "$FILE_PATH")

# 檢查是否是敏感檔案
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    if echo "$FILENAME" | grep -iE "$pattern" &>/dev/null; then
        echo "⚠️  敏感檔案被保護 (Sensitive file protected): $FILE_PATH" >&2
        echo "Use separate secure credentials management" >&2
        exit 2
    fi
done

exit 0
