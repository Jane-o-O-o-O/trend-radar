"""CLI entry point for Trend Radar — beautiful terminal dashboard."""

import json
import sys
import time

import click
from rich.console import Console

from .core import TrendRadar
from .render import JsonRenderer, MarkdownRenderer, TerminalRenderer


def _get_radar(ctx) -> TrendRadar:
    return ctx.obj["radar"]


def _get_console(ctx) -> Console:
    return ctx.obj["console"]


@click.group()
@click.version_option("0.2.0")
@click.option("--db", default=None, help="Path to trends database")
@click.option("--github-token", default=None, help="GitHub personal access token")
@click.option("--config", "config_path", default=None, help="Path to config file")
@click.option("--no-cache", is_flag=True, help="Disable caching")
@click.pass_context
def main(ctx, db, github_token, config_path, no_cache):
    """📡 Trend Radar — Multi-source tech intelligence CLI.

    Aggregate tech trends from GitHub, Hacker News, Reddit, arXiv, RSS,
    and Product Hunt into a single beautiful terminal dashboard.
    """
    ctx.ensure_object(dict)
    ctx.obj["radar"] = TrendRadar(
        db_path=db,
        github_token=github_token,
        config_path=config_path,
        use_cache=not no_cache,
    )
    ctx.obj["console"] = Console()


@main.command()
@click.option("--sources", "-s", default=None, help="Comma-separated sources (github,hackernews,reddit,arxiv,rss,producthunt)")
@click.option("--limit", "-n", default=15, help="Items per source", type=int)
@click.option("--layout", "-l", type=click.Choice(["table", "cards", "compact"]), default="table")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--markdown", "output_md", is_flag=True, help="Output as Markdown")
@click.option("--watch", "-w", is_flag=False, type=int, default=0, help="Auto-refresh every N seconds (0=off)")
@click.option("--no-banner", is_flag=True, help="Hide ASCII banner")
@click.pass_context
def fetch(ctx, sources, limit, layout, output_json, output_md, watch, no_banner):
    """Fetch trending intel from all sources."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)
    source_list = sources.split(",") if sources else None

    def do_fetch():
        with console.status("[bold bright_cyan]📡 Fetching intel...[/]"):
            snapshot = radar.collect(sources=source_list, limit=limit)

        if output_json:
            click.echo(JsonRenderer().render(snapshot))
        elif output_md:
            click.echo(MarkdownRenderer().render(snapshot))
        else:
            TerminalRenderer(console, show_banner=not no_banner).render_snapshot(snapshot, layout=layout)

    if watch > 0:
        try:
            while True:
                console.clear()
                do_fetch()
                console.print(f"\n[dim]Refreshing in {watch}s... (Ctrl+C to stop)[/dim]")
                time.sleep(watch)
        except KeyboardInterrupt:
            console.print("\n[dim]Stopped.[/dim]")
    else:
        do_fetch()


@main.command()
@click.option("--limit", "-n", default=15, help="Items per source", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-banner", is_flag=True, help="Hide ASCII banner")
@click.pass_context
def ai(ctx, limit, output_json, no_banner):
    """Fetch AI/LLM focused intel across all sources."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    with console.status("[bold bright_cyan]🤖 Fetching AI intel...[/]"):
        snapshot = radar.collect_ai_focused(limit=limit)

    if output_json:
        click.echo(JsonRenderer().render(snapshot))
    else:
        TerminalRenderer(console, show_banner=not no_banner).render_snapshot(snapshot)


