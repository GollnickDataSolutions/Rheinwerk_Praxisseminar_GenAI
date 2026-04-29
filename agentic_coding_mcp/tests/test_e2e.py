"""End-to-End Tests für den Tavily MCP Server.

Diese Tests benötigen einen gültigen TAVILY_API_KEY und rufen die echte Tavily API auf.
Sie sind optional und werden nur ausgeführt, wenn TAVILY_API_KEY gesetzt ist.
"""

import pytest
import os
import sys

# Korrekten Import-Pfad verwenden
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tavily_mcp.server import tavily_search, tavily_extract


# Prüfe, ob TAVILY_API_KEY gesetzt ist
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
E2E_SKIP_REASON = "TAVILY_API_KEY ist nicht gesetzt. Setzen Sie die Umgebungsvariable für E2E-Tests."


@pytest.mark.skipif(not TAVILY_API_KEY, reason=E2E_SKIP_REASON)
class TestE2ESearch:
    """End-to-End Tests für die Websuche."""
    
    def test_basic_search(self):
        """Testet eine einfache Websuche mit der echten Tavily API."""
        result = tavily_search(
            query="Was ist Python Programmierung?",
            max_results=2,
            search_depth="basic"
        )
        
        # Grundlegende Validierung
        assert "query" in result
        assert result["query"] == "Was ist Python Programmierung?"
        assert "results" in result
        assert isinstance(result["results"], list)
        assert len(result["results"]) <= 2  # Könnte weniger sein als max_results
        assert "search_metadata" in result
        
        # Prüfe Struktur der einzelnen Ergebnisse
        if result["results"]:
            first_result = result["results"][0]
            assert "title" in first_result
            assert "url" in first_result
            assert "content" in first_result
        
        print(f"E2E Search erfolgreich: {len(result['results'])} Ergebnisse gefunden")
    
    def test_advanced_search(self):
        """Testet eine erweiterte Websuche mit der echten Tavily API."""
        result = tavily_search(
            query="Neueste KI-Entwicklungen 2024",
            max_results=3,
            search_depth="advanced"
        )
        
        assert result["query"] == "Neueste KI-Entwicklungen 2024"
        assert result["search_metadata"]["search_depth"] == "advanced"
        assert isinstance(result["results"], list)
        
        print(f"E2E Advanced Search erfolgreich: {len(result['results'])} Ergebnisse gefunden")
    
    def test_search_with_images(self):
        """Testet Websuche mit Bildern."""
        result = tavily_search(
            query="Bilder von Berlin",
            max_results=2
        )
        
        assert "images" in result
        assert isinstance(result["images"], list)
        # Die Tavily API könnte Bilder zurückgeben oder nicht
        
        print(f"E2E Search mit Bildern: {len(result.get('images', []))} Bilder gefunden")


@pytest.mark.skipif(not TAVILY_API_KEY, reason=E2E_SKIP_REASON) 
class TestE2EExtract:
    """End-to-End Tests für die Inhaltsextraktion."""
    
    def test_basic_extraction(self):
        """Testet Inhaltsextraktion von einer bekannten URL."""
        # Verwende eine stabile, öffentlich zugängliche URL
        urls = ["https://www.python.org"]
        
        result = tavily_extract(urls)
        
        # Grundlegende Validierung
        assert "results" in result
        assert isinstance(result["results"], list)
        assert len(result["results"]) == 1
        
        first_result = result["results"][0]
        assert "url" in first_result
        assert first_result["url"] == "https://www.python.org"
        assert "content" in first_result
        assert len(first_result["content"]) > 0
        
        assert result["metadata"]["total_urls"] == 1
        assert result["metadata"]["successfully_extracted"] == 1
        
        print(f"E2E Extraction erfolgreich: {len(first_result['content'])} Zeichen extrahiert")
    
    def test_multiple_urls_extraction(self):
        """Testet Inhaltsextraktion von mehreren URLs."""
        urls = [
            "https://www.python.org",
            "https://docs.python.org/3/"
        ]
        
        result = tavily_extract(urls)
        
        assert len(result["results"]) == 2
        assert result["metadata"]["total_urls"] == 2
        assert result["metadata"]["successfully_extracted"] == 2
        
        # Prüfe, dass alle URLs in den Ergebnissen enthalten sind
        result_urls = [r["url"] for r in result["results"]]
        for url in urls:
            assert url in result_urls
        
        print(f"E2E Multi-URL Extraction erfolgreich: {len(result['results'])} URLs extrahiert")


@pytest.mark.skipif(not TAVILY_API_KEY, reason=E2E_SKIP_REASON)
class TestE2EErrorHandling:
    """End-to-End Tests für Fehlerbehandlung."""
    
    def test_invalid_query_handling(self):
        """Testet, wie die API mit sehr kurzen oder unsinnigen Queries umgeht."""
        # Eine sehr kurze Query, die möglicherweise keine Ergebnisse liefert
        result = tavily_search(query="a", max_results=1)
        
        # Die API sollte keine Exception werfen, sondern möglicherweise leere Ergebnisse
        assert isinstance(result, dict)
        assert "results" in result
        # Es ist okay, wenn keine Ergebnisse gefunden wurden
        
        print("E2E Invalid Query Handling: API antwortet ordnungsgemäß")
    
    def test_empty_extraction(self):
        """Testet Extraktion von einer nicht-existierenden URL."""
        # Verwendet eine URL, die sehr wahrscheinlich nicht existiert
        urls = ["https://nonexistent-domain-xyz123.test/notfound"]
        
        result = tavily_extract(urls)
        
        # Die API sollte entweder einen leeren Inhalt zurückgeben oder fehlschlagen
        # Wir testen nur, dass keine Exception geworfen wird
        assert isinstance(result, dict)
        
        print("E2E Empty Extraction: API verarbeitet nicht-existierende URL")


if __name__ == "__main__":
    """Einfacher Test-Runner für manuelle Ausführung."""
    import dotenv
    
    # Lade .env Datei, falls vorhanden
    dotenv.load_dotenv()
    
    if not os.getenv("TAVILY_API_KEY"):
        print("Warnung: TAVILY_API_KEY ist nicht gesetzt.")
        print("Setzen Sie die Umgebungsvariable oder erstellen Sie eine .env Datei.")
        exit(1)
    
    # Führe einen einfachen Test durch
    print("Führe E2E-Test durch...")
    
    try:
        # Teste Suche
        search_result = tavily_search(query="Test", max_results=1)
        print(f"✓ Suche erfolgreich: {len(search_result['results'])} Ergebnisse")
        
        # Teste Extraktion
        extract_result = tavily_extract(["https://www.python.org"])
        print(f"✓ Extraktion erfolgreich: {len(extract_result['results'])} URLs")
        
        print("\n✅ Alle E2E-Tests erfolgreich!")
        
    except Exception as e:
        print(f"\n❌ E2E-Test fehlgeschlagen: {e}")
        exit(1)