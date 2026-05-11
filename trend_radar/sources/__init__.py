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
