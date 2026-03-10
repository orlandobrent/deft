# Testbed Phase 1 — Remaining Implementation

## Current State

Phase 1 scaffolding is complete: `pyproject.toml`, `run.py` shim, directory structure,
`__init__.py` files, and `tests/conftest.py` (at `tests/` root, not `tests/fixtures/` —
acceptable deviation). A smoke test (`tests/cli/test_import_smoke.py`) exists and validates
the importlib shim. `todo.md` exists. `Taskfile.yml` has `PROJECT_NAME: deft` and `VERSION: 0.3.0`.

Missing: all content tests (Phase 2), all CLI regression tests (Phase 3), Taskfile pytest
integration (Phase 4), and baseline finalization (Phase 5).

---

## Phase 1 Gap — conftest.py helpers

Spec Task 3.1.1 requires two helper fixtures not yet in `tests/conftest.py`:

- `run_command(cmd_fn, args, tmp_path)` — calls a `cmd_*` function in an isolated temp dir,
  captures stdout/stderr, returns result
- `mock_user_input(monkeypatch, responses)` — patches `ask_input` / `ask_choice` /
  `ask_confirm` with a queue of predetermined responses

Add these to `tests/conftest.py` before writing any CLI tests.

---

## Phase 2 — Content Integrity Suite

*No dependency on Phase 1 gap. Can start immediately.*

### 2.1 Baseline Snapshot (prerequisite for 2.2–2.5)

- Implement `tests/content/snapshots/capture.py`: walk repo, collect all `.md` file paths,
  top-level headers (`#`/`##`), and internal links `[text](path)` per file; output to
  `tests/content/snapshots/baseline.json`
- Run capture against current beta; create `tests/content/snapshots/known_failures.json`
  annotating at minimum: README.md Warping references, `core/project.md` Voxio Bot content,
  missing `strategies/rapid.md` and `strategies/enterprise.md`, `strategies/discuss.md`
  absent from README table
- Commit both files

### 2.2 Structural Checks (after 2.1)

- Implement `tests/content/test_structure.py`
- Assert required top-level dirs: `coding/`, `context/`, `contracts/`, `core/`,
  `deployments/`, `interfaces/`, `languages/`, `meta/`, `resilience/`, `scm/`,
  `strategies/`, `swarm/`, `templates/`, `tools/`, `vbrief/`, `verification/`
- Assert required root files: `main.md`, `README.md`, `REFERENCES.md`, `CHANGELOG.md`,
  `LICENSE.md`, `Taskfile.yml`, `run`, `run.bat`
- Assert strategy files listed in `strategies/README.md` exist on disk;
  xfail `rapid.md` and `enterprise.md`

### 2.3 Standards Compliance (after 2.1)

- Implement `tests/content/test_standards.py`
- RFC2119 legend check: files in `languages/`, `interfaces/`, `tools/`, `strategies/`,
  `context/`, `verification/`, `resilience/` must contain `!=MUST, ~=SHOULD`
- Deprecated path check: no `.md` should contain `core/user.md`; xfail known exceptions
- Deprecated name check: files outside `old/` must not contain `warping`
  (case-insensitive); xfail `README.md`

### 2.4 Contract Checks (after 2.1)

- Implement `tests/content/test_contracts.py`
- Every file linked in `REFERENCES.md` exists on disk
- Every file linked in `strategies/README.md` exists; xfail `rapid.md`, `enterprise.md`
- All `⚠️ See also` link targets resolve
- Assert `strategies/discuss.md` IS listed in `strategies/README.md`
  (currently failing — documents the gap)

### 2.5 Shape Checks (after 2.1)

- Implement `tests/fixtures/shapes.py` with shape schemas:
  - Language files: `## Standards`, `## Commands`, `## Patterns`
  - Strategy files: `## When to Use`, `## Workflow`
  - Interface files: `## Core Architecture` or `## Framework Selection`
  - Tool files: at least one `##` section
- Implement `tests/content/test_shape.py`: parameterize over each category,
  assert files match their schema

---

## Phase 3 — CLI Regression Suite

*Depends on Phase 1 gap (conftest.py helpers) being filled first.*

### 3.2 `cmd_bootstrap` tests

- Implement `tests/cli/test_bootstrap.py`
- Happy path: mocked inputs produce `USER.md` at expected path with `## Identity`
  and `## Communication` sections
- Output path: assert file written to `get_default_paths()['user']`
- No crash: exits without exception given minimal valid inputs

### 3.3 `cmd_project` tests

- Implement `tests/cli/test_project.py`
- Happy path: mocked inputs produce `PROJECT.md` at expected path
- Content: file contains `## Project Configuration` and `## Standards`
- Strategy selection: selected strategy name appears in output

### 3.4 `cmd_validate` tests

- Implement `tests/cli/test_validate.py`
- Valid state: exits without error against valid temp deft dir
- Missing file: reports failure when a required file is absent

### 3.5 `cmd_doctor` tests

- Implement `tests/cli/test_doctor.py`
- Runs without crash
- stdout includes at least one check result line (✓ or ⚠)

---

## Phase 4 — Taskfile Integration

*Depends on Phases 2 and 3 complete.*

Update `Taskfile.yml`:

- Add `task test`: `uv run pytest tests/`
- Add `task test:coverage`: `uv run pytest tests/ --cov --cov-report=html`;
  fails if coverage < 75%
- Add `task fmt`: `uv run ruff format . && uv run black .`
- Replace `task lint`: `uv run ruff check . && uv run mypy run`
  (currently only runs markdownlint)
- Update `task check` deps to add `lint` and `test`

---

## Phase 5 — Baseline Finalization

*Depends on Phase 4 complete.*

- Run `task test` against current beta; capture full result
- Update `known_failures.json` to reflect actual vs expected failures
- Ensure no unexpected failures remain (fix or document each one)
- Verify `task check` blocks on test failure

---

## Dependency Order

```
Phase 1 gap ──────────────────────────────────────────► Phase 3 (CLI tests) ──┐
                                                                                ├──► Phase 4 ──► Phase 5
Phase 2.1 ──► Phase 2.2 ┐                                                      │
             Phase 2.3  ├──────────────────────────────────────────────────────┘
             Phase 2.4  │
             Phase 2.5  ┘
             (2.2–2.5 parallel after 2.1)
```

---

*Generated from spec gap analysis — Deft Directive msadams-branch — 2026-03-10*
