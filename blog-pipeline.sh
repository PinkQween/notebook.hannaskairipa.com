#!/bin/bash
set -euo pipefail

# Paths
sourcePath="/Users/skairipa/Documents/Obsidian/"
destinationPath="/Users/skairipa/notebook.hannaskairipa.com/content"

# GitHub repo URL (SSH is best, not HTTPS)
myrepo="git@github.com:pinkqween/notebook.git"

# Go to script directory (your Hugo site)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Step 1: Sync posts from Obsidian → Hugo
rsync -av --delete "$sourcePath/" "$destinationPath/"

# Step 2: Process images + links
if [ -f "images.py" ]; then
  python3 images.py
else
  echo "images.py not found, skipping image processing"
fi

# Step 3: Build Hugo site
hugo

# Step 4: Git add/commit/push changes
if git diff --quiet && git diff --cached --quiet; then
  echo "No changes to commit."
else
  git add .
  git commit -m "Auto update $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
fi

# Step 5: Deploy public/ to gh-pages branch
echo "🚀 Deploying to GitHub Pages..."

# Remove old gh-pages branch if exists
if git show-ref --quiet refs/heads/gh-pages; then
  git branch -D gh-pages
fi

# Create new branch with only public/ contents
git subtree split --prefix public -b gh-pages
git push origin gh-pages --force
git branch -D gh-pages

echo "✅ Blog updated and deployed!"
