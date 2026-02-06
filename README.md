# 📚 Proyecto MCP: Conexión a Base de Datos Local

Este proyecto es una guía práctica para aprender a utilizar el **Model Context Protocol (MCP)** conectando un modelo de IA (como Claude Desktop) con una base de datos pública o local de manera segura y gratuita.

---

## 1. Estructura del Proyecto
Para que este repositorio sea funcional y seguro, se organiza de la siguiente manera:
* `hello.py`: El servidor MCP (el "traductor" entre la IA y tus datos).
* `crear_db.py`: Script para inicializar tu base de datos SQLite local.
* `.gitignore`: Configuración para NO subir archivos sensibles (como la base de datos o el entorno virtual).

---

## 2. Requisitos Previos e Instalación

### Paso A: Preparar el entorno
Ejecuta estos comandos en tu terminal para configurar un entorno limpio:

```bash
# Al instalar, inicializar y hacer el add, uv crea el .venv automaticamente e instala las dependencias necesarias
pip install uv
uv init
uv add mcp

# Crear la base de datos de prueba
uv run crear_db.py
```

### Paso B: Crear la Base de Datos de Prueba
Ejecuta el script para generar el archivo biblioteca.db con datos iniciales:
```bash
python crear_db.py
```

## 3. Configuración del Servidor MCP (hello.py)
Para que el servidor sea portátil y funcione en cualquier computadora sin cambiar rutas manualmente, usa este código en tu hello.py:

```python
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
```

## 4. Conexión con Claude Desktop
Debes registrar este servidor en tu archivo de configuración de Claude:

Windows: %APPDATA%\Users\ %User_Name%\Claude\claude_desktop_config.json

macOS: ~/Library/Application Support/Claude/claude_desktop_config.json

Configuración JSON:
(Asegúrate de cambiar TU_USUARIO por tu nombre de usuario real y usar barras /)

```json
{
  "mcpServers": {
    "mi_biblioteca": {
      "command": "C:/Users/TU_USUARIO/Documents/poc_lite_mcp/.venv/Scripts/python.exe",
      "args": [
        "C:/Users/TU_USUARIO/Documents/poc_lite_mcp/hello.py"
      ]
    }
  }
}
```

## 5. Pruebas y Validación
1. Reiniciar Claude: Cierra Claude por completo desde la barra de tareas y vuelve a abrirlo.
2. Verificar Conectores: Haz clic en el icono del Martillo o en Conectores; deberías ver mi_biblioteca activo.
3. Consulta de prueba: Escribe en el chat: "¿Qué libros hay en mi biblioteca local?"

## 6. Notas de Seguridad y Desconexión (Importante)
Para mantener tu sistema seguro mientras aprendes, sigue estas reglas:

### Cómo Desconectar el Servidor
- Temporalmente: Simplemente cierra Claude Desktop ("Quit"). El proceso del servidor se detendrá automáticamente.
- Permanentemente: Elimina el bloque "mi_biblioteca" de tu archivo claude_desktop_config.json. Esto impide que la IA intente ejecutar tu código en el futuro.

### Prevención de Vulnerabilidades
- Evita caracteres especiales: No uses nombres de carpetas con ñ, tildes o espacios para evitar errores de ejecución (spawn ENOENT).
- Variables de Entorno: Si decides conectar esto a una base de datos en la nube (como Supabase), nunca escribas la contraseña en el código. Usa un archivo .env y añádelo al .gitignore.
- Exposición de datos: Recuerda que cualquier herramienta que definas con @mcp.tool() le da permiso a la IA para ejecutar esa función. Limita las herramientas solo a lo que necesites consultar.

**Este proyecto es parte de un ejercicio de aprendizaje sobre arquitecturas de IA modular.**
