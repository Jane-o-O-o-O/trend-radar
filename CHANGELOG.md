# Changelog

All notable changes to Trend Radar are documented here.

## [0.8.0] — 2026-05-14

### Added
- **`trend-radar radar`** — Topic distribution spider chart in terminal
- **`trend-radar bookmark add/list/search/remove/star/export`** — Bookmark system with SQLite storage
- **`trend-radar plugins list/load/info`** — Custom data source plugin system
- **`trend-radar compare`** — Compare trends between two time periods
- **`trend-radar completions bash/zsh/fish`** — Shell auto-completion scripts
- **`trend-radar rate-limits`** — View API rate limiter status for all sources
- **Token bucket rate limiter** — Per-source API throttling (`rate_limiter.py`)
- **Radar chart module** — Topic classification + spider chart visualization (`radar_chart.py`)
- **Bookmark module** — Full CRUD with star, search, export (`bookmarks.py`)
- **Plugin module** — Register/load custom DataSource plugins (`plugins.py`)
- **GitHub Actions CI** — Auto-test on Python 3.10-3.13 + lint (`ci.yml`)
- **GitHub Actions Publish** — Auto-publish to PyPI on release (`publish.yml`)
- 65 new tests (359 total, 100% pass rate)

### Changed
- Version bumped to 0.8.0
- README updated with v0.8.0 features, new commands, comparison table
- Duplicate `main()` call in CLI fixed

## [0.7.0] — 2026-05-13

### ✨ New Features
- **Live dashboard** — `trend-radar live` command for real-time auto-refreshing terminal dashboard (like `htop` for tech trends!)
- **Digest reports** — `trend-radar digest` generates shareable Markdown/HTML trend summaries
- **Setup wizard** — `trend-radar init` interactive first-run configuration wizard
- **Version command** — `trend-radar version` shows version and system info
- **Enhanced web dashboard** — Chart.js doughnut/bar charts, new Diff view, stats cards
- **Source distribution visualization** — Visual breakdown in terminal with colored bars
- **Keyword sparkline trends** — Unicode sparklines showing trend direction over time
- **Progress-aware fetching** — Per-source status with item count and cache-hit indicators

### 🌐 Web Dashboard Improvements
- Chart.js integration — Source distribution doughnut chart + keyword bar chart
- New Diff view — Rising/falling trends visualization
- Stats cards — Snapshots, items, sources, cache metrics
- Improved responsive design
- Version display (v0.7.0)

### 🧪 Testing
- 34 new tests for v0.7.0 features (live, digest, init, progress, web dashboard)
- Total: 294 tests all passing
- Test coverage for all new modules and CLI commands

### 🔧 Internal
- New modules: `live.py`, `digest.py`, `init_wizard.py`
- `collect_with_progress()` method for progress callbacks
- Updated public API exports
- Version bumped to 0.7.0

## [0.6.0] — 2026-05-13

### ✨ New Features
- **Cross-source score normalization** — `trend-radar ranked` command shows items on a fair 0-100 scale across all sources (logarithmic scaling per source type)
- **Trend momentum tracking** — `trend-radar momentum` shows velocity, acceleration, and trajectory (viral/rising/stable/falling) for trending items, with 24h score predictions
- **Keyword alerts / watchlist** — `trend-radar alert-add/ alert-list/ alert-remove/ alerts-check` commands to monitor keywords and get notified when trends emerge
- **OPML import** — `trend-radar opml-import` imports RSS feeds from OPML, JSON, or URL list files (compatible with Feedly, Inoreader, etc.)
- **Async source fetching** — `trend_radar.async_fetch` module for true concurrent HTTP with asyncio (faster than thread pool for I/O-bound workloads)
- **Retry with exponential backoff** — `trend_radar.retry` module provides `@retry_with_backoff` decorator and `RobustHttpClient` for resilient API calls

### 🌐 Web API Additions
- `/api/momentum` — Trend momentum endpoint (velocity, acceleration, trajectory)
- `/api/ranked` — Cross-source normalized ranking endpoint
- `/api/alerts` — List all configured alerts
- `/api/alerts/add` — Add keyword alert
- `/api/alerts/check` — Check trends against alert watchlist

### 🧪 Testing
- **260 tests** (up from 215, +21%)
- New test file: `test_v060_features.py` (45 tests) covering all new modules
- Tests for: retry logic, normalization, momentum, alerts CRUD, OPML import, async fetch, CLI commands, web endpoints

### 📦 New Modules
- `trend_radar/retry.py` — Exponential backoff retry decorator + RobustHttpClient
- `trend_radar/normalization.py` — Cross-source score normalization (logarithmic 0-100 scale)
- `trend_radar/momentum.py` — Trend velocity/acceleration tracking + trajectory classification
- `trend_radar/alerts.py` — Keyword alert system with SQLite storage
- `trend_radar/opml.py` — OPML/JSON/URL feed import
- `trend_radar/async_fetch.py` — Async concurrent source fetching

