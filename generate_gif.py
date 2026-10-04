import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# 1. Setup local / user config for Catppuccin Frappe
config_dir = Path.home() / ".config" / "gifos"
config_dir.mkdir(parents=True, exist_ok=True)

with open(config_dir / "ansi_escape_colors.toml", "w") as f:
    f.write("""[catppuccin-frappe]
[catppuccin-frappe.default_colors]
bg = "#303446"
fg = "#C6D0F5"

[catppuccin-frappe.normal_colors]
black = "#51576D"
red = "#E78284"
green = "#A6D189"
yellow = "#E5C890"
blue = "#8CAAEE"
magenta = "#CA9EE6"
cyan = "#81C8BE"
white = "#C6D0F5"

[catppuccin-frappe.bright_colors]
black = "#626880"
red = "#EA999C"
green = "#A6D189"
yellow = "#EF9F76"
blue = "#85C1DC"
magenta = "#F4B8E4"
cyan = "#81C8BE"
white = "#B5BFE2"
""")

with open(config_dir / "gifos_settings.toml", "w") as f:
    f.write("""[general]
color_scheme = "catppuccin-frappe"
fps = 15
loop_count = 0
user_name = "notern"
""")

import gifos
from gifos.utils import fetch_github_stats

FONT_FILE_LOGO = "./fonts/vtks-blocketo.regular.ttf"
FONT_FILE_BITMAP = "./fonts/ter-u14n.pil"
AVATAR_FILE = "./assets/avatar.png"


def main():
    # Terminal dimensions: 780x520 (optimized 3:2 ratio)
    t = gifos.Terminal(780, 520, 15, 15, FONT_FILE_BITMAP, 15)

    year_now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y")
    time_now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%a %b %d %I:%M:%S %p %Z %Y")

    # 1. BIOS boot phase
    t.gen_text("", 1, count=10)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[96mNOTERN-BIOS (CachyOS Edition) v2.6.4\x1b[0m", 1)
    t.gen_text(f"Copyright (C) {year_now}, \x1b[31mNotern Systems\x1b[0m", 2)
    t.gen_text("\x1b[94mHyprland Wayland Compositor - Arch/Cachy Kernel\x1b[0m", 4)
    t.gen_text("CPU: AMD / ARM64 @ 4.20GHz - Low-Level Systems Arch", 6)
    t.gen_text(
        "Press \x1b[94mDEL\x1b[0m to enter SETUP, \x1b[94mESC\x1b[0m to skip Memory Test",
        t.num_rows,
    )
    for i in range(0, 65653, 13107):
        t.delete_row(7)
        t.gen_text(f"Memory Test: {i} KB", 7, contin=True)
    t.delete_row(7)
    t.gen_text("Memory Test: 64MB OK", 7, count=8, contin=True)
    t.gen_text("", 10, count=5, contin=True)

    # 2. Scramble logo boot
    t.clear_frame()
    t.gen_text("Initiating Boot Sequence ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.set_font(FONT_FILE_LOGO, 60)
    os_logo = "NOTERN"
    mid_row = (t.num_rows + 1) // 2
    mid_col = (t.num_cols - len(os_logo) + 1) // 2
    effect_lines = gifos.effects.text_scramble_effect_lines(
        os_logo, 3, include_special=False
    )
    for i in range(len(effect_lines)):
        t.delete_row(mid_row + 1)
        t.gen_text(f"\x1b[95m{effect_lines[i]}\x1b[0m", mid_row + 1, mid_col + 1)

    # 3. Login phase
    t.set_font(FONT_FILE_BITMAP, 15)
    t.clear_frame()
    t.clone_frame(4)
    t.toggle_show_cursor(False)
    t.gen_text("\x1b[93mCachyOS Linux 6.13.0-cachy (tty1)\x1b[0m", 1, count=4)
    t.gen_text("login: ", 3, count=4)
    t.toggle_show_cursor(True)
    t.gen_typing_text("notern", 3, contin=True)
    t.gen_text("", 4, count=4)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=4)
    t.toggle_show_cursor(True)
    t.gen_typing_text("********", 4, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text(f"Last login: {time_now} on tty1", 6)

    # 4. Command typing
    t.gen_prompt(7, count=4)
    prompt_col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mclea", 7, contin=True)
    t.delete_row(7, prompt_col)
    t.gen_text("\x1b[92mclear\x1b[0m", 7, count=2, contin=True)

    # 5. Fetch command
    t.clear_frame()
    t.gen_prompt(1)
    prompt_col = t.curr_col
    t.clone_frame(5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u notern", 1, contin=True)

    # 6. Fetch stats output with avatar
    t.clear_frame()
    t.toggle_show_cursor(False)

    # Paste pixel ghost avatar on the left
    if os.path.exists(AVATAR_FILE):
        t.paste_image(AVATAR_FILE, 3, 2, size_multiplier=0.52)

    # Fetch live stats or fallback
    gh_token = os.getenv("GITHUB_TOKEN")
    stars = "17"
    commits = "3,600+"
    prs = "25"
    top_langs = "Java, C, TypeScript, Python"
    rank = "A"

    if gh_token:
        try:
            stats = fetch_github_stats("zaincyty")
            stars = str(stats.total_stargazers)
            commits = f"{stats.total_commits_last_year:,}"
            prs = str(stats.total_pull_requests_made)
            rank = stats.user_rank.level
            if stats.languages_sorted:
                top_langs = ", ".join([l[0] for l in stats.languages_sorted[:4]])
        except Exception as e:
            print("Notice: fetch_github_stats error, using defaults:", e)

    fetch_lines = f"""\x1b[30;46m notern@cachyos \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mOS:        \x1b[97mCachyOS Linux x86_64\x1b[0m
\x1b[96mWM:        \x1b[97mHyprland (Wayland)\x1b[0m
\x1b[96mTerminal:  \x1b[97mAlacritty + Zsh (p10k)\x1b[0m
\x1b[96mFocus:     \x1b[93mJava · C · Low-Level Systems\x1b[0m
\x1b[96mDomain:    \x1b[95mCybersecurity & Network Engineering\x1b[0m
\x1b[96mSecurity:  \x1b[92mEmbedded Security · Reverse Engineering\x1b[0m

\x1b[30;45m Contact \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mLinkedIn:  \x1b[94mzainul-mutaqin\x1b[0m
\x1b[96mPortfolio: \x1b[94mzainulmutaqin.vercel.app\x1b[0m
\x1b[96mEmail:     \x1b[94makuzainul176@gmail.com\x1b[0m

\x1b[30;43m GitHub Stats \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mRating:    \x1b[92mRank {rank}\x1b[0m
\x1b[96mCommits:   \x1b[97m{commits}\x1b[0m (last year)
\x1b[96mStars:     \x1b[97m{stars}\x1b[0m  |  \x1b[96mPRs: \x1b[97m{prs}\x1b[0m
\x1b[96mLanguages: \x1b[93m{top_langs}\x1b[0m"""

    text_col = 25  # Right next to avatar
    t.gen_text(fetch_lines, 2, text_col, count=5, contin=True)

    t.gen_prompt(t.curr_row)
    t.toggle_show_cursor(True)
    t.gen_typing_text(
        "\x1b[92m# \"Talk is cheap. Show me the code.\" // Close to the metal\x1b[0m",
        t.curr_row,
        contin=True,
    )

    # Freeze final frame for ~6 seconds
    t.gen_text("", t.curr_row, count=90, contin=True)

    # Generate gif
    print("INFO: Generating GIF...")
    t.gen_gif()
    print("INFO: GIF generation complete -> output.gif")


if __name__ == "__main__":
    main()
