# 📡 Trend Radar

> Multi-source tech intelligence CLI — See what's hot before everyone else.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)]()

**Trend Radar** aggregates tech trends from **6 sources** into one terminal dashboard. Stop doom-scrolling — get the signal in seconds.

```
📡 Trend Radar — 2026-05-11 14:30 UTC
  Sources: github, hackernews, reddit, arxiv  |  Items: 67
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐙 GITHUB
 #  Title                          Score  Details
 1  openai/codex-cli                12.4k  AI coding agent for terminal
 2  anthropic/claude-code            8.2k  Anthropic's CLI coding assistant
 3  agent-pulse                      2.1k  Real-time AI agent dashboard

🔶 HACKERNEWS
 #  Title                          Score  Details
 1  Show HN: I built an AI agent     342  Autonomous coding with GPT-5
 2  Why every team needs an MCP      287  MCP is eating the integration world

🔑 Keywords: agent(12) coding(8) LLM(7) mcp(6) dashboard(5) tools(4)
```

## 🚀 Quick Start

```bash
pip install trend-radar

# One command to see everything
trend-radar fetch

# AI-focused intel
trend-radar ai

# Search for a topic
trend-radar search "MCP server"

# View historical trends
trend-radar keywords
```

## 📦 Sources

| Source | What you get | API |
|--------|-------------|-----|
| 🐙 **GitHub** | Trending repos + search | REST API + page scraping |
| 🔶 **Hacker News** | Top/best/new/ask/show stories | Firebase API |
| 🤖 **Reddit** | Hot posts from tech/AI subreddits | JSON API |
| 📄 **arXiv** | Latest AI/ML research papers | Atom API |
| 📡 **RSS** | Tech blogs, AI company blogs | Standard RSS/Atom |

## 🛠️ Commands

```bash
trend-radar fetch                    # Fetch from all sources
trend-radar fetch -s github,hn      # Specific sources only
trend-radar fetch --layout cards     # Card layout
trend-radar fetch --json             # JSON output (for scripting)

trend-radar ai                       # AI/LLM focused intel
trend-radar search "agent framework" # Cross-source search
trend-radar history -h 48            # Last 48h of data
trend-radar keywords                 # Trending keywords
trend-radar stats                    # Database stats
```

## 🤖 Use as a Python Library

```python
from trend_radar import TrendRadar

radar = TrendRadar()

# Fetch trending
snapshot = radar.collect(sources=["github", "hackernews"], limit=10)

# Search
items = radar.search("LLM agent", sources=["github", "arxiv"])

# Analyze
analysis = radar.analyze_opportunities(snapshot)
print(analysis["keywords"])
print(analysis["high_star_repos"])
```

## 🔌 Hermes Agent Integration

Trend Radar can be installed as a Hermes tool for AI-assisted trend analysis:

```python
from trend_radar.hermes_tool import trend_fetch, trend_search, trend_analyze

# In Hermes conversations:
# "What's trending in AI right now?" → trend_fetch(sources="github,hackernews,reddit")
# "Search for MCP server projects" → trend_search("MCP server")
# "What should I build next?" → trend_analyze()
```

## 📊 Data Storage

Trend Radar stores all data in SQLite (`~/.trend-radar/trends.db`) for:
- **Historical tracking** — See how repos/topics evolve over time
- **Keyword trends** — Discover what's heating up
- **Cross-session context** — Build on previous intel

## 🏗️ Architecture

```
trend_radar/
├── cli.py              # Click CLI entry point
├── core.py             # TrendRadar engine — orchestrates everything
├── models.py           # IntelItem, TrendSnapshot data models
├── store.py            # SQLite trend history storage
├── render.py           # Rich terminal + JSON + Markdown renderers
├── sources/            # Data source adapters
│   ├── base.py         # DataSource abstract base class
│   ├── github.py       # GitHub API + Trending scraping
│   ├── hackernews.py   # HN Firebase API (parallel fetch)
│   ├── reddit.py       # Reddit JSON API
│   ├── arxiv.py        # arXiv Atom API
│   └── rss.py          # Generic RSS/Atom feed reader
└── hermes_tool/        # Hermes Agent integration
    └── __init__.py     # Tool schemas + handlers
```

## 🆚 Compared to Existing Tools

| Feature | starcli | hacker-feeds-cli | haxor-news | **trend-radar** |
|---------|---------|------------------|------------|-----------------|
| Data sources | 1 | 5 | 1 | **6** |
| Python | ✅ | ❌ (Node) | ✅ | ✅ |
| Rich rendering | ✅ | ❌ | ❌ | ✅ |
| History/DB | ❌ | ❌ | ❌ | ✅ |
| AI analysis | ❌ | ❌ | ❌ | ✅ |
| Library use | ❌ | ❌ | ✅ | ✅ |
| Hermes tool | ❌ | ❌ | ❌ | ✅ |

## 📝 License

MIT
