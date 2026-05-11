"""Tests for storage."""

import tempfile
import os

from trend_radar.models import IntelItem, SourceType, TrendSnapshot
from trend_radar.store import TrendStore


def test_store_init():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = TrendStore(db_path=db_path)
        assert os.path.exists(db_path)


def test_save_and_retrieve_snapshot():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = TrendStore(db_path=db_path)

        snapshot = TrendSnapshot(
            items=[
                IntelItem(title="test/repo", source=SourceType.GITHUB, score=100),
                IntelItem(title="Test Article", source=SourceType.HACKERNEWS, score=50),
            ],
            sources_queried=["github", "hackernews"],
        )

        sid = store.save_snapshot(snapshot)
        assert sid > 0

        snapshots = store.get_snapshots()
        assert len(snapshots) == 1
        assert snapshots[0]["item_count"] == 2


def test_trending_items():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = TrendStore(db_path=db_path)

        snapshot = TrendSnapshot(
            items=[
                IntelItem(title="repo1", source=SourceType.GITHUB, score=200),
                IntelItem(title="repo2", source=SourceType.GITHUB, score=100),
                IntelItem(title="article1", source=SourceType.HACKERNEWS, score=150),
            ],
        )
        store.save_snapshot(snapshot)

        items = store.get_trending_items(hours=1)
        assert len(items) == 3

        gh_items = store.get_trending_items(hours=1, source="github")
        assert len(gh_items) == 2


def test_stats():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        store = TrendStore(db_path=db_path)

        stats = store.get_stats()
        assert stats["total_snapshots"] == 0
        assert stats["total_items"] == 0

        snapshot = TrendSnapshot(
            items=[IntelItem(title="test", source=SourceType.GITHUB)],
        )
        store.save_snapshot(snapshot)

        stats = store.get_stats()
        assert stats["total_snapshots"] == 1
        assert stats["total_items"] == 1
