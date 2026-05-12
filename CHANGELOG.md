# Changelog

All notable changes to Trend Radar are documented here.

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
