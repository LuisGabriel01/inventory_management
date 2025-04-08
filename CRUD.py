import sqlite3
import os

db = os.path.abspath("db.db")
connect = sqlite3.connect(db)

conn = connect.cursor()

# def add_product(name,brand):
#     conn.execute("""INSERT INTO products (name,brand)
#                  VALUES (?,?)""",(name,brand))
#     connect.commit()

# add_product("nossa senhora","IPE")

def listar_tabelas():
    connect = sqlite3.connect(db)
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print("Tabelas no banco:", cursor.fetchall())
    connect.close()

listar_tabelas()
connect.close()