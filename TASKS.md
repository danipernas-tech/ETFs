Fase 01
- He instalado yfinance en VSCode "pip install yfinance"
- Para descargar el histórico de los ticker uso yf.download()

* La ventana de los 4 ETFs Arranca el 16 de Julio de 2021 limitada por el histórico del ETF de oro

1.1 He usado un diccionario para guarda la clave - valor de el Ticker de cada ETF y su peso en la cartera

1.2 Creamos un .csv donde añadimos una columna para "Fecha" "Ticker" y "Precio"

1.3 Con un bucle for recorremos la clave de cada ETF y nos descargamos los datos

1.4 Guardamos en "cierres" los datos de "Close" que hay en las descargas que hemos hecho con el yf.download

1.5 Recorremos "cierres" con otro for para cada clave y añadimos la fila en el .csv con el orden fecha, ticker, precio