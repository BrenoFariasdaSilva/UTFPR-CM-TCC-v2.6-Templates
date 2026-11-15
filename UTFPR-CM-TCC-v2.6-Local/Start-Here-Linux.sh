#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo 'Python 3 is required; attempting native package installation.'
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update && sudo apt-get install -y python3
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -S --needed --noconfirm python
  else
    echo 'Install Python 3 using your distribution package manager first.' >&2; exit 1
  fi
fi
python3 scripts/compile.py compile "$@"
