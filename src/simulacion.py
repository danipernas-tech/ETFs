import sqlite3
from datetime import date
import csv

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

participaciones = {}
total_aportado = 0
compras = []
nombre_etfs = ["MSCI WORLD", "MSCI EM IMI", "ORO", "SEMI CONDUCTORES"]

for ticker in ETFS:
    participaciones[ticker] = 0
for ticker, fecha, precio in resultados:
    peso = ETFS[ticker]
    if fecha == FECHA_INICIO:
        importe = (CAPITAL_INICIAL + APORTACION_MENSUAL) * peso
    else:
        importe = APORTACION_MENSUAL * peso
    compras.append((fecha, importe))
    compradas = importe/precio
    total_aportado += importe
    participaciones[ticker] += compradas

'''
print(participaciones)
print(total_aportado)
print(len(resultados))
'''

cursor = conexion.execute("""
    SELECT ticker, MAX(fecha), precio
    FROM precios_etf
    GROUP BY ticker
""")
ultimos_precios = cursor.fetchall()

fecha_final = date.fromisoformat(ultimos_precios[0][1])
def valor_con_interes(tasa):
    total = 0
    for fecha, importe in compras:
        fecha_compra = date.fromisoformat(fecha)
        anios = (fecha_final - fecha_compra).days / 365
        total += importe * (1 + tasa) ** anios
    return total



valor_total = 0
valores= {}
longitud = 0

print(f"--- VALOR ACTUAL ---")
for ticker, fecha, precio in ultimos_precios:
    print(f"ETF: {nombre_etfs[longitud]}")
    valor_etf = participaciones[ticker] * precio
    print(f"{ticker}: {valor_etf:.2f}€\n")
    valor_total += valor_etf
    valores[ticker] = valor_etf
    longitud += 1

print()
print("--- PESO ACTUAL DE CADA ETF EN LA CARTERA ---\n")
longitud = 0
for ticker, valor in valores.items():
    peso_actual = valor / valor_total * 100
    peso_objetivo = ETFS[ticker] * 100
    print(f"ETF: {nombre_etfs[longitud]}")
    print(f"Ticker: {ticker}")
    print(f"Peso actual: {peso_actual:.1f}%")
    print(f"Peso objetivo: {peso_objetivo:.1f}%\n")
    longitud += 1


bajo = 0
alto = 1
for i in range(100):
    medio = (bajo+ alto) / 2
    if valor_con_interes(medio) < valor_total:
        bajo = medio
    else:
        alto = medio
print("--- RENTABILIDAD ANUAL REAL ---")
print(f"TIR anual: {medio*100:.2f}%\n")

fecha_inicio = date.fromisoformat(FECHA_INICIO)
dias = (fecha_final - fecha_inicio).days
anios = dias / 365 


ganancia = valor_total - total_aportado
rentabilidad = ganancia / total_aportado * 100
print("--- TOTAL APORTADO ---")
print(f"{total_aportado:.2f}€\n")
print("--- VALOR TOTAL ---")
print(f"{valor_total:.2f}€\n")
print("--- GANANCIAS ---")
print(f"{ganancia:.2f}€\n")
print("--- RENTABILIDAD TOTAL ---")
print(f"{rentabilidad:.2f}%\n")
print("--- DURACIÓN INVERSION (HASTA ÚLTIMO DIA CIERRE) ---")
print(f"Desde {fecha_inicio} hasta {fecha_final}")
print(f"Duración: {dias} dias ({anios:.1f}años)")

with open("data/flujos_tir.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["fecha", "importe"])
    for fecha, importe in compras:
        escritor.writerow([fecha, -importe])
    escritor.writerow([fecha_final, round(valor_total, 2)])

conexion.close()