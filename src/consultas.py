import sqlite3

conexion = sqlite3.connect("data/etfs.db")

cursor = conexion.execute("""
    SELECT ticker, COUNT(*) FROM precios_etf GROUP BY ticker;
""")

print(cursor.fetchall())

conexion.close()