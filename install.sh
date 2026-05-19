#!/bin/bash
set -e

PREFIX="${PREFIX:-$HOME/.local/bin}"
mkdir -p "$PREFIX"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

ln -sf "$SCRIPT_DIR/csf" "$PREFIX/csf"
for helper in "$SCRIPT_DIR"/scripts/csf-*; do
    [ -f "$helper" ] || continue
    name="$(basename "$helper")"
    cp "$helper" "$PREFIX/$name"
    chmod +x "$PREFIX/$name"
done

echo "Installed csf to $PREFIX"
echo "Make sure $PREFIX is in your PATH"
