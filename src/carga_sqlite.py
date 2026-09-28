import sqlite3

conexion = sqlite3.connect("data/etfs.db")

conexion.execute("""
    CREATE TABLE IF NOT EXISTS precios_etf (
        fecha TEXT,
        ticker TEXT,
        precio REAL
    );



""")

conexion.close()
