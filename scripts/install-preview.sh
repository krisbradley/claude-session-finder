#!/bin/bash
set -e

DEST="$HOME/.local/bin/csf-preview"
mkdir -p "$HOME/.local/bin"

curl -fsSL "https://raw.githubusercontent.com/kristopherbradley/claude-sessions-finder/master/scripts/csf-preview" \
  -o "$DEST"
chmod +x "$DEST"

echo "Installed csf-preview to $DEST"
