#%% Pakete
from mcp.server import FastMCP
from tavily import TavilyClient
from typing import Literal
import os
from dotenv import load_dotenv
import logging

# %%
# Environment und Konfiguration laden
load_dotenv()

# Logger einrichten
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# MCP Server initialisieren
mcp = FastMCP(name="Tavily MCP Server")

# %%
def get_tavily_client() -> TavilyClient:
    """Erstellt einen Tavily-Client mit konfiguriertem API-Key.
    
    Returns:
        TavilyClient: Konfigurierter Tavily-Client
        
    Raises:
        ValueError: Wenn TAVILY_API_KEY nicht gesetzt ist
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY ist nicht gesetzt. Bitte setzen Sie die Umgebungsvariable.")
    
    # TavilyClient unterstützt nur api_key Parameter
    # Timeout muss auf der Aufruf-Ebene implementiert werden
    return TavilyClient(api_key=api_key)

# %%
@mcp.tool(name="tavily_search")
def tavily_search(
    query: str,
    max_results: int = 5,
    search_depth: Literal["basic", "advanced"] = "basic"
) -> dict:
    """Führt eine Websuche über die Tavily API durch.
    
    Args:
        query: Die Suchanfrage (Pflicht)
        max_results: Maximale Anzahl der Ergebnisse (Standard: 5)
        search_depth: Suchtiefe - "basic" oder "advanced" (Standard: "basic")
        
    Returns:
        dict: Suchergebnisse mit folgenden Feldern:
            - query: Die ursprüngliche Suchanfrage
            - results: Liste der Suchergebnisse
            - answer: Direkte Antwort (falls verfügbar)
            - images: Bilder zu den Suchergebnissen (falls verfügbar)
            
    Raises:
        Exception: Bei API-Fehlern (401, 429, Timeout, etc.)
    """
    try:
        client = get_tavily_client()
        
        logger.info(f"Starte Tavily-Suche: '{query}' (max_results={max_results}, depth={search_depth})")
        
        # Suchparameter vorbereiten
        search_kwargs = {
            "query": query,
            "max_results": max_results,
            "search_depth": search_depth,
            "include_answer": True,
            "include_images": True,
        }
        
        # Suche durchführen
        response = client.search(**search_kwargs)
        
        logger.info(f"Suche erfolgreich. Gefundene Ergebnisse: {len(response.get('results', []))}")
        
        # Antwort formatieren
        formatted_response = {
            "query": query,
            "results": response.get("results", []),
            "answer": response.get("answer", ""),
            "images": response.get("images", []),
            "search_metadata": {
                "total_results": len(response.get("results", [])),
                "search_depth": search_depth,
            }
        }
        
        return formatted_response
        
    except ValueError as e:
        logger.error(f"Konfigurationsfehler: {e}")
        raise Exception(f"Konfigurationsfehler: {str(e)}")
    except Exception as e:
        logger.error(f"Tavily API Fehler: {e}")
        raise Exception(f"Websuche fehlgeschlagen: {str(e)}")

# %%
@mcp.tool(name="tavily_extract")
def tavily_extract(urls: list[str]) -> dict:
    """Extrahiert Inhalt von URLs über die Tavily API.
    
    Args:
        urls: Liste der URLs, von denen Inhalt extrahiert werden soll (Pflicht)
        
    Returns:
        dict: Extrahierten Inhalt mit folgenden Feldern:
            - results: Liste der extrahierten Inhalte pro URL
            - summary: Zusammenfassung (falls verfügbar)
            - metadata: Metadaten zur Extraktion
            
    Raises:
        Exception: Bei API-Fehlern oder ungültigen URLs
    """
    try:
        client = get_tavily_client()
        
        if not urls:
            raise ValueError("Es muss mindestens eine URL angegeben werden.")
        
        logger.info(f"Extrahiere Inhalt von {len(urls)} URLs")
        
        # Inhalt extrahieren
        response = client.extract(urls)
        
        logger.info(f"Extraktion erfolgreich. Extrahiert: {len(response.get('results', []))} URLs")
        
        # Antwort formatieren
        formatted_response = {
            "results": response.get("results", []),
            "summary": response.get("summary", ""),
            "metadata": {
                "total_urls": len(urls),
                "successfully_extracted": len(response.get("results", [])),
            }
        }
        
        return formatted_response
        
    except ValueError as e:
        logger.error(f"Eingabefehler: {e}")
        raise Exception(f"Eingabefehler: {str(e)}")
    except Exception as e:
        logger.error(f"Tavily API Fehler: {e}")
        raise Exception(f"Inhaltsextraktion fehlgeschlagen: {str(e)}")

# %%
if __name__ == "__main__":
    # Für direkte Ausführung (z.B. zum Testen)
    print("Tavily MCP Server - Web-Suche und Content-Extraktion")
    print("=" * 50)
    mcp.run()