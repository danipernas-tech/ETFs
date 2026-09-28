import sqlite3

conexion = sqlite3.connect("data/etfs.db")

cursor = conexion.execute("""
    SELECT ticker, MIN(fecha), precio
    FROM precios_etf
    WHERE fecha >= '2021-07-16'
    GROUP BY ticker, strftime('%Y-%m', fecha)
    ORDER BY ticker, MIN(fecha);
""")

resultados = cursor.fetchall()
print(resultados)
print(len(resultados))
conexion.close()