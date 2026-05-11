"""Rich terminal renderer for Trend Radar."""

import json
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

from .models import IntelItem, SourceType, TrendSnapshot


SOURCE_EMOJI = {
    SourceType.GITHUB: "🐙",
    SourceType.HACKERNEWS: "🔶",
    SourceType.REDDIT: "🤖",
    SourceType.ARXIV: "📄",
    SourceType.RSS: "📡",
    SourceType.PRODUCTHUNT: "🚀",
}


class TerminalRenderer:
    """Renders trend data as rich terminal output."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def render_snapshot(self, snapshot: TrendSnapshot, layout: str = "table"):
        """Render a trend snapshot."""
        self.console.print()
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
        """Render a list of items."""
        if not items:
            self.console.print("  No items found.", style="dim")
            return

        table = Table(title=title, show_lines=False, expand=True)
        table.add_column("#", style="dim", width=3)
        table.add_column("Source", width=3)
        table.add_column("Title", style="cyan", ratio=3)
        table.add_column("Score", justify="right", width=8)
        table.add_column("Info", ratio=2, style="dim")

        for i, item in enumerate(items, 1):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            info = item.description[:60] + "..." if len(item.description) > 60 else item.description
            if item.repo_language:
                info = f"[{item.repo_language}] {info}"

            table.add_row(
                str(i),
                emoji,
                item.title,
                item.score_display,
                info,
            )

        self.console.print(table)

    def _render_header(self, snapshot: TrendSnapshot):
        """Render dashboard header."""
        ts = snapshot.timestamp.strftime("%Y-%m-%d %H:%M UTC")
        sources = ", ".join(snapshot.sources_queried)

        header = Text(f"📡 Trend Radar — {ts}", style="bold cyan")
        self.console.print(header)
        self.console.print(f"  Sources: {sources}  |  Items: {snapshot.item_count}", style="dim")
        self.console.print("━" * 60, style="dim")

    def _render_table(self, snapshot: TrendSnapshot):
        """Render items as a table grouped by source."""
        for source in SourceType:
            items = snapshot.by_source(source)
            if not items:
                continue

            emoji = SOURCE_EMOJI.get(source, "•")
            table = Table(
                title=f"{emoji} {source.value.upper()}",
                show_lines=False,
                expand=True,
                title_style="bold",
            )
            table.add_column("#", style="dim", width=3)
            table.add_column("Title", style="cyan", ratio=3)
            table.add_column("Score", justify="right", width=8)
            table.add_column("Details", ratio=2, style="dim")

            for i, item in enumerate(items[:10], 1):
                details = item.description[:50] + "..." if len(item.description) > 50 else item.description
                if item.author:
                    details = f"by {item.author}  {details}"

                table.add_row(str(i), item.title, item.score_display, details)

            self.console.print()
            self.console.print(table)

    def _render_cards(self, snapshot: TrendSnapshot):
        """Render items as cards."""
        for item in snapshot.top(15):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            title_text = Text(f"{emoji} {item.title}", style="bold cyan")
            score_text = f"  ⭐ {item.score_display}" if item.score else ""

            panel_content = Text()
            if item.description:
                panel_content.append(item.description[:150] + "\n")
            if item.url:
                panel_content.append(f"🔗 {item.url}\n", style="blue")
            if item.author:
                panel_content.append(f"👤 {item.author}", style="dim")

            self.console.print(
                Panel(
                    panel_content,
                    title=title_text,
                    subtitle=score_text,
                    border_style="dim",
                )
            )

    def _render_compact(self, snapshot: TrendSnapshot):
        """Render compact single-line items."""
        for i, item in enumerate(snapshot.top(30), 1):
            emoji = SOURCE_EMOJI.get(item.source, "•")
            title = item.title[:50]
            score = f"({item.score_display})" if item.score else ""

            self.console.print(f"  {i:>2}. {emoji} {title} {score}", style="cyan" if i <= 5 else None)

    def _render_keywords(self, snapshot: TrendSnapshot):
        """Render trending keywords."""
        kw = snapshot.keywords(15)
        if not kw:
            return

        self.console.print()
        keywords_text = Text("🔑 Keywords: ", style="bold")
        for word, count in kw[:15]:
            style = "bold red" if count >= 3 else "yellow" if count >= 2 else "dim"
            keywords_text.append(f"{word}({count}) ", style=style)

        self.console.print(keywords_text)

    def _render_summary(self, snapshot: TrendSnapshot):
        """Render summary stats."""
        self.console.print()
        by_source = {}
        for item in snapshot.items:
            src = item.source.value
            by_source[src] = by_source.get(src, 0) + 1

        parts = [f"{s}: {c}" for s, c in sorted(by_source.items())]
        self.console.print(f"  📊 Total: {snapshot.item_count}  |  {'  |  '.join(parts)}", style="dim")

        if snapshot.errors:
            self.console.print(f"  ⚠️  Errors: {len(snapshot.errors)}", style="red")


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
        lines = [f"# 📡 Trend Radar — {ts}", ""]

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
