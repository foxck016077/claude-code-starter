#!/usr/bin/env python3
"""
Claude Code Hooks Installer — One-click setup for common hooks
讓小白一鍵安裝常用 hooks，無需手工編寫 shell script
"""

import os
import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

# 常數設定
HOOKS_DIR = Path(__file__).parent
CLAUDE_HOME = Path.home() / ".claude"
SETTINGS_FILE = CLAUDE_HOME / "settings.json"
HOOKS_INSTALL_DIR = CLAUDE_HOME / "hooks"

# Hook 套裝定義
HOOK_PACKS = {
    "safety": {
        "desc": "🔒 Safety Pack — 防止危險操作",
        "hooks": [
            {
                "name": "prevent-dangerous-commands",
                "source": "safety/prevent-dangerous-commands.sh",
                "event": "PreToolUse",
                "tools": ["Bash"],
                "desc": "攔截 rm -rf, git push --force 等危險指令"
            },
            {
                "name": "protect-env-files",
                "source": "safety/protect-env-files.sh",
                "event": "PreToolUse",
                "tools": ["Read", "Edit", "Write"],
                "desc": "禁止讀取/修改 .env, credentials 等敏感檔案"
            },
            {
                "name": "no-auto-push",
                "source": "safety/no-auto-push.sh",
                "event": "PreToolUse",
                "tools": ["Bash"],
                "desc": "禁止自動 git push（必須手動執行）"
            }
        ]
    },
    "quality": {
        "desc": "✨ Quality Pack — 品質控制",
        "hooks": [
            {
                "name": "read-before-edit",
                "source": "quality/read-before-edit.sh",
                "event": "PreToolUse",
                "tools": ["Edit"],
                "desc": "強制先讀檔再改（>100 行警告）"
            },
            {
                "name": "lint-after-write",
                "source": "quality/lint-after-write.sh",
                "event": "PostToolUse",
                "tools": ["Write", "Edit"],
                "desc": "寫完 .py/.js 自動跑 linter（ruff/eslint）"
            }
        ]
    },
    "productivity": {
        "desc": "⚡ Productivity Pack — 效率提升",
        "hooks": [
            {
                "name": "auto-commit-reminder",
                "source": "productivity/auto-commit-reminder.sh",
                "event": "PostToolUse",
                "tools": ["Edit", "Write"],
                "desc": "改動 >5 個檔案時提醒 commit"
            }
        ]
    }
}


def load_settings():
    """讀取 settings.json，若不存在則傳回空 dict"""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"⚠️  Warning: {SETTINGS_FILE} is corrupted, starting fresh")
            return {}
    return {}


def save_settings(settings):
    """保存 settings.json，並備份原檔"""
    # 建立備份
    if SETTINGS_FILE.exists():
        backup_file = SETTINGS_FILE.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        shutil.copy2(SETTINGS_FILE, backup_file)
        print(f"✓ Backup created: {backup_file}")

    # 建立目錄（若不存在）
    CLAUDE_HOME.mkdir(parents=True, exist_ok=True)

    # 寫入 settings.json
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print(f"✓ Settings saved to {SETTINGS_FILE}")


def copy_hook_script(hook_def):
    """複製 hook 腳本到 ~/.claude/hooks/"""
    source_path = HOOKS_DIR / hook_def["source"]
    dest_path = HOOKS_INSTALL_DIR / f"{hook_def['name']}.sh"

    if not source_path.exists():
        print(f"❌ Error: Hook source not found: {source_path}")
        return False

    # 建立目錄
    HOOKS_INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    # 複製並設定執行權限
    shutil.copy2(source_path, dest_path)
    os.chmod(dest_path, 0o755)

    print(f"   ✓ Installed: {dest_path}")
    return True


def register_hook_in_settings(settings, hook_def):
    """在 settings.json 中註冊 hook"""
    if "hooks" not in settings:
        settings["hooks"] = {}

    event = hook_def["event"]
    if event not in settings["hooks"]:
        settings["hooks"][event] = []

    # 檢查是否已存在（避免重複）
    existing_names = [h.get("name") for h in settings["hooks"][event]]
    if hook_def["name"] not in existing_names:
        settings["hooks"][event].append({
            "name": hook_def["name"],
            "handler": f"{HOOKS_INSTALL_DIR / hook_def['name']}.sh",
            "tools": hook_def.get("tools", [])
        })
        return True
    return False


