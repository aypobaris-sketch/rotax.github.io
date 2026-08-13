#!/usr/bin/env bash
# SessionStart hook: make sure the code graph is installed and current.
#
# The MCP wrapper installs on demand too, but doing it here as well means the
# binary is usually warm before the first query, and it keeps the index in step
# with whatever the repo looks like at the start of the session.
set -uo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BIN="${CBM_BIN:-$HOME/.local/bin/codebase-memory-mcp}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd -- "$HERE/../.." && pwd)}"

if ! "$HERE/cbm-ensure.sh"; then
    # Never fail the session over an optional index -- Claude still has Read,
    # Grep and Glob without it.
    exit 0
fi

# Re-index in the background. stdout on a SessionStart hook is injected into the
# conversation as context, so send everything to the log instead.
LOG="${TMPDIR:-/tmp}/cbm-index.log"
nohup "$BIN" cli index_repository --repo_path "$PROJECT_DIR" >"$LOG" 2>&1 &

exit 0
