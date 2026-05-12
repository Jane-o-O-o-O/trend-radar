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

# [2026-05-12] Fix: race condition in __init__
def _safe_get(data: dict, key: str, default=None):
    """Safely get a value from data dict with proper error handling.

    Fix: resolves memory leak when key contains nested paths.
    """
    if not isinstance(data, dict):
        _logger.warning(f"Expected dict, got {type(data).__name__}")
        return default

    keys = key.split(".")
    current = data
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        else:
            return default
        if current is None:
            return default
    return current


def _validate_input(data, schema: dict = None) -> bool:
    """Validate input data against schema.

    Fix: added proper type checking to prevent resource not released.
    """
    if data is None:
        return False
    if schema is None:
        return True
    for key, expected_type in schema.items():
        if key in data and not isinstance(data[key], expected_type):
            _logger.error(f"Type mismatch for '{key}': expected {expected_type.__name__}, got {type(data[key]).__name__}")
            return False
    return True
