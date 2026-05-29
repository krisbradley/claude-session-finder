#!/usr/bin/env python3
"""Render a fake csf fzf UI for demo GIF recording via asciinema+agg."""
import sys, time, re

C = '\033[36m'
D = '\033[2m'
R = '\033[0m'
G = '\033[32m'
BG = '\033[92m'
Y = '\033[33m'
M = '\033[35m'
BR = '\033[91m'
DW = '\033[2;37m'
B = '\033[1m'

COLS = 110
ROWS = 28
LW = 48
RW = 59
PW = RW - 2

SESSIONS = [
    ("now", BG,  12, "Claude session finder",               0),
    (" 3h", G,    9, "Download audio from YouTube video",    1),
    (" 1d", Y,   18, "Build iPad cash register app",         2),
    (" 2d", Y,    7, "Find most recently changed files",     3),
    (" 3d", Y,    5, "Investigate computer overheating",     4),
    (" 5d", DW,  14, "Compress video to under 10MB",         5),
    (" 7d", DW,   3, "Create pixel art martlet character",   6),
    (" 9d", DW,  22, "Set up home network monitoring",       7),
]

PREVIEWS = {
    0: {
        "title": "Implementing csf session finder tool",
        "project": "~/dev/claude-session-finder",
        "started": "2026-05-29 14:30",
        "duration": "2h 15m",
        "msgs": 12,
        "conv": [
            ("14:30", "make a session finder for claude"),
            ("14:32", "add fzf integration with preview"),
            ("14:45", "support CLAUDE_CONFIG_DIR env var"),
            ("14:52", "fix named sessions not appearing"),
            ("15:10", "add search functionality"),
            ("15:30", "update homebrew formula"),
        ],
        "more": 6,
    },
    1: {
        "title": "Download and convert YouTube audio",
        "project": "~/dev/scripts",
        "started": "2026-05-29 11:15",
        "duration": "45m",
        "msgs": 9,
        "conv": [
            ("11:15", "download audio from this youtube vid"),
            ("11:18", "convert it to mp3 format"),
            ("11:22", "trim the first 30 seconds"),
            ("11:30", "normalize the volume levels"),
        ],
        "more": 5,
    },
    2: {
        "title": "Build cash register POS app for iPad",
        "project": "~/dev/register-app",
        "started": "2026-05-28 09:00",
        "duration": "4h 30m",
        "msgs": 18,
        "conv": [
            ("09:00", "build an ipad cash register app"),
            ("09:15", "add product catalog with categories"),
            ("09:30", "implement barcode scanner support"),
            ("09:45", "add cart and checkout flow"),
            ("10:15", "integrate stripe payment processing"),
            ("10:45", "add receipt printing via AirPrint"),
        ],
        "more": 12,
    },
    3: {
        "title": "Find recently modified files in project",
        "project": "~/dev/toolbox",
        "started": "2026-05-27 16:20",
        "duration": "25m",
        "msgs": 7,
        "conv": [
            ("16:20", "find the most recently changed files"),
            ("16:22", "sort by modification date"),
            ("16:25", "filter to only python files"),
            ("16:30", "show git blame for each"),
        ],
        "more": 3,
    },
    4: {
        "title": "Diagnose CPU overheating issues",
        "project": "~/dev/system-tools",
        "started": "2026-05-26 13:00",
        "duration": "1h 10m",
        "msgs": 5,
        "conv": [
            ("13:00", "my computer keeps overheating"),
            ("13:10", "check which processes use most cpu"),
            ("13:25", "monitor temperature sensors"),
            ("13:40", "create a fan speed control script"),
        ],
        "more": 1,
    },
    5: {
        "title": "Compress large video file under 10MB",
        "project": "~/dev/media-tools",
        "started": "2026-05-24 10:00",
        "duration": "50m",
        "msgs": 14,
        "conv": [
            ("10:00", "compress this video to under 10mb"),
            ("10:05", "try h265 encoding, lower bitrate"),
            ("10:15", "reduce resolution to 720p"),
            ("10:25", "strip audio track to save space"),
            ("10:35", "two-pass encoding for quality"),
        ],
        "more": 9,
    },
}


def vlen(s):
    return len(re.sub(r'\033\[[0-9;]*m', '', s))


def rpad(s, width):
    return s + ' ' * max(0, width - vlen(s))


