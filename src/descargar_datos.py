import yfinance as yf
import pandas as pd
import csv
from datetime import date

from config import ETFS

hoy = date.today()
with open("data/datos_etfs.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["Fecha", "Ticker", "Precio"])
    for ticker in ETFS:
            datos = yf.download(ticker, period="max", multi_level_index=False)
            if datos is not None and "Close" in datos:
                cierres = datos["Close"]
                #print(cierres)
                for fecha ,precio in cierres.items():
                        if hoy != fecha.date():
                            escritor.writerow([fecha.date(), ticker, round(precio, 3)])



                      




