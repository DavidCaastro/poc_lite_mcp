import sqlite3


def setup():
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS libros 
                     (id INTEGER PRIMARY KEY, titulo TEXT, autor TEXT)''')

    libros = [
        ('Don Quijote', 'Miguel de Cervantes'),
        ('Cien años de soledad', 'Gabriel García Márquez'),
        ('Rayuela', 'Julio Cortázar')
    ]
    cursor.executemany('INSERT INTO libros (titulo, autor) VALUES (?, ?)', libros)
    conn.commit()
    conn.close()
    print("Base de datos 'biblioteca.db' creada con éxito.")


if __name__ == "__main__":
    setup()