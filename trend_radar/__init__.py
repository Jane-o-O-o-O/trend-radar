"""Trend Radar — Multi-source tech intelligence CLI.

Aggregate GitHub, Hacker News, Reddit, arXiv, RSS, and Product Hunt
trends into a single beautiful terminal dashboard.
"""

__version__ = "0.6.0"

from .core import TrendRadar
from .models import IntelItem, SourceType, TrendSnapshot, STOP_WORDS
from .store import TrendStore
from .config import TrendConfig
from .render import TerminalRenderer, JsonRenderer, MarkdownRenderer
from .normalization import normalize_score, normalized_badge, rank_cross_source
from .momentum import MomentumData, compute_momentum, analyze_snapshot_momentum
from .alerts import AlertStore, Alert, AlertMatch
from .opml import import_feeds, import_opml

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
]
