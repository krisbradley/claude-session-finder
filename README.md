<div align="center">

# `csf`

### Claude Session Finder

browse &nbsp;&middot;&nbsp; search &nbsp;&middot;&nbsp; resume

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![macOS](https://img.shields.io/badge/macOS-only-lightgrey?logo=apple)](README.md)
[![requires fzf](https://img.shields.io/badge/requires-fzf-orange)](https://github.com/junegunn/fzf)

An interactive terminal browser for your [Claude Code](https://claude.ai/code) sessions —
fuzzy search, rich previews, and one-key resume. Finds the session you're looking for
from your local session storage and launches it with `claude --resume`.

<img src="demo.gif?v=4" alt="Demo" width="100%">

</div>

---

## Features

```
  Instant fuzzy search  — titles, projects, and full message content
  Rich session previews — project, duration, conversation snippets
  One-key resume        — Enter jumps straight into claude --resume
  Quick search          — csf <word> opens the top match directly
  Named sessions        — shows /rename titles and /color highlights
  CLI filter modes      — --today, --week, --projects, --stats
  Session management    — delete, export to Markdown, copy ID
```

---

## Install

```bash
brew tap krisbradley/tap
brew install claude-session-finder
```

The formula installs all dependencies automatically:

| Dependency | Purpose |
|-----------|---------|
| `fzf` | Interactive fuzzy finder UI |
| `python3` | Helper scripts |

> **macOS only.** `ctrl-y` uses `pbcopy` and `ctrl-p` uses `open`. Linux would need `xclip`/`xdg-open`.

---

## Usage

### Interactive browser

```bash
csf
```

| Key | Action |
|-----|--------|
| Type | Full-text search across titles, projects, and messages |
| `↑` / `↓` | Navigate sessions |
| `Enter` | Resume session with `claude --resume` |
| `ctrl-d` | Delete session from history |
| `ctrl-y` | Copy session ID to clipboard |
| `ctrl-e` | Export session to Markdown on Desktop |
| `ctrl-p` | Open project folder in Finder |
| `ESC` | Exit |

### Quick search

```bash
csf docker       # opens the most recent session matching "docker"
csf "cash register"  # quotes for multi-word searches
```

### Filter modes

```bash
csf --stats       # total sessions, activity this week, top projects
csf --projects    # browse sessions grouped by project
csf --today       # sessions from today only
csf --week        # sessions from the past 7 days
```

---

## How It Works

### Session data

Claude Code appends a line to `~/.claude/history.jsonl` after each message:

```json
{
  "sessionId": "abc123",
  "timestamp": 1711234567890,
  "project": "/Users/you/dev/my-app",
  "display": "first message text"
}
```

`csf` groups entries by `sessionId`, ranks by recency, and shows titles from Claude's auto-generated `ai-title`, user-assigned `/rename` names, or keyword extraction from the first messages.

### Full-text search

`csf` builds a TSV index at `~/.claude/csf-sessions.tsv` containing the full content of every session. When you type, fzf reloads results via `change:reload(csf-search {q})` — so search reaches every word in every message, not just titles.

### Named sessions

Sessions named with `/rename` or colored with `/color` in Claude Code are displayed with their custom title and ANSI color. Metadata is read from `~/.claude/projects/*/SESSION_ID.jsonl`.

### Configuration

Set `CLAUDE_CONFIG_DIR` to use a non-default Claude installation:

```bash
CLAUDE_CONFIG_DIR=~/my-claude csf
```

### File layout

```
~/.claude/
├── history.jsonl         <- written by Claude Code
├── csf-sessions.tsv      <- full-text search index (built by csf)
├── projects/
│   └── */SESSION_ID.jsonl <- session metadata (ai-title, rename, color)
└── debug/
    └── <session-id>.txt  <- full transcripts (if debug enabled)
```

---

## Keybinding Reference

| Key | Script | What it does |
|-----|--------|-------------|
| `Enter` | `csf` | `claude --resume <session-id>` |
| `ctrl-d` | `csf-delete` | Remove from history and search index |
| `ctrl-y` | inline | `echo <id> \| pbcopy` |
| `ctrl-e` | `csf-export` | Write Markdown to `~/Desktop/` and open |
| `ctrl-p` | inline | `open <project-path>` in Finder |

---

## Manual Install

```bash
git clone https://github.com/krisbradley/claude-session-finder
cd claude-session-finder
./install.sh
```

Or manually:

```bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/csf" ~/.local/bin/csf
for script in scripts/csf-*; do
  cp "$script" ~/.local/bin/ && chmod +x ~/.local/bin/"$(basename "$script")"
done
# Add ~/.local/bin to your PATH if needed
```

---

<div align="center">

MIT License · built for [Claude Code](https://claude.ai/code)

</div>
