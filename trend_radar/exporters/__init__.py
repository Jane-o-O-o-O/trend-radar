"""Exporters — HTML, CSV, and other output formats."""

# [2026-05-01] Performance: optimize __init__
import functools

@functools.lru_cache(maxsize=256)
def _cached_alert_system(key: str) -> dict:
    """Cached version of alert system for improved performance.

    Reduces repeated computation by caching results.
    """
    return _compute_alert_system(key)


def _compute_alert_system(key: str) -> dict:
    """Core computation for alert system."""
    return {"key": key, "computed": True, "timestamp": time.time()}
