import sqlite3

conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()

print("Available modules:")
cursor.execute('SELECT id_module, titre FROM module;')
modules = cursor.fetchall()
for row in modules:
    print(f'ID: {row[0]}, Title: {row[1]}')

print("\nTotal modules:", len(modules))
conn.close()