#!/bin/bash
# Release a new version: bumps __version__, tags, pushes, and updates the Homebrew formula.
# Usage: ./release.sh 0.5.0
set -euo pipefail

VERSION="${1:?usage: ./release.sh <version, e.g. 0.5.0>}"
TAG="v$VERSION"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
TAP_DIR="$REPO_DIR/../homebrew-tap"
FORMULA="$TAP_DIR/Formula/claude-session-finder.rb"
TARBALL_URL="https://github.com/krisbradley/claude-session-finder/archive/refs/tags/$TAG.tar.gz"

if [[ ! -f "$FORMULA" ]]; then
    echo "error: formula not found at $FORMULA" >&2
    exit 1
fi

cd "$REPO_DIR"
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "error: tag $TAG already exists" >&2
    exit 1
fi

# Bump version in csf and commit if it changed
sed -i '' "s/^__version__ = .*/__version__ = '$VERSION'/" csf
if ! git diff --quiet csf; then
    git add csf
    git commit -m "chore: bump version to $VERSION"
fi

git push
git tag "$TAG"
git push origin "$TAG"

# Compute tarball checksum
SHA=$(curl -sL "$TARBALL_URL" | shasum -a 256 | cut -d' ' -f1)
echo "sha256: $SHA"

# Update formula
sed -i '' -E \
    -e "s|archive/refs/tags/v[0-9.]+\.tar\.gz|archive/refs/tags/$TAG.tar.gz|" \
    -e "s|^(  sha256 \").*(\")$|\1$SHA\2|" \
    "$FORMULA"

cd "$TAP_DIR"
git add "$FORMULA"
git commit -m "chore: bump claude-session-finder to $TAG"
git push

echo "Released $TAG"
