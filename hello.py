import sqlite3
from mcp.server.fastmcp import FastMCP

# Creamos el servidor
mcp = FastMCP("MiBiblioteca")

@mcp.tool()
def consultar_libros():
    """Consulta todos los libros de la base de datos local."""
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, autor FROM libros")
    resultados = cursor.fetchall()
    conn.close()
    return [f"{titulo} por {autor}" for titulo, autor in resultados]

if __name__ == "__main__":
    mcp.run()