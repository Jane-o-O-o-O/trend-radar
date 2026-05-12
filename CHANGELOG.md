# Changelog

All notable changes to Trend Radar are documented here.

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
