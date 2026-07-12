# Release archives

Source archives follow the naming convention **`pycommonist-vX.Y.zip`**.

| Version | Archive | Git tag | Notes |
|---------|---------|---------|--------|
| **1.0** | `pycommonist-v1.0.zip` | `pycommonist-v1.0` | Original flat layout (PyQt6). Published on [HAL Software Archive](https://hal.science/) and GitHub. |
| **1.1** | `pycommonist-v1.1.zip` | `pycommonist-v1.1` | Package `src/pycommonist`, MDI sessions, Artwork. |
| **1.2** | `pycommonist-v1.2.zip` | `pycommonist-v1.2` | Security hardening, English UI/docs, smoke test. |

Zip files are **not** stored in git (see `.gitignore`). Attach them to **GitHub Releases** and upload to **HAL** when depositing.

## Build a source archive (HAL / offline install)

```bash
chmod +x scripts/build_release_zip.sh
./scripts/build_release_zip.sh 1.2
# → releases/pycommonist-v1.2.zip
```

The archive includes **README**, **AUTHORS** and **LICENSE** at its root.
