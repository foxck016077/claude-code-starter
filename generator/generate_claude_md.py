#!/usr/bin/env python3
"""
Claude Code CLAUDE.md Generator
互動式產生客製化 CLAUDE.md

使用方法:
  python3 generate_claude_md.py              # 互動式問答
  python3 generate_claude_md.py --preset bot # 快速預設 (bot/web/scraper/trader)
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print colored header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_section(text: str) -> None:
    """Print colored section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}>> {text}{Colors.END}")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.CYAN}→ {text}{Colors.END}")


def get_input_with_default(prompt: str, default: str = None) -> str:
    """Get user input with optional default."""
    if default:
        prompt = f"{prompt} [{Colors.YELLOW}{default}{Colors.END}]: "
    else:
        prompt = f"{prompt}: "

    response = input(prompt).strip()
    return response if response else default


def get_multi_select(options: List[Tuple[str, str]]) -> List[str]:
    """Multi-select from options. Returns list of selected keys."""
    print(f"{Colors.YELLOW}(選擇多個: 輸入編號用空格分隔, 如: 1 3 5){Colors.END}")

    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}. {label}")

    response = input(f"{Colors.BLUE}選擇 (1-{len(options)}){Colors.END}: ").strip()

    selected = []
    if response:
        try:
            indices = [int(x.strip()) for x in response.split()]
            for idx in indices:
                if 1 <= idx <= len(options):
                    selected.append(options[idx - 1][0])
        except ValueError:
            pass

    return selected


def get_single_select(options: List[Tuple[str, str]]) -> str:
    """Single select from options. Returns the selected key."""
    for i, (key, label) in enumerate(options, 1):
        print(f"  {i}. {label}")

    response = input(f"{Colors.BLUE}選擇 (1-{len(options)}){Colors.END}: ").strip()

    try:
        idx = int(response)
        if 1 <= idx <= len(options):
            return options[idx - 1][0]
    except ValueError:
        pass

    return None


# ============================================================================
# PRESET TEMPLATES
# ============================================================================

PRESETS = {
    'bot': {
        'name': 'Telegram/Discord/LINE Bot 開發者',
        'language': 'zh-tw',
        'use_cases': ['bot'],
        'communication': 'direct',
        'safety_rules': ['no_env', 'no_git_config', 'no_auto_push', 'no_dangerous_commands'],
    },
    'web': {
        'name': 'Web App 開發者',
        'language': 'zh-tw',
        'use_cases': ['web', 'automation'],
        'communication': 'direct',
        'safety_rules': ['no_env', 'no_git_config', 'no_auto_push'],
    },
    'scraper': {
        'name': '爬蟲/數據分析師',
        'language': 'zh-tw',
        'use_cases': ['scraper', 'automation'],
        'communication': 'detailed',
        'safety_rules': ['no_env', 'no_auto_push', 'no_dangerous_commands'],
    },
    'trader': {
        'name': '量化交易開發者',
        'language': 'zh-tw',
        'use_cases': ['automation', 'learning'],
        'communication': 'direct',
        'safety_rules': ['no_env', 'no_auto_push', 'no_dangerous_commands', 'no_delete'],
    },
}


# ============================================================================
# TEMPLATE GENERATION
# ============================================================================

def generate_identity_section(name: str, language: str) -> str:
    """Generate identity section based on user input."""
    lang_names = {
        'zh-tw': '繁體中文',
        'zh-cn': '簡體中文',
        'en': 'English',
        'ja': '日本語',
        'vi': 'Tiếng Việt',
    }

    lang_display = lang_names.get(language, language)

    return f"""## 身份
- 我叫 **{name}**，{lang_display}，直接不廢話
- 事實先查再說，標出來源 `[查：<來源>]`，不准猜
- 遇到不確定的，寧可花時間驗證，不快速猜測"""


