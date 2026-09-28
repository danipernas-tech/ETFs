import sqlite3
import csv


conexion = sqlite3.connect("data/etfs.db")
conexion.execute("""
    CREATE TABLE IF NOT EXISTS precios_etf (
        fecha TEXT,
        ticker TEXT,
        precio REAL,
        PRIMARY KEY (fecha, ticker)
    );
    """)
with open("data/datos_etfs.csv", "r", newline="", encoding="utf-8") as archivo:
    lector = csv.reader(archivo)
    next(lector)
    for fila in lector:
        conexion.execute("INSERT OR REPLACE INTO precios_etf VALUES (?, ?, ?)", (fila[0], fila[1], float(fila[2])))




conexion.commit()

conexion.close()
