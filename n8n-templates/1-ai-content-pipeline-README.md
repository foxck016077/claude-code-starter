# AI Content Pipeline: RSS → AI 摘要 → 社群發文

**自動監控 RSS feed、用 AI 改寫內容、自動發佈到 Twitter + Facebook。內容創作者的秘密武器。**

## 功能
- ✅ 每小時檢查 RSS feed 新文章
- ✅ 用 Claude AI 智能摘要（保留重點、加入行銷語氣）
- ✅ 自動發文到 Twitter 和 Facebook
- ✅ Slack 通知發布成功
- ✅ 完整錯誤處理

## 定價
**$29** | 節省 2 小時/天的內容發佈時間

---

## 安裝步驟

### 1. 匯入 Workflow
- 在 n8n 中點 **Create** → **Import from file**
- 選擇 `1-ai-content-pipeline.json`
- 點 **Import**

### 2. 設定環境變數
在 n8n 的 **Settings** → **Environment variables** 中新增：

```
ANTHROPIC_API_KEY=sk-ant-xxxxx              # 從 https://console.anthropic.com 取得
FACEBOOK_PAGE_TOKEN=YOUR_FACEBOOK_TOKEN     # Facebook Graph API token
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN           # （可選）用於錯誤通知
TELEGRAM_CHAT_ID=YOUR_CHAT_ID               # （可選）
```

### 3. 設定 RSS Feed URL
編輯 **RSS Feed Reader** 節點：
- 將 `YOUR_RSS_FEED_URL` 替換成你的 RSS feed
- 範例: `https://techcrunch.com/feed/` 或 `https://medium.com/feed/@yourprofile`

### 4. 連接 Twitter API
編輯 **Twitter Post** 節點：
- 點選 **Authenticate** 用你的 Twitter 帳號授權
- n8n 會自動儲存 OAuth token

### 5. 連接 Facebook Graph API
編輯 **Facebook Post** 節點：
- 將 `YOUR_FACEBOOK_GRAPH_API_ENDPOINT` 替換成：
  ```
  https://graph.facebook.com/v18.0/{page_id}/feed
  ```
- 用你的 Facebook 粉專 ID 替換 `{page_id}`
- 在 Facebook Developer Console 取得 **Page Access Token**

### 6. （可選）設定 Slack 通知
編輯 **Slack Notification** 節點：
- 在 Slack Workspace 建立 Incoming Webhook：https://api.slack.com/messaging/webhooks
- 將 URL 貼到 `YOUR/WEBHOOK/URL` 位置

### 7. 測試
點 **Test workflow** 看是否一切正常

---

## 工作流程圖

```
Schedule Trigger (每1小時)
    ↓
RSS Feed Reader (抓取最新文章)
    ↓
Claude Summarizer (用 AI 改寫+摘要)
    ├→ Twitter Post (發推文)
    ├→ Facebook Post (發臉書)
    ├→ Slack Notification (通知成功)
    └→ Error Handler (出錯通知)
```

---

## 自訂選項

### 改變檢查間隔
編輯 **Schedule Trigger** 節點，改 `hour: 1` 為：
- `hour: 2` = 每 2 小時
- `hour: 0, minute: 30` = 每 30 分鐘

### 改變 AI 提示詞
編輯 **Claude Summarizer** 節點的 `content` 參數：
```json
"content": "Summarize this for LinkedIn (professional tone, max 300 chars): {{description}}"
```

### 只發某個社群
刪除不需要的節點（如只發 Twitter）：
1. 右鍵點 **Facebook Post** 節點 → Delete
2. 重新連接 Twitter 節點到 Slack Notification

### 加入 LinkedIn/Medium
1. 複製 **Twitter Post** 節點
2. 改成 LinkedIn Post 或 Medium API call
3. 連接到主流程

---

## 常見問題

**Q: API Key 從哪裡取？**
- Anthropic: https://console.anthropic.com/account/keys
- Facebook: https://developers.facebook.com/apps → 你的 App → Settings → Basic
- Twitter: https://developer.twitter.com/en/portal/dashboard

**Q: 發文失敗怎麼辦？**
- 檢查 API key 是否正確
- 確認 Twitter/Facebook 帳號權限夠
- 看 n8n 的 Execution log 看錯誤訊息

**Q: 可以改成每天特定時間發嗎？**
- 編輯 Schedule Trigger，改成 `mode: "specificTime"` + `time: "09:00"`

**Q: 可以過濾某些 RSS 文章嗎？**
- 在 **RSS Feed Reader** 後面加一個 **IF** 節點，條件設定為 `title contains 'keyword'`

---

## 更新紀錄
- **v1.0** (2026-04-05): 首版上線，支援 RSS + Claude + Twitter + Facebook

## 支援
問題？Email: support@gumroad.com 或加入我們的 Discord：https://discord.gg/xxxxx

---

**Ready to automate? Hit the "Activate" button and watch the magic happen.** ✨
