#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

diff -ru "${repo_root}/claw-me" "${repo_root}/skills/claw-me"
npx --yes skills@1.5.19 add "${repo_root}" --list | grep -q "claw-me"

printf 'Claw Me skill mirrors match and skills CLI discovery passed.\n'
