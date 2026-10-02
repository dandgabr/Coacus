#!/usr/bin/env bash
# Coacus Universal Bootstrap Installer (Linux / macOS)
# Verifies Python 3.10+, installs it if missing, creates a .venv,
# renders artifacts and installs Coacus into harnesses.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

TARGET_HARNESS="${1:-all}"

echo "===================================================="
echo "  Coacus Universal Bootstrap Installer (POSIX)"
echo "===================================================="

# 1. Detect Python 3.10+
PYTHON_BIN=""
for cmd in python3.14 python3.13 python3.12 python3.11 python3.10 python3 python; do
  if command -v "$cmd" >/dev/null 2>&1; then
    ver="$("$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || true)"
    major="${ver%%.*}"
    minor="${ver##*.}"
    if [ -n "$major" ] && [ "$major" -eq 3 ] && [ "$minor" -ge 10 ]; then
      PYTHON_BIN="$cmd"
      echo "✔ Detected compatible Python: $PYTHON_BIN ($ver)"
      break
    fi
  fi
done

# 2. Install Python if missing
if [ -z "$PYTHON_BIN" ]; then
  echo "⚠ No Python >= 3.10 detected on PATH."
  echo "Attempting to install Python via native package manager..."
  if command -v apt-get >/dev/null 2>&1; then
    echo "Using apt-get..."
    sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
  elif command -v dnf >/dev/null 2>&1; then
    echo "Using dnf..."
    sudo dnf install -y python3 python3-pip
  elif command -v pacman >/dev/null 2>&1; then
    echo "Using pacman..."
    sudo pacman -Sy --noconfirm python python-pip
  elif command -v brew >/dev/null 2>&1; then
    echo "Using Homebrew..."
    brew install python
  else
    echo "❌ Error: Could not automatically install Python 3.10+. Please install Python manually."
    exit 1
  fi
  PYTHON_BIN="python3"
fi

# 3. Create or reuse virtual environment (.venv)
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment at $VENV_DIR..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

VENV_PY="$VENV_DIR/bin/python"

# 4. Generate all Coacus artifacts
echo "Rendering Coacus artifacts..."
"$VENV_PY" scripts/coacus.py generate

# 5. Run installation into target harness(es)
echo "Installing Coacus into harness: $TARGET_HARNESS..."
"$VENV_PY" scripts/coacus_install.py "$TARGET_HARNESS" --verify-after-install

echo "===================================================="
echo "✔ Coacus installation and verification completed successfully!"
echo "Virtual environment ready at: $VENV_DIR"
echo "===================================================="
