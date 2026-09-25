import yfinance as yf
import pandas as pd
import csv

'''
#BUSQUEDA Código de Instrumento de Reuters .DE
# https://live.deutsche-boerse.com/


# DATOS MSCI WORLD
datos_msci_world = yf.download("EUNL.DE", period="max")
#info_msci_world = datos_msci_world.info()
if datos_msci_world is not None:
    datos_msci_world.info()
print(datos_msci_world)
for ticker in yf.download

#DATOS MSCI EM IMI
datos_msci_em_imi = yf.download("IS3N.DE", period="max")
print(datos_msci_em_imi)

#DATOS SEMICONDUCTORES
datos_semiconductores = yf.download("VVSM.DE", period="max")
print(datos_semiconductores)

#DATOS ORO
datos_oro = yf.download("PPFB.DE", period="max")
print(datos_oro)

'''
'''
RECORRER EL DICCIONARIO PARA COMPROBAR E IMPRIMIR LOS DATOS DE CADA
ETF CON PERIÓDO MÁXIMO

etfs = {
    "EUNL.DE" : 0.70,
    "IS3N.DE" : 0.15,
    "PPFB.DE" : 0.10,
    "VVSM.DE" : 0.05
    }

for ticker in etfs:
    datos = yf.download(ticker, period="max")
    print(datos)

SIGUIENTE: 
QUEDARNOS SOLO CON CLOSED
RECORRER E IMPRIMIR CADA FILA "FECHA, TICKER, PRECIO"
GUARDAR EN CSV

'''

etfs = {
    "EUNL.DE" : 0.70,
    "IS3N.DE" : 0.15,
    "PPFB.DE" : 0.10,
    "VVSM.DE" : 0.05
    }


with open("data/datos_etfs.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Fecha", "Ticker", "Precio"])
    for ticker in etfs:
            datos = yf.download(ticker, period="max", multi_level_index=False)
            if datos is not None and "Close" in datos:
                cierres = datos["Close"]
                #print(cierres)
                for fecha ,precio in cierres.items():
                        escritor.writerow([fecha, ticker, precio])