@main.command()
@click.argument("query")
@click.option("--sources", "-s", default="github,hackernews,reddit,arxiv", help="Sources to search")
@click.option("--limit", "-n", default=20, help="Max results", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_context
def search(ctx, query, sources, limit, output_json):
    """Search across all sources for a query."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)
    source_list = sources.split(",")

    with console.status(f"[bold bright_cyan]🔍 Searching for '{query}'...[/]"):
        items = radar.search(query, sources=source_list, limit=limit)

    if output_json:
        from .models import TrendSnapshot
        snapshot = TrendSnapshot(items=items)
        click.echo(JsonRenderer().render(snapshot))
    else:
        TerminalRenderer(console, show_banner=False).render_items(items, title=f"🔍 Search: {query}")


@main.command()
@click.option("--hours", "-h", default=24, help="Hours of history", type=int)
@click.option("--source", "-s", default=None, help="Filter by source")
@click.option("--limit", "-n", default=30, help="Max items", type=int)
@click.pass_context
def history(ctx, hours, source, limit):
    """Show trending items from recent history."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    items_raw = radar.store.get_trending_items(hours=hours, source=source, limit=limit)

    if not items_raw:
        console.print(Panel("[dim]No history found. Run 'trend-radar fetch' first.[/dim]", border_style="dim"))
        return

    from .models import IntelItem, SourceType
    items = []
    for r in items_raw:
        try:
            src = SourceType(r["source"])
        except ValueError:
            src = SourceType.RSS
        items.append(
            IntelItem(
                title=r["title"],
                source=src,
                url=r.get("url", ""),
                description=r.get("description", ""),
                score=r.get("score", 0),
                author=r.get("author", ""),
            )
        )

    TerminalRenderer(console, show_banner=False).render_items(items, title=f"📊 History ({hours}h)")


@main.command()
@click.option("--days", "-d", default=7, help="Days to look back", type=int)
@click.pass_context
def keywords(ctx, days):
    """Show trending keywords from recent data."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    kw = radar.store.get_keyword_trends(days=days)

    if not kw:
        console.print("[dim]No data found. Run 'trend-radar fetch' first.[/dim]")
        return

    from .render import progress_bar
    max_count = max(c for _, c in kw) if kw else 1

    console.print(f"\n[bold]🔑 Trending Keywords ({days} days)[/]\n")
    for word, count in kw[:25]:
        bar = progress_bar(count, max_count, width=30)
        if count >= 5:
            style = "bold bright_red"
        elif count >= 3:
            style = "bright_yellow"
        else:
            style = "dim"
        console.print(f"  [{style}]{word:<20} {bar} {count:>4}[/{style}]")


@main.command()
@click.pass_context
def stats(ctx):
    """Show database and cache statistics."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    st = radar.get_stats()

    from rich.table import Table as RichTable
    tbl = RichTable(title="📊 Trend Radar Stats", show_lines=False, border_style="bright_blue")
    tbl.add_column("Metric", style="bold")
    tbl.add_column("Value", justify="right")

    tbl.add_row("Snapshots", str(st.get("total_snapshots", 0)))
    tbl.add_row("Items", str(st.get("total_items", 0)))
    tbl.add_row("Sources", ", ".join(st.get("sources", [])) or "none")
    tbl.add_row("Latest", st.get("latest_snapshot") or "never")

    if "cache" in st:
        cache = st["cache"]
        tbl.add_row("Cache (memory)", str(cache.get("memory_entries", 0)))
        tbl.add_row("Cache (disk)", str(cache.get("disk_entries", 0)))
        disk_kb = cache.get("disk_size_bytes", 0) / 1024
        tbl.add_row("Cache size", f"{disk_kb:.1f} KB")

    console.print()
    console.print(tbl)


@main.command()
@click.pass_context
def config_show(ctx):
    """Show current configuration."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    import yaml
    cfg = radar.config._config
    console.print("\n[bold]⚙️  Configuration[/]\n")
    console.print(yaml.dump(cfg, default_flow_style=False, sort_keys=False))


@main.command()
@click.argument("key")
@click.argument("value")
@click.pass_context
def config_set(ctx, key, value):
    """Set a configuration value (dot-separated path)."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    # Try to parse as number/bool
    if value.lower() == "true":
        parsed = True
    elif value.lower() == "false":
        parsed = False
    else:
        try:
            parsed = int(value)
        except ValueError:
            try:
                parsed = float(value)
            except ValueError:
                parsed = value

    radar.config.set(key, parsed)
    radar.config.save()
    console.print(f"[green]✓[/] Set [bold]{key}[/] = {parsed}")


@main.command()
@click.pass_context
def sources_list(ctx):
    """List available data sources and their status."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    from .core import SOURCE_CLASSES
    from .render import SOURCE_EMOJI

    from rich.table import Table as RichTable
    tbl = RichTable(title="📡 Data Sources", show_lines=False, border_style="bright_blue")
    tbl.add_column("", width=3)
    tbl.add_column("Source", style="bold")
    tbl.add_column("Status", justify="center")
    tbl.add_column("Class", style="dim")

    for name, cls in SOURCE_CLASSES.items():
        try:
            st = SourceType(name) if name != "producthunt" else SourceType.PRODUCTHUNT
        except ValueError:
            st = SourceType.RSS
        emoji = SOURCE_EMOJI.get(st, "•")
        enabled = name in radar.sources
        status = "[green]✓ enabled[/]" if enabled else "[red]✗ disabled[/]"
        tbl.add_row(emoji, name, status, cls.__name__)

    console.print()
    console.print(tbl)


if __name__ == "__main__":
    main()
