# AI Lead Auto-Responder: 不漏接任何潛在客戶

**Gmail 收到客戶詢問 → AI 智能分析意圖 → 自動起草專業回覆 → Slack/Telegram 實時通知。永遠不會漏掉任何機會。**

## 功能
- ✅ 每 5 分鐘檢查新郵件
- ✅ Claude AI 分析客戶意圖（銷售、支援、合作、垃圾）
- ✅ 自動起草專業英文回覆
- ✅ Slack + Telegram 實時通知
- ✅ Gmail 自動存草稿（可人工審閱再發送）
- ✅ 記錄所有客戶詢問到數據庫
- ✅ 完整錯誤處理

## 定價
**$39** | 轉換率提升 40%，再不漏單

---

## 安裝步驟

### 1. 匯入 Workflow
- 在 n8n 中點 **Create** → **Import from file**
- 選擇 `2-lead-responder.json`
- 點 **Import**

### 2. 設定環境變數
在 n8n 的 **Settings** → **Environment variables** 中新增：

```
ANTHROPIC_API_KEY=sk-ant-xxxxx           # 從 https://console.anthropic.com 取得
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN        # Telegram Bot token
TELEGRAM_CHAT_ID=YOUR_CHAT_ID            # 你的 Telegram 用戶 ID
```

### 3. 連接 Gmail
編輯 **Gmail Trigger** 節點：
- 點選 **Authenticate** 用你的 Gmail 帳號授權
- 確認 n8n 可以讀取未讀郵件
- 保持預設設定（檢查 INBOX，每 5 分鐘）

### 4. 設定 Slack 通知（可選）
編輯 **Slack Alert** 節點：
- 在 Slack Workspace 建立 Incoming Webhook：https://api.slack.com/messaging/webhooks
- 將 Webhook URL 貼到節點中
- 刪除此節點如果你只用 Telegram

### 5. 設定 Telegram 通知
編輯 **Telegram Notification** 節點：
- 確認 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 已設定
- 在 Telegram 中找到你的用戶 ID：與 @userinfobot 對話

### 6. 設定數據庫日誌（可選）
編輯 **Database Log** 節點：
- 如果你有 Google Sheets/Airtable，改成對應的 API URL
- 或保持原樣（需要你自己提供一個 webhook endpoint）

### 7. 測試
1. 傳送一封測試郵件到你的 Gmail
2. 檢查 Gmail 草稿是否被建立
3. 看 Slack/Telegram 是否收到通知

---

## 工作流程圖

```
Gmail Trigger (每 5 分鐘檢查)
    ↓
Claude Intent Analyzer (分析客戶意圖+起草回覆)
    ↓
Gmail Draft Creator (自動建立草稿)
    ├→ Slack Alert (通知團隊)
    ├→ Telegram Notification (個人通知)
    ├→ Database Log (記錄)
    └→ Error Handler (出錯通知)
```

---

## 自訂選項

### 改變檢查間隔
編輯 **Gmail Trigger** 節點：
- `minute: 5` → `minute: 1` = 每分鐘檢查
- `minute: 5` → `minute: 30` = 每 30 分鐘檢查

### 改變回覆語言
編輯 **Claude Intent Analyzer** 節點的 `system` 參數：
```json
"system": "You are a professional sales assistant. Respond in Traditional Chinese. Keep responses concise and friendly."
```

### 只回覆特定主題的郵件
編輯 **Gmail Trigger** 的 `searchQuery`：
- 只回覆銷售相關：`searchQuery: "subject:(inquiry OR question OR interested)"`
- 排除垃圾：`searchQuery: "is:unread -from:noreply* -from:no-reply*"`

### 加入自訂回覆規則
在 **Claude Intent Analyzer** 後面加一個 **IF** 節點：
```
IF: content contains "demo" 
→ 附上 demo 連結
ELSE:
→ 正常回覆
```

### 自動發送而非存草稿
編輯 **Gmail Draft Creator** 改成：
```
operation: "send"
（而非 "draft"）
```
⚠️ 謹慎使用，建議先用草稿審閱！

### 連接 HubSpot/Salesforce
在 **Slack Alert** 後加新節點：
- Type: HubSpot API
- 建立新 contact：姓名 = sender，notes = 郵件內容

---

## 常見問題

**Q: 為什麼有些郵件沒有觸發？**
- 檢查 Gmail 帳號是否允許第三方應用存取
- 確保郵件不在 SPAM 資料夾
- 檢查 n8n 的 Execution log

**Q: 可以改成只回覆某些人嗎？**
- 編輯 Gmail Trigger 的 searchQuery，加上 `from:important@*`

**Q: 回覆內容有時候不好，怎麼改進？**
- 編輯 Claude Intent Analyzer 的 `system` prompt
- 加入你公司的品牌語調說明
- 例如：「...responses should reflect our friendly but professional tone, emphasizing quick support and value delivery.」

**Q: 可以把回覆儲存到數據庫嗎？**
- 是的！編輯 **Database Log** 節點，改成你的 API endpoint
- 或用 n8n 內建的 Airtable/Google Sheets 節點

**Q: Telegram 通知沒收到？**
- 確認 TELEGRAM_BOT_TOKEN 正確（不是 username）
- 確認你的 TELEGRAM_CHAT_ID 正確（用 @userinfobot 查詢）
- 確認 bot 有傳訊息給你的權限

---

## 進階用法

### 多語言回覆
加入條件節點區分郵件語言，對應不同的 Claude 提示詞：
```
IF: 郵件是英文 → 英文回覆
ELSE IF: 郵件是中文 → 繁體中文回覆
ELSE: → 自動偵測語言
```

### 自動標籤和分類
在 **Gmail Draft Creator** 後加：
- 高價值客戶 → 加 label "VIP_LEADS"
- 垃圾詢問 → 加 label "SPAM_AUTO"

### A/B 測試回覆內容
建立兩個不同版本的 Claude Analyzer，隨機選擇：
```
Random 50/50 → Path A (Version 1) 或 Path B (Version 2)
→ 記錄回覆版本 → 追蹤轉換率
```

---

## 更新紀錄
- **v1.0** (2026-04-05): 首版上線，支援 Gmail + Claude + Slack + Telegram

## 支援
問題？Email: support@gumroad.com 或加入我們的 Discord：https://discord.gg/xxxxx

---

**Ready to automate your sales? Never miss a lead again.** 🚀
