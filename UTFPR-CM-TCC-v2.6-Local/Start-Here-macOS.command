#!/bin/bash
set -e
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is needed for the one-click setup."
  if ! command -v brew >/dev/null 2>&1; then
    echo 'Installing Homebrew requires your confirmation and possibly macOS administrator privileges.'
    read -r -p 'Install Homebrew from its official website? [y/N] ' answer
    [[ "$answer" =~ ^[yYsS]$ ]] || exit 1
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  for bin in /opt/homebrew/bin /usr/local/bin; do [ -d "$bin" ] && export PATH="$bin:$PATH"; done
  brew install python
fi
set +e
python3 scripts/compile.py compile "$@"
status=$?
set -e
echo; read -r -p 'Press Enter to close this window...' _
exit "$status"
