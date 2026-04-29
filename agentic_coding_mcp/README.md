# Tavily MCP Server

Ein in Python geschriebener MCP-Server, der MCP-Clients (z. B. Claude Desktop) Web-Suche und Content-Extraktion über die [Tavily API](https://tavily.com) bereitstellt.

## Features

- **`tavily_search`** – Websuche mit konfigurierbarer Tiefe und Ergebnismenge
- **`tavily_extract`** – Inhaltsextraktion von URLs
- Vollständige Fehlerbehandlung (401, 429, Timeout)
- Umfassende Testabdeckung mit gemockten API-Aufrufen
- Kompatibel mit Claude Desktop und anderen MCP-Clients

## Installation

### Voraussetzungen

- Python 3.11 oder höher
- Tavily API-Key ([kostenlos registrieren](https://tavily.com))

### Schnellstart

```bash
# Repository klonen
git clone <repository-url>
cd agentic_coding_mcp

# Dependencies installieren (empfohlen mit uv)
uv sync

# Oder mit pip
pip install -e .

# Environment einrichten
cp .env.example .env
# Bearbeiten Sie .env und fügen Sie Ihren Tavily API-Key ein
```

## Verwendung

### Als MCP-Server

1. **Mit Python direkt**:
   ```bash
   export TAVILY_API_KEY=tvly-...
   python -m tavily_mcp
   ```

2. **In Claude Desktop konfigurieren**:
   Fügen Sie folgendes zu Ihrer Claude Desktop Konfiguration hinzu (`~/Library/Application Support/Claude/claude_desktop_config.json` auf macOS):

   ```json
   {
     "mcpServers": {
       "tavily": {
         "command": "python",
         "args": ["-m", "tavily_mcp"],
         "env": {
           "TAVILY_API_KEY": "tvly-..."
         }
       }
     }
   }
   ```

3. **Mit uvx (ohne Installation)**:
   ```bash
   uvx tavily-mcp
   ```

### Tools

#### `tavily_search`

Führt eine Websuche über die Tavily API durch.

**Parameter:**
- `query` (str, **Pflicht**): Die Suchanfrage
- `max_results` (int, Default: 5): Maximale Anzahl der Ergebnisse
- `search_depth` (Literal["basic", "advanced"], Default: "basic"): Suchtiefe

**Beispiel-Antwort:**
```json
{
  "query": "Was ist Python Programmierung?",
  "results": [
    {
      "title": "Python Programmierung - Einführung",
      "url": "https://example.com/python",
      "content": "Python ist eine interpretierte, objektorientierte Programmiersprache...",
      "score": 0.95
    }
  ],
  "answer": "Python ist eine beliebte Programmiersprache für KI und Data Science.",
  "images": ["https://example.com/python-logo.png"],
  "search_metadata": {
    "total_results": 1,
    "search_depth": "basic"
  }
}
```

#### `tavily_extract`

Extrahiert Inhalt von URLs.

**Parameter:**
- `urls` (list[str], **Pflicht**): Liste der URLs zur Extraktion

**Beispiel-Antwort:**
```json
{
  "results": [
    {
      "url": "https://www.python.org",
      "title": "Welcome to Python.org",
      "content": "The official home of the Python Programming Language...",
      "summary": "Offizielle Python-Website mit Downloads und Dokumentation"
    }
  ],
  "summary": "Extrahiert von python.org",
  "metadata": {
    "total_urls": 1,
    "successfully_extracted": 1
  }
}
```

## Entwicklung

### Projektstruktur

```
tavily-mcp-server/
├── pyproject.toml              # Projektkonfiguration
├── .env.example               # Beispiel-Umgebungsvariablen
├── README.md                  # Diese Datei
├── src/tavily_mcp/
│   ├── __init__.py            # Paket-Metadaten
│   ├── __main__.py            # CLI-Einstiegspunkt
│   └── server.py              # Haupt-MCP-Server-Implementierung
└── tests/
    ├── test_server.py         # Unit-Tests mit gemocktem Tavily-Client
    └── test_e2e.py            # End-to-End Tests (optional)
```

### Tests ausführen

```bash
# Alle Tests ausführen (ohne E2E)
pytest

# Mit Coverage-Bericht
pytest --cov=tavily_mcp --cov-report=html

# E2E-Tests (benötigt TAVILY_API_KEY)
export TAVILY_API_KEY=tvly-...
pytest tests/test_e2e.py

# Einzelnen Test ausführen
pytest tests/test_server.py::TestTavilySearch::test_successful_search
```

### Coverage-Ziel

Das Projekt strebt eine Testabdeckung von ≥ 80% an. Aktueller Status:

```bash
pytest --cov=tavily_mcp --cov-report=term-missing
```

## Fehlerbehandlung

Der Server behandelt folgende Fehler:

- **401 Unauthorized**: Ungültiger oder fehlender API-Key
- **429 Too Many Requests**: Rate Limit überschritten
- **Timeout**: API-Antwort dauert zu lange (konfigurierbar via `TAVILY_TIMEOUT`)
- **Invalid Input**: Fehlende oder ungültige Parameter

Fehler werden als MCP-Fehler mit aussagekräftigen Fehlermeldungen propagiert.

## Konfiguration

### Umgebungsvariablen

| Variable | Beschreibung | Standard |
|----------|--------------|----------|
| `TAVILY_API_KEY` | Tavily API-Key (erforderlich) | - |
| `TAVILY_TIMEOUT` | Timeout für API-Aufrufe in Sekunden | 30 |

### Fortgeschrittene Konfiguration

Der Server verwendet die folgenden Tavily-API-Parameter:

- **Max Retries**: 2 (fest)
- **Search Depth**: `basic` oder `advanced`
- **Include Answer**: Immer `true` für `tavily_search`
- **Include Images**: Immer `true` für `tavily_search`

## Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei für Details.

## Autor

Bert Gollnick · [GitHub](https://github.com/yourusername)

## Changelog

### v0.1.0 (29.04.2026)
- Initiale Version mit `tavily_search` und `tavily_extract` Tools
- Vollständige Testabdeckung mit gemockten API-Aufrufen
- Umfassende Fehlerbehandlung
- Claude Desktop Integration
- Deutsche Dokumentation und Code-Kommentare