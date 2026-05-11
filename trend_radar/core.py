"""Core engine — orchestrates sources, storage, and rendering."""

import os
from typing import Optional

from .models import IntelItem, SourceType, TrendSnapshot
from .sources import DataSource
from .sources.github import GitHubSource
from .sources.hackernews import HackerNewsSource
from .sources.reddit import RedditSource
from .sources.arxiv import ArxivSource
from .sources.rss import RSSSource
from .store import TrendStore


class TrendRadar:
    """Main engine that aggregates all data sources."""

    def __init__(self, db_path: Optional[str] = None, github_token: Optional[str] = None):
        self.store = TrendStore(db_path)
        self.github_token = github_token or os.getenv("GITHUB_TOKEN", "")

        # Initialize sources
        self.sources: dict[str, DataSource] = {
            "github": GitHubSource(token=self.github_token),
            "hackernews": HackerNewsSource(),
            "reddit": RedditSource(),
            "arxiv": ArxivSource(),
            "rss": RSSSource(),
        }

    def collect(
        self,
        sources: list[str] | None = None,
        limit: int = 25,
        save: bool = True,
        **kwargs,
    ) -> TrendSnapshot:
        """Collect intel from all (or specified) sources."""
        target_sources = sources or list(self.sources.keys())
        snapshot = TrendSnapshot()

        for name in target_sources:
            source = self.sources.get(name)
            if not source:
                snapshot.errors.append(f"Unknown source: {name}")
                continue

            try:
                items = source.fetch(limit=limit, **kwargs)
                snapshot.items.extend(items)
                snapshot.sources_queried.append(name)
            except Exception as e:
                snapshot.errors.append(f"{name}: {e}")

        if save:
            self.store.save_snapshot(snapshot)

        return snapshot

    def collect_ai_focused(self, limit: int = 25, save: bool = True) -> TrendSnapshot:
        """Collect with AI/LLM focus across all sources."""
        snapshot = TrendSnapshot()

        # GitHub: search for AI repos
        try:
            gh_items = self.sources["github"].search("AI LLM agent", limit=limit, min_stars=50)
            snapshot.items.extend(gh_items)
            snapshot.sources_queried.append("github")
        except Exception as e:
            snapshot.errors.append(f"github: {e}")

        # HN: top stories
        try:
            hn_items = self.sources["hackernews"].fetch(limit=limit)
            snapshot.items.extend(hn_items)
            snapshot.sources_queried.append("hackernews")
        except Exception as e:
            snapshot.errors.append(f"hackernews: {e}")

        # Reddit: AI subreddits
        try:
            reddit_items = self.sources["reddit"].fetch_ai_trends(limit=limit)
            snapshot.items.extend(reddit_items)
            snapshot.sources_queried.append("reddit")
        except Exception as e:
            snapshot.errors.append(f"reddit: {e}")

        # arXiv: AI papers
        try:
            arxiv_items = self.sources["arxiv"].fetch(limit=limit // 2, category="ai")
            snapshot.items.extend(arxiv_items)
            snapshot.sources_queried.append("arxiv")
        except Exception as e:
            snapshot.errors.append(f"arxiv: {e}")

        if save:
            self.store.save_snapshot(snapshot)

        return snapshot

    def search(self, query: str, sources: list[str] | None = None, limit: int = 25) -> list[IntelItem]:
        """Search across sources for a query."""
        items = []
        target = sources or ["github", "hackernews", "reddit", "arxiv"]

        if "github" in target:
            try:
                items.extend(self.sources["github"].search(query, limit=limit))
            except Exception:
                pass

        if "arxiv" in target:
            try:
                items.extend(self.sources["arxiv"].search(query, limit=limit))
            except Exception:
                pass

        # For HN and Reddit, filter fetched items
        if "hackernews" in target:
            try:
                hn = self.sources["hackernews"].fetch(limit=50)
                items.extend([i for i in hn if query.lower() in i.title.lower()][:limit])
            except Exception:
                pass

        if "reddit" in target:
            try:
                rd = self.sources["reddit"].fetch(limit=50)
                items.extend([i for i in rd if query.lower() in i.title.lower()][:limit])
            except Exception:
                pass

        return sorted(items, key=lambda x: x.score, reverse=True)[:limit]

    def analyze_opportunities(self, snapshot: TrendSnapshot) -> dict:
        """Analyze a snapshot for opportunities."""
        from collections import Counter

        # Keywords
        keywords = snapshot.keywords(30)

        # Source distribution
        source_dist = Counter(i.source.value for i in snapshot.items)

        # Top items
        top = snapshot.top(10)

        # High-star repos (potential competition or inspiration)
        high_star = [i for i in snapshot.items if i.source == SourceType.GITHUB and (i.repo_stars or 0) >= 100]

        # Languages
        lang_dist = Counter(i.repo_language for i in snapshot.items if i.repo_language)

        return {
            "total_items": snapshot.item_count,
            "sources_queried": snapshot.sources_queried,
            "top_items": [i.to_dict() for i in top],
            "keywords": keywords,
            "source_distribution": dict(source_dist),
            "high_star_repos": [i.to_dict() for i in high_star[:10]],
            "language_distribution": dict(lang_dist.most_common(10)),
            "errors": snapshot.errors,
        }

    def get_stats(self) -> dict:
        """Get engine statistics."""
        return self.store.get_stats()
