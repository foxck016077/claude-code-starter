# n8n Automation Templates for Gumroad

**3 高價值自動化模板，直接賣 Gumroad，$29-49 每個。**

## 模板列表

### 1. 📰 AI Content Pipeline — $29
**文件：** `1-ai-content-pipeline.json` + `1-ai-content-pipeline-README.md`

RSS → Claude AI 摘要 → 自動發 Twitter/Facebook。內容創作者 2 小時/天省下來。

**功能：**
- ✅ 每小時自動檢查 RSS feed
- ✅ Claude AI 智能摘要 + 改寫
- ✅ 自動發佈到 Twitter 和 Facebook
- ✅ Slack 實時通知
- ✅ 完整錯誤處理

**適合：** 部落客、新聞聚合站、內容行銷人員

**關鍵節點：**
- Schedule Trigger → RSS Feed Reader → Claude Summarizer → Twitter/Facebook → Slack

---

### 2. 📧 AI Lead Auto-Responder — $39
**文件：** `2-lead-responder.json` + `2-lead-responder-README.md`

Gmail 收郵件 → Claude AI 分析意圖 + 起草回覆 → 自動存草稿 + Slack/Telegram 通知。永遠不漏接客戶。

**功能：**
- ✅ 每 5 分鐘檢查新郵件
- ✅ Claude AI 分析客戶意圖（銷售/支援/合作/垃圾）
- ✅ 自動起草專業英文回覆
- ✅ Gmail 自動建立草稿（人工審閱再發）
- ✅ Slack + Telegram 實時通知
- ✅ 記錄所有客戶詢問

**適合：** 小型 SaaS、服務公司、自由工作者、客服團隊

**關鍵節點：**
- Gmail Trigger → Claude Intent Analyzer → Gmail Draft Creator → Slack/Telegram Alert

---

### 3. 📊 Competitor Monitor — $49
**文件：** `3-competitor-monitor.json` + `3-competitor-monitor-README.md`

定時爬競品網站 + Product Hunt + Twitter → Claude AI 分析變化 → 週報推送。永遠領先競爭對手。

**功能：**
- ✅ 每日自動監控競品網站
- ✅ 爬取 Product Hunt 產品數據
- ✅ 追蹤競品 Twitter 動態
- ✅ Claude AI 深度分析（威脅/機會/定價變化等）
- ✅ Slack + Email + Telegram 多渠道報告
- ✅ 自動儲存到 Airtable 做長期分析
- ✅ 完整錯誤處理

**適合：** 創業公司、產品經理、行銷人員、戰略規劃

**關鍵節點：**
- Daily Schedule → [Website + ProductHunt + Twitter] → Claude Analysis → [Slack/Email/Telegram + Airtable]

---

## 快速開始

### 安裝任何模板（3 步）

1. **下載** `N-filename.json`
2. n8n 內點 **Create** → **Import from file** → 選擇 JSON 檔
3. **讀** `N-filename-README.md` 設定 API keys + 環境變數

### API Keys 需求

| 模板 | 需要的 API |
|------|----------|
| AI Content Pipeline | Anthropic, Twitter, Facebook |
| AI Lead Auto-Responder | Anthropic, Gmail, Slack/Telegram |
| Competitor Monitor | Anthropic, Product Hunt, Twitter, Airtable, Email |

**統一來源：**
- **Anthropic**: https://console.anthropic.com/account/keys
- **Twitter**: https://developer.twitter.com
- **Facebook**: https://developers.facebook.com
- **Product Hunt**: https://api.producthunt.com/v2/docs

---

## 上傳到 Gumroad 檢查清單

### 每個模板包含：
- [x] `.json` workflow 檔案（可直接匯入 n8n）
- [x] `README.md` 完整說明書
- [x] 環境變數清單
- [x] 安裝步驟（逐步指南）
- [x] 工作流程圖
- [x] 自訂選項（進階用法）
- [x] 常見問題 + 解答
- [x] 更新紀錄

