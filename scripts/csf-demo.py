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
PURPLE = '\033[38;5;141m'
ORANGE = '\033[38;5;208m'

COLS = 110
ROWS = 28
LW = 48
RW = 59
PW = RW - 2

SESSIONS = [
    ("now", BG,   8, "Refactor auth middleware for JWT",      0, None),
    (" 1h", BG,  14, "Debug flaky integration tests",         1, None),
    (" 3h", G,    6, "Add dark mode to settings page",        2, "cyan"),
    (" 1d", Y,   22, "Migrate database to Postgres 16",       3, None),
    (" 2d", Y,   11, "Build iPad cash register app",          4, "orange"),
    (" 4d", Y,    9, "Set up CI/CD pipeline for monorepo",    5, None),
    (" 1w", DW,  17, "Compress video to under 10MB",          6, None),
    ("2w",  DW,   4, "Create pixel art character sprites",    7, "purple"),
]

SESSION_COLORS = {
    "cyan": '\033[36m',
    "orange": '\033[38;5;208m',
    "purple": '\033[38;5;141m',
}

PREVIEWS = {
    0: {
        "title": "Refactor auth middleware for JWT",
        "project": "~/dev/api-server",
        "started": "2026-06-08 10:15",
        "duration": "1h 45m",
        "msgs": 8,
        "conv": [
            ("10:15", "refactor the auth middleware to use JWT"),
            ("10:20", "extract token validation into its own module"),
            ("10:35", "add refresh token rotation"),
            ("10:50", "write tests for token expiry edge cases"),
            ("11:10", "update the openapi spec for new headers"),
        ],
        "more": 3,
    },
    1: {
        "title": "Debug flaky integration tests",
        "project": "~/dev/api-server",
        "started": "2026-06-08 08:30",
        "duration": "2h 10m",
        "msgs": 14,
        "conv": [
            ("08:30", "the user_signup test keeps failing on CI"),
            ("08:35", "check if it's a race condition"),
            ("08:50", "found it — shared db state between tests"),
            ("09:10", "add transaction rollback per test"),
            ("09:30", "run the full suite 5 times to confirm"),
            ("09:45", "also fix the flaky payment_flow test"),
        ],
        "more": 8,
    },
    2: {
        "title": "Add dark mode to settings page",
        "project": "~/dev/web-app",
        "started": "2026-06-08 06:00",
        "duration": "55m",
        "msgs": 6,
        "conv": [
            ("06:00", "add dark mode toggle to settings"),
            ("06:10", "use css custom properties for theming"),
            ("06:25", "persist preference in localStorage"),
            ("06:35", "respect prefers-color-scheme default"),
        ],
        "more": 2,
    },
    3: {
        "title": "Migrate database to Postgres 16",
        "project": "~/dev/infrastructure",
        "started": "2026-06-07 09:00",
        "duration": "5h 20m",
        "msgs": 22,
        "conv": [
            ("09:00", "plan the postgres 14 to 16 migration"),
            ("09:20", "set up pg_upgrade with --link mode"),
            ("09:45", "test migration on staging snapshot"),
            ("10:30", "fix incompatible extensions"),
            ("11:00", "benchmark query performance after"),
            ("11:30", "write runbook for production cutover"),
        ],
        "more": 16,
    },
    4: {
        "title": "Build cash register POS app for iPad",
        "project": "~/dev/register-app",
        "started": "2026-06-06 09:00",
        "duration": "4h 30m",
        "msgs": 11,
        "conv": [
            ("09:00", "build an ipad cash register app"),
            ("09:15", "add product catalog with categories"),
            ("09:30", "implement barcode scanner support"),
            ("09:45", "add cart and checkout flow"),
            ("10:15", "integrate stripe payment processing"),
            ("10:45", "add receipt printing via AirPrint"),
        ],
        "more": 5,
    },
    5: {
        "title": "Set up CI/CD pipeline for monorepo",
        "project": "~/dev/platform",
        "started": "2026-06-04 14:00",
        "duration": "2h 15m",
        "msgs": 9,
        "conv": [
            ("14:00", "set up github actions for our monorepo"),
            ("14:15", "only build changed packages on push"),
            ("14:30", "add caching for node_modules and turbo"),
            ("14:50", "deploy preview envs for each PR"),
            ("15:10", "add slack notifications for failures"),
        ],
        "more": 4,
    },
    6: {
        "title": "Compress large video file under 10MB",
        "project": "~/dev/media-tools",
        "started": "2026-06-01 10:00",
        "duration": "50m",
        "msgs": 17,
        "conv": [
            ("10:00", "compress this video to under 10mb"),
            ("10:05", "try h265 encoding, lower bitrate"),
            ("10:15", "reduce resolution to 720p"),
            ("10:25", "strip audio track to save space"),
            ("10:35", "two-pass encoding for quality"),
        ],
        "more": 12,
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
    lines.append(f"📁 Project:   {p['project']}")
    lines.append(f"📅 Started:   {p['started']}")
    lines.append(f"⏱️  Duration:  {p['duration']}")
    lines.append(f"💬 Messages:  {p['msgs']}")
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

    if sel < len(sessions):
        pid = sessions[sel][4]
    else:
        pid = -1
    plines = preview_lines(pid)

    bdr = D
    rst = R

    label = f" {B}{M}✦{rst} {B}{M}Claude Session Finder{rst} {B}{M}✦{rst} "
    label_vlen = 26
    ld = (COLS - 2 - label_vlen) // 2
    rd = COLS - 2 - label_vlen - ld
    sys.stdout.write(f'\033[1;1H{bdr}╭{"─" * ld}{rst}{label}{bdr}{"─" * rd}╮{rst}')

    for row in range(2, ROWS):
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
            tago, tcol, msgs, title, _, color = s
            ptr = f"{BR}❯{rst}" if idx == sel else " "
            max_t = LW - 15
            if len(title) > max_t:
                title = title[:max_t - 2].rstrip() + ".."
            if color and color in SESSION_COLORS:
                title = f"{SESSION_COLORS[color]}{title}{rst}"
            left = f" {ptr} {tcol}{tago}{rst} {D}│{rst} {C}{msgs:>3}{rst} {D}│{rst} {title}"
        elif row == ROWS - 2:
            left = f" {D}enter{rst} open  {D}^d{rst} delete  {D}^e{rst} export  {D}^y{rst} copy id  {D}^p{rst} project"

        pidx = row - 2
        right = plines[pidx] if pidx < len(plines) else ""

        line = f"{bdr}│{rst}{rpad(left, LW)}{bdr}│{rst} {rpad(right, RW - 1)}{bdr}│{rst}"
        sys.stdout.write(f'\033[{row};1H{line}')

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

    draw(0)
    time.sleep(2.0)

    # Navigate down through sessions
    for i in range(1, 6):
        time.sleep(0.35)
        draw(i)
    time.sleep(0.8)

    # Navigate back up
    for i in range(4, 0, -1):
        time.sleep(0.25)
        draw(i)
    time.sleep(0.6)

    # Search "postgres"
    q = "postgres"
    for j in range(1, len(q) + 1):
        time.sleep(0.10)
        f = filt(q[:j]) or SESSIONS
        draw(0, q[:j], sessions=f)
    time.sleep(1.8)

    # Clear search
    for j in range(len(q) - 1, 0, -1):
        time.sleep(0.04)
        f = filt(q[:j]) or SESSIONS
        draw(0, q[:j], sessions=f)
    draw(0, "")
    time.sleep(0.4)

    # Search "ipad"
    q2 = "ipad"
    for j in range(1, len(q2) + 1):
        time.sleep(0.10)
        f = filt(q2[:j]) or SESSIONS
        draw(0, q2[:j], sessions=f)
    time.sleep(1.8)

    # Clear and return to full list
    for j in range(len(q2) - 1, 0, -1):
        time.sleep(0.04)
        f = filt(q2[:j]) or SESSIONS
        draw(0, q2[:j], sessions=f)
    draw(0, "")
    time.sleep(1.5)

    sys.stdout.write('\033[?25h')
    sys.stdout.flush()


if __name__ == '__main__':
    main()
