"""Regression guard: utility and asset symbols importable from specify_cli."""

from pathlib import Path

import importlib.metadata

from specify_cli import (
    CLAUDE_LOCAL_PATH,
    CLAUDE_NPM_LOCAL_PATH,
    check_tool,
    get_speckit_version,
    handle_vscode_settings,
    init_git_repo,
    is_git_repo,
    merge_json_files,
    run_command,
)

def test_utils_symbols_importable():
    assert callable(check_tool)
    assert callable(merge_json_files)
    assert callable(is_git_repo)

def test_get_speckit_version_returns_string():
    version = get_speckit_version()
    assert isinstance(version, str) and len(version) > 0


def test_get_speckit_version_prefers_checked_out_pyproject(monkeypatch):
    monkeypatch.setattr(importlib.metadata, "version", lambda name: "0.0.0")

    assert get_speckit_version() == "0.8.15.dev0"

def test_claude_paths_are_paths():
    assert isinstance(CLAUDE_LOCAL_PATH, Path)
    assert isinstance(CLAUDE_NPM_LOCAL_PATH, Path)
