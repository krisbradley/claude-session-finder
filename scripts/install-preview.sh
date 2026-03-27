#!/bin/bash
set -e

BASE="https://raw.githubusercontent.com/kristopherbradley/claude-session-finder/master/scripts"
mkdir -p "$HOME/.local/bin"

# Install helper scripts
for script in csf-preview csf-search; do
  curl -fsSL "$BASE/$script" -o "$HOME/.local/bin/$script"
  chmod +x "$HOME/.local/bin/$script"
  echo "Installed $script"
done

# Install csf-summarize Python script
curl -fsSL "$BASE/csf-summarize" -o "$HOME/.local/share/csf-summarize.py"

# Set up venv with sumy + numpy
echo "Setting up Python venv for csf-summarize..."
python3 -m venv "$HOME/.local/share/csf-venv"
"$HOME/.local/share/csf-venv/bin/pip" install sumy numpy -q

# Write wrapper that uses venv python
cat > "$HOME/.local/bin/csf-summarize" << EOF
#!/bin/bash
exec "\$HOME/.local/share/csf-venv/bin/python3" "\$HOME/.local/share/csf-summarize.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/csf-summarize"

echo ""
echo "All done. Run: csf-summarize"
