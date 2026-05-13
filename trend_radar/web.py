"""Web dashboard — FastAPI-based web interface for Trend Radar."""

import json
from datetime import datetime, timezone
from typing import Optional

try:
    from fastapi import FastAPI, Query
    from fastapi.responses import HTMLResponse, JSONResponse
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False


def create_app(radar=None, host: str = "127.0.0.1", port: int = 8765):
    """Create the FastAPI web application."""
    if not HAS_FASTAPI:
        raise ImportError("fastapi and uvicorn are required. Install with: pip install fastapi uvicorn")

    from .core import TrendRadar

    app = FastAPI(
        title="Trend Radar",
        description="Multi-source tech intelligence dashboard",
        version="0.6.0",
    )

    _radar = radar or TrendRadar()

    @app.get("/", response_class=HTMLResponse)
    async def index():
        """Serve the main dashboard page."""
        return _dashboard_html()

    @app.get("/api/fetch")
    async def api_fetch(
        sources: Optional[str] = Query(None, description="Comma-separated source names"),
        limit: int = Query(15, ge=1, le=100),
        layout: str = Query("table"),
    ):
        """Fetch trending intel as JSON."""
        source_list = sources.split(",") if sources else None
        snapshot = _radar.collect(sources=source_list, limit=limit, save=False)
        return JSONResponse({
            "timestamp": snapshot.timestamp.isoformat(),
            "sources": snapshot.sources_queried,
            "item_count": snapshot.item_count,
            "items": [item.to_dict() for item in snapshot.items],
            "keywords": snapshot.keywords(20),
            "errors": snapshot.errors,
        })

    @app.get("/api/ai")
    async def api_ai(limit: int = Query(15, ge=1, le=100)):
        """Fetch AI-focused intel as JSON."""
        snapshot = _radar.collect_ai_focused(limit=limit, save=False)
        return JSONResponse({
            "timestamp": snapshot.timestamp.isoformat(),
            "item_count": snapshot.item_count,
            "items": [item.to_dict() for item in snapshot.items],
            "keywords": snapshot.keywords(20),
        })

    @app.get("/api/search")
    async def api_search(
        q: str = Query(..., description="Search query"),
        sources: Optional[str] = Query(None),
        limit: int = Query(20, ge=1, le=100),
    ):
        """Search across sources."""
        source_list = sources.split(",") if sources else None
        items = _radar.search(q, sources=source_list, limit=limit)
        return JSONResponse({
            "query": q,
            "count": len(items),
            "items": [item.to_dict() for item in items],
        })

    @app.get("/api/keywords")
    async def api_keywords(days: int = Query(7, ge=1, le=365)):
        """Get trending keywords."""
        kw = _radar.store.get_keyword_trends(days=days)
        return JSONResponse({
            "days": days,
            "keywords": [{"word": w, "count": c} for w, c in kw],
        })

    @app.get("/api/stats")
    async def api_stats():
        """Get database and cache statistics."""
        stats = _radar.get_stats()
        return JSONResponse(stats)

    @app.get("/api/sources")
    async def api_sources():
        """List available sources."""
        from .core import SOURCE_CLASSES
        return JSONResponse({
            name: {"enabled": name in _radar.sources, "class": cls.__name__}
            for name, cls in SOURCE_CLASSES.items()
        })

    @app.get("/api/diff")
    async def api_diff():
        """Compare latest two snapshots — show rising/falling trends."""
        diff_data = _radar.diff_snapshots()
        return JSONResponse(json.loads(json.dumps(diff_data, default=str)))

    @app.get("/api/health")
    async def api_health():
        """Check data source connectivity and response times."""
        results = _radar.check_health()
        return JSONResponse(results)

    @app.get("/api/top")
    async def api_top(
        limit: int = Query(20, ge=1, le=100),
        hours: int = Query(24, ge=1, le=720),
        source: Optional[str] = Query(None),
        topic: Optional[str] = Query(None),
    ):
        """Get top trending items."""
        items = _radar.get_top_items(limit=limit, hours=hours, source=source, topic=topic)
        return JSONResponse({
            "count": len(items),
            "items": [item.to_dict() for item in items],
        })


    @app.get("/api/momentum")
    async def api_momentum(
        hours: int = Query(48, ge=1, le=720),
        limit: int = Query(20, ge=1, le=100),
    ):
        """Get trend momentum — velocity and acceleration."""
        from .momentum import analyze_snapshot_momentum
        data = analyze_snapshot_momentum(_radar.store, hours=hours)
        return JSONResponse([d.to_dict() for d in data[:limit]])

    @app.get("/api/ranked")
    async def api_ranked(
        sources: Optional[str] = Query(None),
        limit: int = Query(20, ge=1, le=100),
    ):
        """Get cross-source normalized ranking."""
        from .normalization import rank_cross_source
        source_list = sources.split(",") if sources else None
        snapshot = _radar.collect(sources=source_list, limit=limit, save=False)
        ranked_items = rank_cross_source(snapshot.items, top_n=limit)
        return JSONResponse({
            "count": len(ranked_items),
            "items": [i.to_dict() for i in ranked_items],
        })

    @app.get("/api/alerts")
    async def api_alerts_list():
        """List all configured alerts."""
        from .alerts import AlertStore
        store = AlertStore()
        return JSONResponse([a.to_dict() for a in store.list_alerts()])

    @app.post("/api/alerts/add")
    async def api_alerts_add(
        keyword: str = Query(...),
        threshold: int = Query(1, ge=1),
        source: Optional[str] = Query(None),
    ):
        """Add a keyword alert."""
        from .alerts import AlertStore
        store = AlertStore()
        alert = store.add_alert(keyword, threshold=threshold, source_filter=source)
        return JSONResponse(alert.to_dict())

    @app.get("/api/alerts/check")
    async def api_alerts_check(
        sources: Optional[str] = Query(None),
        limit: int = Query(25, ge=1, le=100),
    ):
        """Check current trends against alerts."""
        from .alerts import AlertStore
        store = AlertStore()
        source_list = sources.split(",") if sources else None
        snapshot = _radar.collect(sources=source_list, limit=limit, save=False)
        items_dicts = [i.to_dict() for i in snapshot.items]
        matches = store.check_alerts(items_dicts)
        return JSONResponse([m.to_dict() for m in matches])

    return app


