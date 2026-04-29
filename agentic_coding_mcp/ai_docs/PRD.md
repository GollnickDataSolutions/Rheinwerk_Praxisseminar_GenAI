# PRD: Tavily MCP Server

**Autor:** Bert Gollnick · **Datum:** 29. April 2026 · **Status:** Draft v0.1

## 1. Ziel

Ein in Python geschriebener MCP-Server, der MCP-Clients (z. B. Claude Desktop) Web-Suche und Content-Extraktion über die [Tavily API](https://tavily.com) bereitstellt. Lokal, via `stdio`, mit Tests.

## 2. Tools

**`tavily_search`** — Websuche
- `query` (str, Pflicht)
- `max_results` (int, Default 5)
- `search_depth` (`basic` | `advanced`, Default `basic`)

**`tavily_extract`** — Inhalt aus URLs extrahieren
- `urls` (list[str], Pflicht)

## 3. Tech-Stack

- Python 3.11+
- `mcp` (FastMCP), `tavily-python`, `python-dotenv`
- Tests: `pytest`, `pytest-asyncio`
- API-Key über Env-Variable `TAVILY_API_KEY`

## 4. Projektstruktur

```
tavily-mcp-server/
├── pyproject.toml
├── .env.example
├── src/tavily_mcp/
│   ├── __main__.py
│   └── server.py
└── tests/
    ├── test_server.py     # Unit-Tests mit gemocktem Tavily-Client
    └── test_e2e.py     agentic_coding_mcp\ai_docs\PRD.md   # Smoke-Test gegen echte API (optional)
```
agentic_coding_mcp\ai_docs\PRD.md
## 5. Tests

- **Unit:** Tool-Calls mit gemocktem `TavilyClient`, Schema-Validierung, Fehlerpfade (401, 429, Timeout)
- **E2E:** ein realer Search-Call gegen Tavily, nur wenn `TAVILY_API_KEY` gesetzt ist
- Coverage-Ziel: 80 %

## 6. Setup

```bash
uv sync
export TAVILY_API_KEY=tvly-...
python -m tavily_mcp
```

Claude-Desktop-Konfiguration:
```json
{
  "mcpServers": {
    "tavily": {
      "command": "python",
      "args": ["-m", "tavily_mcp"],
      "env": { "TAVILY_API_KEY": "tvly-..." }
    }
  }
}
```

## 7. Erfolgskriterien

- Server startet, registriert beide Tools, läuft in Claude Desktop
- `pytest` grün, Coverage ≥ 80 %
- Tavily-Fehler (401/429/Timeout) werden sauber als MCP-Fehler propagiert, kein Crash