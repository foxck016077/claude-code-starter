# Multi-Agent 實戰指南：Claude Code 協作系統

> 你開了兩個 Claude Code 終端，卻發現他們根本不知道對方在幹嘛？這就是爲什麼需要「真正的多 agent」。

## 「多開視窗」vs「真正的多 agent」

### 多開視窗的問題
```
Agent A (終端1)          Agent B (終端2)
改 src/main.js -----> 不知道          改 src/main.js ✗ 衝突!
```
- 各自獨立，無溝通機制
- 容易改同一個檔案造成衝突
- 沒有審核流程，品質無保證
- 「我改完了」卻不知道另一個 agent 有沒有完成

### 真正的多 agent
```
Agent A (開發者)         Agent B (審查者)
改完代碼 ──> review/ ──> 檢查品質 ──> 批准/打回
```
- 有分工，知道對方的職責
- 有交接點（review/ 目錄、結果檔案）
- 有協議，避免衝突
- 可追蹤，知道進度

---

## 三種 Multi-Agent 模式（由簡到繁）

### 模式 1：手動分工（最簡單，適合小團隊）

**場景：** 一個人用兩個 agent，一個寫 code 一個寫 test

**實作方法：**
- 約定不同的工作目錄
- 不同的 CLAUDE.md 定義職責

**目錄結構：**
```
project/
├── src/              # Agent A 只改這裡
├── tests/            # Agent B 只改這裡
├── .claude-code/
│   ├── agents/
│   │   ├── developer/
│   │   │   └── CLAUDE.md    # Agent A 的指示
│   │   └── tester/
│   │       └── CLAUDE.md    # Agent B 的指示
```

**Agent A (Developer) CLAUDE.md：**
```markdown
# Role: Code Developer
- 只修改 src/ 下的檔案
- 每個功能做完後更新 .claude-code/status.json
- 禁止改 tests/ 或 docs/
- 看到 .claude-code/review-queue/ 就停手，等 tester 審完

## Status
新增功能後寫到 .claude-code/status.json：
{"last_task": "新增 auth 模組", "status": "ready_for_review", "timestamp": "2026-04-05T10:00:00Z"}
```

**Agent B (Tester) CLAUDE.md：**
```markdown
# Role: QA & Test Engineer
- 只修改 tests/ 下的檔案
- 每天檢查 .claude-code/status.json，看有沒有新任務
- 寫測試驗證 Agent A 的代碼
- 如果發現 bug，寫進 .claude-code/review-queue/bugs.md
- 全通過後更新 status.json 標記「verified」

## Test Routine
1. 讀 status.json
2. 跑 tests/
3. 記錄結果
```

**status.json 格式：**
```json
{
  "last_task": "新增 auth 模組",
  "status": "ready_for_review",
  "completed_by": "agent_a",
  "timestamp": "2026-04-05T10:00:00Z",
  "test_status": null
}
```

改成：
```json
{
  "last_task": "新增 auth 模組",
  "status": "verified",
  "completed_by": "agent_a",
  "verified_by": "agent_b",
  "test_status": "all_pass",
  "timestamp": "2026-04-05T10:00:00Z"
}
```

---

### 模式 2：CLAUDE.md 角色定義（推薦小到中型團隊）

加上「責任邊界」檔案，避免衝突。

**新增檔案：.claude-code/BOUNDARIES.md**
```markdown
# 工作邊界定義

## 禁區清單
- `config/` — 配置檔只有 Agent Admin 能改
- `package.json` — 只有 Agent Infra 能改
- `.env` — 禁止改，用 .env.example 溝通

## 工作日誌
所有 agent 改檔後必須記到 .claude-code/CHANGES.log：
```
Agent A | 2026-04-05 10:00 | src/auth.js | 新增 OAuth
Agent B | 2026-04-05 10:15 | tests/auth.test.js | 驗證通過
```

## 衝突解決
- 如果兩個 agent 同時改同一檔，保留時間戳較晚的版本
- 衝突詳情寫進 .claude-code/CONFLICTS.md
```

**三個 Agent 的分工範例：**

```
Agent Developer (開發)
├── src/ 全權
├── 新增功能
└── 定期更新 .claude-code/status.json

Agent QA (測試)
├── tests/ 全權
├── 驗證代碼品質
└── 如果有 bug 寫進 .claude-code/issues.md

Agent Reviewer (最高層級)
├── 審核 issues.md
├── 決定要不要打回給 Developer
└── 最終批准上線
```

---

### 模式 3：協作系統（進階，適合大型專案）

**元件：**

