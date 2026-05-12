"""Trend Radar — Multi-source tech intelligence CLI.

Aggregate GitHub, Hacker News, Reddit, arXiv, RSS, and Product Hunt
trends into a single beautiful terminal dashboard.
"""

__version__ = "0.3.0"

from .core import TrendRadar
from .models import IntelItem, SourceType, TrendSnapshot, STOP_WORDS
from .store import TrendStore
from .config import TrendConfig

__all__ = [
    "TrendRadar",
    "IntelItem",
    "SourceType",
    "TrendSnapshot",
    "TrendStore",
    "TrendConfig",
    "STOP_WORDS",
]
