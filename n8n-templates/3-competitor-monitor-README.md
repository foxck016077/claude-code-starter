# Competitor Monitor: 自動追蹤競品動態

**每天自動爬取競品網站 + Product Hunt + Twitter → AI 分析變化 → Slack/Email/Telegram 週報推送。永遠領先競爭對手。**

## 功能
- ✅ 每日自動監控競品網站更新
- ✅ 爬取 Product Hunt 產品數據
- ✅ 追蹤競品 Twitter 動態
- ✅ Claude AI 深度分析市場變化
- ✅ Slack + Email + Telegram 多渠道報告
- ✅ 自動儲存到 Airtable 作長期分析
- ✅ 識別威脅和機會

## 定價
**$49** | 競爭情報價值遠超 $49

---

## 安裝步驟

### 1. 匯入 Workflow
- 在 n8n 中點 **Create** → **Import from file**
- 選擇 `3-competitor-monitor.json`
- 點 **Import**

### 2. 設定環境變數
在 n8n 的 **Settings** → **Environment variables** 中新增：

```
ANTHROPIC_API_KEY=sk-ant-xxxxx                 # Claude API key
COMPETITOR_NAME=CompanyName                    # 競品公司名稱（用於搜尋）
COMPETITOR_WEBSITE_URL=https://example.com     # 競品官網 URL
COMPETITOR_TWITTER=@competitor_handle          # 競品 Twitter handle
PRODUCT_HUNT_API_TOKEN=xxxxx                   # Product Hunt API token
TWITTER_BEARER_TOKEN=xxxxx                     # Twitter API v2 Bearer token
TELEGRAM_BOT_TOKEN=xxxxx                       # Telegram Bot token
TELEGRAM_CHAT_ID=xxxxx                         # 你的 Telegram Chat ID
SENDER_EMAIL=your@email.com                    # 寄信人信箱（SendGrid）
RECIPIENT_EMAIL=boss@company.com               # 收信人信箱
AIRTABLE_WEBHOOK_URL=https://...              # Airtable Webhook URL（可選）
```

### 3. 取得 API Keys

#### 3.1 Claude API
- 訪問 https://console.anthropic.com/account/keys
- 建立新 API key
- 複製到 `ANTHROPIC_API_KEY`

#### 3.2 Product Hunt API
- 訪問 https://api.producthunt.com/v2/docs
- 認證取得 token
- 複製到 `PRODUCT_HUNT_API_TOKEN`

#### 3.3 Twitter API v2
- 訪問 https://developer.twitter.com/en/portal/dashboard
- 建立新應用並升級為 v2 API
- 取得 Bearer Token
- 複製到 `TWITTER_BEARER_TOKEN`

#### 3.4 SendGrid（Email）
- 在 n8n 中連接 SendGrid（**Add credentials**）
- 或手動取得 SendGrid API key：https://app.sendgrid.com/settings/api_keys
- 在 **Email Report** 節點填入

#### 3.5 Airtable（可選）
- 在 Airtable 建立新 Base（名為 `Competitor Analysis`）
- 建立新 Table（名為 `Reports`）
- 生成 Webhook URL：https://airtable.com/api/webhooks

### 4. 配置監控目標

編輯 **Daily_Schedule** 節點：
- 改變執行時間（預設 09:00）
- 範例：改成 `08:30` = 每天早上 8:30 執行

編輯環境變數以監控不同競品：
```
COMPETITOR_NAME=Notion          # 監控 Notion
COMPETITOR_WEBSITE_URL=https://notion.so
COMPETITOR_TWITTER=@NotionHQ
```

### 5. 連接通知渠道

#### 5.1 Slack（可選）
編輯 **Slack Report** 節點：
- 在 Slack Workspace 建立 Incoming Webhook：https://api.slack.com/messaging/webhooks
- 貼上 Webhook URL 到 `https://hooks.slack.com/services/YOUR/WEBHOOK/URL`

#### 5.2 Telegram
編輯 **Telegram Report** 節點：
- 確認 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 已設定
- 與 @userinfobot 對話確認你的 Chat ID

#### 5.3 Email
編輯 **Email Report** 節點：
- 使用 SendGrid 或其他 SMTP 服務
- 設定送信者和收信者地址

### 6. 測試
1. 手動觸發 workflow（點 **Test workflow**）
2. 檢查 Slack/Email/Telegram 是否收到報告
3. 檢查 Airtable 是否有新紀錄

---

## 工作流程圖

