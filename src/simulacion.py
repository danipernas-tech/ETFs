import sqlite3

from config import ETFS, FECHA_INICIO, CAPITAL_INICIAL, APORTACION_MENSUAL

conexion = sqlite3.connect("data/etfs.db")

cursor = conexion.execute("""
    SELECT ticker, MIN(fecha), precio
    FROM precios_etf
    WHERE fecha >= ?
    GROUP BY ticker, strftime('%Y-%m', fecha)
    ORDER BY ticker, MIN(fecha);
""", (FECHA_INICIO,))


resultados = cursor.fetchall()
for ticker, fecha, precio in resultados:
    peso = ETFS[ticker]
    if fecha == FECHA_INICIO:
        importe = CAPITAL_INICIAL * peso
    else:
        importe = APORTACION_MENSUAL * peso
    print(ticker, fecha, importe)

print(len(resultados))
conexion.close()