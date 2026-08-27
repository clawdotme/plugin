#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "${repo_root}/scripts/sync-skill.py" --check
python3 "${repo_root}/scripts/validate.py"
pnpm --dir "${repo_root}/tools" install --frozen-lockfile --ignore-scripts
pnpm --dir "${repo_root}/tools" exec skills add "${repo_root}" --list | grep -q "claw-me"

printf 'Claw Me plugin manifests, skill mirrors, and Skills CLI discovery passed.\n'
