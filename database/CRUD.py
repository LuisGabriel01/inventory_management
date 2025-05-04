import sqlite3


def connect_db():
    connect = sqlite3.connect("database\\db.db")
    return connect

def dql(query):
    cursor = connect_db().cursor()
    select = cursor.execute(query)
    sel = select.fetchall()
    cursor.close()
    return list(sel)

def dml(execute):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute(execute)
    connect.commit()
    cursor.close()
    return

def get_columns(table):
    connect = connect_db()
    cursor = connect.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    colunas = [col[1] for col in cursor.fetchall()]
    return tuple(colunas)
