"""Unit-Tests für den Tavily MCP Server."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Mock das tavily Paket bevor der Import erfolgt
sys.modules['tavily'] = MagicMock()

# Korrekten Import-Pfad verwenden
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Jetzt können wir server.py importieren (muss nach dem Mock erfolgen)
from tavily_mcp.server import get_tavily_client, tavily_search, tavily_extract


class TestGetTavilyClient:
    """Tests für die get_tavily_client Funktion."""
    
    def test_missing_api_key(self):
        """Testet, ob ein ValueError geworfen wird, wenn TAVILY_API_KEY nicht gesetzt ist."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="TAVILY_API_KEY ist nicht gesetzt"):
                get_tavily_client()
    
    def test_valid_api_key(self):
        """Testet, ob ein TavilyClient mit gültigem API-Key erstellt wird."""
        test_key = "test-api-key-123"
        with patch.dict(os.environ, {"TAVILY_API_KEY": test_key}):
            # Mock den TavilyClient Constructor
            with patch('tavily_mcp.server.TavilyClient') as mock_tavily_class:
                mock_client_instance = Mock()
                mock_tavily_class.return_value = mock_client_instance
                
                # Rufe die Funktion auf
                client = get_tavily_client()
                
                # Überprüfe, ob der Constructor korrekt aufgerufen wurde
                mock_tavily_class.assert_called_once_with(
                    api_key=test_key
                )
                # Die Funktion sollte die Client-Instanz zurückgeben
                assert client == mock_client_instance
    
    def test_custom_timeout(self):
        """Testet, dass TavilyClient ohne Timeout-Parameter erstellt wird."""
        with patch.dict(os.environ, {"TAVILY_API_KEY": "test-key", "TAVILY_TIMEOUT": "60"}):
            with patch('tavily_mcp.server.TavilyClient') as mock_tavily_class:
                mock_client_instance = Mock()
                mock_tavily_class.return_value = mock_client_instance
                
                get_tavily_client()
                
                # TavilyClient wird nur mit api_key aufgerufen
                mock_tavily_class.assert_called_once_with(
                    api_key="test-key"
                )


class TestTavilySearch:
    """Tests für die tavily_search Funktion."""
    
    @pytest.fixture
    def mock_tavily_response(self):
        """Fixture für eine gemockte Tavily API-Antwort."""
        return {
            "results": [
                {
                    "title": "Test Result 1",
                    "url": "https://example.com/1",
                    "content": "Test content 1",
                    "score": 0.95
                },
                {
                    "title": "Test Result 2", 
                    "url": "https://example.com/2",
                    "content": "Test content 2",
                    "score": 0.85
                }
            ],
            "answer": "This is a test answer",
            "images": ["https://example.com/image1.jpg"],
            "query": "test search"
        }
    
    def test_successful_search(self, mock_tavily_response):
        """Testet eine erfolgreiche Websuche."""
        # Mocke get_tavily_client und den TavilyClient
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.search.return_value = mock_tavily_response
            mock_get_client.return_value = mock_client
            
            # Rufe die Suchfunktion auf
            result = tavily_search(
                query="test query",
                max_results=3,
                search_depth="advanced"
            )
            
            # Überprüfe API-Aufruf
            mock_client.search.assert_called_once_with(
                query="test query",
                max_results=3,
                search_depth="advanced",
                include_answer=True,
                include_images=True
            )
            
            # Überprüfe Ergebnisstruktur
            assert result["query"] == "test query"
            assert len(result["results"]) == 2
            assert result["answer"] == "This is a test answer"
            assert len(result["images"]) == 1
            assert result["search_metadata"]["total_results"] == 2
            assert result["search_metadata"]["search_depth"] == "advanced"
    
    def test_search_with_defaults(self, mock_tavily_response):
        """Testet Websuche mit Standardwerten."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.search.return_value = mock_tavily_response
            mock_get_client.return_value = mock_client
            
            result = tavily_search(query="test query")
            
            mock_client.search.assert_called_once_with(
                query="test query",
                max_results=5,
                search_depth="basic",
                include_answer=True,
                include_images=True
            )
            
            assert result["query"] == "test query"
    
    def test_search_api_error(self):
        """Testet Fehlerbehandlung bei API-Fehlern."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.search.side_effect = Exception("API error")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(Exception, match="Websuche fehlgeschlagen"):
                tavily_search(query="test query")
    
    def test_configuration_error(self):
        """Testet Fehlerbehandlung bei Konfigurationsfehlern."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_get_client.side_effect = ValueError("API key missing")
            
            with pytest.raises(Exception, match="Konfigurationsfehler"):
                tavily_search(query="test query")


class TestTavilyExtract:
    """Tests für die tavily_extract Funktion."""
    
    @pytest.fixture
    def mock_extract_response(self):
        """Fixture für eine gemockte Tavily Extract-Antwort."""
        return {
            "results": [
                {
                    "url": "https://example.com/1",
                    "title": "Test Page 1",
                    "content": "Test content from page 1",
                    "summary": "Summary 1"
                },
                {
                    "url": "https://example.com/2",
                    "title": "Test Page 2", 
                    "content": "Test content from page 2",
                    "summary": "Summary 2"
                }
            ],
            "summary": "Overall summary of extracted content"
        }
    
    def test_successful_extraction(self, mock_extract_response):
        """Testet erfolgreiche Inhaltsextraktion."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.extract.return_value = mock_extract_response
            mock_get_client.return_value = mock_client
            
            urls = ["https://example.com/1", "https://example.com/2"]
            result = tavily_extract(urls)
            
            # Überprüfe API-Aufruf
            mock_client.extract.assert_called_once_with(urls)
            
            # Überprüfe Ergebnisstruktur
            assert len(result["results"]) == 2
            assert result["summary"] == "Overall summary of extracted content"
            assert result["metadata"]["total_urls"] == 2
            assert result["metadata"]["successfully_extracted"] == 2
    
    def test_no_urls_provided(self):
        """Testet Fehlerbehandlung bei leerer URL-Liste."""
        with pytest.raises(Exception, match="Eingabefehler"):
            tavily_extract([])
    
    def test_extract_api_error(self):
        """Testet Fehlerbehandlung bei API-Fehlern während der Extraktion."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.extract.side_effect = Exception("Extraction failed")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(Exception, match="Inhaltsextraktion fehlgeschlagen"):
                tavily_extract(["https://example.com"])
    
    def test_missing_api_key_for_extract(self):
        """Testet Fehlerbehandlung bei fehlendem API-Key für Extraktion."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_get_client.side_effect = ValueError("API key missing")
            
            with pytest.raises(Exception, match="Eingabefehler"):
                tavily_extract(["https://example.com"])


class TestErrorScenarios:
    """Tests für verschiedene Fehlerszenarien."""
    
    def test_401_unauthorized(self):
        """Simuliert 401 Unauthorized Fehler."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.search.side_effect = Exception("401 Unauthorized")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(Exception, match="Websuche fehlgeschlagen"):
                tavily_search(query="test")
    
    def test_429_rate_limit(self):
        """Simuliert 429 Rate Limit Fehler."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.extract.side_effect = Exception("429 Too Many Requests")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(Exception, match="Inhaltsextraktion fehlgeschlagen"):
                tavily_extract(["https://example.com"])
    
    def test_timeout_error(self):
        """Simuliert Timeout Fehler."""
        with patch('tavily_mcp.server.get_tavily_client') as mock_get_client:
            mock_client = Mock()
            mock_client.search.side_effect = Exception("Timeout after 30 seconds")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(Exception, match="Websuche fehlgeschlagen"):
                tavily_search(query="test")