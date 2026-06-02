#!/usr/bin/env bash
#
# Robust, fast checkout for repositories with large/deeply-nested submodule trees.
# Driven entirely by INPUT_* environment variables set by the composite action
# (checkout/action.yml). Safe to run standalone for debugging:
#
#   INPUT_REPOSITORY=owner/repo INPUT_REF=main INPUT_PATH=repo ./checkout.sh
#
# What it does that actions/checkout does not:
#   * Enables Windows long-path support (core.longpaths) so deep submodule paths
#     don't fail with "Filename too long".
#   * Recovers from a dirty / half-finished previous run (hard reset + clean of
#     every submodule) before updating.
#   * Fetches submodules in PARALLEL (git --jobs / submodule.fetchJobs), which
#     actions/checkout still does serially (PR #1569 unmerged as of v6).
#   * Clones once and reuses the persisted working dir on later runs, so warm
#     self-hosted runners only fetch+reset instead of re-cloning.

set -euo pipefail

# ---- Inputs (with defaults) -------------------------------------------------
REPO="${INPUT_REPOSITORY:-${GITHUB_REPOSITORY:-}}"
REF="${INPUT_REF:-}"
DEST="${INPUT_PATH:-.}"
SERVER="${INPUT_SERVER_URL:-https://github.com}"
DEPTH="${INPUT_FETCH_DEPTH:-1}"
SUBMODULES="${INPUT_SUBMODULES:-recursive}"   # recursive | true | false
SHALLOW_SUB="${INPUT_SHALLOW_SUBMODULES:-true}"
JOBS="${INPUT_JOBS:-8}"
CLEAN="${INPUT_CLEAN:-true}"
TOKEN="${INPUT_TOKEN:-}"

# Default the ref to the workflow's commit when checking out the triggering repo.
if [ -z "$REF" ]; then
  if [ "$REPO" = "${GITHUB_REPOSITORY:-}" ] && [ -n "${GITHUB_SHA:-}" ]; then
    REF="$GITHUB_SHA"
  fi
fi

if [ -z "$REPO" ]; then
  echo "::error::checkout: 'repository' is empty and GITHUB_REPOSITORY is unset." >&2
  exit 1
fi
if [ -z "$REF" ]; then
  echo "::error::checkout: 'ref' is empty. Pass 'ref' when checking out a repository other than the one that triggered the workflow." >&2
  exit 1
fi

URL="${SERVER}/${REPO}.git"

# ---- Build arg arrays -------------------------------------------------------
# Auth header is kept out of logs and inherited by submodule subprocesses via -c.
AUTH_ARGS=()
if [ -n "$TOKEN" ]; then
  HEADER="AUTHORIZATION: basic $(printf 'x-access-token:%s' "$TOKEN" | base64 | tr -d '\n')"
  AUTH_ARGS=(-c "http.${SERVER}/.extraheader=${HEADER}")
fi

DEPTH_ARGS=()
if [ "$DEPTH" != "0" ]; then DEPTH_ARGS=(--depth "$DEPTH"); fi

SUB_DEPTH_ARGS=()
if [ "$SHALLOW_SUB" = "true" ]; then SUB_DEPTH_ARGS=(--depth 1); fi

RECURSE_ARGS=()
if [ "$SUBMODULES" = "recursive" ]; then RECURSE_ARGS=(--recursive); fi

# ---- 1) Long-path support (no-op off Windows) -------------------------------
git config --global core.longpaths true

echo "==> Checking out ${REPO}@${REF} into '${DEST}'"

# ---- 2) Clone once, reuse on later runs -------------------------------------
if [ ! -d "${DEST}/.git" ]; then
  echo "==> Cloning (fresh) ${URL}"
  git "${AUTH_ARGS[@]}" clone "${DEPTH_ARGS[@]}" "${URL}" "${DEST}"
fi
cd "${DEST}"
git config core.longpaths true

# ---- 3) Fetch the requested ref (branch, tag, or SHA) -----------------------
# Prefer fetching the ref directly so FETCH_HEAD is exactly the remote tip; this
# guarantees we end up on the freshly-fetched commit and never a stale local
# branch. Fall back to fetching everything if the server rejects a direct ref
# (e.g. a SHA on a server without allowReachableSHA1InWant).
echo "==> Fetching ${REF}"
if git "${AUTH_ARGS[@]}" fetch "${DEPTH_ARGS[@]}" --force --tags origin "${REF}"; then
  TARGET="FETCH_HEAD"
else
  git "${AUTH_ARGS[@]}" fetch "${DEPTH_ARGS[@]}" --force --tags origin
  TARGET="${REF}"
fi

# ---- 4) Recover from a dirty / half-finished previous run -------------------
if [ "$CLEAN" = "true" ]; then
  echo "==> Cleaning working tree and submodules"
  git reset --hard
  git clean -ffd
  git submodule foreach --recursive 'git reset --hard' 2>/dev/null || true
  git submodule foreach --recursive 'git clean -ffd' 2>/dev/null || true
fi

# ---- 5) Check out exactly what we fetched -----------------------------------
git checkout --force "${TARGET}"
git reset --hard "${TARGET}"

# ---- 6) Submodules: the part actions/checkout does serially — parallelize ---
if [ "$SUBMODULES" != "false" ]; then
  echo "==> Updating submodules (jobs=${JOBS}, recursive=$([ "$SUBMODULES" = recursive ] && echo yes || echo no), shallow=${SHALLOW_SUB})"
  git submodule sync --recursive
  git "${AUTH_ARGS[@]}" \
    -c "submodule.fetchJobs=${JOBS}" \
    -c "fetch.parallel=${JOBS}" \
    submodule update --init --force --jobs "${JOBS}" \
    "${RECURSE_ARGS[@]}" "${SUB_DEPTH_ARGS[@]}"
fi

echo "==> Done. Status:"
git status -s -b
