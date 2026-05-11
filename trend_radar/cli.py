"""CLI entry point for Trend Radar."""

import json
import sys

import click
from rich.console import Console

from .core import TrendRadar
from .render import JsonRenderer, MarkdownRenderer, TerminalRenderer


@click.group()
@click.version_option("0.1.0")
@click.option("--db", default=None, help="Path to trends database")
@click.option("--github-token", default=None, help="GitHub personal access token")
@click.pass_context
def main(ctx, db, github_token):
    """📡 Trend Radar — Multi-source tech intelligence CLI."""
    ctx.ensure_object(dict)
    ctx.obj["radar"] = TrendRadar(db_path=db, github_token=github_token)
    ctx.obj["console"] = Console()


@main.command()
@click.option("--sources", "-s", default=None, help="Comma-separated sources (github,hackernews,reddit,arxiv,rss)")
@click.option("--limit", "-n", default=15, help="Items per source")
@click.option("--layout", "-l", type=click.Choice(["table", "cards", "compact"]), default="table")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.option("--markdown", "output_md", is_flag=True, help="Output as Markdown")
@click.pass_context
def fetch(ctx, sources, limit, layout, output_json, output_md):
    """Fetch trending intel from all sources."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    source_list = sources.split(",") if sources else None

    with console.status("📡 Fetching intel..."):
        snapshot = radar.collect(sources=source_list, limit=limit)

    if output_json:
        click.echo(JsonRenderer().render(snapshot))
    elif output_md:
        click.echo(MarkdownRenderer().render(snapshot))
    else:
        TerminalRenderer(console).render_snapshot(snapshot, layout=layout)


@main.command()
@click.option("--limit", "-n", default=15, help="Items per source")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_context
def ai(ctx, limit, output_json):
    """Fetch AI/LLM focused intel across all sources."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    with console.status("🤖 Fetching AI intel..."):
        snapshot = radar.collect_ai_focused(limit=limit)

    if output_json:
        click.echo(JsonRenderer().render(snapshot))
    else:
        TerminalRenderer(console).render_snapshot(snapshot)


@main.command()
@click.argument("query")
@click.option("--sources", "-s", default="github,hackernews,reddit,arxiv", help="Sources to search")
@click.option("--limit", "-n", default=20, help="Max results")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
@click.pass_context
def search(ctx, query, sources, limit, output_json):
    """Search across all sources for a query."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    source_list = sources.split(",")

    with console.status(f"🔍 Searching for '{query}'..."):
        items = radar.search(query, sources=source_list, limit=limit)

    if output_json:
        from .models import TrendSnapshot
        snapshot = TrendSnapshot(items=items)
        click.echo(JsonRenderer().render(snapshot))
    else:
        TerminalRenderer(console).render_items(items, title=f"🔍 Search: {query}")


@main.command()
@click.option("--hours", "-h", default=24, help="Hours of history")
@click.option("--source", "-s", default=None, help="Filter by source")
@click.option("--limit", "-n", default=30, help="Max items")
@click.pass_context
def history(ctx, hours, source, limit):
    """Show trending items from recent history."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    items_raw = radar.store.get_trending_items(hours=hours, source=source, limit=limit)

    if not items_raw:
        console.print("  No history found. Run 'trend-radar fetch' first.", style="dim")
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

    TerminalRenderer(console).render_items(items, title=f"📊 History ({hours}h)")


@main.command()
@click.pass_context
def keywords(ctx):
    """Show trending keywords from recent data."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    kw = radar.store.get_keyword_trends(days=7)

    if not kw:
        console.print("  No data found. Run 'trend-radar fetch' first.", style="dim")
        return

    console.print("\n🔑 Trending Keywords (7 days)\n", style="bold")
    for word, count in kw[:20]:
        bar = "█" * min(count, 30)
        style = "bold red" if count >= 5 else "yellow" if count >= 3 else "dim"
        console.print(f"  {word:<20} {bar} {count}", style=style)


@main.command()
@click.pass_context
def stats(ctx):
    """Show database statistics."""
    radar = ctx.obj["radar"]
    console = ctx.obj["console"]

    st = radar.get_stats()

    console.print("\n📊 Trend Radar Stats\n", style="bold")
    console.print(f"  Snapshots: {st['total_snapshots']}")
    console.print(f"  Items:     {st['total_items']}")
    console.print(f"  Sources:   {', '.join(st['sources']) or 'none'}")
    console.print(f"  Latest:    {st['latest_snapshot'] or 'never'}")


if __name__ == "__main__":
    main()