def interactive_menu():
    """互動選擇要安裝哪些 hooks"""
    print("\n" + "="*60)
    print("Claude Code Hooks Installer")
    print("="*60)
    print("\nAvailable Hook Packs:\n")

    packs = list(HOOK_PACKS.items())
    for idx, (key, pack) in enumerate(packs, 1):
        print(f"{idx}. {pack['desc']}")
        print(f"   • {len(pack['hooks'])} hooks included")
        print()

    print("Options:")
    print("  0. All (全裝)")
    print("  X. Safety only (只裝安全)")
    print("  Y. Quality only (只裝品質)")
    print("  Z. Productivity only (只裝效率)")
    print("  Q. Quit")
    print()

    choice = input("Choose (0/1/2/3/X/Y/Z/Q): ").upper().strip()
    return choice


def get_selected_packs(choice):
    """根據選擇傳回要安裝的套裝"""
    if choice == "0":
        return list(HOOK_PACKS.keys())
    elif choice == "1":
        return ["safety"]
    elif choice == "2":
        return ["quality"]
    elif choice == "3":
        return ["productivity"]
    elif choice == "X":
        return ["safety"]
    elif choice == "Y":
        return ["quality"]
    elif choice == "Z":
        return ["productivity"]
    elif choice == "Q":
        return []
    else:
        print("Invalid choice")
        return []


def install_hooks(selected_packs, settings):
    """安裝選中的 hooks"""
    total_hooks = 0

    print(f"\n{'='*60}")
    print(f"Installing {len(selected_packs)} hook pack(s)...")
    print(f"{'='*60}\n")

    for pack_key in selected_packs:
        if pack_key not in HOOK_PACKS:
            continue

        pack = HOOK_PACKS[pack_key]
        print(f"📦 {pack['desc']}")

        for hook_def in pack["hooks"]:
            # 複製腳本
            if copy_hook_script(hook_def):
                # 註冊到 settings.json
                if register_hook_in_settings(settings, hook_def):
                    print(f"   → Registered in settings.json")
                    total_hooks += 1
                else:
                    print(f"   ⚠️  Already registered (skipped)")

        print()

    return total_hooks


def show_summary(settings):
    """顯示安裝摘要"""
    print(f"{'='*60}")
    print("✓ Installation Complete!")
    print(f"{'='*60}\n")

    print(f"Total hooks registered: {sum(len(h) for h in settings.get('hooks', {}).values())}\n")

    if "hooks" in settings:
        for event, hooks in settings["hooks"].items():
            print(f"  {event}:")
            for hook in hooks:
                print(f"    • {hook['name']}")

    print(f"\nLocation: {HOOKS_INSTALL_DIR}")
    print(f"Settings: {SETTINGS_FILE}")
    print("\nNext steps:")
    print("  1. Review the installed hooks (optional)")
    print("  2. Reload Claude Code or restart your terminal")
    print("  3. Hooks will activate automatically on next session")
    print()


def main():
    """主程式"""
    args = sys.argv[1:]

    # 處理命令行參數
    if "--all" in args:
        selected = list(HOOK_PACKS.keys())
    elif "--safety" in args:
        selected = ["safety"]
    elif "--quality" in args:
        selected = ["quality"]
    elif "--productivity" in args:
        selected = ["productivity"]
    else:
        # 互動模式
        choice = interactive_menu()
        selected = get_selected_packs(choice)

    if not selected:
        print("Installation cancelled.")
        sys.exit(0)

    # 讀取現有設定
    settings = load_settings()

    # 安裝 hooks
    total = install_hooks(selected, settings)

    # 保存設定
    save_settings(settings)

    # 顯示摘要
    show_summary(settings)

    if total == 0:
        print("⚠️  No new hooks were installed (all already registered)")

    sys.exit(0)


if __name__ == "__main__":
    main()
