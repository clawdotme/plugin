#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

diff -ru "${repo_root}/claw-me" "${repo_root}/skills/claw-me"
python3 "${repo_root}/scripts/validate.py"
npx --yes skills@1.5.19 add "${repo_root}" --list | grep -q "claw-me"

printf 'Claw Me plugin manifests, skill mirrors, and Skills CLI discovery passed.\n'
