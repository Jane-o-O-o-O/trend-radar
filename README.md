# 📡 Trend Radar

> **Multi-source tech intelligence CLI** — See what's hot before everyone else.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-154%20passed-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
[![PyPI](https://img.shields.io/pypi/v/trend-radar?color=blue)](https://pypi.org/project/trend-radar/)

**One command. Six sources. Zero doom-scrolling.**

Trend Radar aggregates tech trends from **GitHub**, **Hacker News**, **Reddit**, **arXiv**, **RSS feeds**, and **Product Hunt** into a single, beautiful terminal dashboard. Track keywords over time, search across all sources, and never miss what's trending.

```
╭──────────────────────────────────────────────────────────────────────╮
│ 📡 Trend Radar                                                       │
│ 2026-05-12 02:00 UTC                                                 │
│ Sources: 🐙 github  🔶 hackernews  🤖 reddit  📄 arxiv  📡 rss       │
│ Items: 67                                                            │
╰──────────────────────────────────────────────────────────────────────╯

╭── 🐙 GITHUB ─────────────────────────────────────────────────────────╮
│ #  Title                          Score       Details                 │
│ 1  openai/codex-cli              🔥 12.4k    AI coding agent         │
│ 2  anthropic/claude-code          🟡 8.2k    CLI coding assistant    │
╰──────────────────────────────────────────────────────────────────────╯

╭── 🔶 HACKERNEWS ─────────────────────────────────────────────────────╮
│ #  Title                          Score       Details                 │
│ 1  Show HN: I built an AI agent   🔵 342     Autonomous coding       │
│ 2  Why every team needs MCP       🔵 287     MCP integration         │
╰──────────────────────────────────────────────────────────────────────╯

┌─ 🔑 Trending Keywords ─────────────────────────────────────────────────┐
│ agent      ████████████████████████  12                               │
│ coding     █████████████████         8                                │
│ llm        ██████████████            7                                │
│ mcp        ████████████              6                                │
└────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# Install (core)
pip install trend-radar

# Install with all features (web dashboard + interactive shell)
pip install trend-radar[all]

# Fetch from all sources
trend-radar fetch

# AI-focused intelligence
trend-radar ai

# Search for a topic
trend-radar search "MCP server"

# Interactive shell (REPL mode)
trend-radar shell

# Web dashboard
trend-radar serve

# Export as standalone HTML dashboard
trend-radar fetch --html -o dashboard.html

# Export as CSV
trend-radar fetch --csv -o trends.csv
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-source aggregation** | GitHub, HN, Reddit, arXiv, RSS, Product Hunt |
| 🎨 **Beautiful terminal output** | Rich-powered tables, cards, compact layouts |
| 🔑 **Trending keywords** | Auto-extracted keyword frequency analysis |
| 📊 **History tracking** | SQLite-backed trend history with time-series |
| 💾 **Two-level caching** | Memory TTL + disk SQLite cache |
| ⚙️ **YAML configuration** | `~/.trend-radar/config.yaml` for all settings |
| 🌐 **Web dashboard** | FastAPI-powered web UI with real-time API |
| 💻 **Interactive shell** | prompt_toolkit REPL with tab completion |
| 📄 **Export formats** | JSON, Markdown, HTML, CSV |
| 🔄 **Watch mode** | Auto-refresh every N seconds |
| 🤖 **Hermes Agent** | Built-in AI agent tool integration |

## 📦 Data Sources

| Source | Emoji | What you get | API |
|--------|-------|-------------|-----|
| **GitHub** | 🐙 | Trending repos + search | REST API + page scraping |
| **Hacker News** | 🔶 | Top/best/new/ask/show stories | Firebase API |
| **Reddit** | 🤖 | Hot posts from tech/AI subreddits | JSON API |
| **arXiv** | 📄 | Latest AI/ML research papers | Atom API |
| **RSS/Atom** | 📡 | Tech blogs (TechCrunch, OpenAI, etc.) | Standard RSS/Atom |
| **Product Hunt** | 🚀 | Today's trending products | Web scraping |

## 🛠️ Commands

```bash
# Fetch trending intel
trend-radar fetch                         # All sources, table layout
trend-radar fetch -s github,hn            # Specific sources
trend-radar fetch --layout cards          # Card layout
trend-radar fetch --layout compact        # Compact single-line
trend-radar fetch --json                  # JSON output (for scripting)
trend-radar fetch --markdown              # Markdown output
trend-radar fetch --html                  # Standalone HTML dashboard
trend-radar fetch --csv                   # CSV spreadsheet
trend-radar fetch --watch 30              # Auto-refresh every 30s
trend-radar fetch -o dashboard.html       # Auto-detect format from extension
trend-radar fetch -o trends.csv           # Save as CSV
trend-radar fetch -o report.md            # Save as Markdown

# AI-focused intel
trend-radar ai                            # AI/LLM across all sources
trend-radar ai --json                     # JSON output

# Search
trend-radar search "agent framework"      # Cross-source search
trend-radar search "MCP" -s github,arxiv  # Search specific sources

# History & Analysis
trend-radar history -h 48                 # Last 48h of data
trend-radar keywords                      # Trending keywords (7 days)
trend-radar keywords -d 30                # Last 30 days
trend-radar stats                         # Database statistics

# Interactive shell
trend-radar shell                         # Launch REPL with tab completion

# Web dashboard
trend-radar serve                         # Start web UI on :8765
trend-radar serve -p 3000                 # Custom port

# Configuration
trend-radar config-show                   # Show current config
trend-radar config-set sources.reddit.enabled false
trend-radar config-set display.layout compact
trend-radar sources-list                  # List all sources + status
```

## 🌐 Web Dashboard

Launch a beautiful web dashboard with real-time API:

```bash
# Install web dependencies
pip install trend-radar[web]

# Start the server
trend-radar serve --port 8765
```

Then open `http://localhost:8765` for the interactive dashboard, or use the API directly:

```bash
# REST API endpoints
curl http://localhost:8765/api/fetch
curl http://localhost:8765/api/ai
curl http://localhost:8765/api/search?q=MCP
curl http://localhost:8765/api/keywords?days=7
curl http://localhost:8765/api/stats
```

## 💻 Interactive Shell

Launch an interactive REPL with tab completion:

```bash
pip install trend-radar[shell]
trend-radar shell
```

```
📡 trend-radar> fetch --limit 10
📡 trend-radar> search MCP server
📡 trend-radar> keywords --days 30
📡 trend-radar> stats
📡 trend-radar> exit
```

## 🤖 Use as a Python Library

```python
from trend_radar import TrendRadar

radar = TrendRadar()

# Fetch trending from all sources
snapshot = radar.collect(sources=["github", "hackernews"], limit=10)
print(f"Got {snapshot.item_count} items")

# Top items by score
for item in snapshot.top(5):
    print(f"  {item.title} ({item.score_display})")

# Trending keywords
for word, count in snapshot.keywords(10):
    print(f"  {word}: {count}")

# AI-focused collection
snapshot = radar.collect_ai_focused(limit=15)

# Search
items = radar.search("MCP server", limit=20)

# Analysis
analysis = radar.analyze_opportunities(snapshot)

# Export to HTML
from trend_radar.exporters.html import HtmlRenderer
html = HtmlRenderer().render(snapshot)
with open("dashboard.html", "w") as f:
    f.write(html)

# Export to CSV
from trend_radar.exporters.csv_export import CsvRenderer
csv_data = CsvRenderer().render(snapshot)
```

## ⚙️ Configuration

Config file: `~/.trend-radar/config.yaml`

```yaml
sources:
  github:
    enabled: true
    token: ""           # Set GITHUB_TOKEN env var or fill this
    min_stars: 10
  hackernews:
    enabled: true
    category: top
  reddit:
    enabled: true
    subreddits:
      - MachineLearning
      - LocalLLaMA
      - artificial
      - programming
  arxiv:
    enabled: true
    category: ai
  rss:
    enabled: true
    feeds: {}           # Add custom feeds
  producthunt:
    enabled: true

display:
  layout: table          # table | cards | compact
  items_per_source: 15
  show_keywords: true
  color_theme: default   # default | monokai | dracula

cache:
  enabled: true
  memory_ttl: 300        # 5 minutes in-memory
  disk_ttl: 3600         # 1 hour on disk

output:
  format: terminal       # terminal | json | markdown | html | csv
```

## 🏗️ Architecture

```
trend_radar/
├── __init__.py          # Public API exports
├── core.py              # TrendRadar engine — orchestrates everything
├── models.py            # IntelItem, TrendSnapshot, SourceType
├── store.py             # SQLite storage for history tracking
├── cache.py             # Two-level cache (memory TTL + disk SQLite)
├── config.py            # YAML config system
├── render.py            # Rich terminal renderer (tables, cards, compact)
├── cli.py               # Click CLI with all commands
├── shell.py             # Interactive REPL with prompt_toolkit
├── web.py               # FastAPI web dashboard + REST API
├── exporters/
│   ├── __init__.py
│   ├── html.py          # Standalone HTML dashboard exporter
│   └── csv_export.py    # CSV spreadsheet exporter
├── sources/
│   ├── __init__.py      # DataSource ABC
│   ├── github.py        # GitHub trending + search API
│   ├── hackernews.py    # HN Firebase API (parallel fetching)
│   ├── reddit.py        # Reddit JSON API
│   ├── arxiv.py         # arXiv Atom API
│   ├── rss.py           # RSS/Atom feed parser
│   └── producthunt.py   # Product Hunt scraper
└── hermes_tool/
    └── __init__.py      # Hermes Agent integration
```

## 🔌 Hermes Agent Integration

Trend Radar works as a Hermes Agent tool:

```python
from trend_radar.hermes_tool import trend_fetch, trend_search, trend_keywords

# Fetch trending intel
result = trend_fetch(sources="github,hackernews", limit=10)

# Search across sources
result = trend_search("AI agent framework")

# Get trending keywords
result = trend_keywords(days=7)
```

## 🧪 Development

```bash
git clone https://github.com/Jane-o-O-o-O/trend-radar.git
cd trend-radar
pip install -e ".[all,dev]"
pytest
```

## 📊 Comparison

| Feature | Trend Radar | starcli | hn-cli | newsboat |
|---------|:-----------:|:------:|:------:|:--------:|
| Multi-source | ✅ 6 sources | GitHub only | HN only | RSS only |
| Terminal UI | ✅ Rich | ✅ | ❌ | ✅ |
| Web dashboard | ✅ FastAPI | ❌ | ❌ | ❌ |
| Interactive shell | ✅ REPL | ❌ | ❌ | ❌ |
| History tracking | ✅ SQLite | ❌ | ❌ | ✅ |
| Keyword trends | ✅ | ❌ | ❌ | ❌ |
| HTML export | ✅ | ❌ | ❌ | ❌ |
| CSV export | ✅ | ❌ | ❌ | ❌ |
| Caching | ✅ Two-level | ❌ | ❌ | ❌ |
| Python API | ✅ | ❌ | ❌ | ❌ |
| AI agent tool | ✅ Hermes | ❌ | ❌ | ❌ |

## 📝 License

MIT © [Jane-o-O-o-O](https://github.com/Jane-o-O-o-O)
