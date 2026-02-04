import sqlite3
import os
from mcp.server.fastmcp import FastMCP

# Configuración de rutas automáticas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "biblioteca.db")

mcp = FastMCP("MiBiblioteca")


@mcp.tool()
def consultar_libros():
    """Consulta todos los libros de la base de datos local."""
    if not os.path.exists(DB_PATH):
        return "Error: La base de datos no existe. Ejecuta primero crear_db.py"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, autor FROM libros")
    resultados = cursor.fetchall()
    conn.close()
    return [f"{titulo} por {autor}" for titulo, autor in resultados]


if __name__ == "__main__":
    mcp.run()