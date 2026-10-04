import os
from datetime import datetime
from math import ceil
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image

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


# Fix paste_image to support RGBA alpha transparency
def custom_paste_image(
    self,
    image_file: str,
    row_num: int,
    col_num: int = 1,
    size_multiplier: float = 1,
) -> None:
    x1, y1, _, _ = self.cursor_to_box(row_num, col_num, 1, 1, True, True)
    with Image.open(image_file) as image:
        image_width, image_height = image.size
        image = image.resize(
            (
                int(image_width * size_multiplier),
                int(image_height * size_multiplier),
            ),
            Image.Resampling.LANCZOS,
        )
        font_h = getattr(self, "_Terminal__font_height")
        line_s = getattr(self, "_Terminal__line_spacing")
        font_w = getattr(self, "_Terminal__font_width")
        rows_covered = ceil(image.height / (font_h + line_s))
        cols_covered = ceil(image.width / font_w) + 1
        col_in_row = getattr(self, "_Terminal__col_in_row")
        for i in range(rows_covered):
            col_in_row[row_num + i] = cols_covered
        self.image_col = col_num + cols_covered
        frame = getattr(self, "_Terminal__frame")
        mask = image if image.mode == "RGBA" else None
        frame.paste(image, (x1, y1), mask=mask)
        gen_frame = getattr(self, "_Terminal__gen_frame")
        gen_frame(frame)


gifos.Terminal.paste_image = custom_paste_image

FONT_FILE_LOGO = "./fonts/vtks-blocketo.regular.ttf"
FONT_FILE_BITMAP = "./fonts/ter-u14n.pil"
AVATAR_FILE = "./assets/avatar.png"


def main():
    # Terminal dimensions: 780x520
    t = gifos.Terminal(780, 520, 15, 15, FONT_FILE_BITMAP, 15)

    # Clean custom prompt: notern@cachyos ~>
    t.set_prompt("\x1b[0;92mnotern\x1b[0m@\x1b[0;94mcachyos \x1b[90m~>\x1b[0m ")

    year_now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y")
    time_now = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%a %b %d %I:%M:%S %p %Z %Y")

    # 1. BIOS boot phase (minimal & sleek)
    t.gen_text("", 1, count=8)
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
    t.gen_text("Memory Test: 64MB OK", 7, count=6, contin=True)
    t.gen_text("", 10, count=4, contin=True)

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
    t.clone_frame(4)
    t.toggle_show_cursor(True)
    t.gen_typing_text("\x1b[91mfetch.s", 1, contin=True)
    t.delete_row(1, prompt_col)
    t.gen_text("\x1b[92mfetch.sh\x1b[0m", 1, contin=True)
    t.gen_typing_text(" -u notern", 1, contin=True)

    # 6. Fetch stats output with avatar
    t.clear_frame()
    t.toggle_show_cursor(False)

    # Paste pixel ghost avatar seamlessly on the left
    if os.path.exists(AVATAR_FILE):
        t.paste_image(AVATAR_FILE, 3, 2, size_multiplier=0.52)

    fetch_lines = """\x1b[30;46m notern@cachyos \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mOS:        \x1b[97mCachyOS Linux x86_64\x1b[0m
\x1b[96mWM:        \x1b[97mHyprland (Wayland)\x1b[0m
\x1b[96mShell:     \x1b[97mzsh 5.9 (p10k)\x1b[0m
\x1b[96mEditor:    \x1b[97mNeovim\x1b[0m

\x1b[30;45m Focus Areas \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mLanguages: \x1b[93mJava · C\x1b[0m
\x1b[96mDomain:    \x1b[95mCybersecurity & Network Engineering\x1b[0m
\x1b[96mSecurity:  \x1b[92mLow-Level & Embedded Security\x1b[0m

\x1b[30;44m Contact \x1b[0m
\x1b[90m--------------------------------------------------\x1b[0m
\x1b[96mLinkedIn:  \x1b[94mzainul-mutaqin\x1b[0m
\x1b[96mPortfolio: \x1b[94mzainulmutaqin.vercel.app\x1b[0m
\x1b[96mEmail:     \x1b[94makuzainul176@gmail.com\x1b[0m"""

    text_col = 25  # Right next to avatar
    t.gen_text(fetch_lines, 2, text_col, count=5, contin=True)

    t.gen_prompt(t.curr_row)
    t.toggle_show_cursor(True)
    t.gen_typing_text(
        "\x1b[90m# ready.\x1b[0m",
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
