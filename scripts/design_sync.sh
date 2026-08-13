#!/usr/bin/env bash
# Copy the vendored sqlfluff-design static assets into Flask's static folder.
# Run before local development and before deploy (see .github/workflows/deploy.yaml).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source="$repo_root/vendor/sqlfluff-design/static/sqlfluff-design"
dest="$repo_root/src/app/static/sqlfluff-design"

test -d "$source" || {
  echo "error: $source not found — did you run 'git submodule update --init'?" >&2
  exit 1
}

mkdir -p "$dest"
rsync -a --delete "$source/" "$dest/"
echo "synced sqlfluff-design assets to $dest"
