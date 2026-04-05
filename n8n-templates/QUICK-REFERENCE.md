# n8n Templates — 快速參考卡

> 用戶購買後的第一份文件（快速開始）

---

## 🎁 你買了什麼

### 方案選擇
- **單個模板** → 下載對應的 JSON + README
- **Bundle** → 同時下載 3 個 JSON + 3 個 README

### 檔案說明
```
1-ai-content-pipeline.json
└─ 可直接匯入 n8n 的 workflow，600+ 行

1-ai-content-pipeline-README.md
└─ 完整安裝指南 (132 行)，從零開始也能做

2-lead-responder.json
└─ Lead 自動回覆 workflow

2-lead-responder-README.md
└─ 郵件自動化詳細指南 (180 行)

3-competitor-monitor.json
└─ 競品監控 workflow (多資料來源)

3-competitor-monitor-README.md
└─ 情報分析詳細指南 (248 行)
```

---

## ⚡ 5 分鐘快速開始

### 1️⃣ 打開 n8n
```
訪問 n8n.io (雲端免費版)
或 localhost:5678 (本地版本)
登入/註冊帳號
```

### 2️⃣ 匯入 Workflow
```
點 【Create】→ 【Import from file】
選擇 JSON 檔案
等 3 秒鐘...
✅ Workflow 匯入完成！
```

### 3️⃣ 設定 API Keys
打開 JSON 對應的 README，找到 **"設定環境變數"** 章節
根據指示：
```
1. n8n Settings → Environment variables
2. 複製 API key（見 README）
3. 貼到對應的變數名稱
```

**各模板需要的 API：**
- Content Pipeline: Anthropic + Twitter + Facebook
- Lead Responder: Gmail + Anthropic
- Competitor Monitor: Anthropic + Product Hunt + Twitter

### 4️⃣ 測試
```
點 【Test workflow】
看看有沒有錯誤
成功！✅
```

### 5️⃣ 啟動
```
點 【Activate】
自動執行開始！
```

---

## 🔑 API Key 速查表

| API | 取得位置 | 免費額度 |
|-----|---------|--------|
| **Anthropic** (Claude) | https://console.anthropic.com/account/keys | 有 |
| **Twitter API v2** | https://developer.twitter.com/en/portal/dashboard | 有限 |
| **Facebook Graph** | https://developers.facebook.com | 有 |
| **Product Hunt** | https://api.producthunt.com/v2/docs | 有 |
| **Gmail** | n8n 內自動授權 | 無限 |
| **Telegram Bot** | @BotFather | 無限 |

---

## 📋 常見問題（3 分鐘答疑）

### Q1: JSON 檔案放哪裡？
**A:** 不用放任何地方。直接在 n8n 網頁上「Import from file」上傳，不用下載到電腦。

### Q2: 需要寫程式碼嗎？
**A:** 完全不用。只需要複製貼上 API key，再按幾個鈕就好。

### Q3: API key 安全嗎？
**A:** 安全。你的 key 只儲存在你的 n8n 環境變數裡，我們看不到。

### Q4: 可以改 workflow 嗎？
**A:** 可以！README 裡有 5-10 個自訂選項，都可以改。

### Q5: 出錯怎麼辦？
**A:** 看 README 的 FAQ 章節。99% 的問題都有答案。

### Q6: 可以在本地 n8n 用嗎？
**A:** 可以。JSON 是通用的，本地版本和雲端版本都能用。

### Q7: 有更新嗎？
**A:** 有。買過的用戶自動取得所有未來更新（v1.1, v2.0 等）。

### Q8: 不滿意可以退款嗎？
**A:** 是的。30 天內無條件全額退款。

---

## 🚀 下一步

### 推薦順序

**Day 1:** 匯入 + 設定 API
```
→ 選一個最想要的模板先做
→ 花 15-30 分鐘設定
→ 執行一次測試
```

**Day 2-7:** 優化和自訂
```
→ 改提示詞（README 有範例）
→ 改檢查頻率（每小時變成每 30 分鐘）
→ 加新的通知渠道（Slack/Telegram/Email）
```

**Week 2+:** 監控和改進
```
→ 檢查執行日誌
→ 看是否有錯誤
→ 根據結果調整參數
```

