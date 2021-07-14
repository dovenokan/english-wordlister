import sqlite3

conn = sqlite3.connect('wordlisterdb.db')
print("Opened database successfully")

conn.execute('CREATE TABLE userlist (id integer primary key autoincrement, username TEXT, email TEXT, password TEXT)')
print("Table created successfully")

conn.close()