def generate_core_rules() -> str:
    """Generate core rules section."""
    return """## 核心規則
1. **只做被要求的事** — 做 A 就只做 A，想改別的先回報
2. **改前先報告** — 說清改什麼、為什麼、影響範圍，確認才動手
3. **先讀再改** — 改 code 前先讀相關檔案和 context，不熟就回報
4. **一次做一件事** — 不開多條線，做完一件再做下一件
5. **做壞就還原** — revert 優先，不疊補丁
6. **有驗證才動手** — 實作前先定義怎麼驗證（測試/預期輸出/截圖）"""


def generate_use_cases_section(use_cases: List[str]) -> str:
    """Generate project/use case section based on user selection."""
    sections = []

    if 'web' in use_cases:
        sections.append("""### Web App 開發
- 改 code 前讀整個檔案結構 (`ls -la src/`)
- 小改先跑本地測試再 commit
- 改 config 檔先備份原版
- 不自動安裝新套件，先確認版本相容性""")

    if 'bot' in use_cases:
        sections.append("""### Bot 開發
- 改 Bot 邏輯前先讀現有的 message handlers
- 測試改動不部署，確認不會炸才上線
- 改 schedule/cron 前確認現有的排程依賴
- 不改 Bot token 或環境設定，一律請示""")

    if 'scraper' in use_cases:
        sections.append("""### 爬蟲/數據分析
- 大量爬取前先小跑 2-3 筆驗證邏輯
- 改 Selector 前先手動測試一次
- 爬蟲改動不自動執行，先看輸出確認
- 遇到 IP ban/限流，先停下來報告，不盲目重試""")

    if 'automation' in use_cases:
        sections.append("""### 自動化腳本
- 改 cron/排程前確認現有依賴和影響
- 自動化指令要有乾淨的 rollback 方案
- 批量操作前小跑試手，確認無誤再全量
- 排程指令不互相打架，有 lock 機制""")

    if 'learning' in use_cases:
        sections.append("""### 學習/練習項目
- 重構前先確認現有測試通過
- 學習新技術時可以嘗試，但完成後要有驗證
- 代碼風格保持一致，不突然換框架""")

    if sections:
        return "\n## 專案類型\n" + "\n".join(sections)

    return ""


def generate_safety_section(safety_rules: List[str]) -> str:
    """Generate safety/red lines section."""
    sections = []

    sections.append("## 絕對紅線（改前必讀）")

    if 'no_env' in safety_rules:
        sections.append("""- **不碰 .env / 密鑰檔案** — 任何情況都不改，不上傳，定期 grep 檢查
  - `.env`, `.env.local`, `credentials.json`, `secrets.yaml` 等一律 skip
  - 改檔案前先 grep 確認沒有敏感信息""")

    if 'no_git_config' in safety_rules:
        sections.append("""- **不改 git 設定** — 不動 `.git/config`, `~/.gitconfig`, `.gitignore`
  - user.name / user.email 只讀不改
  - 加新的 ignore rule 要先確認現有規則""")

    if 'no_auto_push' in safety_rules:
        sections.append("""- **不自動 push** — 改完 commit 就停，等確認再 push
  - 危險分支 (main/master) 一律不 push
  - 有 pre-commit hook 失敗就停，不強推 (--no-verify)""")

    if 'no_delete' in safety_rules:
        sections.append("""- **不刪檔案** — 除非明確要求，否則只改不刪
  - 舊檔案移到 `./archive/` 或加 `.bak` 後綴
  - git rm 前確認有備份和 git history""")

    if 'no_dangerous_commands' in safety_rules:
        sections.append("""- **不執行危險指令** — `rm -rf`, `git reset --hard`, `pkill`, `dd` 等一律手動確認
  - 涉及系統層操作的要詳細報告，等回應
  - Batch 操作前走 dry-run (--dry-run) 或 -v 檢查""")

    return "\n".join(sections)


