"""CLI entry point for Trend Radar — beautiful terminal dashboard."""

import json
import sys
import time

import click
from rich.console import Console
from rich.panel import Panel

from .core import TrendRadar
from .render import JsonRenderer, MarkdownRenderer, TerminalRenderer


def _get_radar(ctx) -> TrendRadar:
    return ctx.obj["radar"]


def _get_console(ctx) -> Console:
    return ctx.obj["console"]


@click.group()
@click.version_option("0.5.0")
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
@click.option("--html", "output_html", is_flag=True, help="Output as standalone HTML")
@click.option("--csv", "output_csv", is_flag=True, help="Output as CSV")
@click.option("--watch", "-w", is_flag=False, type=int, default=0, help="Auto-refresh every N seconds (0=off)")
@click.option("--no-banner", is_flag=True, help="Hide ASCII banner")
@click.option("--output", "-o", "output_file", default=None, help="Write output to file")
@click.option("--topic", "-t", default=None, help="Filter by topic (ai, web, mobile, security, devops, data, lang)")
@click.option("--no-parallel", is_flag=True, help="Disable parallel source fetching")
@click.pass_context
def fetch(ctx, sources, limit, layout, output_json, output_md, output_html, output_csv, watch, no_banner, output_file, topic, no_parallel):
    """Fetch trending intel from all sources."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)
    source_list = sources.split(",") if sources else None

    def do_fetch():
        with console.status("[bold bright_cyan]📡 Fetching intel...[/]"):
            snapshot = radar.collect(
                sources=source_list,
                limit=limit,
                parallel=not no_parallel,
            )

        # Apply topic filter
        if topic and snapshot.items:
            snapshot.items = [i for i in snapshot.items if radar._matches_topic(i, topic)]

        if output_json:
            text = JsonRenderer().render(snapshot)
        elif output_md:
            text = MarkdownRenderer().render(snapshot)
        elif output_html:
            from .exporters.html import HtmlRenderer
            text = HtmlRenderer().render(snapshot)
        elif output_csv:
            from .exporters.csv_export import CsvRenderer
            text = CsvRenderer().render(snapshot)
        elif output_file:
            # Auto-detect format from extension
            ext = output_file.rsplit(".", 1)[-1].lower() if "." in output_file else ""
            if ext == "html" or ext == "htm":
                from .exporters.html import HtmlRenderer
                text = HtmlRenderer().render(snapshot)
            elif ext == "csv":
                from .exporters.csv_export import CsvRenderer
                text = CsvRenderer().render(snapshot)
            elif ext == "json":
                text = JsonRenderer().render(snapshot)
            else:
                text = MarkdownRenderer().render(snapshot)
        else:
            TerminalRenderer(console, show_banner=not no_banner).render_snapshot(snapshot, layout=layout)
            return

        if output_file:
            from pathlib import Path
            Path(output_file).write_text(text, encoding="utf-8")
            console.print(f"[green]✓[/] Output written to [bold]{output_file}[/]")
        else:
            click.echo(text)

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
    from .models import SourceType
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


@main.command()
@click.option("--host", "-h", default="127.0.0.1", help="Host to bind")
@click.option("--port", "-p", default=8765, help="Port to listen on", type=int)
@click.option("--no-browser", is_flag=True, help="Don't auto-open browser")
@click.pass_context
def serve(ctx, host, port, no_browser):
    """Start the web dashboard server."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    try:
        from .web import create_app, HAS_FASTAPI
        if not HAS_FASTAPI:
            console.print("[red]Error:[/red] fastapi and uvicorn are required.")
            console.print("Install with: [bold]pip install fastapi uvicorn[/]")
            sys.exit(1)
    except ImportError:
        console.print("[red]Error:[/red] fastapi and uvicorn are required.")
        console.print("Install with: [bold]pip install fastapi uvicorn[/]")
        sys.exit(1)

    app = create_app(radar=radar, host=host, port=port)

    console.print(f"\n[bold bright_cyan]📡 Trend Radar Web Dashboard[/]")
    console.print(f"   [dim]Open:[/] [link=http://{host}:{port}]http://{host}:{port}[/link]")
    console.print(f"   [dim]API:[/]  [link=http://{host}:{port}/api/fetch]http://{host}:{port}/api/fetch[/link]")
    console.print(f"\n[dim]Press Ctrl+C to stop.[/]\n")

    if not no_browser:
        import webbrowser
        try:
            webbrowser.open(f"http://{host}:{port}")
        except Exception:
            pass

    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="warning")


@main.command()
@click.pass_context
def shell(ctx):
    """Launch interactive Trend Radar shell."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)
    from .shell import run_shell
    run_shell(radar, console)


@main.command()
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-banner", is_flag=True, help="Hide ASCII banner")
@click.pass_context
def diff(ctx, output_json, no_banner):
    """Compare latest two snapshots — show rising/falling trends."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    with console.status("[bold bright_cyan]📊 Computing diff...[/]"):
        diff_data = radar.diff_snapshots()

    if output_json:
        import json
        click.echo(json.dumps(diff_data, indent=2, ensure_ascii=False, default=str))
    else:
        from .render import TerminalRenderer
        TerminalRenderer(console, show_banner=not no_banner).render_diff(diff_data)


@main.command()
@click.option("--limit", "-n", default=20, help="Max items", type=int)
@click.option("--hours", "-h", default=24, help="Hours to look back", type=int)
@click.option("--source", "-s", default=None, help="Filter by source")
@click.option("--topic", "-t", default=None, help="Filter by topic (ai, web, mobile, security, devops, data, lang)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--no-banner", is_flag=True, help="Hide ASCII banner")
@click.pass_context
def top(ctx, limit, hours, source, topic, output_json, no_banner):
    """Quick view of top trending items across all sources."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    with console.status("[bold bright_cyan]🏆 Loading top items...[/]"):
        items = radar.get_top_items(limit=limit, hours=hours, source=source, topic=topic)

    if output_json:
        from .models import TrendSnapshot
        snapshot = TrendSnapshot(items=items)
        click.echo(JsonRenderer().render(snapshot))
    else:
        topic_label = f" [{topic}]" if topic else ""
        source_label = f" ({source})" if source else ""
        from .render import TerminalRenderer
        TerminalRenderer(console, show_banner=not no_banner).render_items(
            items, title=f"🏆 Top {limit}{topic_label}{source_label} ({hours}h)"
        )


@main.command()
@click.pass_context
def health(ctx):
    """Check data source connectivity and response times."""
    radar = _get_radar(ctx)
    console = _get_console(ctx)

    with console.status("[bold bright_cyan]🏥 Checking sources...[/]"):
        results = radar.check_health()

    from .render import TerminalRenderer
    TerminalRenderer(console, show_banner=False).render_health(results)


if __name__ == "__main__":
    main()