```
Daily Schedule (每天 09:00)
    ├→ Fetch Competitor Website (抓網站)
    ├→ Fetch ProductHunt Data (抓 PH 數據)
    └→ Fetch Twitter Data (抓 Twitter)
           ↓
    Claude Analysis (AI 深度分析)
           ├→ Slack Report
           ├→ Telegram Report
           ├→ Email Report
           └→ Store Analysis (存到 Airtable)
```

---

## 自訂選項

### 監控多個競品
複製整個 workflow 並改變 `COMPETITOR_NAME`：
- Workflow 1: 監控 Notion
- Workflow 2: 監控 Figma
- Workflow 3: 監控 Slack

### 改變檢查頻率
編輯 **Daily Schedule** 節點：
- 每小時：`mode: "everyX", hour: 1`
- 每週一次：`mode: "everyX", dayOfWeek: "1"` + `hour: 9`

### 自訂分析焦點
編輯 **Claude Analysis** 節點的 `system` prompt：
```json
"system": "Focus only on: 1) Pricing changes 2) New feature announcements 3) Customer reviews on Product Hunt. Ignore marketing content."
```

### 只監控特定 Twitter 主題
編輯 **Fetch Twitter Data** 的搜尋參數：
```
query={{encodeURIComponent($env["COMPETITOR_TWITTER"] + " (pricing OR feature OR launch)")}}
```

### 加入 GitHub 監控
在 **Daily_Schedule** 後加新節點：
- Type: GitHub API
- 監控競品 repos 的 releases/commits
- 整合到 Claude Analysis

### 長期趨勢分析
連接到 Google Sheets 做月度/季度對比：
1. 在 **Store Analysis** 後加 Google Sheets 節點
2. 每月執行 SQL 查詢：`SELECT * FROM reports WHERE date > DATE_SUB(NOW(), INTERVAL 30 DAY)`
3. 產生趨勢圖表

---

## 常見問題

**Q: Website 抓取失敗怎麼辦？**
- 檢查網址是否有防火牆/robots.txt 限制
- 改用 Jina Reader：`https://r.jina.ai/{{url}}`（自動繞過反爬蟲）
- 檢查 HTTP status code

**Q: Twitter API 配額用完怎麼辦？**
- Twitter API v2 有免費配額限制（450 requests/15min）
- 改成每天只執行一次而非每小時
- 或升級到 Pro plan

**Q: 能監控多個競品嗎？**
- 是的！在環境變數建立陣列：
```
COMPETITORS=["Notion", "Figma", "Slack"]
```
- 在 workflow 加入 Loop 節點遍歷每個競品

**Q: 分析內容不準確？**
- 調整 Claude prompt，加入更具體的分析框架
- 例如：「以 Porter's Five Forces 分析...」
- 或限制字數：`max_tokens: 1500`

**Q: 能加入客戶評論監控嗎？**
- 可以！加新節點監控：
  - Trustpilot 評論
  - Google Reviews
  - AppStore 評論

**Q: 老闆想看可視化報表怎麼辦？**
- 連接 Data Studio/Looker：自動產生儀表板
- 或用 Slack Block 做圖表

---

## 進階用法

### 自動生成競爭對手分析報告
加入 Google Docs 節點，每週自動生成完整報告：
```
1. 競品動態摘要
2. 市場風險評估
3. 推薦行動清單
4. KPI 對比圖表
```

### 威脅預警系統
加入條件節點，當偵測到重大變化時（如降價、大更新）：
```
IF: Analysis contains "price drop" OR "major feature"
→ 立即推送 Critical Alert
→ Slack + SMS + 郵件通知 CEO
```

### 自動競爭對標
連接你自己的 analytics，自動對比：
- 我們 vs 競品：功能數、定價、用戶評論
- 生成對標報告

### 市場時序分析
用 Claude 做時序分析：
```
"Analyze competitor activity patterns: which days are most active? 
When do they announce features? Any seasonal patterns?"
```

### 自動生成行動計劃
加入最後一個 Claude 節點：
```
"Based on this competitive threat, recommend 3 action items
we should take in the next 30 days. Be specific and prioritized."
```

---

## 更新紀錄
- **v1.0** (2026-04-05): 首版上線，支援網站 + Product Hunt + Twitter + Airtable 儲存

## 支援
問題？Email: support@gumroad.com 或加入我們的 Discord：https://discord.gg/xxxxx

---

**Ready to stay ahead of competition? Set it and forget it.** 🎯
