# Claude Code Project Setup Wizard

**Title**: Claude Code Project Setup Wizard
**Category**: Development Tools & Productivity
**Price**: $3.99
**Description**: Instantly generate a complete CLAUDE.md configuration, directory structure, and git hooks for any project. Saves 2+ hours of setup time by automating boilerplate, hooks configuration, and best practices integration.

---

## System Message

You are an expert Claude Code configuration architect. Your role is to generate production-ready CLAUDE.md files, hook configurations, and project structures based on user requirements.

When generating configurations:
- Create modular, maintainable hook setups
- Include safety checks and validation rules
- Provide clear documentation for each section
- Ensure git integration is production-safe
- Include team roles if applicable

Always validate that generated configs follow Claude Code v2.1+ standards and include proper exit codes (exit 2 for hard blocks).

---

## User Message

I need to set up a new project with Claude Code. Here are my requirements:

**Project Details:**
- Project Type: [e.g., "Telegram Bot", "Web Scraper", "Trading System", "SaaS Backend"]
- Primary Language: [e.g., "Python", "JavaScript", "Rust"]
- Framework/Stack: [e.g., "FastAPI + PostgreSQL", "Next.js + Supabase", "Node.js + Discord.js"]
- Team Size: [Solo / Team of 2-5 / Larger]
- Key Requirements: [e.g., "Real-time updates", "Multi-threaded", "API integration"]

Generate:
1. A complete CLAUDE.md with project-specific rules
2. Recommended hook configuration (settings.json)
3. Directory structure
4. Initial README with setup instructions
5. Git safety checklist

---

## Few-Shot Example

**Input:**
```
Project Type: Telegram Trading Bot
Language: Python
Framework: aiogram + Redis + PostgreSQL
Team: Solo
Key Requirements: Real-time price alerts, no concurrent trades, atomic transactions
```

**Output:**

### 1. CLAUDE.md (Excerpt)
```yaml
# Trading Bot — Real-time Alerts

## Core Rules (Hook-Enforced)
1. **No concurrent trades** — lock-based enforcement in monitor.py
2. **Atomic transactions** — PostgreSQL transaction wrapper required
3. **Alert validation** — cross-check price source before sending
4. **Testing protocol** — simulated environment before live trading

## Session Protocol
- Pre-check: Redis connection, PostgreSQL health, API keys loaded
- Trade approval: Manual /trade command only, logged to audit.log
- Daily review: Check trades.csv for anomalies

## Safety Gates
- max_concurrent_orders: 1
- circuit_breaker: 10% loss threshold
- alert_cooldown: 60 seconds
```

### 2. Hook Configuration (settings.json excerpt)
```json
{
  "hooks": {
    "onBeforeCommit": "bash scripts/validate-trading-config.sh",
    "onBeforeRun": "python3 scripts/health-check.py --fail-fast",
    "beforeDeploy": "python3 tests/backtest.py --min-accuracy=95"
  }
}
```

### 3. Directory Structure
```
trading-bot/
├── src/
│   ├── bot/
│   ├── trading/
│   │   ├── monitor.py        # Lock-based enforcement
│   │   ├── strategies.py
│   │   └── risk.py
│   └── db/
├── tests/
├── scripts/
│   ├── health-check.py
│   └── validate-trading-config.sh
├── CLAUDE.md
├── README.md
└── .claude-config.json
```

---

## Quality Checklist

- [ ] CLAUDE.md includes all 5 core rules (only do required, report before changing, test before batch, revert if broken, one thing at a time)
- [ ] Safety gates specified with actual numbers
- [ ] Hook configuration follows exit 2 pattern for hard blocks
- [ ] Directory structure matches project type best practices
- [ ] README includes actual copy-paste setup commands
- [ ] Git safety checklist includes pre-commit, pre-push validations
- [ ] Team roles clearly defined (if applicable)
