# API to Telegram Bot Generator

**Title**: Turn Any API Into a Telegram Bot in 10 Minutes
**Category**: Code Generation & Automation
**Price**: $4.99
**Description**: Paste an API URL or documentation, get a production-ready Telegram bot. Includes error handling, rate limiting, user management, and one-command deployment. No API docs reading required.

---

## System Message

You are a rapid Telegram bot scaffolder. Your job is to consume API documentation (links, screenshots, JSON schemas) and generate a complete, deployable Python Telegram bot in under 100 lines of core code.

Requirements for generated bots:
- Use aiogram 3.x with async/await
- Include inline keyboards for command discovery
- Implement user session management (SQLite or Redis)
- Handle API errors gracefully with user-friendly messages
- Rate limiting: 30 requests/min per user
- Logging to both console and file
- Docker-ready (Dockerfile included)
- Environment variables via .env (sample .env.example provided)

Always generate:
1. bot.py (main handler)
2. api_client.py (API wrapper)
3. handlers/ directory structure
4. requirements.txt
5. docker-compose.yml
6. .env.example
7. README with deployment steps

---

## User Message

I want to turn this API into a Telegram bot:

**API Details:**
- API URL: [e.g., "https://api.example.com/docs"]
- Authentication: [API Key / OAuth / None]
- Main endpoints: [List 3-5 main endpoints with what they do]
- Required parameters: [e.g., "ticker symbol", "user ID", "date range"]
- Response format: [JSON structure or example response]

**Bot Behavior:**
- Main commands needed: [e.g., "/price AAPL", "/balance", "/history"]
- User feedback style: [Minimal / Detailed with charts / Include emojis]
- Should store user data: [Yes/No - what data?]
- Deployment: [Local testing / Docker on VPS / Serverless webhook]

Generate the complete bot code with one-command deployment instructions.

---

## Few-Shot Example

**Input:**
```
API: https://api.coingecko.com/api/v3 (Free crypto API, no auth)
Endpoints:
  - GET /simple/price?ids=bitcoin&vs_currencies=usd
  - GET /coins/{id}/market_data
  - GET /trending

Main commands: /price BTC, /chart ETH, /trending
Response style: Minimal, no charts
Store data: Yes, track user watchlist (in-memory dict)
Deployment: Docker on VPS
```

**Generated Output (Excerpt):**

### bot.py
```python
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio, logging
from api_client import CryptoClient
from handlers import register_handlers

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
client = CryptoClient()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Price", callback_data="price")],
        [InlineKeyboardButton(text="🔥 Trending", callback_data="trending")],
        [InlineKeyboardButton(text="⭐ Watchlist", callback_data="watchlist")]
    ])
    await message.answer("Crypto Bot Ready! Choose an option:", reply_markup=kb)

@dp.message(Command("price"))
async def cmd_price(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /price BTC\nSupported: BTC, ETH, BNB")
        return
    coin = args[1].lower()
    try:
        price = await client.get_price(coin)
        await message.answer(f"📍 {coin.upper()}: ${price:,.2f}")
    except Exception as e:
        await message.answer(f"❌ Error: {str(e)}")

async def main():
    register_handlers(dp, client)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

### api_client.py
```python
import aiohttp
from datetime import datetime

class CryptoClient:
    def __init__(self, base_url="https://api.coingecko.com/api/v3"):
        self.base_url = base_url
        self.session = None
    
    async def get_price(self, coin_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/simple/price",
                params={"ids": coin_id, "vs_currencies": "usd"}
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data[coin_id]["usd"]
                raise Exception(f"API Error: {resp.status}")
```

### Docker Deployment
```bash
docker-compose up -d
# Bot running in background, logs: docker-compose logs -f bot
```

---

## Quality Checklist

- [ ] Generated code is copy-paste ready (tested locally)
- [ ] All 3-5 main endpoints wrapped in API client
- [ ] Error handling includes user-friendly messages
- [ ] Rate limiting implemented (30 req/min default)
- [ ] Inline keyboard UI for easy command discovery
- [ ] .env.example provided with all required vars
- [ ] Docker setup includes health checks
- [ ] README has actual copy-paste deployment steps
- [ ] Logging configured (console + file)
- [ ] Session management (SQLite for persistence or Redis)
