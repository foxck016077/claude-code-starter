# 完整安裝 & 設定指南

歡迎使用 Claude Code CLAUDE.md 產生器！本指南涵蓋所有安裝、使用和進階設定。

## 目錄

1. [前置要求](#前置要求)
2. [快速安裝](#快速安裝)
3. [使用方式](#使用方式)
4. [預設詳解](#預設詳解)
5. [進階設定](#進階設定)
6. [故障排除](#故障排除)

---

## 前置要求

### 必需

- Python 3.6+（檢查: `python3 --version`）
- 終端 / 命令行
- 任意文本編輯器（vim, nano, VS Code 等）

### 選項（推薦）

- git（version control）
- Claude Code 環境

### 系統支持

| OS | 支持 | 備註 |
|----|------|------|
| macOS | ✓ | 最佳支持 |
| Linux | ✓ | 完全支持 |
| Windows | ✓ | WSL 推薦 |

---

## 快速安裝

### 方法 1: 直接執行（推薦）

```bash
# 下載或複製 generator 資料夾
cd ~/claude-code-starter/generator

# 執行
python3 generate_claude_md.py
```

### 方法 2: 加入 PATH（全域可用）

```bash
# 複製到全域路徑
sudo cp generate_claude_md.py /usr/local/bin/
chmod +x /usr/local/bin/generate_claude_md.py

# 之後任何地方都可以執行
generate_claude_md.py
```

### 方法 3: 建立別名（推薦）

```bash
# 加入 ~/.bashrc 或 ~/.zshrc
alias claude-gen="python3 ~/claude-code-starter/generator/generate_claude_md.py"

# 重新載入 shell
source ~/.bashrc

# 現在可以直接執行
claude-gen
```

---

## 使用方式

### 基本用法

```bash
# 互動式模式（推薦新手）
python3 generate_claude_md.py

# 快速預設
python3 generate_claude_md.py --preset=bot
python3 generate_claude_md.py --preset=web
python3 generate_claude_md.py --preset=scraper
python3 generate_claude_md.py --preset=trader
```

### 進階用法

```bash
# 指定輸出路徑
python3 generate_claude_md.py --preset=bot > ~/my-project/CLAUDE.md

# 互動式 + 重定向（更新現有檔案）
python3 generate_claude_md.py | tee ~/my-project/CLAUDE.md

# 在子 shell 中測試
(cd /tmp && python3 ~/path/to/generate_claude_md.py --preset=web)
```

---

## 預設詳解

### 1. Bot 預設 (`--preset=bot`)

**目標使用者:** Telegram/Discord/LINE Bot 開發者

**特點:**
- 強調排程隔離（不互相打架）
- 環境變數保護（Token / API Key）
- 測試驗證前不部署

**包含規則:**
- Bot 邏輯開發指南
- Schedule/Cron 管理
- 環境變數保護
- 快速部署前檢查

**何時用:**
```bash
python3 generate_claude_md.py --preset=bot
```

**例子應用:**
```
我有一個 Telegram Bot，要改消息處理邏輯
→ 用 Bot 預設，Claude 會提醒先讀現有 handlers、測試不部署
```

---

### 2. Web 預設 (`--preset=web`)

**目標使用者:** React/Vue/Next.js/Node.js 開發者

**特點:**
- 版本相容性檢查
- 本地測試強制
- Config 備份
- 套件安裝審批

**包含規則:**
- Web App 開發指南
- 自動化腳本管理
- Config 改動流程
- 依賴管理

**何時用:**
```bash
python3 generate_claude_md.py --preset=web
```

**例子應用:**
```
我有一個 Next.js 應用，要升級 React 版本
→ 用 Web 預設，Claude 會檢查版本相容性、跑本地測試
```

---

### 3. Scraper 預設 (`--preset=scraper`)

**目標使用者:** 爬蟲開發者、數據分析師

**特點:**
- 批量操作前小跑測試
- Selector 驗證
- IP ban 預警
- 速率控制

**包含規則:**
- 爬蟲開發指南
- 數據分析流程
- 速率控制策略
- 錯誤處理

**何時用:**
```bash
python3 generate_claude_md.py --preset=scraper
```

**例子應用:**
```
我要爬 1000 個頁面的商品數據
→ 用 Scraper 預設，Claude 會先跑 5 頁測試 Selector、確認速率
```

---

### 4. Trader 預設 (`--preset=trader`)

**目標使用者:** 量化交易、自動交易開發者

**特點:**
- 模擬驗證強制
- 回滾方案必備
- 排程干擾檢查
- 高風險操作審批

**包含規則:**
- 自動化腳本指南
- 排程管理
- 模擬測試流程
- Rollback 策略

**何時用:**
```bash
python3 generate_claude_md.py --preset=trader
```

**例子應用:**
```
我要改量化交易的進場邏輯
→ 用 Trader 預設，Claude 會要求回測數據、模擬驗證、交叉確認
```

---

## 進階設定

### 自訂預設

編輯 `generate_claude_md.py`，在 `PRESETS` 字典加新預設：

```python
PRESETS = {
    'bot': {...},
    'web': {...},
    # 加你的預設
    'mobile': {
        'name': '行動應用開發者',
        'language': 'zh-tw',
        'use_cases': ['automation', 'learning'],
        'communication': 'direct',
        'safety_rules': ['no_env', 'no_auto_push', 'no_dangerous_commands'],
    }
}
```

執行:
```bash
python3 generate_claude_md.py --preset=mobile
```

### 自訂問題流程

編輯 `interactive_mode()` 函數，加新問題：

```python
def interactive_mode() -> Dict:
    # ... 現有問題 ...
    
    # 加新問題
    print_section("問題 7：你有專屬的 git workflow 嗎？")
    git_workflow = input("例如: git flow, trunk-based, 或留空跳過: ").strip()
    
    return {
        # ... 現有字段 ...
        'git_workflow': git_workflow,
    }
```

然後修改 `generate_claude_md()` 使用這個字段。

### 擴展規則模板

編輯 `generate_*_section()` 函數，自訂規則內容：

```python
def generate_custom_section(custom: str) -> str:
    """自訂規則段."""
    if not custom:
        return ""
    
    # 加前置文字
    return f"""## 自訂規則

{custom}

*補充說明: 這些規則在你的專案中優先級最高，覆蓋通用規則*"""
```

---

## 故障排除

### 問題 1: 「command not found: python3」

**原因:** Python 3 未安裝或不在 PATH

**解決:**
```bash
# 檢查 Python 版本
python --version
python3 --version

# 如果 python3 不存在，試試 python
python generate_claude_md.py

# 或完整路徑
/usr/bin/python3 generate_claude_md.py
```

### 問題 2: 「選擇未正確註冊」或「預設不存在」

**原因:** 輸入格式錯誤

**解決:**
```bash
# 多選: 用空格分隔數字
選擇 (1-5): 1 2 4

# 單選: 只輸入一個數字
選擇 (1-3): 2

# 預設: 檢查拼寫
python3 generate_claude_md.py --preset=bot  ✓ 正確
python3 generate_claude_md.py --preset=Bot  ✗ 錯誤（大小寫敏感）
```

### 問題 3: 「CLAUDE.md 無法寫入」

**原因:** 目錄權限不足

**解決:**
```bash
# 檢查目錄權限
ls -la .

# 如果有 x，改成可寫
chmod 755 .

# 或改輸出路徑
python3 generate_claude_md.py --preset=web > ~/Desktop/CLAUDE.md
```

### 問題 4: Claude Code 沒讀到規則

**原因:** CLAUDE.md 不在專案根目錄或路徑錯誤

**解決:**
```bash
# 確認位置
ls -la ~/my-project/CLAUDE.md  # 應該存在

# 確認內容
head ~/my-project/CLAUDE.md    # 應該以 # 開頭

# 確認讀權限
cat ~/my-project/CLAUDE.md     # 應該可讀

# 通知 Claude Code 重新載入
# 方法 1: 重啟 Claude Code
# 方法 2: 在 Claude Code 中執行 `cat CLAUDE.md` 確認
```

### 問題 5: 色彩輸出在某些終端看起來很亂

**原因:** 終端不支援 ANSI 色碼

**解決:**
```bash
# 禁用色彩輸出（編輯 generate_claude_md.py）
# 在最上面加:
NO_COLOR = True

# 或用環境變數
NO_COLOR=1 python3 generate_claude_md.py
```

---

## 最佳實踐

### 1. 版本控制

```bash
# 把 CLAUDE.md 納入 git
git add CLAUDE.md
git commit -m "Add CLAUDE.md: Claude Code working guidelines"
git push
```

**為什麼:** 讓團隊對齊規則，並追蹤規則的演變

### 2. 定期更新

```bash
# 每月檢查一次
# 在月初執行
python3 generate_claude_md.py --preset=web > CLAUDE.md.new

# 比較差異
diff CLAUDE.md CLAUDE.md.new

# 確認無誤後更新
mv CLAUDE.md.new CLAUDE.md
```

### 3. 團隊同步

```bash
# 在 README.md 加說明
echo "規則檔: CLAUDE.md（每月更新）" >> README.md

# 分享給新隊友
cp CLAUDE.md ~/onboarding/new-team-member-CLAUDE.md
```

### 4. 自訂化清單

```bash
# 創建 CLAUDE-custom.md 記錄專案特定規則
cat > CLAUDE-custom.md << 'EOF'
# 我們專案的特殊規則

## 額外的安全檢查
- 改 payment 相關代碼必須三人審核
- 資料庫 migration 要在開發環境測試 3 次

## 效能要求
- 新 API 端點必須 < 200ms
- 前端 Lighthouse 不低於 90

## 部署流程
- 週一到週五才能部署
- 部署前必須通知 DevOps
EOF
```

---

## 進階：批量產生多個預設

```bash
#!/bin/bash
# generate-all-presets.sh

for preset in bot web scraper trader; do
    echo "生成 $preset 預設..."
    python3 generate_claude_md.py --preset=$preset > examples/${preset}-CLAUDE.md
    echo "✓ 完成: examples/${preset}-CLAUDE.md"
done

echo ""
echo "全部預設已生成:"
ls -lh examples/*-CLAUDE.md
```

執行:
```bash
chmod +x generate-all-presets.sh
./generate-all-presets.sh
```

---

## 支持 & 回饋

如果遇到問題或有改進建議：

1. **檢查文檔**
   - [README.md](README.md) — 完整功能說明
   - [QUICKSTART.md](QUICKSTART.md) — 5 分鐘上手
   - [EXAMPLES.md](EXAMPLES.md) — 預設比較

2. **查看例子**
   ```bash
   ls examples/
   cat examples/web-CLAUDE.md
   ```

3. **提交回饋**
   - 描述問題或建議
   - 附加 terminal 輸出日誌
   - 說明使用場景

---

## 常見提問 (FAQ)

**Q: 能同時用多個 CLAUDE.md 嗎？**  
A: 不行，一個目錄只讀一個。用不同的目錄或 git branch 隔離。

**Q: CLAUDE.md 改了多久才生效？**  
A: 立即生效（下次 Claude Code session）。

**Q: 可以自動套用某個預設到整個組織嗎？**  
A: 可以，在公司的模板 repo 裡預設一個 CLAUDE.md。

**Q: 如果我討厭互動式，能全自動嗎？**  
A: 用預設模式: `python3 generate_claude_md.py --preset=web`

**Q: 能在 CI/CD 中自動生成嗎？**  
A: 可以，加到 GitHub Actions:
```yaml
- run: python3 generator/generate_claude_md.py --preset=web > CLAUDE.md
- run: git add CLAUDE.md && git commit -m "Auto: update CLAUDE.md"
```

---

**下一步:**
1. 執行 `python3 generate_claude_md.py` 試試
2. 讀 [QUICKSTART.md](QUICKSTART.md) 快速了解
3. 檢查 [EXAMPLES.md](EXAMPLES.md) 看預設差異
4. 把 CLAUDE.md 加入你的專案 git
5. 告訴 Claude Code 開始使用新規則