def _dashboard_html() -> str:
    """Return the embedded dashboard HTML."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>📡 Trend Radar Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; min-height: 100vh; }
.container { max-width: 1000px; margin: 0 auto; padding: 20px; }
.header { text-align: center; padding: 30px; border-bottom: 1px solid #21262d; }
.header h1 { font-size: 2em; color: #58a6ff; }
.header p { color: #8b949e; margin-top: 8px; }
.controls { display: flex; gap: 12px; justify-content: center; margin: 20px 0; flex-wrap: wrap; }
.btn { padding: 10px 20px; border: 1px solid #30363d; background: #21262d; color: #c9d1d9; border-radius: 6px; cursor: pointer; font-size: 0.95em; transition: all 0.2s; }
.btn:hover { background: #30363d; border-color: #58a6ff; color: #58a6ff; }
.btn.active { background: #1f6feb; border-color: #1f6feb; color: white; }
select, input { padding: 10px 14px; border: 1px solid #30363d; background: #161b22; color: #c9d1d9; border-radius: 6px; font-size: 0.95em; }
.search-box { display: flex; gap: 8px; justify-content: center; margin: 16px 0; }
.search-box input { width: 300px; }
.results { margin-top: 20px; }
.item { padding: 14px 16px; border-bottom: 1px solid #21262d; display: flex; gap: 14px; align-items: flex-start; transition: background 0.15s; }
.item:hover { background: #161b22; }
.item-rank { color: #8b949e; font-weight: bold; min-width: 30px; text-align: right; padding-top: 2px; }
.item-content { flex: 1; }
.item-title { font-weight: 600; }
.item-title a { color: #58a6ff; text-decoration: none; }
.item-title a:hover { text-decoration: underline; }
.item-meta { font-size: 0.85em; color: #8b949e; margin-top: 4px; }
.item-desc { font-size: 0.85em; color: #8b949e; margin-top: 4px; }
.item-score { font-weight: bold; min-width: 70px; text-align: right; padding-top: 2px; }
.source-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 8px; }
.source-github { background: #6e549420; color: #6e5494; }
.source-hackernews { background: #ff660020; color: #ff6600; }
.source-reddit { background: #ff450020; color: #ff4500; }
.source-arxiv { background: #b31b1b20; color: #b31b1b; }
.source-rss { background: #ee802f20; color: #ee802f; }
.source-producthunt { background: #da552f20; color: #da552f; }
.keywords { margin-top: 24px; padding: 20px; background: #161b22; border-radius: 8px; }
.keywords h3 { margin-bottom: 12px; }
.keyword-cloud { display: flex; flex-wrap: wrap; gap: 8px; }
.kw-tag { padding: 4px 12px; background: #0d1117; border: 1px solid #30363d; border-radius: 16px; font-size: 0.9em; color: #58a6ff; }
.status { text-align: center; padding: 40px; color: #8b949e; }
.loading { display: none; text-align: center; padding: 20px; color: #58a6ff; }
.footer { text-align: center; padding: 30px; color: #484f58; font-size: 0.85em; border-top: 1px solid #21262d; margin-top: 40px; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📡 Trend Radar</h1>
    <p>Multi-source tech intelligence dashboard</p>
  </div>

  <div class="controls">
    <button class="btn active" onclick="fetchAll()">📡 Fetch All</button>
    <button class="btn" onclick="fetchAI()">🤖 AI Intel</button>
    <button class="btn" onclick="showKeywords()">🔑 Keywords</button>
    <button class="btn" onclick="showStats()">📊 Stats</button>
    <select id="sourceSelect">
      <option value="">All Sources</option>
      <option value="github">🐙 GitHub</option>
      <option value="hackernews">🔶 HN</option>
      <option value="reddit">🤖 Reddit</option>
      <option value="arxiv">📄 arXiv</option>
      <option value="rss">📡 RSS</option>
    </select>
  </div>

  <div class="search-box">
    <input type="text" id="searchInput" placeholder="Search across all sources..." onkeydown="if(event.key==='Enter')doSearch()">
    <button class="btn" onclick="doSearch()">🔍 Search</button>
  </div>

  <div class="loading" id="loading">📡 Loading...</div>
  <div class="results" id="results"></div>
</div>

<div class="footer">
  Trend Radar · <a href="https://github.com/Jane-o-O-o-O/trend-radar" style="color:#58a6ff">GitHub</a>
</div>

<script>
const emoji = {github:'🐙',hackernews:'🔶',reddit:'🤖',arxiv:'📄',rss:'📡',producthunt:'🚀'};
const colors = {github:'#6e5494',hackernews:'#ff6600',reddit:'#ff4500',arxiv:'#b31b1b',rss:'#ee802f',producthunt:'#da552f'};

function showLoading() { document.getElementById('loading').style.display = 'block'; }
function hideLoading() { document.getElementById('loading').style.display = 'none'; }

function scoreFmt(n) { return n >= 1000 ? (n/1000).toFixed(1)+'k' : String(n); }

async function fetchAll() {
  showLoading();
  const src = document.getElementById('sourceSelect').value;
  const url = '/api/fetch' + (src ? '?sources='+src : '');
  const resp = await fetch(url);
  const data = await resp.json();
  hideLoading();
  renderItems(data.items, '📡 Trending', data.keywords);
}

async function fetchAI() {
  showLoading();
  const resp = await fetch('/api/ai');
  const data = await resp.json();
  hideLoading();
  renderItems(data.items, '🤖 AI Intel', data.keywords);
}

async function showKeywords() {
  showLoading();
  const resp = await fetch('/api/keywords');
  const data = await resp.json();
  hideLoading();
  let html = '<div class="keywords"><h3>🔑 Trending Keywords</h3><div class="keyword-cloud">';
  data.keywords.forEach(k => { html += '<span class="kw-tag">'+k.word+' ('+k.count+')</span>'; });
  html += '</div></div>';
  document.getElementById('results').innerHTML = html;
}

async function showStats() {
  showLoading();
  const resp = await fetch('/api/stats');
  const data = await resp.json();
  hideLoading();
  let html = '<div class="keywords"><h3>📊 Statistics</h3><div style="margin-top:12px">';
  for (const [k,v] of Object.entries(data)) {
    if (typeof v === 'object') { for (const [a,b] of Object.entries(v)) html += '<p><strong>'+k+'.'+a+':</strong> '+b+'</p>'; }
    else html += '<p><strong>'+k+':</strong> '+v+'</p>';
  }
  html += '</div></div>';
  document.getElementById('results').innerHTML = html;
}

async function doSearch() {
  const q = document.getElementById('searchInput').value.trim();
  if (!q) return;
  showLoading();
  const resp = await fetch('/api/search?q='+encodeURIComponent(q));
  const data = await resp.json();
  hideLoading();
  renderItems(data.items, '🔍 Search: '+q, null);
}

function renderItems(items, title, keywords) {
  let html = '<h3 style="margin:16px 0;color:#58a6ff">'+title+'</h3>';
  items.forEach((item, i) => {
    const src = item.source;
    const em = emoji[src] || '•';
    const score = scoreFmt(item.score);
    html += '<div class="item"><span class="item-rank">'+(i+1)+'</span><div class="item-content">';
    html += '<div class="item-title"><span class="source-badge source-'+src+'">'+em+' '+src+'</span>';
    html += '<a href="'+item.url+'" target="_blank">'+item.title+'</a></div>';
    if (item.description) html += '<div class="item-desc">'+item.description.substring(0,150)+'</div>';
    if (item.author) html += '<div class="item-meta">👤 '+item.author+'</div>';
    html += '</div><span class="item-score" style="color:'+(colors[src]||'#58a6ff')+'">'+score+'</span></div>';
  });
  if (keywords) {
    html += '<div class="keywords"><h3>🔑 Keywords</h3><div class="keyword-cloud">';
    keywords.slice(0,15).forEach(([w,c]) => { html += '<span class="kw-tag">'+w+' ('+c+')</span>'; });
    html += '</div></div>';
  }
  document.getElementById('results').innerHTML = html;
}

// Auto-fetch on load
fetchAll();
</script>
</body>
</html>"""
