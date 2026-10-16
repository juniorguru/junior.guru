#!/bin/bash
# Prepares Claude Code cloud sessions for running tests and linters
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

uv sync
npm ci --no-audit --no-fund

# The preinstalled Chromium doesn't match the build pinned by the playwright
# package, and running 'playwright install' isn't possible in cloud sessions
echo 'export JG_CHROMIUM_EXECUTABLE_PATH=/opt/pw-browsers/chromium' >> "$CLAUDE_ENV_FILE"
