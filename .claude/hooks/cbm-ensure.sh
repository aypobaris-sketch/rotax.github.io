#!/usr/bin/env bash
# Install codebase-memory-mcp if it is missing.
#
# Claude Code on the web runs in a throwaway container: the binary lives in
# $HOME, which is wiped between sessions, while this repo is re-cloned every
# time. Keeping the installer here is what makes the setup survive.
#
# Safe to call repeatedly and from several places at once -- an flock keeps the
# MCP wrapper and the SessionStart hook from installing on top of each other,
# and an existing binary short-circuits the whole thing.
set -uo pipefail

BIN="${CBM_BIN:-$HOME/.local/bin/codebase-memory-mcp}"
INSTALLER_URL="https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh"

if [ -x "$BIN" ]; then
    exit 0
fi

# Serialize concurrent callers. The winner installs; everyone else falls through
# to the re-check below and finds the binary already in place.
LOCK="${TMPDIR:-/tmp}/cbm-install.lock"
if command -v flock >/dev/null 2>&1; then
    exec 9>"$LOCK" && flock 9
fi

if [ -x "$BIN" ]; then
    exit 0
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "cbm-ensure: curl is required to install codebase-memory-mcp" >&2
    exit 1
fi

# Log to stderr so a hook or MCP launch never mistakes progress output for
# protocol data on stdout.
echo "cbm-ensure: installing codebase-memory-mcp (~280MB, one time per container)..." >&2
if ! curl -fsSL "$INSTALLER_URL" | bash >&2; then
    echo "cbm-ensure: install failed" >&2
    exit 1
fi

if [ ! -x "$BIN" ]; then
    echo "cbm-ensure: installer finished but $BIN is missing" >&2
    exit 1
fi

echo "cbm-ensure: ready ($("$BIN" --version 2>&1))" >&2
