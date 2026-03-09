"""
conftest.py — Shared pytest fixtures for the Deft Directive testbed.

Import strategy: tests import from `run` (the shim in run.py) which loads
the extension-less `run` CLI file via importlib. See run.py for details.

Author: Scott Adams (msadams) — 2026-03-09
"""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def deft_root() -> Path:
    """Return the absolute path to the deft repo root.

    Used by content tests to locate .md files and other framework assets.
    """
    # conftest.py lives at tests/ — repo root is one level up
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def tmp_project_dir(tmp_path: Path) -> Path:
    """Create a temporary directory with a minimal deft-like structure.

    Provides an isolated workspace for CLI tests so they don't touch
    the real repo or the user's config files.

    Structure created:
        tmp_path/
        ├── main.md
        ├── core/
        └── languages/
    """
    (tmp_path / "main.md").write_text("# Test main.md\n")
    (tmp_path / "core").mkdir()
    (tmp_path / "languages").mkdir()
    return tmp_path


@pytest.fixture
def mock_user_config(tmp_path: Path) -> Path:
    """Create a temporary USER.md with minimal valid content.

    Used by bootstrap and project command tests to provide a pre-existing
    user config without touching ~/.config/deft/USER.md.
    """
    user_md = tmp_path / "USER.md"
    user_md.write_text(
        "# User Preferences\n\n"
        "## Identity\n\nName: Test User\n\n"
        "## Communication\n\nStyle: concise\n"
    )
    return user_md


@pytest.fixture(scope="session")
def deft_module():
    """Load the deft CLI module via the run.py importlib shim.

    Returns the loaded module so tests can call cmd_* functions directly.
    All CLI tests should use this fixture rather than importing run directly,
    so the import strategy is centralised here.

    Example:
        def test_something(deft_module):
            result = deft_module.get_script_dir()
            assert result.is_dir()
    """
    import importlib.util
    from pathlib import Path

    run_py = Path(__file__).parent.parent / "run.py"
    spec = importlib.util.spec_from_file_location("run", run_py)
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


@pytest.fixture
def isolated_env(tmp_project_dir: Path, monkeypatch: pytest.MonkeyPatch):
    """Combine tmp_project_dir with env var overrides for CLI isolation.

    Sets DEFT_USER_PATH and DEFT_PROJECT_PATH to temp locations so CLI
    commands don't read/write real config files during tests.
    """
    user_md = tmp_project_dir / "USER.md"
    project_md = tmp_project_dir / "PROJECT.md"
    monkeypatch.setenv("DEFT_USER_PATH", str(user_md))
    monkeypatch.setenv("DEFT_PROJECT_PATH", str(project_md))
    monkeypatch.chdir(tmp_project_dir)
    return tmp_project_dir
