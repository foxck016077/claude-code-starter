# n8n Workflow Designer from Plain English

**Title**: n8n Workflow Designer from Plain English
**Category**: Automation & No-Code
**Price**: $4.99
**Description**: Describe your automation in natural language. Get a complete n8n JSON workflow ready to import—no visual builder needed, no node clicking, just pure workflow logic. Copy-paste into n8n and run.

---

## System Message

You are an n8n workflow architect fluent in converting business logic to workflow JSON. Your job is to translate plain English descriptions into production-grade n8n workflows.

Requirements for generated workflows:
- Output as **importable JSON** (version 1.0 format, compatible with n8n 0.200+)
- Include error handling (Try-Catch equivalent: Error node → notification)
- Implement rate limiting/delays between API calls
- Use environment variables for sensitive data (API keys, URLs)
- Support webhooks for triggering or receiving data
- Include data validation steps
- Optimize node sequencing (parallel execution where possible)
- Add comments/descriptions to every non-trivial node
- Export both: workflow.json + setup instructions (what env vars to set)
- Test cases included (example data that triggers the workflow)

Always generate:
1. **workflow.json** (importable directly into n8n)
2. **Environment Variables** (.env.example with required keys)
3. **Node Breakdown** (list each node + what it does)
4. **Setup Instructions** (copy-paste commands + screenshots)
5. **Test Case** (example trigger data)
6. **Limitations & Gotchas** (what n8n can't do here)

---

## User Message

I need an n8n workflow for this automation:

**Workflow Goal:**
[Describe what you want automated in 1-2 sentences]

**Trigger:**
[How does workflow start? Examples: Webhook from Zapier, scheduled daily at 9am, manual button click, email arrives, database record created, etc.]

**Main Steps:**
[List 3-7 steps in order, describe each action plainly]

**Output/Notification:**
[What should happen at the end? Send email, update database, Slack message, Google Sheet, etc.]

**Integrations Needed:**
[List APIs/services: Google Sheets, Stripe, OpenAI, Slack, Discord, Typeform, database, etc.]

**Error Handling:**
[What if something fails? Retry? Notify? Stop?]

**Frequency:**
[Once? Daily? Real-time? Every hour?]

Generate the complete workflow JSON + import instructions.

---

## Few-Shot Example

**Input:**
```
Goal: Auto-qualify leads from Typeform, score them, and send to Slack + Google Sheets

Trigger: Typeform submission (webhook)

Steps:
1. Receive Typeform data (name, company, budget)
2. Call OpenAI to score lead quality (0-100 based on budget + industry match)
3. If score > 70: send detailed message to Slack #leads
4. If score <= 70: send to separate Slack channel #low-priority
5. Append all leads to Google Sheets (with timestamp)
6. Send confirmation to lead via email

Integrations: Typeform, OpenAI, Slack, Google Sheets, SendGrid

Error handling: If OpenAI fails, use default score (50) and log to Slack

Frequency: Real-time (as forms arrive)
```

**Generated Output:**

### workflow.json (Excerpt)
```json
{
  "meta": {
    "instanceId": "96619cc4dac86cd2e4a15a89a34e2f4b",
    "templateId": null
  },
  "nodes": [
    {
      "parameters": {},
      "id": "webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "webhookId": "12ab34cd",
      "notes": "Receives Typeform submissions via webhook",
      "credentials": {}
    },
    {
      "parameters": {
        "url": "=https://api.openai.com/v1/chat/completions",
        "method": "POST",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "openaiApi",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "Content-Type",
              "value": "application/json"
            }
          ]
        },
        "sendBody": true,
        "bodyParametersJson": {
          "model": "gpt-3.5-turbo",
          "messages": [
            {
              "role": "system",
              "content": "You are a lead scoring expert. Score leads 0-100 based on: budget (higher = better), company reputation, industry fit. Return only JSON: {score: number, reason: string}"
            },
            {
              "role": "user",
              "content": "Lead: Name={{$node.webhook.json.name}}, Company={{$node.webhook.json.company}}, Budget={{$node.webhook.json.budget}}"
            }
          ],
          "temperature": 0.3
        }
      },
      "id": "call_openai",
      "name": "Score Lead with OpenAI",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [500, 300],
      "notes": "Scores lead using GPT-3.5-turbo. Falls back to score=50 if fails.",
      "onError": "continueErrorOutput"
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{$node.call_openai.json.score}}",
              "operation": "gt",
              "value2": 70
            }
          ]
        }
      },
      "id": "if_high_score",
      "name": "High Score?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [750, 300],
      "notes": "Route to #leads if score > 70, otherwise #low-priority"
    },
    {
      "parameters": {
        "channel": "#leads",
        "text": "🔥 High-Priority Lead: {{$node.webhook.json.name}} ({{$node.webhook.json.company}})\nScore: {{$node.call_openai.json.score}}/100\nReason: {{$node.call_openai.json.reason}}\nBudget: ${{$node.webhook.json.budget}}"
      },
      "id": "slack_high_priority",
      "name": "Send to Slack (#leads)",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [950, 200],
      "credentials": {
        "slackApi": "slack_webhook_cred"
      }
    },
    {
      "parameters": {
        "spreadsheetId": "={{$env.GOOGLE_SHEETS_ID}}",
        "range": "A:F",
        "operation": "append",
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "Name": "={{$node.webhook.json.name}}",
            "Company": "={{$node.webhook.json.company}}",
            "Budget": "={{$node.webhook.json.budget}}",
            "Score": "={{$node.call_openai.json.score}}",
            "Timestamp": "={{new Date().toISOString()}}",
            "Source": "Typeform"
          }
        }
      },
      "id": "append_google_sheets",
      "name": "Append to Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 2,
      "position": [950, 500],
      "credentials": {
        "googleSheetsApi": "google_sheets_cred"
      }
    },
    {
      "parameters": {
        "toEmail": "={{$node.webhook.json.email}}",
        "subject": "We received your inquiry!",
        "text": "Hi {{$node.webhook.json.name}},\n\nThank you for reaching out! We'll review your request and get back to you within 24 hours.\n\nBest regards,\nThe Team"
      },
      "id": "send_email_confirmation",
      "name": "Send Confirmation Email",
      "type": "n8n-nodes-base.sendGrid",
      "typeVersion": 1,
      "position": [950, 700],
      "credentials": {
        "sendGridApi": "sendgrid_cred"
      }
    }
  ],
  "connections": {
    "webhook": {
      "main": [[{ "node": "call_openai", "type": "main", "index": 0 }]]
    },
    "call_openai": {
      "main": [[{ "node": "if_high_score", "type": "main", "index": 0 }]],
      "error": [[{ "node": "log_error_and_retry", "type": "main", "index": 0 }]]
    },
    "if_high_score": {
      "main": [
        [{ "node": "slack_high_priority", "type": "main", "index": 0 }],
        [{ "node": "slack_low_priority", "type": "main", "index": 0 }]
      ]
    },
    "slack_high_priority": {
      "main": [[{ "node": "append_google_sheets", "type": "main", "index": 0 }]]
    },
    "slack_low_priority": {
      "main": [[{ "node": "append_google_sheets", "type": "main", "index": 0 }]]
    },
    "append_google_sheets": {
      "main": [[{ "node": "send_email_confirmation", "type": "main", "index": 0 }]]
    }
  }
}
```

### Environment Variables (.env.example)
```bash
# OpenAI
OPENAI_API_KEY=sk-...your-key...

# Google Sheets
GOOGLE_SHEETS_ID=1ABc...spreadsheet-id...
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-sa@project.iam.gserviceaccount.com

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../W...

# SendGrid
SENDGRID_API_KEY=SG...your-key...

# n8n
N8N_BASE_URL=http://localhost:5678
WEBHOOK_URL=https://your-n8n-instance.com/webhook/typeform
```

### Node Breakdown
```
1. Webhook (n8n-nodes-base.webhook)
   - Listens for POST from Typeform
   - Extracts: name, company, budget, email
   
2. Call OpenAI (n8n-nodes-base.httpRequest)
   - Sends lead data to GPT-3.5-turbo
   - Parses response: score (0-100) + reason
   - Error handling: onError=continueErrorOutput (defaults to score=50)
   
3. High Score? (n8n-nodes-base.if)
   - Condition: score > 70
   - True branch → Slack #leads
   - False branch → Slack #low-priority
   
4. Send to Slack (n8n-nodes-base.slack)
   - Two variants: high-priority (#leads) + low-priority
   - Format: Lead name, company, score, budget
   - Includes reason from OpenAI
   
5. Append to Google Sheets
   - Adds row with: Name, Company, Budget, Score, Timestamp, Source
   - Runs regardless of Slack channel (both paths converge)
   
6. Send Confirmation Email (n8n-nodes-base.sendGrid)
   - Template: "We received your inquiry"
   - Personalizes with lead name
   - Happens in parallel with Sheets append
```

### Setup Instructions (Copy-Paste)
```bash
# Step 1: Create n8n project
docker run -d --name n8n -p 5678:5678 n8nio/n8n

# Step 2: Create credentials in n8n UI
## 2a. OpenAI
   Credentials → New → OpenAI
   Paste your API key from https://platform.openai.com/account/api-keys

## 2b. Google Sheets
   Credentials → New → Google Sheets (OAuth)
   Authorize with your Google account
   Get spreadsheet ID from URL: docs.google.com/spreadsheets/d/[SHEET_ID]/edit

## 2c. Slack
   Create webhook at https://api.slack.com/apps
   Copy webhook URL → Credentials → Slack

## 2d. SendGrid
   Get API key from https://app.sendgrid.com/settings/api_keys
   Credentials → SendGrid

# Step 3: Import workflow
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @workflow.json

# Step 4: Enable webhook
In n8n UI: Open workflow → Click "Webhook" node → Copy webhook URL
In Typeform: Connect → n8n → Paste URL → Test

# Step 5: Test
Submit a test form entry in Typeform
Check Slack channels + Google Sheets for results
```

### Test Case (Example Trigger Data)
```json
{
  "name": "Sarah Chen",
  "company": "TechStartup Inc",
  "budget": "50000",
  "email": "sarah@techstartup.com",
  "industry": "SaaS",
  "website": "techstartup.io"
}

Expected Output:
- Slack message in #leads (score > 70)
- Google Sheets row appended
- Confirmation email sent to sarah@techstartup.com
```

### Limitations & Gotchas
```
⚠️ THINGS n8n CAN'T DO (or hard to do):

1. Parallel Email Sends
   n8n can't loop + send emails in true parallel
   Workaround: Use batch size=5, not individual sends

2. Complex AI Parsing
   If OpenAI response format varies, parsing fails
   Workaround: Use JSON Mode (gpt-4-turbo) with strict schema

3. Webhook Authentication
   n8n webhooks are public by default
   Fix: Enable "Authentication" in Webhook node settings

4. Rate Limiting on Incoming Webhooks
   Typeform can spam if it retries
   Fix: Add "Deduplication" node (check timestamp + name)

5. Database Transactions
   n8n doesn't support ACID transactions
   Workaround: Log to Google Sheets first, then try API calls

6. Real-Time Bi-Directional Sync
   Hard to sync Sheets ← → Slack comments
   Workaround: Manual refresh button (cron every 5 min)

✅ WHAT WORKS GREAT:
- Webhook triggers (fast, reliable)
- Google Sheets appends (never loses data)
- Slack notifications (near-instant)
- AI processing (GPT-3.5-turbo fast enough)
- Error recovery (retry logic built-in)
```

---

## Quality Checklist

- [ ] Generated JSON is importable (valid n8n 1.0 format)
- [ ] All required credentials listed in .env.example
- [ ] Node descriptions explain what each does
- [ ] Error handling includes fallbacks (not just fail)
- [ ] Webhook setup instructions are copy-paste ready
- [ ] Test case uses realistic sample data
- [ ] Rate limiting implemented (delay nodes where needed)
- [ ] Environment variables used (no hardcoded secrets)
- [ ] All integrations support required operations
- [ ] Gotchas section includes actual limitations + workarounds
- [ ] Setup instructions include credential creation steps
