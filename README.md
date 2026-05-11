# 📡 Trend Radar

> **Multi-source tech intelligence CLI** — See what's hot before everyone else.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)]()
[![Tests](https://img.shields.io/badge/tests-72%20passed-brightgreen.svg)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)]()

**One command. Six sources. Zero doom-scrolling.**

Trend Radar aggregates tech trends from **GitHub**, **Hacker News**, **Reddit**, **arXiv**, **RSS feeds**, and **Product Hunt** into a single, beautiful terminal dashboard. Track keywords over time, search across all sources, and never miss what's trending.

```
╭─────────────────────────────────────────────────────────────────╮
│ 📡 Trend Radar                                                  │
│ 2026-05-12 02:00 UTC                                            │
│ Sources: 🐙 github  🔶 hackernews  🤖 reddit  📄 arxiv  📡 rss  │
│ Items: 67                                                       │
╰─────────────────────────────────────────────────────────────────╯

╭── 🐙 GITHUB ────────────────────────────────────────────────────╮
│ #  Title                          Score  Details                 │
│ 1  openai/codex-cli              12.4k  AI coding agent         │
│ 2  anthropic/claude-code          8.2k  CLI coding assistant    │
╰─────────────────────────────────────────────────────────────────╯

╭── 🔶 HACKERNEWS ────────────────────────────────────────────────╮
│ #  Title                          Score  Details                 │
│ 1  Show HN: I built an AI agent   342  Autonomous coding        │
│ 2  Why every team needs MCP       287  MCP integration          │
╰─────────────────────────────────────────────────────────────────╯

┌─ 🔑 Trending Keywords ──────────────────────────────────────────┐
│ agent      ████████████████████████  12                         │
│ coding     █████████████████         8                          │
│ llm        ██████████████            7                          │
│ mcp        ████████████              6                          │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# Install
pip install trend-radar

# Fetch from all sources
trend-radar fetch

# AI-focused intelligence
trend-radar ai

# Search for a topic
trend-radar search "MCP server"

# Auto-refresh every 60 seconds
trend-radar fetch --watch 60

# View historical trends
trend-radar keywords

# Database stats
trend-radar stats
```

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
trend-radar fetch --watch 30              # Auto-refresh every 30s

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

# Configuration
trend-radar config-show                   # Show current config
trend-radar config-set sources.reddit.enabled false
trend-radar config-set display.layout compact
trend-radar sources-list                  # List all sources + status
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

cache:
  enabled: true
  memory_ttl: 300        # 5 minutes in-memory
  disk_ttl: 3600         # 1 hour on disk
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
pip install -e ".[dev]"
pytest
```

## 📝 License

MIT © [Jane-o-O-o-O](https://github.com/Jane-o-O-o-O)