def generate_communication_section(style: str) -> str:
    """Generate communication style section."""
    styles = {
        'direct': """## 溝通風格：簡潔直接
- 結果優先，不废话
- 發現問題直接提，不等提醒
- 改動前快速回報，3 行以內
- 遇到卡點立即回報，不盲目試錯超過 2 次""",

        'detailed': """## 溝通風格：詳細解釋
- 每個步驟說清楚為什麼這樣做
- 遇到決策點列出選項和原因
- 改動後解釋影響範圍和驗證方式
- 提供背景知識幫助理解""",

        'do_first': """## 溝通風格：先做再說
- 有想法直接執行，邊做邊優化
- 小改動不必每次都報告，做完 commit 說明即可
- 遇到不確定的，先試試看再報告結果
- 改動範圍超過預期才停下來確認"""
    }

    return styles.get(style, styles['direct'])


def generate_custom_section(custom: str) -> str:
    """Generate custom rules section if provided."""
    if not custom or custom.strip() == "":
        return ""

    return f"""## 自訂規則
{custom}"""


def generate_final_notes() -> str:
    """Generate closing notes section."""
    return """## Session 結束前
- 確保改動已 commit（git repo）
- 列出做了什麼、為什麼做、有什麼限制

## 參考資源
- 遇到不確定的技術問題，先查文檔或搜索，給出來源
- 有設定檔衝突時，備份原版再改
- 大改動前 grep 全倉庫找相關檔案"""


# ============================================================================
# MAIN INTERACTIVE FLOW
# ============================================================================

def interactive_mode() -> Dict:
    """Run interactive Q&A mode."""
    print_header("Claude Code CLAUDE.md 產生器")
    print_info("回答 6-7 個問題，客製化你的工作規則")

    # Q1: Name
    print_section("問題 1：你的名字")
    print("Claude Code 會怎麼稱呼你？(例: Hope, Hunter, Dev)")
    name = get_input_with_default("你的名字", "Assistant")

    # Q2: Language
    print_section("問題 2：工作語言")
    language = get_single_select([
        ('zh-tw', '繁體中文'),
        ('zh-cn', '簡體中文'),
        ('en', 'English'),
        ('ja', '日本語'),
        ('vi', 'Tiếng Việt'),
    ])
    if not language:
        language = 'en'

    # Q3: Use cases
    print_section("問題 3：主要工作內容")
    print("你用 Claude Code 主要做什麼？(可多選)")
    use_cases = get_multi_select([
        ('web', '寫網站/Web App'),
        ('bot', '寫 Bot (Telegram/Discord/LINE)'),
        ('scraper', '數據分析/爬蟲'),
        ('automation', '自動化腳本'),
        ('learning', '學習程式設計'),
    ])

    # Q4: Safety rules
    print_section("問題 4：絕對不能碰的地方")
    print("有什麼 Claude 應該避免操作的？")
    safety_rules = get_multi_select([
        ('no_env', '不要動 .env / 密鑰檔案'),
        ('no_git_config', '不要改 git 設定'),
        ('no_auto_push', '不要自動 push'),
        ('no_delete', '不要刪除檔案'),
        ('no_dangerous_commands', '不要執行危險指令 (rm -rf/pkill 等)'),
    ])

    # Q5: Communication style
    print_section("問題 5：溝通風格")
    print("你喜歡 Claude 怎麼跟你溝通？")
    communication = get_single_select([
        ('direct', '簡潔直接（工程師對工程師）'),
        ('detailed', '詳細解釋（像老師教學生）'),
        ('do_first', '先做再說（不要問，直接動手）'),
    ])
    if not communication:
        communication = 'direct'

    # Q6: Custom rules
    print_section("問題 6：有其他特殊規則嗎？(選填)")
    print("例如: 不要改資料庫連線、先跑測試再改、必須用某個框架等")
    print("(直接按 Enter 跳過)")
    custom_rules = ""
    custom_input = input(f"{Colors.BLUE}自訂規則{Colors.END}: ").strip()
    if custom_input:
        custom_rules = custom_input

    return {
        'name': name,
        'language': language,
        'use_cases': use_cases or ['automation'],
        'safety_rules': safety_rules or ['no_env', 'no_auto_push'],
        'communication': communication,
        'custom_rules': custom_rules,
    }


