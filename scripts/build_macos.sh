#!/usr/bin/env bash
#
# build_macos.sh
#
# Helper script to build a macOS application bundle for PolarAttack using PyInstaller.
# - Produces a one-folder build (dist/PolarAttack) by default (recommended if bundling Chromium).
# - Bundles the `ui/` resources, the mac `chromedriver` (if present), and `chromium_mac/` (if present).
# - Attempts to include PyQt5 Qt plugin folder (platforms, imageformats, styles) automatically.
#
# Usage:
#   chmod +x build_macos.sh
#   ./build_macos.sh
#
# Notes:
# - Run this on macOS (Darwin). Building a macOS app on Linux/Windows is not supported by PyInstaller.
# - Recommended: use a virtualenv and Python 3.8+.
# - If you bundle a Chromium binary, ensure it is placed at `chromium_mac/Chromium.app/.../Chromium`
#   (i.e. place the entire `chromium_mac` directory in the project root).
# - Place the mac `chromedriver` executable (named `chromedriver`) in the project root if you want it bundled.
# - If you need a signed .app or notarization for distribution outside your machine, handle codesign/notarize separately.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project root: ${PROJECT_ROOT}"

# Ensure we are on macOS
if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "ERROR: This build script is intended to run on macOS (Darwin)."
  echo "Please run this script on a macOS machine."
  exit 1
fi
# remove dist and build

PYTHON="${PYTHON:-python3}"

# Check main.py existence
if [[ ! -f "${PROJECT_ROOT}/main.py" ]]; then
  echo "ERROR: main.py not found in project root (${PROJECT_ROOT}). Aborting."
  exit 2
fi

# Check for optional resources
[[ -d "${PROJECT_ROOT}/ui" ]] && echo "Found ui/ folder and its resources." || echo "WARNING: ui/ folder not found (UI assets may be missing)."
[[ -f "${PROJECT_ROOT}/chromedriver" ]] && echo "Found chromedriver (will be bundled)." || echo "WARNING: chromedriver not found. Selenium requires a compatible chromedriver at runtime."
[[ -d "${PROJECT_ROOT}/chromium_mac" ]] && echo "Found chromium_mac/ folder (will be bundled)." || echo "Info: chromium_mac/ not found. App will try to use system Chrome/Chromium."

# Install dependencies (optional)
echo
echo "Ensuring build dependencies (requirements.txt + pyinstaller) are installed in the active Python environment..."
"${PYTHON}" -m pip install --upgrade pip >/dev/null || true
"${PYTHON}" -m pip install -r "${PROJECT_ROOT}/requirements.txt" pyinstaller

# Compose PyInstaller --add-data arguments (macOS uses SRC:DEST pairs)
ADD_DATA_ARGS=()

if [[ -d "${PROJECT_ROOT}/ui" ]]; then
  # Add whole ui folder into bundle as "ui"
  ADD_DATA_ARGS+=("--add-data" "${PROJECT_ROOT}/ui:ui")
fi

if [[ -f "${PROJECT_ROOT}/chromedriver" ]]; then
  # Put chromedriver at the root of the bundle so paths.resource_path("chromedriver") finds it
  ADD_DATA_ARGS+=("--add-data" "${PROJECT_ROOT}/chromedriver:.")
  # Make sure it's executable in the bundle (we'll attempt to set perms later if needed)
fi

if [[ -d "${PROJECT_ROOT}/chromium_mac" ]]; then
  # Include entire chromium_mac tree under chromium_mac in the bundle
  ADD_DATA_ARGS+=("--add-data" "${PROJECT_ROOT}/chromium_mac:chromium_mac")
fi

# Try to auto-detect PyQt5 Qt plugin folder and include it (helps avoid platform plugin runtime errors)
# This is best-effort: if PyQt5 isn't importable in the current environment, we skip it.
QT_PLUGINS_DIR="$("${PYTHON}" - <<'PYCODE' 2>/dev/null || true
import sys, os
try:
    import PyQt5
    from PyQt5 import QtCore
    qt_plugins = os.path.join(os.path.dirname(QtCore.__file__), "plugins")
    if os.path.isdir(qt_plugins):
        print(qt_plugins)
except Exception:
    pass
PYCODE
)"

if [[ -n "${QT_PLUGINS_DIR}" && -d "${QT_PLUGINS_DIR}" ]]; then
  echo "Detected Qt plugins at: ${QT_PLUGINS_DIR} (will be included in the bundle)"
  # Place them under PyQt5/plugins in the bundle so Qt finds them relative to the runtime
  ADD_DATA_ARGS+=("--add-data" "${QT_PLUGINS_DIR}:PyQt5/plugins")
else
  echo "Warning: Could not auto-detect PyQt5 plugin directory. PyInstaller's hooks may still collect necessary Qt files."
fi

# PyInstaller flags
# - windowed: GUI app without console
# - onedir: produce a folder (recommended if bundling big binaries like Chromium)
APP_NAME="PolarAttack"
ICON_PATH="ui/icons/PolarAttack.icns"
PYINSTALLER_FLAGS=(--noconfirm --clean --windowed --onedir --name "${APP_NAME}" --icon "${ICON_PATH}")

# Add the computed data args
echo "PyInstaller will bundle the following extra data (SRC:DEST):"
for ((i=0;i<${#ADD_DATA_ARGS[@]};i+=2)); do
  echo "  ${ADD_DATA_ARGS[i+1]}"
done

# Build command
cd "${PROJECT_ROOT}"
echo
echo "Invoking PyInstaller..."
set -x
"${PYTHON}" -m PyInstaller "${PYINSTALLER_FLAGS[@]}" "${ADD_DATA_ARGS[@]}" main.py
set +x
echo

# Post-build checks
DIST_DIR="${PROJECT_ROOT}/dist/${APP_NAME}"
if [[ -d "${DIST_DIR}" ]]; then
  echo "Build completed. Output directory: ${DIST_DIR}"
  # Ensure chromedriver is executable if we bundled it
  if [[ -f "${DIST_DIR}/chromedriver" ]]; then
    chmod +x "${DIST_DIR}/chromedriver" || true
    echo "Set executable bit for ${DIST_DIR}/chromedriver"
  fi
  echo
  echo "Run the app with:"
  echo "  open \"${DIST_DIR}/${APP_NAME}.app\" || \"${DIST_DIR}/${APP_NAME}\"/PolarAttack"
  echo
  echo "Notes:"
  echo " - If you bundled Chromium, ensure the chromedriver binary is compatible with the Chromium build."
  echo " - If you see Qt plugin errors at runtime (platform plugin), re-run with explicit --add-data to include the correct plugin folders,"
  echo "   or edit this script/spec to include the Qt 'platforms' plugin path reported in the error message."
  echo " - For distribution outside of your machine, sign and notarize the .app according to Apple's guidelines."
else
  echo "ERROR: Expected build output folder not found: ${DIST_DIR}"
  exit 10
fi

echo "Done. :()"
