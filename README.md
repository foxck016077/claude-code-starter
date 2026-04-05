# Claude Code Starter Kit

**Claude Code 上手太難？這個包幫你 5 分鐘搞定。**

---

## 這是什麼？

Claude Code 很強，但文檔分散、上手曲線陡。這個 starter kit 包含：

1. **快速入門指南** — 0 到 1，沒有廢話
2. **Multi-Agent 協作系統** — 怎麼讓 2 個以上的 AI agent 協作不打架
3. **安全 Hooks** — 自動檢查，防止危險操作
4. **CLAUDE.md 範本** — 複製貼上就能用

---

## 包含什麼

```
claude-code-starter/
├── guides/
│   ├── getting-started.md      # 快速上手（5 分鐘）
│   └── multi-agent.md          # 多 agent 協作指南（完整）
├── hooks/
│   ├── safety/
│   │   ├── no-auto-push.sh     # 防止自動 git push
│   │   ├── protect-env-files.sh # 防止改 .env
│   │   └── prevent-dangerous-commands.sh  # 黑名單指令
│   └── quality/
│       └── read-before-edit.sh # 編輯前先讀檔案
├── guides/
│   ├── getting-started.md      # 5 分鐘快速入門
│   └── multi-agent.md          # Multi-Agent 實戰指南
├── gumroad/
│   └── listing.md              # Gumroad 上架文案
└── README.md                   # 這個檔案
```

---

## 快速開始（3 步）

### 1. 產生你的 CLAUDE.md

```bash
cd claude-code-starter/generator
python3 generate_claude_md.py --preset=bot    # Bot 開發者
python3 generate_claude_md.py --preset=web    # Web 開發者
python3 generate_claude_md.py --preset=scraper # 爬蟲開發者
python3 generate_claude_md.py                 # 互動問答（自訂）
```

把產生的 `CLAUDE.md` 放到你的專案根目錄。

### 2. 安裝 Hooks

```bash
cd claude-code-starter/hooks
python3 install.py --all       # 全裝（安全+品質+效率）
python3 install.py --safety    # 只裝安全防護
```

### 3. 開始用 Claude Code

Hooks 即時生效，CLAUDE.md 下次 session 自動載入。

---

## 常見場景

### 場景 1：我是初學者，不知道怎麼用 Claude Code

讀這個：[guides/getting-started.md](./guides/getting-started.md)

5 分鐘學會基本操作。

### 場景 2：我想用 2 個 AI agent，但不想他們互相衝突

讀這個：[guides/multi-agent.md](./guides/multi-agent.md)

涵蓋：
- 怎麼定義 agent 的職責
- 怎麼避免檔案衝突
- 完整的實作例子（copy-paste ready）

### 場景 3：我想加安全檢查（防止 git push、改 .env 等）

啟用 hooks：

編輯 `~/.claude-code/settings.json`，加入：

```json
{
  "hooks": {
    "before-command": "bash ~/.claude-code/hooks/safety/prevent-dangerous-commands.sh",
    "before-file-edit": "bash ~/.claude-code/hooks/quality/read-before-edit.sh"
  }
}
```

### 場景 4：我有一個複雜的專案，想定制 CLAUDE.md

複製 `templates/CLAUDE.md.project` 到你的專案根目錄：

```bash
cp templates/CLAUDE.md.project ~/my-project/CLAUDE.md
```

然後改成符合你的專案。

---

## 特色

✅ **零依賴** — 純 bash + Markdown，不需要額外工具

✅ **實戰導向** — 每個指南都有可直接複製的例子

✅ **多語言** — 繁體中文 + 英文註解

✅ **開箱即用** — Hooks、範本都準備好，copy-paste 就行

✅ **進階支援** — 從單個 agent 到 5+ agent 協作系統都有方案

---

## 核心指南

### [快速入門](./guides/getting-started.md)（5 分鐘）

- 安裝 Claude Code
- 建第一個 CLAUDE.md
- 跑第一個任務
- 常見問題 Q&A

**適合：** 完全新手

### [Multi-Agent 實戰指南](./guides/multi-agent.md)（20 分鐘）

- 「多開視窗」vs「真正的多 agent」的區別
- 三種協作模式（簡單→複雜）
- 完整的雙 agent 系統實作（copy-paste ready）
- 常見問題 + 解決方案

**適合：** 想 scale up，或想讓多個 agent 協作

---

## 範本檔案

### CLAUDE.md 全局版（推薦用這個開始）

```bash
cp templates/CLAUDE.md.global ~/.claude/CLAUDE.md
```

包含：
- 身份設定
- 核心規則（只做被要求的、改前報告、小測試先行）
- 工作優先序
- Session 結束檢查清單

### CLAUDE.md 專案版（針對單一專案的細節）

```bash
cp templates/CLAUDE.md.project ~/my-project/CLAUDE.md
```

