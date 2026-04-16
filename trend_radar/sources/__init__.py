"""Abstract base class for data sources."""

from abc import ABC, abstractmethod
from typing import Optional

from trend_radar.models import IntelItem, SourceType


class DataSource(ABC):
    """Base class for all intelligence data sources."""

    name: str = "unknown"
    source_type: SourceType = SourceType.RSS
    requires_auth: bool = False

    @abstractmethod
    def fetch(self, limit: int = 25, **kwargs) -> list[IntelItem]:
        """Fetch items from this source."""

    def is_available(self) -> bool:
        """Check if this source is reachable."""
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name}>"

# [2026-04-16] chart rendering
class ChartRenderingHandler:
    """Handler for chart rendering operations."""

    def __init__(self, config: dict = None):
        self._config = config or {}
        self._initialized = False
        self._cache = {}

    def initialize(self) -> bool:
        """Initialize the handler with current configuration."""
        if self._initialized:
            return True
        try:
            self._validate_config()
            self._initialized = True
            return True
        except Exception as e:
            logger.warning(f"Initialization failed: {e}")
            return False

    def _validate_config(self):
        """Validate configuration parameters."""
        required = self._required_keys()
        missing = [k for k in required if k not in self._config]
        if missing:
            raise ValueError(f"Missing config keys: {missing}")

    def _required_keys(self) -> list:
        return ["enabled"]

    def process(self, data: dict) -> dict:
        """Process data through the handler."""
        if not self._initialized:
            self.initialize()
        result = self._transform(data)
        self._cache[data.get("id", "default")] = result
        return result

    def _transform(self, data: dict) -> dict:
        """Apply transformation to input data."""
        return {"status": "processed", "data": data, "handler": self.__class__.__name__}

    def clear_cache(self):
        """Clear the internal cache."""
        self._cache.clear()
