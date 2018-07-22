import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, is_admin int)"
cursor.execute(create_table)
create_table = "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)
connection.commit()
connection.close()
