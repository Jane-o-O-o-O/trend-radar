# 📡 Trend Radar

**Multi-source tech intelligence CLI — GitHub/HN/Reddit/arXiv/RSS/Product Hunt in one command.**

> See what's trending before everyone else. No browser tabs, no doom-scrolling.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-260%20passed-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()
[![PyPI](https://img.shields.io/pypi/v/trend-radar?color=blue)](https://pypi.org/project/trend-radar/)

**One command. Six sources. Zero doom-scrolling.**

### Why Trend Radar?

| Feature | Hacker News Only | GitHub Trending | Trend Radar |
|---------|-----------------|-----------------|-------------|
| Sources | 1 | 1 | **6** (GitHub + HN + Reddit + arXiv + RSS + Product Hunt) |
| Keyword tracking | ❌ | ❌ | ✅ Historical trends |
| Score normalization | ❌ | ❌ | ✅ Cross-source 0-100 scale |
| Trend momentum | ❌ | ❌ | ✅ Velocity + acceleration tracking |
| Keyword alerts | ❌ | ❌ | ✅ Watchlist with threshold alerts |
| OPML import | ❌ | ❌ | ✅ Import from Feedly/Inoreader |
| Web dashboard | ❌ | ❌ | ✅ Interactive charts |
| JSON/CSV export | ❌ | ❌ | ✅ |
| Interactive shell | ❌ | ❌ | ✅ |
| Self-contained | ❌ | ❌ | ✅ No API keys needed |

Trend Radar aggregates tech trends from **GitHub**, **Hacker News**, **Reddit**, **arXiv**, **RSS feeds**, and **Product Hunt** into a single, beautiful terminal dashboard. Track keywords over time, search across all sources, and never miss what's trending.

### 🆕 What's New in v0.6.0
- **`trend-radar ranked`** — Cross-source normalized ranking (fair 0-100 comparison across GitHub, HN, Reddit)
- **`trend-radar momentum`** — Trend velocity & acceleration tracking with 24h predictions
- **`trend-radar alert-add`** — Keyword watchlist with threshold alerts
- **`trend-radar opml-import`** — Import RSS feeds from OPML/JSON files
- **Retry with exponential backoff** — Resilient API calls across all sources
- **Async fetching** — True concurrent HTTP with asyncio
- **260 tests** all passing |

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

# Fetch from all sources (parallel by default!)
trend-radar fetch

# AI-focused intelligence
trend-radar ai

# Search for a topic
trend-radar search "MCP server"

# Filter by topic
trend-radar fetch --topic ai

# Compare trends (rising/falling)
trend-radar diff

# Quick top items
trend-radar top --topic ai -n 10

# Cross-source normalized ranking (fair comparison!)
trend-radar ranked

# Trend momentum — see velocity & acceleration
trend-radar momentum

# Set keyword alerts
trend-radar alert-add "MCP server" --threshold 3
trend-radar alerts-check

# Import RSS feeds from OPML (Feedly, Inoreader export)
trend-radar opml-import feeds.opml

# Check source health
trend-radar health

# Interactive shell (REPL mode)
trend-radar shell

# Web dashboard
trend-radar serve

# Export as standalone HTML dashboard
trend-radar fetch --html -o dashboard.html

# Export as CSV
trend-radar fetch --csv -o trends.csv

# Docker (web dashboard)
docker build -t trend-radar .
docker run -p 8765:8765 trend-radar
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Multi-source aggregation** | GitHub, HN, Reddit, arXiv, RSS, Product Hunt |
| ⚡ **Parallel fetching** | All sources fetched concurrently via ThreadPoolExecutor |
| 🎨 **Beautiful terminal output** | Rich-powered tables, cards, compact layouts |
| 📊 **Trend diff** | Compare snapshots — see rising/falling/new items |
| 🏆 **Topic filtering** | Filter by AI, Web, Mobile, Security, DevOps, Data, Lang |
| 🔑 **Trending keywords** | Auto-extracted keyword frequency analysis |
| 📊 **History tracking** | SQLite-backed trend history with time-series |
| 💾 **Two-level caching** | Memory TTL + disk SQLite cache |
| ⚙️ **YAML configuration** | `~/.trend-radar/config.yaml` for all settings |
| 🌐 **Web dashboard** | FastAPI-powered web UI with real-time API |
| 💻 **Interactive shell** | prompt_toolkit REPL with tab completion |
| 📄 **Export formats** | JSON, Markdown, HTML, CSV |
| 🔄 **Watch mode** | Auto-refresh every N seconds |
| 🏥 **Health checks** | Source connectivity and latency monitoring |
| 🐳 **Docker ready** | One-command web dashboard deployment |
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
trend-radar fetch                         # All sources, table layout (parallel!)
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
trend-radar fetch --topic ai              # Filter by topic
trend-radar fetch --no-parallel           # Sequential (non-parallel) fetch

# AI-focused intel
trend-radar ai                            # AI/LLM across all sources
trend-radar ai --json                     # JSON output

# Search
trend-radar search "agent framework"      # Cross-source search
trend-radar search "MCP" -s github,arxiv  # Search specific sources

# Trend diff (rising/falling detection)
trend-radar diff                          # Compare last two snapshots
trend-radar diff --json                   # JSON output

# Top items
trend-radar top                           # Top 20 across all sources
trend-radar top --topic ai -n 10          # Top 10 AI items
trend-radar top --source github           # Top GitHub items only

# Health check
trend-radar health                        # Check all source connectivity

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
curl http://localhost:8765/api/diff
curl http://localhost:8765/api/top?limit=10&topic=ai
curl http://localhost:8765/api/health
```

## 🐳 Docker

```bash
# Build and run the web dashboard
docker build -t trend-radar .
docker run -p 8765:8765 trend-radar

# Fetch from CLI inside Docker
docker run trend-radar fetch --json

# With persistent data volume
docker run -v trend-data:/data trend-radar serve --host 0.0.0.0
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

# Fetch trending from all sources (parallel!)
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

# Trend diff (rising/falling)
diff = radar.diff_snapshots()
for item in diff["rising"][:5]:
    print(f"  🔺 {item['title']} (+{item['score_delta']})")

# Topic-filtered top items
items = radar.get_top_items(limit=10, topic="ai")

# Health check
health = radar.check_health()
for name, info in health.items():
    print(f"  {name}: {info['status']} ({info['latency_ms']}ms)")

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
| Parallel fetching | ✅ ThreadPool | ❌ | ❌ | ❌ |
| Terminal UI | ✅ Rich | ✅ | ❌ | ✅ |
| Trend diff | ✅ Rising/falling | ❌ | ❌ | ❌ |
| Topic filtering | ✅ 7 topics | ❌ | ❌ | ❌ |
| Web dashboard | ✅ FastAPI | ❌ | ❌ | ❌ |
| Interactive shell | ✅ REPL | ❌ | ❌ | ❌ |
| History tracking | ✅ SQLite | ❌ | ❌ | ✅ |
| Keyword trends | ✅ | ❌ | ❌ | ❌ |
| HTML export | ✅ | ❌ | ❌ | ❌ |
| CSV export | ✅ | ❌ | ❌ | ❌ |
| Caching | ✅ Two-level | ❌ | ❌ | ❌ |
| Health checks | ✅ | ❌ | ❌ | ❌ |
| Docker | ✅ | ❌ | ❌ | ❌ |
| Python API | ✅ | ❌ | ❌ | ❌ |
| AI agent tool | ✅ Hermes | ❌ | ❌ | ❌ |

## 📝 License

MIT © [Jane-o-O-o-O](https://github.com/Jane-o-O-o-O)