包含：
- 專案描述
- 技術棧
- 工作邊界（你改什麼，不改什麼）
- 成功標準

---

## Hooks（自動化工具）

### 什麼是 Hook？

Hook 是自動檢查，在 Claude Code 執行特定操作前跑。

例如：`before-git-push` hook 會在 push 前檢查「你真的想要推嗎？」

### 可用的 Hooks

#### Safety（安全）
- `no-auto-push.sh` — 禁止自動 `git push`（要手動確認）
- `protect-env-files.sh` — 禁止改 `.env` 檔（防止洩密）
- `prevent-dangerous-commands.sh` — 黑名單指令（自訂）

#### Quality（品質）
- `read-before-edit.sh` — 改檔案前必須先讀一次

### 怎麼啟用？

編輯 `~/.claude-code/settings.json`：

```json
{
  "hooks": {
    "before-git-push": "bash ~/.claude-code/hooks/safety/no-auto-push.sh",
    "before-file-edit": "bash ~/.claude-code/hooks/quality/read-before-edit.sh",
    "before-command": "bash ~/.claude-code/hooks/safety/prevent-dangerous-commands.sh"
  }
}
```

### 怎麼寫自己的 Hook？

Hook 就是 bash 腳本。格式：

```bash
#!/bin/bash
# my-hook.sh

COMMAND="$1"

# 檢查什麼
if [[ "$COMMAND" == "dangerous" ]]; then
    echo "❌ 危險操作被阻止" >&2
    exit 2  # 這會中斷操作
fi

exit 0  # 通過
```

---

## 例子

### 例子 1：簡單的單 Agent 設定

```bash
cd my-project
cp ../claude-code-starter/templates/CLAUDE.md.project ./CLAUDE.md
```

編輯 CLAUDE.md，定義你的工作。

跑：
```bash
claude "實作新登入頁面"
```

### 例子 2：雙 Agent 協作（完整設定）

見 `examples/multi-agent-setup/`

```bash
cp -r examples/multi-agent-setup ~/my-project
cd ~/my-project
```

包含：
- 完整的目錄結構
- Developer 的 CLAUDE.md
- Reviewer 的 CLAUDE.md
- BOUNDARIES.md（清楚定義邊界）
- status.json（狀態機制）

可以直接開始用。

---

## 常見問題

### Q: CLAUDE.md 是什麼？為什麼我需要？

**A:** CLAUDE.md 是你給 AI agent 的「工作指示書」。

沒有 CLAUDE.md，Claude Code 每次都要問你「我該怎麼做」。

有 CLAUDE.md，Claude Code 看到你的規則後，自己決定怎麼做（而不是問你）。

### Q: Hooks 會拖慢效率嗎？

**A:** 不會。Hook 執行時間 < 100ms，基本感覺不到。

而且 hook 往往幫你省更多時間（防止推錯代碼、改錯配置）。

### Q: 我可以只用指南，不用 Hooks 嗎？

**A:** 可以。指南和 Hooks 獨立。

- 想快速上手 → 讀指南
- 想加安全檢查 → 用 Hooks
- 兩個都要 → 都用

### Q: 多 agent 需要寫程式嗎？

**A:** 不需要。上面的例子都用 JSON + Markdown 檔案，完全手工操作。

進階才需要寫程式（例如：自動監視檔案變化，自動啟動對應的 agent）。

### Q: 我想改 Hook 的邏輯，怎麼做？

**A:** Hook 就是 bash 腳本，可以任意修改。

例如，如果你想禁止 `rm -rf` 指令：

```bash
# hooks/safety/prevent-dangerous-commands.sh

if echo "$COMMAND" | grep -E "rm -rf" &>/dev/null; then
    echo "❌ 禁止 rm -rf" >&2
    exit 2
fi
```

### Q: 這些工具是免費的嗎？

**A:** 是的。這個 starter kit 是開源的，MIT 授權。

Claude Code 本身需要 Claude API 訂閱（或 Anthropic 的其他方案）。

---

## 後續步驟

- [ ] 讀 [快速入門指南](./guides/getting-started.md)
- [ ] 建立自己的 CLAUDE.md
- [ ] 安裝 Hooks
- [ ] 跑第一個任務
- [ ] 如果有多個 agent，讀 [Multi-Agent 指南](./guides/multi-agent.md)

---

## 授權

MIT License

可自由使用、修改、分發。

---

## 貢獻

有想法？找到 bug？

1. Fork this repo
2. 開 issue 或 PR
3. 我會審查並合併

---

## 延伸資源

- [Claude Code 官方文檔](https://claudecode.dev/docs)
- [Claude API 文檔](https://www.anthropic.com/docs)
- [Bash scripting 指南](https://www.gnu.org/software/bash/manual/)

---

**最後更新：** 2026-04-05

**版本：** 1.0.0

**維護者：** Claude Code 社群