1. **review-queue/** — 待審清單
   ```
   review-queue/
   ├── 001-auth.md          # Developer 提交
   ├── 001-auth.approved    # Reviewer 批准
   ├── 002-payment.md       # 新的待審
   └── 002-payment.rejected # 打回
   ```

2. **日報機制** — 每日自動總結進度
   ```
   logs/
   ├── 2026-04-05.md        # 誰改了什麼
   ├── 2026-04-06.md
   └── ...
   ```

3. **Escalation** — 遇到困難的上報流程
   ```
   Agent A 卡住 → 寫進 .claude-code/blockers.md
   Agent Reviewer 看到 → 決定要不要換 Agent B 幫忙
   ```

**日報 CLAUDE.md 定義：**
```markdown
# Role: Daily Report Agent
## 每天 18:00 自動執行
1. 掃描 .claude-code/CHANGES.log
2. 掃描 review-queue/ 狀態
3. 生成 logs/YYYY-MM-DD.md：
   - Developer 完成了什麼
   - QA 驗證了什麼
   - Reviewer 批准了什麼
   - 有沒有 blocker
```

---

## 實戰範例：建一個簡單的雙 Agent 系統

### Step 1：建立目錄結構
```bash
mkdir -p project/{src,tests,.claude-code/{agents/{developer,reviewer},logs}}
cd project
```

### Step 2：建立全局 BOUNDARIES.md

**文件：project/.claude-code/BOUNDARIES.md**
```markdown
# Multi-Agent Boundaries

## 工作分區
- **Agent Developer** 控制：src/
- **Agent Reviewer** 控制：無代碼控制權，純審查

## 交接檔案
所有交接都通過 .claude-code/ 下的檔案：
- status.json — 當前進度
- issues.md — 發現的問題
- changes.log — 改動日誌

## 禁止事項
- Developer 改 tests/
- Developer 改 .env
- Reviewer 改 src/ 代碼（只能標記「needs revision」）
```

### Step 3：Agent Developer 的 CLAUDE.md

**文件：project/.claude-code/agents/developer/CLAUDE.md**
```markdown
# Agent: Developer

你是代碼開發人員。

## 職責
1. 實作功能（只改 src/）
2. 完成後寫進 status.json：`"status": "ready_for_review"`
3. 看到 status.json 標記 `"status": "needs_revision"` 就要改

## 禁區
- 不改 tests/
- 不改 .env
- 不改 docs/

## 交接
完成一個功能就：
```bash
# 更新 status.json
cat > ../.claude-code/status.json << 'EOF'
{
  "feature": "新增使用者認證",
  "status": "ready_for_review",
  "files_changed": ["src/auth.js", "src/utils/hash.js"],
  "timestamp": "2026-04-05T10:15:00Z"
}
EOF
```
```

### Step 4：Agent Reviewer 的 CLAUDE.md

**文件：project/.claude-code/agents/reviewer/CLAUDE.md**
```markdown
# Agent: Code Reviewer

你是代碼審查人員。

## 職責
1. 每天檢查 status.json，看有沒有新提交
2. 讀 Developer 改的檔案（根據 status.json 的 files_changed）
3. 審查代碼品質：
   - 有沒有邏輯錯誤
   - 有沒有安全漏洞
   - 有沒有命名規範問題
4. 批准或打回

## 批准流程
```bash
# 檢查無誤，標記通過
cat > ../.claude-code/status.json << 'EOF'
{
  "feature": "新增使用者認證",
  "status": "approved",
  "reviewed_by": "reviewer",
  "notes": "代碼品質高，已批准部署",
  "timestamp": "2026-04-05T11:00:00Z"
}
EOF
```

## 打回流程
```bash
# 發現問題，寫進 issues.md
cat > ../.claude-code/issues.md << 'EOF'
# Issues Found

## Issue #1: Missing error handling
- File: src/auth.js, line 42
- Problem: hash() 沒有 try-catch
- Fix: 加上例外處理

## Issue #2: SQL injection risk
- File: src/auth.js, line 18
- Problem: 直接拼 SQL query，應該用 parameterized query
EOF

# 更新 status
cat > ../.claude-code/status.json << 'EOF'
{
  "feature": "新增使用者認證",
  "status": "needs_revision",
  "reviewed_by": "reviewer",
  "notes": "見 issues.md，需修正 2 個問題",
  "timestamp": "2026-04-05T11:00:00Z"
}
EOF
```

## 驗收清單
- [ ] 代碼符合命名規範
- [ ] 有錯誤處理
- [ ] 沒有 SQL injection
- [ ] 測試涵蓋主要路徑
```

### Step 5：手動執行示例

**Scenario：Developer 完成功能**

終端 1 (Developer Session)：
```bash
cd project
# 寫完代碼
echo 'export default function authenticate() { ... }' > src/auth.js

# 通知 Reviewer
cat > .claude-code/status.json << 'EOF'
{"feature": "auth", "status": "ready_for_review", "timestamp": "2026-04-05T10:15:00Z"}
EOF

# 告訴 Claude Code
echo "✅ 完成 src/auth.js，等 Reviewer 審查"
```

**終端 2 (Reviewer Session)：**
```bash
cd project

# 讀取狀態
cat .claude-code/status.json
# {"feature": "auth", "status": "ready_for_review", ...}

# 讀開發者改的檔案
cat src/auth.js

# 審查…… (假設找到問題)

# 打回
cat > .claude-code/status.json << 'EOF'
{"feature": "auth", "status": "needs_revision", "reviewed_by": "reviewer", "timestamp": "2026-04-05T11:00:00Z"}
EOF

cat > .claude-code/issues.md << 'EOF'
# Issues Found

## Missing error handling in auth.js line 15
The hash() call needs try-catch
EOF

# 告訴 Claude Code
echo "❌ 發現問題，已回傳至 issues.md"
```

**回到終端 1：**
```bash
# 檢查反饋
cat .claude-code/status.json
cat .claude-code/issues.md

# 修改代碼
# ……

# 再次提交
cat > .claude-code/status.json << 'EOF'
{"feature": "auth", "status": "ready_for_review", "revision": 2, "timestamp": "2026-04-05T12:00:00Z"}
EOF
```

---

## 常見問題

### Q: Agent 之間怎麼溝通？
**A:** 通過檔案，不通過文字。
- Developer 改完 → 寫 status.json
- Reviewer 看到 → 讀相關檔案 → 寫 issues.md 或更新 status.json
- Developer 看到 → 改代碼 → 回傳

好處：
- 不需要打字溝通，節省 token
- 有歷史紀錄，可追蹤
- 自動化容易（定時檢查 status.json）

### Q: 怎麼避免兩個 agent 改同一個檔案？
**A:** 建立 BOUNDARIES.md，清楚寫出邊界。

如果還是衝突（很罕見）：
1. 用 git 查誰改的（`git log --oneline src/auth.js`）
2. 手動合併，或者
3. 保留時間戳較晚的版本

### Q: 需要寫程式嗎？
**A:** 不需要。上面的例子都用 bash + JSON，不需要額外代碼。

進階才需要程式（例如：自動監視 status.json，啟動對應的 agent）。

### Q: 可以支援 3 個以上的 agent 嗎？
**A:** 可以。只要有清楚的邊界定義。例如：
```
Developer → Tester → Reviewer → DevOps (部署)
```

每個 agent 都有一個 CLAUDE.md，定義「我看什麼，我改什麼，我完成後寫什麼」。

### Q: status.json 誰負責管理？
**A:** 每個 agent 只改自己相關的欄位。例如：
```json
{
  "feature": "auth",
  "status": "ready_for_review",        ← Developer 設定
  "reviewed_by": "reviewer",            ← Reviewer 設定
  "notes": "code quality good",         ← Reviewer 設定
  "test_status": "all_pass",            ← Tester 設定
  "timestamp": "2026-04-05T11:00:00Z"
}
```

### Q: 什麼時候用模式 1，什麼時候用模式 2？
- **模式 1（手動分工）**：小專案，2 個 agent，控制簡單
- **模式 2（角色定義）**：3-5 個 agent，需要清楚的職責邊界
- **模式 3（協作系統）**：大專案，需要日報、escalation、自動化

---

## 實作檢查清單

建立一個雙 agent 系統時，確保：

- [ ] 建立 .claude-code/BOUNDARIES.md，列出誰改什麼
- [ ] 每個 agent 有自己的 CLAUDE.md（在子目錄裡）
- [ ] 建立 .claude-code/status.json，格式清楚
- [ ] 定義交接的檔案名稱（不要隨意亂起名）
- [ ] 試跑 2-3 個迴圈，確保流程順暢
- [ ] 如果卡住，先檢查 BOUNDARIES.md 有沒有清楚說明

---

## 範本檔案清單

複製以下到你的專案：

1. **BOUNDARIES.md** — 工作邊界
2. **.claude-code/agents/developer/CLAUDE.md** — Dev agent 指示
3. **.claude-code/agents/reviewer/CLAUDE.md** — Review agent 指示
4. **.claude-code/status.json** — 當前狀態（初始值：`{"status": "idle"}`)

開始時可以手動更新 status.json，之後習慣了再考慮自動化。
