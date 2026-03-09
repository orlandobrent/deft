# Implementation Plan — Phase 1: Testbed Foundation

Actionable step-by-step plan derived from `SPECIFICATION.md`.
Do not begin Phase 2 (Content Suite) or Phase 3 (CLI Suite) work until all steps
in this plan are complete and verified.

**Source:** `SPECIFICATION.md` — Phase 1 (Tasks 1.1.1, 1.1.2, 1.2.1)
**Branch:** `msadams-branch`
**Prerequisites:** Python 3.11+ and `uv` installed on the machine

---

## Standing Rules

> **⚠️ No auto-push.** After committing, STOP. Do not push to `origin` until
> the author has vetted the changes locally. Push only when explicitly instructed.

---

## Pre-Flight Checks

Before writing any files, verify the environment is ready:

1. Confirm Python version: `python --version` — must be 3.11 or higher
2. Confirm `uv` is installed: `uv --version` — if missing, install from https://docs.astral.sh/uv/getting-started/installation/
3. Confirm you are on `msadams-branch`: `git branch --show-current`
4. Confirm working directory is repo root: `pwd` should show `E:\Repos\deft`

---

## Step 1 — Create Test Directory Structure
*Task 1.2.1 — no dependencies, do this first*

Create the following directories and empty `__init__.py` files:

```
tests/
tests/cli/
tests/content/
tests/content/snapshots/
tests/fixtures/
tests/fixtures/mock_configs/
```

Add an empty `__init__.py` to each directory (makes them Python packages, required
for pytest to discover tests correctly across subdirectories).

**Verify:** Run `python -m pytest --collect-only` from repo root — should exit 0
with "no tests ran" (no errors about missing modules or directories).

---

## Step 2 — Create `pyproject.toml`
*Task 1.1.1 — no dependencies, can be done in parallel with Step 1*

Create `pyproject.toml` at repo root with the following:

**Sections required:**
- `[project]` — name, version, requires-python = ">=3.11"
- `[project.optional-dependencies]` — `dev` group containing:
  - pytest >= 7.4
  - pytest-cov >= 4.1
  - pytest-mock >= 3.12
  - ruff >= 0.1
  - black >= 23
  - mypy >= 1.7
- `[tool.pytest.ini_options]` — testpaths = ["tests"], addopts with --cov and
  --cov-report=term-missing
- `[tool.coverage.run]` — source = ["."], omit test files and venv
- `[tool.coverage.report]` — fail_under = 75
- `[tool.ruff]` — line-length = 100, select rules per languages/python.md
- `[tool.black]` — line-length = 100
- `[tool.mypy]` — python_version = "3.11", disallow_untyped_defs = true

**Verify:** Run `uv sync --extra dev` — should complete without errors and create
a `.venv` directory. Then run `uv run python -m pytest --collect-only` — exits 0.

---

## Step 3 — Populate `run.py` as the Import Shim
*Prerequisite for all CLI tests — tackle now, not at Phase 3*

The `run` CLI file has no `.py` extension, which means Python cannot import it with
a normal `import run` statement. `run.py` exists in the repo at 0 bytes and is
referenced nowhere — making it the safe, zero-impact modification point.

**Approach (decided): Option A — `run.py` as importlib shim**
- `run.bat` calls `python run` (the extension-less file) — unaffected
- No documentation or scripts reference `run.py`
- Populating `run.py` breaks nothing currently working

**What to put in `run.py`:**
A module loader that imports the extension-less `run` file by path using `importlib`,
exposes it as `deft_run`, and re-exports everything at module level so tests can do
`from run import cmd_bootstrap` naturally.

Add a module-level docstring explaining this is a test import shim, not a CLI entry point.

**Verify:** Write a single smoke test that imports `get_script_dir` from `run` via
`run.py` and asserts it returns a `Path`. Keep this as `tests/cli/test_import_smoke.py`.
If it passes, all CLI tests are unblocked.

---