---

## 📚 詳細文檔位置

如果想深入了解：

1. **功能說明** → README 開頭的「功能」章節
2. **安裝步驟** → README 的「安裝步驟」（7 步）
3. **API 設定** → README 的「設定環境變數」
4. **自訂選項** → README 的「自訂選項」（5-10 個）
5. **常見問題** → README 的「FAQ」（10-15 題）
6. **進階用法** → README 的「進階用法」或「更多範例」

---

## 🎯 各模板的典型用途

### 📰 AI Content Pipeline ($29)
**適合你如果：**
- 有 RSS feed（部落格、新聞）要發文
- 用 Twitter/Facebook 做行銷
- 想每週省 10 小時發文

**典型用法：**
```
Morning: 部落格更新自動發到社群
Afternoon: 競品文章自動轉發
Evening: 一天的工作都幫你完成了 😎
```

### 📧 AI Lead Auto-Responder ($39)
**適合你如果：**
- 有 Gmail 收客戶詢問
- 想更快回覆潛在客戶
- 擔心漏掉重要郵件

**典型用法：**
```
客戶寄詢問 → AI 自動起草 → 你審閱 → 發送
全程 2 分鐘 vs 原本 15 分鐘 ✨
```

### 📊 Competitor Monitor ($49)
**適合你如果：**
- 想追蹤競品動態
- 需要市場情報做決策
- 害怕被超越

**典型用法：**
```
每天早上 9 點: 你收到競品分析報告
包含: 新功能、定價變化、客戶評價
3 分鐘讀完，掌握市場脈動 📊
```

---

## 🛠️ 工具要求

### 最低需求
- ✅ n8n 帳號（免費）
- ✅ 至少一個 API key（Anthropic 推薦先做）
- ✅ 15 分鐘設定時間

### 進階選項
- ⭐ Slack 帳號（通知更快）
- ⭐ Telegram Bot（推播通知）
- ⭐ Airtable（儲存數據）

---

## 💡 最佳實踐

1. **先小測** — 用測試資料執行一次，確認沒錯誤
2. **再上線** — 驗證成功後再 activate
3. **監控日誌** — 每週看一下執行紀錄
4. **定期改進** — 根據結果調整參數
5. **記錄變化** — 記下改了什麼，為什麼改

---

## 🆘 陷阱和常見錯誤

❌ **不要做**
- 直接 activate，不測試
- API key 複製錯誤
- 忘記選擇正確的環境變數
- 改了 prompt 後沒看結果

✅ **一定要做**
- 複製完 API key 後確認一次
- 用 Test 功能檢查有沒有錯誤
- 監控前幾次執行的日誌
- 根據實際結果微調參數

---

## 📞 需要幫助？

### 如果卡住了
1. **先讀 README** 的 FAQ（99% 的問題都在裡面）
2. **檢查 n8n 日誌** — 看看哪一步出錯
3. **試試測試模式** — 不 activate，先 test 看錯誤訊息
4. **查 API 文檔** — 確認 key 格式正確

### 如果還是不行
- Email: support@gumroad.com
- 提供：買了哪個模板 + 錯誤訊息 + 已試過什麼

---

## 🎓 學習資源

**n8n 新手？**
- https://n8n.io/docs/getting-started/ — 官方文檔
- https://n8n.io/workflows — 公開範例

**Anthropic API？**
- https://docs.anthropic.com/en/api/getting-started — 入門指南
- https://console.anthropic.com/docs/models/overview — 模型說明

**想深入了解？**
- README 裡的「進階用法」章節有 5+ 個複雜範例
- 可以組合節點做出更複雜的 workflow

---

## ✨ 下次更新預告

### v1.1（預計 1-2 個月）
- 中文 UI 支援
- 更多通知選項（WeChat, Discord）
- 新增預置 prompt 庫

### v2.0（預計 3-6 個月）
- OAuth credentials 預設
- 社群共享的自訂範例
- 更多模板加入

---

**準備好自動化你的工作了嗎？讓我們開始吧！** 🚀

下一步：打開 n8n，選一個模板，然後看著魔法發生。

有問題？見 README！ 👈
