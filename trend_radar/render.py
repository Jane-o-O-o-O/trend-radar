"""Rich terminal renderer for Trend Radar — stunning visual output.

This module is responsible for the 'wow factor' that earns stars.
Every output should look like a premium dashboard.
"""

import json
import math
from typing import Optional

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.emoji import Emoji
from rich.markup import escape
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from .models import IntelItem, SourceType, TrendSnapshot


SOURCE_EMOJI = {
    SourceType.GITHUB: "🐙",
    SourceType.HACKERNEWS: "🔶",
    SourceType.REDDIT: "🤖",
    SourceType.ARXIV: "📄",
    SourceType.RSS: "📡",
    SourceType.PRODUCTHUNT: "🚀",
}

SOURCE_COLORS = {
    SourceType.GITHUB: "bright_white on grey11",
    SourceType.HACKERNEWS: "bold bright_yellow",
    SourceType.REDDIT: "bold bright_red",
    SourceType.ARXIV: "bold bright_cyan",
    SourceType.RSS: "bold bright_magenta",
    SourceType.PRODUCTHUNT: "bold bright_green",
}

SOURCE_BORDER = {
    SourceType.GITHUB: "bright_white",
    SourceType.HACKERNEWS: "yellow",
    SourceType.REDDIT: "red",
    SourceType.ARXIV: "cyan",
    SourceType.RSS: "magenta",
    SourceType.PRODUCTHUNT: "green",
}


BANNER_ART = r"""
[bold bright_cyan]
  ████████╗██████╗ ███████╗███╗   ██╗██████╗     ██████╗  █████╗ ██████╗  █████╗ ██████╗ 
  ╚══██╔══╝██╔══██╗██╔════╝████╗  ██║██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
     ██║   ██████╔╝█████╗  ██╔██╗ ██║██║  ██║    ██████╔╝███████║██║  ██║███████║██████╔╝
     ██║   ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║    ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗
     ██║   ██║  ██║███████╗██║ ╚████║██████╔╝    ██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
[/bold bright_cyan]
[dim]  Multi-source tech intelligence · GitHub · HN · Reddit · arXiv · RSS · Product Hunt[/dim]
"""


def sparkline(values: list[int], width: int = 20) -> str:
    """Generate a Unicode sparkline from a list of values."""
    if not values or max(values) == 0:
        return "─" * width

    blocks = " ▁▂▃▄▅▆▇█"
    mn, mx = min(values), max(values)
    rng = mx - mn or 1

    # Sample values to fit width
    if len(values) > width:
        step = len(values) / width
        sampled = [values[int(i * step)] for i in range(width)]
    else:
        sampled = values + [0] * (width - len(values))

    return "".join(blocks[min(int((v - mn) / rng * 8), 8)] for v in sampled)


def progress_bar(value: int, max_val: int, width: int = 20) -> str:
    """Generate a colored progress bar string."""
    if max_val <= 0:
        return "░" * width
    filled = min(int(value / max_val * width), width)
    return "█" * filled + "░" * (width - filled)


