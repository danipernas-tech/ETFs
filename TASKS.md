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


FASE 03

3.1 Decisiones
    - 10.000 € el 16/07/2021 repartidos 70/15/10/5 en los 4 fondos
    - 250 €/mes el primer día de cotización de cada mes, con el mismo reparto

3.2 src/config.py con ETFS, CAPITAL_INICIAL, APORTACION_MENSUAL y FECHA_INICIO: la cartera definida en un único sitio y se importa desde los scripts

3.3 Consulta del primer día de cotización de cada mes: WHERE + GROUP BY ticker, strftime('%Y-%m', fecha) + MIN(fecha) + ORDER BY
    - Con MIN(), SQLite devuelve el precio de esa misma fila 

3.4 Placeholder ? en el SELECT, pasando (FECHA_INICIO,) (tupla de un elemento)

3.5 src/simulacion.py: importe de cada compra = capital inicial o aportación mensual × peso

3.6 El primer mes lleva 10.000€ + 250€ (Total aportado 25.750€)

3.7 Valor final = participaciones * último precio (MAX(fecha)) * ticker

3.8 Resultados del backtest (16/07/2021 - 25/09/2026):
 
3.9 Desviación de pesos (sin rebalanceo):
    - Aportado: 25.750 €
    - Valor total: 45.363,40 €
    - Ganancia: 19.613,40 € (+76,17% total)
    - TIR anual: 15,88% (calculada por bisección)

Aprendido:
    - fetchall() solo una vez: el cursor se agota
    - SQL no da error si un filtro no encuentra nada, devuelve []

FASES SIGUIENTES
- Fase 4: proyección a 10, 20 y 30 años con escenarios (pesimista, base y optimista)
- Fase 5: conclusiones con números
- Fase 6: README



