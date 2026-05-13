"""Trend momentum — track velocity and acceleration of trends.

Instead of just knowing "this repo has 5000 stars", we track:
- Velocity: How fast the score is changing per hour
- Acceleration: Is the velocity increasing or decreasing?
- Trajectory: Is this a steady climber or a viral spike?

This data enables predictions like "this will hit 10k stars by tomorrow".
"""

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from .models import IntelItem, SourceType


@dataclass
class MomentumData:
    """Momentum analysis for a single tracked item."""

    title: str
    source: str
    current_score: int = 0
    previous_score: int = 0
    score_delta: int = 0
    velocity: float = 0.0          # score change per hour
    acceleration: float = 0.0      # velocity change per hour
    hours_tracked: float = 0.0
    trajectory: str = "stable"     # viral | rising | stable | falling | dead
    confidence: float = 0.0        # 0-1, based on data points

    @property
    def is_trending(self) -> bool:
        """Is this item actively trending upward?"""
        return self.trajectory in ("viral", "rising") and self.velocity > 0

    @property
    def predicted_score_24h(self) -> int:
        """Predict score in 24 hours based on current momentum."""
        if self.velocity <= 0:
            return max(0, self.current_score + int(self.velocity * 24))
        # Apply acceleration
        predicted = self.current_score + self.velocity * 24 + 0.5 * self.acceleration * 24 * 24
        return max(0, int(predicted))

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "source": self.source,
            "current_score": self.current_score,
            "previous_score": self.previous_score,
            "score_delta": self.score_delta,
            "velocity": round(self.velocity, 2),
            "acceleration": round(self.acceleration, 2),
            "hours_tracked": round(self.hours_tracked, 1),
            "trajectory": self.trajectory,
            "confidence": round(self.confidence, 2),
            "predicted_24h": self.predicted_score_24h,
        }


def classify_trajectory(velocity: float, acceleration: float, score: int) -> str:
    """Classify the trajectory of a trend.

    Args:
        velocity: Score change per hour.
        acceleration: Velocity change per hour.
        score: Current absolute score.

    Returns:
        Trajectory label: viral, rising, stable, falling, or dead.
    """
    if score == 0:
        return "dead"

    # Viral: high velocity AND accelerating
    if velocity > 100 and acceleration > 10:
        return "viral"

    # Rising: positive velocity
    if velocity > 10:
        return "rising"

    # Stable: near zero velocity
    if abs(velocity) <= 10:
        return "stable"

    # Falling: negative velocity
    if velocity < -10:
        return "falling"

    return "dead" if score < 10 else "stable"


def compute_momentum(
    title: str,
    source: str,
    current_score: int,
    previous_score: int,
    hours_between: float,
    earlier_score: Optional[int] = None,
    earlier_hours: Optional[float] = None,
) -> MomentumData:
    """Compute momentum metrics for a single item.

    Args:
        title: Item title.
        source: Source name.
        current_score: Latest score.
        previous_score: Previous score.
        hours_between: Hours between the two measurements.
        earlier_score: Optional third data point for acceleration.
        earlier_hours: Hours between previous and earlier measurements.

    Returns:
        MomentumData with velocity, acceleration, and trajectory.
    """
    delta = current_score - previous_score

    # Velocity: score change per hour
    if hours_between > 0:
        velocity = delta / hours_between
    else:
        velocity = float(delta)

    # Acceleration: requires 3 data points
    acceleration = 0.0
    if earlier_score is not None and earlier_hours is not None and earlier_hours > 0:
        prev_velocity = (previous_score - earlier_score) / earlier_hours
        if hours_between > 0:
            acceleration = (velocity - prev_velocity) / hours_between

    # Confidence based on data availability
    confidence = 0.5 if earlier_score is None else 0.8
    if hours_between > 1:
        confidence = min(1.0, confidence + 0.2)

    trajectory = classify_trajectory(velocity, acceleration, current_score)

    return MomentumData(
        title=title,
        source=source,
        current_score=current_score,
        previous_score=previous_score,
        score_delta=delta,
        velocity=velocity,
        acceleration=acceleration,
        hours_tracked=hours_between,
        trajectory=trajectory,
        confidence=confidence,
    )


def analyze_snapshot_momentum(store: "TrendStore", hours: float = 48) -> list[MomentumData]:
    """Analyze momentum across all items in recent snapshots.

    Args:
        store: TrendStore instance.
        hours: How far back to look for history.

    Returns:
        List of MomentumData sorted by velocity descending.
    """
    from .store import TrendStore

    snapshots = store.get_snapshots(limit=10)
    if len(snapshots) < 2:
        return []

    # Get items from latest two snapshots
    current_items = store.get_snapshot_items(snapshots[0]["id"])
    previous_items = store.get_snapshot_items(snapshots[1]["id"])

    # Build lookup
    prev_map: dict[str, dict] = {}
    for item in previous_items:
        key = item["title"].lower().strip()
        if key not in prev_map or item.get("score", 0) > prev_map[key].get("score", 0):
            prev_map[key] = item

    # Compute time between snapshots
    try:
        ts_format = "%Y-%m-%dT%H:%M:%S"
        ts0 = datetime.fromisoformat(snapshots[0]["timestamp"][:19])
        ts1 = datetime.fromisoformat(snapshots[1]["timestamp"][:19])
        hours_between = max(0.1, (ts0 - ts1).total_seconds() / 3600)
    except (ValueError, KeyError):
        hours_between = 24.0

    results = []
    for item in current_items:
        key = item["title"].lower().strip()
        if key in prev_map:
            momentum = compute_momentum(
                title=item["title"],
                source=item.get("source", "unknown"),
                current_score=item.get("score", 0),
                previous_score=prev_map[key].get("score", 0),
                hours_between=hours_between,
            )
            results.append(momentum)

    return sorted(results, key=lambda x: x.velocity, reverse=True)
