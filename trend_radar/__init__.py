"""Trend Radar — Multi-source tech intelligence CLI.

Aggregate GitHub, Hacker News, Reddit, arXiv, RSS, and Product Hunt
trends into a single beautiful terminal dashboard.
"""

__version__ = "0.8.0"

from .core import TrendRadar
from .models import IntelItem, SourceType, TrendSnapshot, STOP_WORDS
from .store import TrendStore
from .config import TrendConfig
from .render import TerminalRenderer, JsonRenderer, MarkdownRenderer
from .normalization import normalize_score, normalized_badge, rank_cross_source
from .momentum import MomentumData, compute_momentum, analyze_snapshot_momentum
from .alerts import AlertStore, Alert, AlertMatch
from .opml import import_feeds, import_opml
from .live import LiveDashboard
from .digest import generate_digest_markdown, generate_digest_html
from .init_wizard import run_init_wizard
from .radar_chart import render_radar_chart, render_topic_breakdown, compute_topic_distribution
from .bookmarks import BookmarkStore
from .plugins import PluginManager
from .rate_limiter import TokenBucketRateLimiter, RateLimiterRegistry

__all__ = [
    "TrendRadar",
    "IntelItem",
    "SourceType",
    "TrendSnapshot",
    "TrendStore",
    "TrendConfig",
    "STOP_WORDS",
    "TerminalRenderer",
    "JsonRenderer",
    "MarkdownRenderer",
    "normalize_score",
    "normalized_badge",
    "rank_cross_source",
    "MomentumData",
    "compute_momentum",
    "analyze_snapshot_momentum",
    "AlertStore",
    "Alert",
    "AlertMatch",
    "import_feeds",
    "import_opml",
    "LiveDashboard",
    "generate_digest_markdown",
    "generate_digest_html",
    "run_init_wizard",
    "render_radar_chart",
    "render_topic_breakdown",
    "compute_topic_distribution",
    "BookmarkStore",
    "PluginManager",
    "TokenBucketRateLimiter",
    "RateLimiterRegistry",
]
