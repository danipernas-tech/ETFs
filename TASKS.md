Fase 01
- He instalado yfinance en VSCode "pip install yfinance"
- Para descargar el histórico de los ticker uso yf.download()

* La ventana de los 4 ETFs Arranca el 16 de Julio de 2021 limitada por el histórico del ETF de oro

1.1 He usado un diccionario para guarda la clave - valor de el Ticker de cada ETF y su peso en la cartera

1.2 Creamos un .csv donde añadimos una columna para "Fecha" "Ticker" y "Precio"

1.3 Con un bucle for recorremos la clave de cada ETF y nos descargamos los datos

1.4 Guardamos en "cierres" los datos de "Close" que hay en las descargas que hemos hecho con el yf.download

1.5 Recorremos "cierres" con otro for para cada clave y añadimos la fila en el .csv con el orden fecha, ticker, precio

1.6 Limpieza de datos antes de guardar
    - Fecha sin hora con fecha.date() (Timestamp de pandas)
    - Precios redondeados a 3 decimales con round()
    - Excluimos la fila del día actual para no tener el precio de cierre de un día no finalizado (con date.today())

1.7 Resultado
    - data/datos_etfs.csv (fecha, ticker, precio)
    - Script src/descargar_datos.py


FASE 02

2.1 Creamos la base de datos data/etfs.db con sqlite3

2.2 Tabla precios_etf: fecha TEXT, ticker TEXT y precio REAL

2.3 Leemos el CSV con csv.reader (convertimos el precio con float(), ya que del CSV llega todo como texto)

2.4 Insertamos con INSERT y placeholders 

2.5 Problema encontrado: al ejecutar el script varias veces se duplicaban las filas
    Solución: Clave primaria compuesta (fecha + ticker) + INSERT OR REPLACE

2.6 Comprobación en src/consultas.py con SELECT ticker, COUNT(*)

