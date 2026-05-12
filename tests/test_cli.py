"""End-to-end CLI tests using Click's CliRunner."""

import json
import tempfile
import os
from unittest.mock import patch, MagicMock

from click.testing import CliRunner
from trend_radar.cli import main
from trend_radar.models import IntelItem, SourceType, TrendSnapshot


def _make_runner():
    return CliRunner()


def _mock_snapshot():
    """Create a mock snapshot with test data."""
    return TrendSnapshot(
        items=[
            IntelItem(title="test-repo", source=SourceType.GITHUB, score=5000,
                      url="https://github.com/test/repo", description="A test repo",
                      author="tester", repo_stars=5000, repo_language="Python"),
            IntelItem(title="Show HN: Test", source=SourceType.HACKERNEWS, score=300,
                      url="https://news.ycombinator.com/item/1", description="Test HN post"),
            IntelItem(title="AI agent tool", source=SourceType.REDDIT, score=150,
                      url="https://reddit.com/r/ai/1", description="Test reddit post"),
        ],
        sources_queried=["github", "hackernews", "reddit"],
    )


def test_cli_version():
    runner = _make_runner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0." in result.output


def test_cli_help():
    runner = _make_runner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Trend Radar" in result.output
    assert "fetch" in result.output
    assert "search" in result.output


def test_cli_fetch_help():
    runner = _make_runner()
    result = runner.invoke(main, ["fetch", "--help"])
    assert result.exit_code == 0
    assert "--sources" in result.output
    assert "--layout" in result.output
    assert "--output" in result.output


def test_cli_fetch_json(tmp_path):
    """Test fetch with JSON output."""
    runner = _make_runner()
    mock_snap = _mock_snapshot()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.collect.return_value = mock_snap

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "fetch", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data
        assert data["item_count"] == 3


def test_cli_fetch_markdown(tmp_path):
    """Test fetch with Markdown output."""
    runner = _make_runner()
    mock_snap = _mock_snapshot()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.collect.return_value = mock_snap

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "fetch", "--markdown"])
        assert result.exit_code == 0
        assert "# 📡 Trend Radar" in result.output


def test_cli_fetch_output_file(tmp_path):
    """Test fetch with --output file."""
    runner = _make_runner()
    mock_snap = _mock_snapshot()
    out_file = tmp_path / "output.md"

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.collect.return_value = mock_snap

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "fetch", "--json", "-o", str(out_file)])
        assert result.exit_code == 0
        assert out_file.exists()
        content = out_file.read_text()
        data = json.loads(content)
        assert "items" in data


def test_cli_search_json(tmp_path):
    """Test search with JSON output."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.search.return_value = [
            IntelItem(title="found", source=SourceType.GITHUB, score=100),
        ]

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "search", "test", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["item_count"] == 1


def test_cli_search_no_results(tmp_path):
    """Test search with no results."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.search.return_value = []

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "search", "nonexistent"])
        assert result.exit_code == 0


def test_cli_stats(tmp_path):
    """Test stats command."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.get_stats.return_value = {
            "total_snapshots": 5,
            "total_items": 150,
            "sources": ["github", "hackernews"],
            "latest_snapshot": "2026-05-12T00:00:00",
        }

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "stats"])
        assert result.exit_code == 0


def test_cli_keywords_empty(tmp_path):
    """Test keywords with no data."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.store = MagicMock()
        instance.store.get_keyword_trends.return_value = []

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "keywords"])
        assert result.exit_code == 0


def test_cli_keywords_with_data(tmp_path):
    """Test keywords with data."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.store = MagicMock()
        instance.store.get_keyword_trends.return_value = [
            ("agent", 12), ("llm", 8), ("ai", 6), ("code", 4),
        ]

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "keywords"])
        assert result.exit_code == 0


def test_cli_history_empty(tmp_path):
    """Test history with no data."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.store = MagicMock()
        instance.store.get_trending_items.return_value = []

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "history"])
        assert result.exit_code == 0


def test_cli_history_with_data(tmp_path):
    """Test history with data."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.store = MagicMock()
        instance.store.get_trending_items.return_value = [
            {"title": "test", "source": "github", "url": "https://x.com",
             "description": "desc", "score": 100, "author": "user"},
        ]

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "history"])
        assert result.exit_code == 0


def test_cli_config_show(tmp_path):
    """Test config-show command."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.config = MagicMock()
        instance.config._config = {"sources": {"github": {"enabled": True}}}

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "config-show"])
        assert result.exit_code == 0


def test_cli_config_set(tmp_path):
    """Test config-set command."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.config = MagicMock()

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "config-set", "sources.github.enabled", "true"])
        assert result.exit_code == 0
        instance.config.set.assert_called_once()


def test_cli_sources_list(tmp_path):
    """Test sources-list command."""
    runner = _make_runner()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.sources = {"github": MagicMock(), "hackernews": MagicMock()}

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "sources-list"])
        assert result.exit_code == 0


def test_cli_fetch_specific_sources(tmp_path):
    """Test fetch with specific sources."""
    runner = _make_runner()
    mock_snap = _mock_snapshot()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.collect.return_value = mock_snap

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "fetch", "-s", "github,hn", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data


def test_cli_ai_command(tmp_path):
    """Test AI-focused command."""
    runner = _make_runner()
    mock_snap = _mock_snapshot()

    with patch("trend_radar.cli.TrendRadar") as MockRadar:
        instance = MockRadar.return_value
        instance.collect_ai_focused.return_value = mock_snap

        result = runner.invoke(main, ["--db", str(tmp_path / "test.db"),
                                       "--config", str(tmp_path / "cfg.yaml"),
                                       "ai", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert "items" in data
