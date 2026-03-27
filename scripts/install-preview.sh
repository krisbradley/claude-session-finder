#!/bin/bash
set -e

BASE="https://raw.githubusercontent.com/kristopherbradley/claude-session-finder/master/scripts"
mkdir -p "$HOME/.local/bin"

for script in csf-preview csf-search; do
  curl -fsSL "$BASE/$script" -o "$HOME/.local/bin/$script"
  chmod +x "$HOME/.local/bin/$script"
  echo "Installed $script to $HOME/.local/bin/$script"
done