## Step 4 — Create `tests/fixtures/conftest.py`
*Task 1.1.2 — depends on Step 2 (pyproject.toml) and Step 3 (import strategy)*

This file provides shared fixtures used across all test files. Create it with:

**Fixture: `deft_root`**
- Returns: `Path` pointing to the repo root
- Used by: all content tests to locate `.md` files

**Fixture: `tmp_project_dir`**
- Scope: function (fresh per test)
- Creates a temporary directory containing a minimal deft-like structure:
  - `main.md` (empty)
  - `core/` directory
  - `languages/` directory
- Returns: `Path` to the temp directory
- Used by: CLI tests that need an isolated workspace

**Fixture: `mock_user_config`**
- Creates a temp `USER.md` with minimal valid content
- Returns: `Path` to the temp file
- Used by: bootstrap and project command tests

**Fixture: `deft_module`**
- Loads the `run` file as a Python module via `run.py` shim (see Step 3)
- Returns: the loaded module
- Used by: all CLI tests to call `cmd_*` functions

**Verify:** Run `pytest tests/fixtures/ --collect-only` — exits 0 with no import errors.

---

## Step 5 — Add `.gitignore` Entries
*Housekeeping — do before first commit*

Add the following to `.gitignore` if not already present:

```
# Python toolchain
.venv/
__pycache__/
*.pyc
.coverage
htmlcov/
.pytest_cache/

# pyproject build artifacts
dist/
*.egg-info/
```

**Verify:** `git status` should not show `.venv/` or `__pycache__/` as untracked.

---

## Step 6 — Smoke Test the Full Setup
*Verify all of Phase 1 before moving on*

Run the following sequence and confirm each exits cleanly:

```powershell
uv sync --extra dev
uv run python -m pytest --collect-only
uv run python -m pytest tests/ -v
uv run ruff check .
uv run black --check .
```

Expected outcomes:
- `--collect-only` finds at minimum `test_import_smoke.py` from Step 3
- `pytest tests/ -v` — 1 test passes (import smoke test), 0 failures
- `ruff` and `black` — 0 errors on the new test files (the main `run` script
  will likely have ruff/black findings; exclude it from linting scope for now
  by adding it to `[tool.ruff] exclude` and `[tool.black] exclude` in pyproject.toml)

---

## Step 7 — Commit Phase 1
*Only commit once Step 6 is fully clean*

Stage and commit the following files:

```
pyproject.toml
tests/__init__.py
tests/cli/__init__.py
tests/cli/test_import_smoke.py
tests/content/__init__.py
tests/content/snapshots/__init__.py
tests/fixtures/__init__.py
tests/fixtures/conftest.py
tests/fixtures/mock_configs/  (directory, add .gitkeep)
.gitignore (updated)
```

Suggested commit message:
```
feat(tests): add Phase 1 testbed foundation

- pyproject.toml with pytest, ruff, black, mypy, pytest-cov
- tests/ directory structure (cli/, content/, fixtures/)
- conftest.py with shared fixtures
- run import strategy via run.py importlib shim (Option A)
- import smoke test confirming run module loads correctly
```

---

## Phase 1 Complete — Handoff Criteria

Before starting Phase 2 (Content Suite) or Phase 3 (CLI Suite), confirm:

- `uv sync --extra dev` works from a clean checkout
- `uv run pytest tests/` passes with 0 failures
- `run` module imports cleanly in tests (smoke test green)
- All new files committed to `msadams-branch`
- `.venv/` is gitignored and not tracked

**Next steps after Phase 1:**
- Phase 2 and Phase 3 can start in parallel — see `SPECIFICATION.md` for task details
- Phase 2 entry point: `tests/content/snapshots/capture.py` (Task 2.1.1)
- Phase 3 entry point: extend `conftest.py` with CLI helpers (Task 3.1.1)

---

*Derived from SPECIFICATION.md — Deft Directive msadams-branch — 2026-03-08*
