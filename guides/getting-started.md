# 快速入門：5 分鐘上手 Claude Code

> 從零到一，沒有廢話。

---

## Step 1: 檢查你有沒有 Claude Code

在終端執行：
```bash
which claude
```

如果看到路徑（例如 `/opt/homebrew/bin/claude`），說明已裝好。

**如果沒有：** 去 [claudecode.dev](https://claudecode.dev) 下載並安裝。（Mac/Linux/Windows 都有）

---

## Step 2: 初始化你的專案

進入你的專案目錄，執行一次 Claude Code：
```bash
cd ~/my-awesome-project
claude "初始化這個專案"
```

這會自動建立 `.claude-code/` 目錄。

---

## Step 3: 建立自己的 CLAUDE.md

你可以建立一個 CLAUDE.md 檔，告訴 Claude Code「你是誰」和「你該怎麼做」。

最簡單的範本：

**檔案：~/.claude/CLAUDE.md**（全局，所有專案用同一個）

```markdown
# My AI Assistant

## 身份
我叫 Hope，你的 AI 團隊成員。

## 核心規則
1. **只做被要求的事** — 做 A 就只做 A，想改別的先回報
2. **改前先說清楚** — 說「改什麼」「為什麼」「影響什麼」，等確認再動手
3. **小測試先行** — 批量改之前跑 2-3 筆，確認無誤
4. **做壞就還原** — 出問題就 git revert，不疊補丁

## 工作優先序
1. 修 Bug（交易、安全相關優先）
2. 新增功能（有驗證計畫的先做）
3. 優化代碼
4. 寫文件

## Session 結束檢查清單
- [ ] 改動已 commit（含 message）
- [ ] 測試全通過
- [ ] 更新 ~/.claude/session-handoff.md
```

或者每個專案有自己的 CLAUDE.md：

**檔案：~/my-awesome-project/CLAUDE.md**

```markdown
# Project: My Awesome Project

## 當前狀態
- 架構：Node.js + Express + PostgreSQL
- 上線時間：2026-04-05
- 主要功能：用戶認證、支付

## 我的工作
你是後端開發者。
1. 寫新 API（放在 src/routes/）
2. 寫測試（放在 tests/）
3. 改 bug（根據 issue tracker）

## 禁區
- 不改前端代碼（src/client/）
- 不改部署配置（除非特別要求）
- 不改 .env（只能改 .env.example）

## 成功標準
- 代碼通過 npm test
- API 文檔已更新
- 性能測試不下滑
```

---

## Step 4：安裝 Hooks（可選但推薦）

Hooks 是自動化工具，可以幫你檢查代碼、防止危險操作。

複製 `hooks/` 目錄到你的專案：
```bash
cp -r ~/claude-code-starter/hooks ~/.claude-code/hooks
```

然後在 `~/.claude-code/settings.json` 加入：
```json
{
  "hooks": {
    "before-git-push": "bash ~/.claude-code/hooks/safety/no-auto-push.sh",
    "before-file-edit": "bash ~/.claude-code/hooks/quality/read-before-edit.sh"
  }
}
```

（如果沒有 settings.json，先建立）

**Hooks 的作用：**
- 禁止自動 `git push`（要手動確認）
- 改檔案前自動讀一次（確保你知道改什麼）
- 禁止改 `.env` 檔（防止洩密）

---

## Step 5：開始使用

### 基本用法：提出任務
```bash
claude "修改登入流程，用 OAuth 替代密碼"
```

Claude Code 會：
1. 問你細節（需要改哪些檔？怎麼驗證？）
2. 讀相關檔案，理解現在狀況
3. 提議改動計畫
4. 等你確認後開始改
5. 改完跑測試
6. 報告結果

### 多個任務：用 review queue

如果有好幾個任務，建立 `review-queue/` 目錄：
```bash
mkdir -p .claude-code/review-queue
```

然後用 Markdown 列待做項目：

**檔案：.claude-code/review-queue/2026-04-05.md**
```markdown
# Tasks for 2026-04-05

## 優先
- [ ] 修 #142: 支付 API 回傳 500 錯誤
- [ ] 修 #139: 登入頁面 CSS 破掉

## 普通
- [ ] 新增匯率查詢 API
- [ ] 優化資料庫查詢

## 低優先
- [ ] 重構 utils/string.js
```

跟 Claude Code 說：
```bash
claude "檢查 review-queue/ 有什麼待做，優先做 priority 區"
```

---

## 常見提問

### Q: 我怎麼知道 Claude Code 有沒有改好？
**A:** 看終端輸出。Claude Code 完成後會說：
```
✅ 完成！
改檔：src/auth.js, tests/auth.test.js
測試：npm test 全通過
```

以及 git log 會有新 commit。

### Q: 如果改壞了怎麼辦？
**A:** 很簡單：
```bash
git revert HEAD
```

或回到上一個可用版本：
```bash
git checkout src/auth.js
```

### Q: 每次都要建 CLAUDE.md 嗎？
**A:** 不一定。CLAUDE.md 的目的是「幫 AI 更好理解你的需求」，如果你覺得溝通很順暢，可以不要。

但如果發現 Claude Code 老是做錯方向，就加一個 CLAUDE.md 試試。

### Q: 能多個 Claude Code session 同時進行嗎？
**A:** 可以，但要小心衝突。建議用 BOUNDARIES.md（見 multi-agent 指南）清楚定義「誰改什麼」。

### Q: Settings.json 有哪些選項？
**A:** 見 Claude Code 官方文檔。常用的：
```json
{
  "editor": "code",              // 用什麼編輯器打開檔案
  "gitCommitTemplate": "{task}", // commit message 模板
  "maxContextTokens": 100000,    // token 預算
  "hooks": { ... }               // 自動化 hook
}
```

---

## 檢查清單

啟動新專案時，確保：
- [ ] 有 README.md（描述這個專案在幹什麼）
- [ ] 有 .gitignore（該忽略的都忽略）
- [ ] 有測試（npm test / pytest / unittest）
- [ ] 考慮加 CLAUDE.md（如果想要更好的結果）
- [ ] 試過基本命令（claude "簡單任務"）

---

## 下一步

- 多 agent 協作？ → 讀 [multi-agent.md](./multi-agent.md)
- 設定 Hooks？ → 見 hooks/ 目錄
- 想自動化？ → 考慮用 settings.json 的 `cron` 或 `schedule`

---

## 快速參考

| 任務 | 指令 |
|------|------|
| 啟動 Claude Code | `claude` |
| 給任務 | `claude "描述任務"` |
| 檢查 git 狀態 | `git status` |
| 看最近改動 | `git log --oneline -5` |
| 還原上次改動 | `git revert HEAD` |
| 跑測試 | `npm test` 或 `pytest` |

有問題？看 Claude Code 的幫助：
```bash
claude --help
```
