import os
import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MiBiblioteca")

# Definimos la ruta exacta al archivo .db
# Sustituye esta ruta por la ruta REAL de tu carpeta
DB_PATH = "C:/Users/Josue David Peñuela/Documents/David/poc_lite_mcp/biblioteca.db"


@mcp.tool()
def consultar_libros():
    """Consulta todos los libros de la base de datos local."""
    if not os.path.exists(DB_PATH):
        return "Error: No se encuentra el archivo biblioteca.db en la ruta especificada."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT titulo, autor FROM libros")
        resultados = cursor.fetchall()
        return [f"{titulo} por {autor}" for titulo, autor in resultados]
    except sqlite3.OperationalError as e:
        return f"Error de base de datos: {e}"
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()