class TerminalRenderer:
    """Renders trend data as rich terminal output — the wow factor."""

    def __init__(self, console: Optional[Console] = None, show_banner: bool = True):
        self.console = console or Console()
        self.show_banner = show_banner

    def render_snapshot(self, snapshot: TrendSnapshot, layout: str = "table"):
        """Render a trend snapshot with full visual flair."""
        if self.show_banner:
            self.console.print(BANNER_ART)

        self._render_header(snapshot)

        if layout == "table":
            self._render_table(snapshot)
        elif layout == "cards":
            self._render_cards(snapshot)
        elif layout == "compact":
            self._render_compact(snapshot)

        self._render_keywords(snapshot)
        self._render_summary(snapshot)

    def render_items(self, items: list[IntelItem], title: str = "Trending"):
        """Render a list of items as a beautiful table."""
        if not items:
            self.console.print(
                Panel("[dim]No items found.[/dim]", border_style="dim")
            )
            return

        table = Table(
            title=f"[bold]{title}[/bold]",
            show_lines=False,
            expand=True,
            border_style="bright_blue",
            title_style="bold bright_cyan",
            header_style="bold bright_white on grey11",
        )
        table.add_column("#", style="dim", width=3, justify="right")
        table.add_column("", width=3)
        table.add_column("Title", style="cyan", ratio=3, no_wrap=False)
        table.add_column("Score", justify="right", width=8)
        table.add_column("Details", ratio=2, style="dim", no_wrap=False)

        for i, item in enumerate(items, 1):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            info = item.description[:60] + "…" if len(item.description) > 60 else item.description
            if item.repo_language:
                info = f"[bright_green]{item.repo_language}[/] {info}"

            # Color score based on magnitude
            score_str = self._colored_score(item)

            table.add_row(str(i), emoji, item.title, score_str, info)

        self.console.print()
        self.console.print(table)

    def _colored_score(self, item: IntelItem) -> Text:
        """Return a colored score display."""
        display = item.score_display
        if item.score >= 5000:
            return Text(display, style="bold bright_red")
        elif item.score >= 1000:
            return Text(display, style="bold bright_yellow")
        elif item.score >= 100:
            return Text(display, style="bright_green")
        elif item.score > 0:
            return Text(display, style="dim")
        return Text(display, style="dim")

    def _render_header(self, snapshot: TrendSnapshot):
        """Render a stunning dashboard header."""
        ts = snapshot.timestamp.strftime("%Y-%m-%d %H:%M UTC")

        header_table = Table.grid(padding=1)
        header_table.add_column(ratio=1)
        header_table.add_row(
            f"[bold bright_cyan]📡 Trend Radar[/]  [dim]·[/]  [bright_white]{ts}[/]"
        )

        # Source badges
        source_badges = []
        for src_name in snapshot.sources_queried:
            try:
                src_type = SourceType(src_name)
                emoji = SOURCE_EMOJI.get(src_type, "•")
            except ValueError:
                emoji = "•"
            badge = f"{emoji} {src_name}"
            source_badges.append(badge)

        badges_text = "  ".join(source_badges) if source_badges else "none"

        self.console.print()
        self.console.print(
            Panel(
                Group(
                    Align.center(header_table),
                    Align.center(
                        Text.from_markup(
                            f"[dim]Sources:[/] {badges_text}  [dim]│[/]  "
                            f"[dim]Items:[/] [bold]{snapshot.item_count}[/]"
                        )
                    ),
                ),
                border_style="bright_cyan",
                padding=(0, 2),
            )
        )

    def _render_table(self, snapshot: TrendSnapshot):
        """Render items grouped by source in colored tables."""
        any_items = False

        for source in SourceType:
            items = snapshot.by_source(source)
            if not items:
                continue

            any_items = True
            emoji = SOURCE_EMOJI.get(source, "•")
            border = SOURCE_BORDER.get(source, "dim")

            # Sort by score descending
            items_sorted = sorted(items, key=lambda x: x.score, reverse=True)

            table = Table(
                show_lines=False,
                expand=True,
                border_style=border,
                header_style=f"bold {border}",
                title_justify="left",
                padding=(0, 1),
            )
            table.add_column("#", style="dim", width=3, justify="right")
            table.add_column("Title", style="bright_white", ratio=3, no_wrap=False)
            table.add_column("Score", justify="right", width=9)
            table.add_column("Details", ratio=2, style="dim", no_wrap=False)

            max_score = max((it.score for it in items_sorted), default=1) or 1

            for i, item in enumerate(items_sorted[:10], 1):
                score_text = self._colored_score(item)

                # Build detail string
                details_parts = []
                if item.author:
                    details_parts.append(f"[bright_cyan]{item.author}[/]")
                if item.description:
                    desc = item.description[:50] + "…" if len(item.description) > 50 else item.description
                    details_parts.append(desc)
                details = "  ".join(details_parts)

                # Sparkline mini-bar for score
                bar = progress_bar(item.score, max_score, width=12)

                table.add_row(str(i), item.title, score_text, details)

            self.console.print()
            self.console.print(
                Panel(
                    table,
                    title=f"[bold]{emoji} {source.value.upper()}[/]",
                    title_align="left",
                    border_style=border,
                    padding=(0, 0),
                )
            )

        if not any_items:
            self.console.print(Panel("[dim]No items found from any source.[/dim]", border_style="dim"))

    def _render_cards(self, snapshot: TrendSnapshot):
        """Render items as panels/cards."""
        for i, item in enumerate(snapshot.top(12), 1):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            border = SOURCE_BORDER.get(item.source, "dim")

            # Title
            title = Text(f" {emoji} {item.title} ", style="bold bright_white")

            # Content
            content = Text()
            if item.description:
                content.append(item.description[:200] + "\n\n")
            if item.url:
                content.append(f"🔗 {item.url}\n", style="bright_blue underline")
            if item.author:
                content.append(f"👤 {item.author}", style="dim")

            # Subtitle with score
            subtitle = f"⭐ {item.score_display}" if item.score else ""

            self.console.print(
                Panel(
                    content,
                    title=title,
                    subtitle=subtitle,
                    subtitle_align="right",
                    border_style=border,
                    padding=(0, 2),
                )
            )

    def _render_compact(self, snapshot: TrendSnapshot):
        """Render compact single-line items."""
        items = snapshot.top(40)
        max_score = max((it.score for it in items), default=1) or 1

        self.console.print()
        for i, item in enumerate(items, 1):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            title = item.title[:55]
            bar = progress_bar(item.score, max_score, width=8)

            score_display = item.score_display
            rank_color = "bright_white" if i <= 3 else "bright_cyan" if i <= 10 else "dim"

            self.console.print(
                f"  [{rank_color}]{i:>2}.[/{rank_color}] {emoji} {title:<58} "
                f"{bar} [{rank_color}]{score_display:>7}[/{rank_color}]"
            )

    def _render_keywords(self, snapshot: TrendSnapshot):
        """Render trending keywords as a beautiful tag cloud."""
        kw = snapshot.keywords(20)
        if not kw:
            return

        self.console.print()
        self.console.print(Rule("[bold]🔑 Trending Keywords[/]", style="bright_blue"))

        # Build keyword display with frequency bars
        kw_table = Table(show_header=False, show_lines=False, padding=(0, 1), expand=True)
        kw_table.add_column("Word", style="bold", width=18)
        kw_table.add_column("Bar", ratio=2)
        kw_table.add_column("Count", justify="right", width=5)

        max_count = max(c for _, c in kw) if kw else 1
        for word, count in kw[:15]:
            bar = progress_bar(count, max_count, width=25)
            if count >= 5:
                style = "bright_red"
            elif count >= 3:
                style = "bright_yellow"
            else:
                style = "dim"

            kw_table.add_row(
                f"[{style}]{word}[/{style}]",
                f"[{style}]{bar}[/{style}]",
                f"[{style}]{count}[/{style}]",
            )

        self.console.print(kw_table)

    def _render_summary(self, snapshot: TrendSnapshot):
        """Render summary statistics."""
        by_source = {}
        for item in snapshot.items:
            src = item.source.value
            by_source[src] = by_source.get(src, 0) + 1

        parts = []
        for src_name, count in sorted(by_source.items()):
            try:
                src_type = SourceType(src_name)
                emoji = SOURCE_EMOJI.get(src_type, "•")
            except ValueError:
                emoji = "•"
            parts.append(f"{emoji} {src_name}({count})")

        summary_line = "  │  ".join(parts)

        self.console.print()
        self.console.print(Rule(style="dim"))
        self.console.print(
            f"  📊 [bold]{snapshot.item_count}[/] items  │  {summary_line}",
            style="dim",
        )

        if snapshot.errors:
            self.console.print(
                f"  ⚠️  [red]{len(snapshot.errors)} error(s)[/red]: "
                + "; ".join(snapshot.errors[:3]),
            )

        self.console.print()