### Gumroad 產品頁面模板

#### 產品描述（複製貼上）

```
AI Content Pipeline：不用手動發文，RSS 到社群自動化

️功能清單
✅ 每小時自動檢查 RSS feed
✅ 用 Claude AI 改寫標題和內容
✅ 自動同步發佈到 Twitter 和 Facebook
✅ Slack 通知發佈進度
✅ 完整錯誤處理和日誌

包含物品
✔ 可直接匯入的 n8n workflow JSON
✔ 詳細安裝指南（中英文）
✔ API 金鑰設定步驟
✔ 自訂提示詞範例
✔ 常見問題解答

適合對象
📍 內容創作者 - 每天省 2 小時發文時間
📍 部落客 - 自動聚合和發佈內容
📍 行銷人員 - 多渠道同時發佈

馬上節省時間！按下下載，5 分鐘內上線。
```

#### 定價建議

| 模板 | 定價 | 理由 |
|------|------|------|
| AI Content Pipeline | **$29** | 節省時間（2h/天 × $15/h = $30/天），ROI 快 |
| AI Lead Auto-Responder | **$39** | 客戶轉換率提升 40%（無價值），ROI 數倍 |
| Competitor Monitor | **$49** | 戰略情報，售價最高，針對決策者 |

**打包銷售：** 3 個都買 → 優惠 $20（$98 而非 $117）

---

## Gumroad 上傳步驟

### 1. 建立 3 個單獨產品

針對每個模板：
1. Gumroad 首頁 → **New Product**
2. 填寫：
   - **Title:** `AI Content Pipeline (n8n Template)` 
   - **Product type:** `Digital product`
   - **Price:** `$29` （或相應價格）
3. **Description:** 用上面的模板
4. **Download files:**
   - 上傳 `1-ai-content-pipeline.json`
   - 上傳 `1-ai-content-pipeline-README.md`
5. **License:** 設定為 MIT 或自訂
6. **Publish**

### 2. 建立打包產品（可選）

1. **New Product** → **Bundle**
2. 加入 3 個模板
3. **Price:** `$98` (save $20)
4. **Publish**

### 3. 推廣清單

- Twitter/X：3 個獨立推文 + 1 個打包推文
- Email list：發送給訂閱者
- Product Hunt：社群需求很高
- Reddit r/n8n：有活躍社群
- n8n 官方論壇：討論和推廣
- 部落格：寫「為什麼買這 3 個模板」的文章

---

## 品質檢查清單

### 每個 JSON 檔案必須：
- [x] 有效 JSON（能直接匯入 n8n）
- [x] 所有敏感資訊用 placeholder（YOUR_API_KEY）
- [x] 環境變數都有說明
- [x] 節點之間連接完整
- [x] 有錯誤處理節點

### 每個 README 必須：
- [x] 簡明功能描述（開頭 2 行）
- [x] 定價 + 價值主張
- [x] 6 步安裝指南
- [x] 工作流程圖
- [x] 自訂選項（至少 5 個）
- [x] FAQ 10+ 問答
- [x] 支援聯絡方式

---

## 版本和更新

**Current Version:** 1.0 (2026-04-05)

**未來計劃：**
- v1.1: 加入 Zapier 版本
- v1.2: 加入預置 credentials（OAuth templates）
- v2.0: 加入中文介面

---

## 授權

所有模板基於 **MIT License**。用戶可以：
- ✅ 自由使用、修改、分享
- ❌ 不能聲稱自己是原創者
- ❌ 不能移除歸屬聲明

---

## 聯絡和支援

- **Email:** support@gumroad.com
- **Discord:** https://discord.gg/xxxxx
- **FAQ:** 見各模板 README
- **Bug Report:** GitHub Issues (如果有 repo)

---

**感謝選擇我們的模板！享受自動化帶來的自由。** 🚀
