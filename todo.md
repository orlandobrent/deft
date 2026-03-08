# Todo

Deferred work items captured during planning. See SPECIFICATION.md for Phase 1 scope.

---

## Phase 1 — Testbed (In Progress)

See `SPECIFICATION.md` for full implementation plan.

---

## Deferred from Phase 1 — Testbed Completions

### CI: GitHub Actions workflow
- Create `.github/workflows/test.yml`
- Trigger on push to `beta` and on all PRs targeting `beta`
- Steps: checkout, setup Python, `uv sync`, `task test:coverage`
- Blocked by: Phase 1 testbed must be stable first
- Context: agreed during spec interview to defer; local `task check` gate is Phase 1 scope

### CLI tests: additional commands
- Add tests for `cmd_spec`, `cmd_install`, `cmd_reset`, `cmd_update`
- Happy path + key error cases for each
- Context: Phase 1 covers core four only (bootstrap, project, validate, doctor)

### CLI tests: error and edge cases
- Invalid input handling, missing config files, bad paths, permission errors
- Currently only happy path tested in Phase 1
- Context: deferred to keep Phase 1 scope manageable

### GitHub Issues migration
- Migrate items from this file to GitHub Issues
- Link issues to PRs as work is completed
- Context: owner is new to GitHub; defer until comfortable with PR workflow

---

## Phase 2 — Deft Directive v0.6.0 Upgrade

*Do not start until Phase 1 testbed is complete and passing — tests will validate this work.*

### Rename: "Warping" → "Deft Directive"
- `README.md` still says "Warping Process", "What is Warping?", "Contributing to Warping", etc.
- `Taskfile.yml` has `PROJECT_NAME: warping` and `VERSION: 0.2.0`
- `warping.sh` still present — remove or deprecate (replaced by `run` in v0.5.0)
- `CHANGELOG.md` header says "Warping framework"
- Verify: `test_standards.py` xfail for Warping references should flip to passing

### Clean leaked personal files
- `core/project.md` — contains Voxio Bot private project config; replace with generic
  framework template (see `templates/project.md.template` for reference)
- `PROJECT.md` (repo root) — leftover from bootstrap test run; remove or replace with
  a proper example
- Verify: `test_standards.py` xfail for Voxio Bot content should flip to passing

### Add missing strategies
- `strategies/rapid.md` — Quick prototypes, SPECIFICATION only workflow
- `strategies/enterprise.md` — Compliance-heavy, PRD → ADR → SPECIFICATION workflow
- Both listed in `strategies/README.md` as "(future)" with no backing file
- Verify: `test_structure.py` xfails for these should flip to passing

### Add `strategies/discuss.md` to README table
- File exists and is complete but missing from `strategies/README.md` strategy table
- Verify: `test_contracts.py` discuss.md assertion should flip to passing

### Port `SKILL.md` from master
- Three commits on master updated SKILL.md that never landed in beta:
  - `a6f120a` Add Claude Code skill integration
  - `cc442fc` Add comprehensive New Project Workflow
  - `2f2a89e` Add clawd.bot compatibility
- Cherry-pick or manually apply these changes

### Write CHANGELOG for post-v0.5.0 work
- No changelog entries exist for context engineering module, canonical vBRIEF pattern,
  or any of the work above
- Add v0.6.0 entry covering all Phase 2 changes

---

## Future Phases (Unscheduled)

### testbed: LLM-assisted content validation
- Explore using an LLM to verify semantic correctness of `.md` files
  (e.g. "does this strategy file give actionable guidance?")
- Currently out of scope — shape/pattern checks are sufficient for regression testing
- Revisit when framework content volume makes manual review impractical

### Spec: self-upgrade to Deft Directive product
- Use the framework to spec its own evolution as a product ("Deft Directive")
- Includes branding, public docs, distribution packaging
- Deferred until Phase 1 + Phase 2 are stable

---

*Created from spec interview — Deft Directive msadams-branch — 2026-03-08*
