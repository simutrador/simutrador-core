# simutrador-core

Core models and utilities for the SimuTrador platform.

## 📚 Documentation

- **WebSocket API**: [SimuTrade WebSocket API v2.0](https://github.com/simutrador/simutrador-docs/blob/main/SimuTrador/simutrador-server/ws_api_v2.md) - Complete API specification for trading simulation
- **Project Overview**: [SimuTrador Architecture](https://github.com/simutrador/simutrador-docs/blob/main/SimuTrador/main.md)
- **Package Documentation**: All models include full type hints and docstrings

## Publishing

This repo includes a helper script to publish releases to TestPyPI and PyPI using `uv`.

Prerequisites:

- `uv` installed
- macOS/Linux shell (uses `bash` and `sed`)
- Tokens for TestPyPI and PyPI

### Configure authentication (one-time)

Option A — ~/.pypirc (recommended)

Create file at `~/.pypirc`:

```
[distutils]
index-servers = pypi testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-<YOUR_REAL_PYPI_TOKEN>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-<YOUR_TESTPYPI_TOKEN>
```

Secure it:

```
chmod 600 ~/.pypirc
```

Option B — Permanent env vars

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```
export PYPI_TOKEN="pypi-<YOUR_REAL_PYPI_TOKEN>"
export TESTPYPI_TOKEN="pypi-<YOUR_TESTPYPI_TOKEN>"
```

Reload your shell:

```
source ~/.zshrc
```

### One-command publish

From the repo root:

```
chmod +x scripts/publish.sh
scripts/publish.sh --bump patch
```

This will:

- Bump the version (patch), or keep current if you press Enter
- Run checks (ruff --fix, pyright), build the package
- Publish to TestPyPI (using token from `TESTPYPI_TOKEN`, `~/.pypirc [testpypi]`, or `UV_PUBLISH_TOKEN`)
- Prompt to publish to PyPI (using token from `PYPI_TOKEN`, `~/.pypirc [pypi]`, or `UV_PUBLISH_TOKEN`)

Other common flows:

```
# Skip TestPyPI and go straight to PyPI
scripts/publish.sh --bump patch --skip-testpypi --publish-pypi

# Set an exact version and auto-publish to PyPI
scripts/publish.sh --set-version 1.1.0 --publish-pypi
```

### How tokens are discovered

The script resolves tokens per step in this order:

- For TestPyPI:

  1. `TESTPYPI_TOKEN`
  2. `~/.pypirc` `[testpypi]` `password`
  3. `UV_PUBLISH_TOKEN` (fallback)

- For PyPI:
  1. `PYPI_TOKEN`
  2. `~/.pypirc` `[pypi]` `password`
  3. `UV_PUBLISH_TOKEN` (fallback)

You can override the pypirc path via `PYPIRC_PATH=/custom/path scripts/publish.sh ...`.

### Notes

- TestPyPI publishing uses `uv publish --index testpypi` (configured under `[[tool.uv.index]]` in `pyproject.toml`).
- PyPI publishing uses `uv publish`.
- Package must have a new, unique version each publish.
- The package is typed (ships `py.typed`).
