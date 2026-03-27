#!/bin/bash
set -e

DEST="$HOME/.local/bin/claude-sessions-preview"
mkdir -p "$HOME/.local/bin"

curl -fsSL "https://raw.githubusercontent.com/kristopherbradley/claude-session-finder/master/scripts/claude-sessions-preview" \
  -o "$DEST"
chmod +x "$DEST"

echo "Installed claude-sessions-preview to $DEST"
