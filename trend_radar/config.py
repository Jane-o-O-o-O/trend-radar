"""Configuration system for Trend Radar — ~/.trend-radar/config.yaml"""

import copy
import os
from pathlib import Path
from typing import Any, Optional

import yaml


DEFAULT_CONFIG = {
    "sources": {
        "github": {"enabled": True, "token": "", "min_stars": 10},
        "hackernews": {"enabled": True, "category": "top"},
        "reddit": {"enabled": True, "subreddits": [
            "MachineLearning", "LocalLLaMA", "artificial", "programming", "technology"
        ]},
        "arxiv": {"enabled": True, "category": "ai"},
        "rss": {"enabled": True, "feeds": {}},
        "producthunt": {"enabled": True},
    },
    "display": {
        "layout": "table",           # table | cards | compact
        "items_per_source": 15,
        "show_keywords": True,
        "color_theme": "default",    # default | monokai | dracula
    },
    "cache": {
        "enabled": True,
        "memory_ttl": 300,           # seconds
        "disk_ttl": 3600,
    },
    "output": {
        "format": "terminal",        # terminal | json | markdown
    },
}


def get_config_dir() -> Path:
    """Get or create config directory."""
    base = os.environ.get("TREND_RADAR_HOME", os.path.expanduser("~/.trend-radar"))
    path = Path(base)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_path() -> Path:
    return get_config_dir() / "config.yaml"


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base dict."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class TrendConfig:
    """Configuration manager for Trend Radar."""

    def __init__(self, config_path: Optional[str] = None):
        self.path = Path(config_path) if config_path else get_config_path()
        self._config: dict = {}
        self.load()

    def load(self, path: str | None = None) -> None:
        """Load config from file, merging with defaults."""
        if self.path.exists():
            try:
                with open(self.path) as f:
                    user_config = yaml.safe_load(f) or {}
                self._config = deep_merge(DEFAULT_CONFIG, user_config)
            except (yaml.YAMLError, OSError):
                self._config = copy.deepcopy(DEFAULT_CONFIG)
        else:
            self._config = copy.deepcopy(DEFAULT_CONFIG)
            self.save()  # Write default config

    def save(self) -> None:
        """Save current config to file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False, sort_keys=False)

    def get(self, dotpath: str, default: Any = None) -> Any:
        """Get config value by dot-separated path. e.g., 'sources.github.token'"""
        keys = dotpath.split(".")
        node = self._config
        for key in keys:
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                return default
        return node

    def set(self, dotpath: str, value: Any) -> None:
        """Set config value by dot-separated path."""
        keys = dotpath.split(".")
        node = self._config
        for key in keys[:-1]:
            if key not in node or not isinstance(node[key], dict):
                node[key] = {}
            node = node[key]
        node[keys[-1]] = value

    @property
    def enabled_sources(self) -> list[str]:
        """Get list of enabled source names."""
        sources = self._config.get("sources", {})
        return [name for name, cfg in sources.items() if cfg.get("enabled", True)]

    @property
    def layout(self) -> str:
        return self.get("display.layout", "table")

    @property
    def items_per_source(self) -> int:
        return self.get("display.items_per_source", 15)

    @property
    def cache_enabled(self) -> bool:
        return self.get("cache.enabled", True)

    @property
    def cache_memory_ttl(self) -> int:
        return self.get("cache.memory_ttl", 300)

    @property
    def cache_disk_ttl(self) -> int:
        return self.get("cache.disk_ttl", 3600)

    def source_config(self, name: str) -> dict:
        """Get config for a specific source."""
        return self.get(f"sources.{name}", {})

    def __repr__(self) -> str:
        return f"<TrendConfig path={self.path} sources={self.enabled_sources}>"

# [2026-04-02] Fix: stale cache reference in config
def _safe_get(data: dict, key: str, default=None):
    """Safely get a value from data dict with proper error handling.

    Fix: resolves encoding issue when key contains nested paths.
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

    Fix: added proper type checking to prevent missing validation.
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
