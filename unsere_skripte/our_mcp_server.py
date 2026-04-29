#%% Pakete
from mcp.server import FastMCP
import os
# %%
mcp = FastMCP(name="MCP Server 2026-04-29")

@mcp.tool(name="list_files")
def list_files(folder_path: str) -> list[str]:
    """ Listet alle Dateien im übergebenen Ordner auf.
    Args:
        folder_path: der zu durchsuchende Ordner
    Return:
        list[str]: eine Liste mit Dateinamen aus dem Ordner
    """
    return os.listdir(folder_path)

# list_files("C:\\Temp")

@mcp.tool(name="save_markdown")
def write_markdown_file(file_path: str, content: str) -> str:
    """ Schreibt eine Markdowndatei
    Args:
        file_path: Speicherort der Datei
        content: Inhalt, der gespeichert werden soll
    Returns:
        Statusmeldung
    """
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Datei {file_path} wurde erfolgreich gespeichert."

if __name__=="__main__":
    mcp.run()