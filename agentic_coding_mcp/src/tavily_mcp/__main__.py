#!/usr/bin/env python3
"""Haupt-Einstiegspunkt für den Tavily MCP Server."""

import sys
from tavily_mcp.server import mcp

def main() -> None:
    """Hauptfunktion des MCP-Servers."""
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer wurde beendet.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fehler beim Start des Servers: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()