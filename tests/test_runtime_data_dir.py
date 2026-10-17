"""Data-directory resolution must ignore CLAUDE_PLUGIN_DATA leaked by other plugins."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import runtime  # noqa: E402


def _plugin_root(tmp_path: Path) -> Path:
    root = tmp_path / "installed" / "claude-seo"
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text('{"version":"2.4.3"}\n', encoding="utf-8")
    return root


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("CLAUDE_PLUGIN_DATA", "CLAUDE_PLUGIN_ROOT", "CLAUDE_SEO_DATA_DIR"):
        monkeypatch.delenv(name, raising=False)


@pytest.mark.parametrize("folder", ["claude-seo", "claude-seo-stolosdigital", "claude-seo-agricidaniel-claude-seo"])
def test_own_plugin_data_folder_is_trusted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, folder: str) -> None:
    root = _plugin_root(tmp_path)
    data = tmp_path / ".claude" / "plugins" / "data" / folder
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(data))
    assert runtime._data_dir(root) == (data.resolve(), "plugin")


@pytest.mark.parametrize("folder", ["codex-openai-codex", "claude-seo2", "seo-cockpit-stolosdigital", "claude"])
def test_foreign_plugin_data_falls_back_to_own_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, folder: str
) -> None:
    root = _plugin_root(tmp_path)
    foreign = tmp_path / ".claude" / "plugins" / "data" / folder
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(foreign))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path / "plugins" / "codex"))
    data_dir, mode = runtime._data_dir(root)
    assert mode == "plugin-fallback"
    assert data_dir.name == "claude-seo"
    assert data_dir != foreign.resolve()


def test_plugin_data_trusted_when_plugin_root_is_this_checkout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _plugin_root(tmp_path)
    data = tmp_path / "custom-host-data"
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(data))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(root))
    assert runtime._data_dir(root) == (data.resolve(), "plugin")


def test_explicit_override_wins_over_any_plugin_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _plugin_root(tmp_path)
    override = tmp_path / "my-seo-data"
    monkeypatch.setenv("CLAUDE_SEO_DATA_DIR", str(override))
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "data" / "claude-seo-stolosdigital"))
    assert runtime._data_dir(root) == (override.resolve(), "override")


def test_foreign_plugin_env_does_not_turn_source_checkout_into_plugin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _plugin_root(tmp_path)
    (root / ".git").mkdir()
    monkeypatch.setenv("CLAUDE_PLUGIN_DATA", str(tmp_path / "data" / "codex-openai-codex"))
    monkeypatch.setenv("CLAUDE_PLUGIN_ROOT", str(tmp_path / "plugins" / "codex"))
    assert runtime._data_dir(root) == (root, "manual")