## [0.5.0] — 2026-05-13

### ✨ New Features
- **Parallel source fetching** — All data sources now fetched concurrently via ThreadPoolExecutor (3-5x faster!)
- **`trend-radar diff`** — Compare latest two snapshots to detect rising, falling, new, and gone trends
- **`trend-radar top`** — Quick view of top trending items with topic/source filtering
- **`trend-radar health`** — Check data source connectivity and response latency
- **Topic filtering** — `--topic` flag filters by AI, Web, Mobile, Security, DevOps, Data, or Lang
- **Docker support** — Dockerfile for one-command web dashboard deployment

### 🎨 Visual Improvements
- Trend diff renderer with rising (🔺), falling (🔻), new (🆕), and gone (💨) sections
- Health check renderer with latency display and status indicators
- Both new renderers use color-coded Rich panels

### 🌐 Web API
- `/api/diff` — Trend diff endpoint
- `/api/health` — Source health check endpoint
- `/api/top` — Top items with topic/source/limit filtering

### 💻 Shell
- New shell commands: `diff`, `top`, `health`
- Tab completion updated for all new commands

### 🏗️ Architecture
- `TrendRadar.collect()` now accepts `parallel=True` parameter
- `TrendRadar.diff_snapshots()` — Snapshot diff engine
- `TrendRadar.get_top_items()` — Topic-filtered top items
- `TrendRadar.check_health()` — Source health checker
- `TrendRadar._matches_topic()` — Topic keyword matcher (7 topics)
- `TrendStore.get_snapshot_items()` — Per-snapshot item retrieval
- `TerminalRenderer.render_diff()` — Diff visualization
- `TerminalRenderer.render_health()` — Health check visualization

### 🧪 Tests
- **215 tests** (up from 154, +40%)
- New test files: `test_v050_features.py`, `test_cli_v050.py`, `test_web_v050.py`
- Tests for concurrent fetching, diff, top, health, topic filtering, Dockerfile

### 📦 Infrastructure
- Dockerfile added (Python 3.12 slim, pip install trend-radar[all])
- `.dockerignore` added
- Version bumped to 0.5.0

## [0.4.0] — 2026-05-12

### ✨ New Features
- **Interactive Shell** — `trend-radar shell` launches a REPL with tab completion (prompt_toolkit)
- **Web Dashboard** — `trend-radar serve` starts a FastAPI web UI with REST API on `:8765`
- **HTML Export** — `--html` flag generates a standalone dark-themed HTML dashboard with charts
- **CSV Export** — `--csv` flag exports trend data as spreadsheet-ready CSV
- **Auto-detect output format** — `-o file.html` automatically selects HTML renderer from extension

### 🎨 Visual Improvements
- Score tier badges with icons (🔥 for 10k+, 🔴🟡🟢🔵⚪ for lower scores)
- Gradient progress bars using Rich Text colors
- Enhanced card layout with rank badges (🥇🥈🥉)
- Average score in summary footer
- Improved compact view with tier icons

### 📦 Infrastructure
- New `exporters/` module with `html.py` and `csv_export.py`
- New `shell.py` module for interactive REPL
- New `web.py` module for FastAPI dashboard
- Optional dependency groups: `pip install trend-radar[web|shell|all]`
- Version bumped to 0.4.0

### 🧪 Tests
- **154 tests** (up from 125)
- New test files: `test_html_export.py`, `test_csv_export.py`, `test_shell.py`, `test_web.py`
- New CLI tests for HTML/CSV output and new commands
- Updated render tests for score_badge and gradient_bar

### 📖 Documentation
- README overhaul with feature comparison table
- Web dashboard documentation with API examples
- Interactive shell usage guide
- Export format examples (HTML, CSV)

## [0.3.0] — 2026-05-12

### ✨ New Features
- CLI end-to-end tests using Click CliRunner
- SQLite store complete test coverage
- Individual data source tests
- `--output/-o` file export
- GitHub Actions CI/CD

### 🐛 Bug Fixes
- Fixed Panel/SourceType import in cli.py
- Fixed RSS source root.iter() slice bug
- Unified STOP_WORDS constant

### 📖 Documentation
- Added CONTRIBUTING.md
- Added CHANGELOG.md

## [0.2.0] — 2026-05-12

### ✨ New Features
- Two-level cache (memory TTL + disk SQLite)
- YAML configuration system
- Rich terminal rendering (tables, cards, compact)
- Product Hunt data source
- Hermes Agent tool integration

## [0.1.0] — 2026-05-11

### 🎉 Initial Release
- 6 data sources: GitHub, Hacker News, Reddit, arXiv, RSS, Product Hunt
- SQLite storage with history tracking
- TrendRadar core engine
- Click CLI with fetch/search/ai/history/keywords/stats commands
- Basic terminal output