def preset_mode(preset_name: str) -> Dict:
    """Load preset configuration."""
    if preset_name not in PRESETS:
        print(f"{Colors.RED}✗ Unknown preset: {preset_name}{Colors.END}")
        print(f"Available presets: {', '.join(PRESETS.keys())}")
        sys.exit(1)

    preset = PRESETS[preset_name]
    print_success(f"Loaded preset: {preset['name']}")
    return preset


def generate_claude_md(config: Dict) -> str:
    """Generate complete CLAUDE.md content."""
    sections = []

    # Header
    sections.append(f"# {config['name']} — Claude Code 工作規則")

    # Identity
    sections.append(generate_identity_section(config['name'], config['language']))

    # Core rules
    sections.append(generate_core_rules())

    # Use cases
    use_case_section = generate_use_cases_section(config.get('use_cases', []))
    if use_case_section:
        sections.append(use_case_section)

    # Safety
    sections.append(generate_safety_section(config.get('safety_rules', [])))

    # Communication
    sections.append(generate_communication_section(config.get('communication', 'direct')))

    # Custom
    custom = generate_custom_section(config.get('custom_rules', ''))
    if custom:
        sections.append(custom)

    # Final notes
    sections.append(generate_final_notes())

    return "\n".join(sections)


def display_preview(content: str) -> None:
    """Display preview of generated CLAUDE.md."""
    print_section("產生的 CLAUDE.md 預覽")
    print(f"{Colors.CYAN}{content}{Colors.END}")


def save_to_file(content: str, filepath: Path) -> bool:
    """Save content to file."""
    try:
        filepath.write_text(content, encoding='utf-8')
        print_success(f"已寫入 {filepath}")
        return True
    except Exception as e:
        print(f"{Colors.RED}✗ 寫入失敗: {e}{Colors.END}")
        return False


def main():
    """Main entry point."""
    # Parse arguments
    preset_name = None
    output_path = Path('CLAUDE.md')
    no_confirm = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--preset' and i + 1 < len(args):
            preset_name = args[i + 1]
            i += 2
        elif args[i].startswith('--preset='):
            preset_name = args[i].split('=', 1)[1]
            i += 1
        elif args[i] == '--output' and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        elif args[i].startswith('--output='):
            output_path = Path(args[i].split('=', 1)[1])
            i += 1
        elif args[i] in ('--no-confirm', '-y'):
            no_confirm = True
            i += 1
        elif args[i] in ('--help', '-h'):
            print("Usage: python3 generate_claude_md.py [OPTIONS]")
            print("  --preset=NAME    Quick preset: bot, web, scraper, trader")
            print("  --output=PATH    Output file path (default: ./CLAUDE.md)")
            print("  --no-confirm, -y Skip confirmation, write directly")
            print("  --help, -h       Show this help")
            sys.exit(0)
        else:
            i += 1

    # Get configuration
    if preset_name:
        config = preset_mode(preset_name)
    else:
        try:
            config = interactive_mode()
        except EOFError:
            print(f"\n{Colors.YELLOW}Non-interactive terminal detected. Use --preset=bot/web/scraper/trader{Colors.END}")
            sys.exit(1)

    # Generate content
    claude_md_content = generate_claude_md(config)

    # Display preview
    display_preview(claude_md_content)

    # Ask to save (skip if --no-confirm)
    if no_confirm:
        save_to_file(claude_md_content, output_path)
        print_success(f"Saved to {output_path}")
    else:
        print_section("確認保存")
        try:
            response = input(f"{Colors.YELLOW}要寫入 {output_path} 嗎？ (Y/n){Colors.END}: ").strip().lower()
        except EOFError:
            response = 'y'

        if response in ('y', 'yes', ''):
            if save_to_file(claude_md_content, output_path):
                print_success(f"完成！你的 CLAUDE.md 已準備好")
                print(f"{Colors.CYAN}下次用 Claude Code 時，它會讀到這些規則{Colors.END}\n")
            else:
                sys.exit(1)
        else:
            print(f"{Colors.YELLOW}已取消保存{Colors.END}")
            sys.exit(0)


if __name__ == '__main__':
    main()
