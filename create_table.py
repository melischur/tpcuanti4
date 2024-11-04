import sqlite3

# Conexión a la base de datos (si no existe, se crea automáticamente)
conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

# Crear la tabla si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        author TEXT NOT NULL
    )
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()