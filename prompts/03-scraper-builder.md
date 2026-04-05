# Web Scraper Generator with Anti-Detection

**Title**: Web Scraper Generator with Anti-Detection
**Category**: Data Extraction & Automation
**Price**: $4.99
**Description**: Describe a website and what data you want. Get a production-grade web scraper with built-in anti-detection (rotating proxies, user-agent rotation, request delays). Never get blocked again.

---

## System Message

You are an expert web scraper architect specializing in evasion techniques. Your job is to generate robust, maintainable scrapers that blend in with real traffic.

Requirements for generated scrapers:
- Use Playwright (better JS handling than Selenium, native stealth)
- Implement realistic delays (2-5s between requests, randomized)
- User-agent rotation from 100+ real browser strings
- Proxy rotation support (IP:port list or free proxy pool)
- Headless=false for JS-heavy sites (but browser set to non-headless-looking UA)
- Request retries with exponential backoff
- Smart cookie jar management
- Cloudflare/WAF bypass (challenge detection + retry logic)
- Output to CSV or JSON with validation
- Logging for debugging without exposing proxies/IPs

Always generate:
1. scraper.py (main orchestrator)
2. extractors/ (site-specific CSS/XPath selectors)
3. proxy_manager.py (rotation logic)
4. config.yaml (easy tuning)
5. docker-compose.yml (headless browser + proxy rotation)
6. tests/ (data validation)
7. README with setup & safety guidelines

---

## User Message

I need a web scraper for this site:

**Target Details:**
- Website URL: [e.g., "example.com/products"]
- What to extract: [List 3-5 fields: price, title, description, rating, stock status, etc.]
- Data structure: [Single page / Paginated / Infinite scroll / AJAX-loaded]
- Authentication needed: [Yes/No - login required?]
- Update frequency: [How often: hourly, daily, weekly?]
- Anti-bot detection: [None visible / Cloudflare / reCAPTCHA / Rotating IP required?]
- Output format: [CSV for spreadsheet / JSON for API / Database insert]

Provide complete scraper code with anti-detection built-in. I just want to run it and get data.

---

## Few-Shot Example

**Input:**
```
Site: ecommerce.example.com/products
Extract: name, price, rating, stock_status, seller
Pagination: 1000+ pages (next button)
Auth: None
Detection: Cloudflare present
Update: Daily batch
Output: JSON with deduplication
```

**Generated Output (Excerpt):**

### scraper.py
```python
import asyncio
import json
from playwright.async_api import async_playwright
from proxy_manager import ProxyManager
from extractors import ProductExtractor
from config import SCRAPER_CONFIG
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RobustScraper:
    def __init__(self, config):
        self.config = config
        self.proxy_manager = ProxyManager(config['proxies'])
        self.extractor = ProductExtractor()
        self.data = []
    
    async def scrape_page(self, page, url):
        """Scrape single page with Cloudflare bypass"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use real browser context
                context = await page.context.browser.new_context(
                    proxy={"server": self.proxy_manager.get_proxy()},
                    user_agent=self.proxy_manager.get_user_agent()
                )
                page = await context.new_page()
                
                # Add random delay
                await asyncio.sleep(random.uniform(2, 5))
                
                # Navigate with Cloudflare handling
                try:
                    await page.goto(url, wait_until="networkidle", timeout=30000)
                except Exception as e:
                    if "Cloudflare" in str(e):
                        logger.warning(f"Cloudflare detected, retrying with different proxy...")
                        await context.close()
                        continue
                    raise
                
                # Extract data
                products = await self.extractor.extract(page)
                self.data.extend(products)
                
                await context.close()
                return products
            
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def run(self):
        """Main scraping loop"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Headless=false looks more real
            page = await browser.new_page()
            
            for page_num in range(1, self.config['max_pages'] + 1):
                url = f"{self.config['base_url']}?page={page_num}"
                logger.info(f"Scraping page {page_num}...")
                
                try:
                    await self.scrape_page(page, url)
                except Exception as e:
                    logger.error(f"Failed to scrape page {page_num}: {e}")
            
            await browser.close()
        
        # Save results with deduplication
        self._save_data()
        logger.info(f"Scraping complete. {len(self.data)} items collected.")
    
    def _save_data(self):
        """Save to JSON with dedup"""
        seen = set()
        unique_data = []
        for item in self.data:
            key = (item['name'], item['seller'])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        with open(self.config['output_file'], 'w') as f:
            json.dump(unique_data, f, indent=2, ensure_ascii=False)

async def main():
    scraper = RobustScraper(SCRAPER_CONFIG)
    await scraper.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### proxy_manager.py
```python
import random
from typing import Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
    # ... 100+ real user agents
]

class ProxyManager:
    def __init__(self, proxy_list: Optional[list] = None):
        self.proxies = proxy_list or self._load_free_proxies()
        self.current_index = 0
    
    def get_proxy(self) -> str:
        """Round-robin proxy selection"""
        proxy = self.proxies[self.current_index % len(self.proxies)]
        self.current_index += 1
        return f"http://{proxy}"
    
    def get_user_agent(self) -> str:
        return random.choice(USER_AGENTS)
```

### config.yaml
```yaml
base_url: "https://ecommerce.example.com/products"
max_pages: 100
proxies:
  - "proxy1.com:8080"
  - "proxy2.com:8080"
output_file: "data/products.json"
request_timeout: 30000
delay_min: 2
delay_max: 5
```

### docker-compose.yml
```yaml
version: '3'
services:
  scraper:
    build: .
    environment:
      - PROXY_LIST=proxies.txt
    volumes:
      - ./data:/app/data
    command: python scraper.py
```

---

## Quality Checklist

- [ ] Scraper handles Cloudflare/WAF without manual intervention
- [ ] Proxy rotation automatic (supports free pools + paid services)
- [ ] User-agent rotation from 100+ real browsers
- [ ] Request delays randomized (2-5s default, configurable)
- [ ] Retry logic with exponential backoff
- [ ] Data validation and deduplication
- [ ] CSV + JSON export supported
- [ ] Docker setup for headless deployment
- [ ] Logging includes timing, errors, not exposing secrets
- [ ] README includes legal disclaimer (robots.txt, terms of service)
- [ ] Tests included for CSS selector validation
