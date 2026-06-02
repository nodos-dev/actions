# Nodos Actions

Shared GitHub Actions and scripts for Nodos repositories.

## `checkout` — fast, robust submodule checkout

Use this instead of `actions/checkout` for repos with large or deeply-nested
submodule trees. It is long-path safe on Windows, recovers submodules left dirty
by a failed previous run, and **fetches submodules in parallel** (`--jobs`) —
which `actions/checkout` still does serially.

```yaml
- name: Checkout Nodos
  uses: nodos-dev/actions/checkout@main
  with:
    ref: ${{ github.sha }}
    path: ./Nodos
    jobs: 8            # parallel submodule fetch
```

Cross-repo / private example (relies on the runner's ambient git credentials by
default; pass `token` if the runner is not pre-authenticated):

```yaml
- uses: nodos-dev/actions/checkout@main
  with:
    repository: nodos-dev/workspace
    ref: dev
    path: ./nodos-workspace
    # token: ${{ secrets.CI_TOKEN }}
```

| Input | Default | Description |
| --- | --- | --- |
| `repository` | `${{ github.repository }}` | `owner/name` to check out. |
| `ref` | triggering SHA | Branch, tag, or SHA. Required for other repos. |
| `path` | `.` | Destination directory (reused across runs). |
| `server-url` | `https://github.com` | Git server base URL. |
| `fetch-depth` | `1` | Main-repo shallow depth (`0` = full). |
| `submodules` | `recursive` | `recursive`, `true`, or `false`. |
| `shallow-submodules` | `true` | Shallow-fetch submodules. |
| `jobs` | `8` | Parallel submodule fetch jobs. |
| `clean` | `true` | Hard-reset + clean tree and submodules first. |
| `token` | _(empty)_ | HTTPS auth token; empty = ambient credentials. |

---

## Action Matrix

Badges below show the latest GitHub Actions run status for each build workflow on the `dev`, `nodos-1.3`, and `nodos-1.2` branches.

| Component | dev | nodos-1.3 | nodos-1.2 |
| --- | --- | --- | --- |
| Nodos | [![dev](https://github.com/mediaz/nodos/actions/workflows/release.yml/badge.svg?branch=dev)](https://github.com/mediaz/nodos/actions/workflows/release.yml?query=branch%3Adev) | [![1.3](https://github.com/mediaz/nodos/actions/workflows/release.yml/badge.svg?branch=1.3)](https://github.com/mediaz/nodos/actions/workflows/release.yml?query=branch%3A1.3) | [![1.2](https://github.com/mediaz/nodos/actions/workflows/release.yml/badge.svg?branch=1.2)](https://github.com/mediaz/nodos/actions/workflows/release.yml?query=branch%3A1.2) |
| aja | [![dev](https://github.com/nodos-dev/aja/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/aja/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/aja/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/aja/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/aja/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/aja/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| audio | [![dev](https://github.com/nodos-dev/audio/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/audio/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/audio/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/audio/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/audio/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/audio/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| decklink | [![dev](https://github.com/nodos-dev/decklink/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/decklink/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/decklink/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/decklink/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/decklink/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/decklink/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| display | [![dev](https://github.com/nodos-dev/display/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/display/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/display/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/display/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/display/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/display/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| mediaio | [![dev](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/mediaio/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| modules | [![dev](https://github.com/nodos-dev/modules/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/modules/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/modules/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/modules/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/modules/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/modules/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| nos.sys.vulkan | [![dev](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/mediaz/nos-sys-vulkan/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| rive | [![dev](https://github.com/nodos-dev/rive/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/rive/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/rive/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/rive/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/rive/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/rive/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| sys-device | [![dev](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/sys-device/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| sys-settings | [![dev](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/sys-settings/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| test | [![dev](https://github.com/nodos-dev/test/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/test/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/test/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/test/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/test/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/test/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| transfer | [![dev](https://github.com/nodos-dev/transfer/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/transfer/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/transfer/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/transfer/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/transfer/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/transfer/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
| webcam | [![dev](https://github.com/nodos-dev/webcam/actions/workflows/build.yml/badge.svg?branch=dev)](https://github.com/nodos-dev/webcam/actions/workflows/build.yml?query=branch%3Adev) | [![nodos-1.3](https://github.com/nodos-dev/webcam/actions/workflows/build.yml/badge.svg?branch=nodos-1.3)](https://github.com/nodos-dev/webcam/actions/workflows/build.yml?query=branch%3Anodos-1.3) | [![nodos-1.2](https://github.com/nodos-dev/webcam/actions/workflows/build.yml/badge.svg?branch=nodos-1.2)](https://github.com/nodos-dev/webcam/actions/workflows/build.yml?query=branch%3Anodos-1.2) |
