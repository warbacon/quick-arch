#!/bin/sh

SCRIPT_DIR=$(dirname "$0")

if [ "$(id -u)" -eq 0 ]; then
  sudo=""
else
  sudo="sudo"
fi

if ! command -v "python" >/dev/null 2>&1; then
  $sudo pacman -S --noconfirm python
fi

$sudo python "$SCRIPT_DIR/src/quick_arch.py"
