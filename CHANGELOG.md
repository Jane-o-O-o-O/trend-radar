# 📋 Changelog

All notable changes to Trend Radar will be documented in this file.

## [0.3.0] — 2026-05-12

### Added
- **CLI end-to-end tests** — 18 tests using Click's CliRunner
- **SQLite store tests** — 14 tests for TrendStore
- **Data source tests** — 17 tests for HN, Reddit, arXiv, RSS, GitHub sources
- **`--output` / `-o` flag** — write fetch results to file (JSON/Markdown)
- **GitHub Actions CI/CD** — automated testing on Python 3.10/3.11/3.12
- **CONTRIBUTING.md** — developer guide for contributors
- **CHANGELOG.md** — this file

### Fixed
- **Panel import bug** in `cli.py` `history` command (NameError on empty history)
- **Duplicated stop-words** — consolidated to single `STOP_WORDS` constant in `models.py`

### Changed
- `STOP_WORDS` is now a public constant exported from the package
- Version bumped to 0.3.0

## [0.2.0] — 2026-05-12

### Added
- Two-level caching system (memory TTL + SQLite disk cache)
- YAML configuration system (`~/.trend-radar/config.yaml`)
- Product Hunt data source (web scraping)
- Rich terminal rendering with 3 layouts (table/cards/compact)
- Keyword trend analysis with progress bars
- `--watch` auto-refresh mode
- `--json` / `--markdown` output formats
- Hermes Agent tool integration
- 72 unit tests

## [0.1.0] — 2026-05-11

### Added
- Initial release
- 5 data sources: GitHub, Hacker News, Reddit, arXiv, RSS
- SQLite storage with trend tracking
- Basic CLI with Click
- Search across sources
- AI-focused intelligence mode