def preview_lines(preview_id):
    if preview_id not in PREVIEWS:
        return [''] * (ROWS - 4)
    p = PREVIEWS[preview_id]
    sep = '─' * PW
    lines = []
    lines.append(sep)
    t = p["title"]
    if len(t) > PW - 4:
        t = t[:PW - 6] + ".."
    lines.append(f"  {t}")
    lines.append(sep)
    lines.append(f" Project:   {p['project']}")
    lines.append(f" Started:   {p['started']}")
    lines.append(f" Duration:  {p['duration']}")
    lines.append(f" Messages:  {p['msgs']}")
    lines.append(sep)
    lines.append("")
    lines.append(sep)
    for ts, msg in p["conv"]:
        entry = f" {ts}  {msg}"
        if len(entry) > PW:
            entry = entry[:PW - 2] + ".."
        lines.append(entry)
    if p["more"] > 0:
        lines.append(f"  ... +{p['more']} more")
    lines.append(sep)
    while len(lines) < ROWS - 4:
        lines.append("")
    return lines[:ROWS - 4]


def draw(sel=0, query="", sessions=None, count_total=None):
    if sessions is None:
        sessions = SESSIONS
    if count_total is None:
        count_total = len(SESSIONS)
    count_str = f"{len(sessions)}/{count_total}"

    # Determine which preview to show based on selected session's original index
    if sel < len(sessions):
        pid = sessions[sel][4]
    else:
        pid = -1
    plines = preview_lines(pid)

    bdr = D
    rst = R

    # Top border with label
    label = f" {B}{M}✦{rst} {B}{M}Claude Session Finder{rst} {B}{M}✦{rst} "
    label_vlen = 26
    ld = (COLS - 2 - label_vlen) // 2
    rd = COLS - 2 - label_vlen - ld
    sys.stdout.write(f'\033[1;1H{bdr}╭{"─" * ld}{rst}{label}{bdr}{"─" * rd}╮{rst}')

    # Content rows (2 through ROWS-1)
    for row in range(2, ROWS):
        # Left pane content
        left = ""
        if row == 2:
            left = f"  {D}{count_str}{rst}"
        elif row == 3:
            left = f"  {D}time│   # │ description{rst}"
        elif row == 4:
            cur = "|" if query else ""
            left = f"  {M}>{rst} {query}{cur}"
        elif 5 <= row <= 4 + len(sessions):
            idx = row - 5
            s = sessions[idx]
            tago, tcol, msgs, title, _ = s
            ptr = f"{BR}>{rst}" if idx == sel else " "
            max_t = LW - 15
            if len(title) > max_t:
                title = title[:max_t - 2].rstrip() + ".."
            left = f" {ptr} {tcol}{tago}{rst} {D}│{rst} {C}{msgs:>3}{rst} {D}│{rst} {title}"
        elif row == ROWS - 2:
            left = f" {D}enter{rst} open  {D}^d{rst} del  {D}^e{rst} export  {D}^y{rst} copy id"

        # Right pane content
        pidx = row - 2
        right = plines[pidx] if pidx < len(plines) else ""

        # Build the full line: │<left padded to LW>│ <right padded to RW>│
        line = f"{bdr}│{rst}{rpad(left, LW)}{bdr}│{rst} {rpad(right, RW - 1)}{bdr}│{rst}"
        sys.stdout.write(f'\033[{row};1H{line}')

    # Bottom border
    ld2 = 49 - 1
    rd2 = COLS - 2 - ld2 - 1
    sys.stdout.write(f'\033[{ROWS};1H{bdr}╰{"─" * ld2}┴{"─" * rd2}╯{rst}')
    sys.stdout.flush()


def filt(query):
    q = query.lower()
    return [s for s in SESSIONS if q in s[3].lower()]


def main():
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

    # 1. Show initial UI
    draw(0)
    time.sleep(2.0)

    # 2. Navigate down
    for i in range(1, 5):
        time.sleep(0.4)
        draw(i)
    time.sleep(0.8)

    # 3. Navigate back up
    for i in range(3, 0, -1):
        time.sleep(0.3)
        draw(i)
    time.sleep(0.6)

    # 4. Search "compress" — filter progressively
    q = "compress"
    for j in range(1, len(q) + 1):
        time.sleep(0.12)
        f = filt(q[:j]) or SESSIONS
        draw(0, q[:j], sessions=f)
    time.sleep(1.5)

    # 5. Clear search
    for j in range(len(q) - 1, 0, -1):
        time.sleep(0.05)
        f = filt(q[:j]) or SESSIONS
        draw(0, q[:j], sessions=f)
    draw(0, "")
    time.sleep(0.5)

    # 6. Search "ipad" — filter progressively
    q2 = "ipad"
    for j in range(1, len(q2) + 1):
        time.sleep(0.12)
        f = filt(q2[:j]) or SESSIONS
        draw(0, q2[:j], sessions=f)
    time.sleep(1.5)

    # 7. Clear and return to full list
    for j in range(len(q2) - 1, 0, -1):
        time.sleep(0.05)
        f = filt(q2[:j]) or SESSIONS
        draw(0, q2[:j], sessions=f)
    draw(0, "")
    time.sleep(1.5)

    sys.stdout.write('\033[?25h')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