class JsonRenderer:
    """Renders trend data as JSON."""

    def render(self, snapshot: TrendSnapshot) -> str:
        data = {
            "timestamp": snapshot.timestamp.isoformat(),
            "sources": snapshot.sources_queried,
            "item_count": snapshot.item_count,
            "errors": snapshot.errors,
            "items": [item.to_dict() for item in snapshot.items],
            "keywords": snapshot.keywords(20),
        }
        return json.dumps(data, indent=2, ensure_ascii=False)


class MarkdownRenderer:
    """Renders trend data as Markdown."""

    def render(self, snapshot: TrendSnapshot) -> str:
        ts = snapshot.timestamp.strftime("%Y-%m-%d %H:%M UTC")
        lines = [
            f"# 📡 Trend Radar — {ts}",
            "",
            f"> {snapshot.item_count} items from {', '.join(snapshot.sources_queried)}",
            "",
        ]

        for source in SourceType:
            items = snapshot.by_source(source)
            if not items:
                continue

            emoji = SOURCE_EMOJI.get(source, "•")
            lines.append(f"## {emoji} {source.value.upper()}")
            lines.append("")

            for i, item in enumerate(items[:10], 1):
                score_str = f" (⭐{item.score_display})" if item.score else ""
                lines.append(f"{i}. **[{item.title}]({item.url})**{score_str}")
                if item.description:
                    lines.append(f"   {item.description[:150]}")
                lines.append("")

        # Keywords
        kw = snapshot.keywords(15)
        if kw:
            lines.append("## 🔑 Trending Keywords")
            lines.append("")
            lines.append(", ".join(f"**{w}**({c})" for w, c in kw))
            lines.append("")

        return "\n".join(lines)
