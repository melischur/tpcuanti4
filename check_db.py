import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('projects.db')
c = conn.cursor()

# Obtener las tablas en la base de datos
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

conn.close()
