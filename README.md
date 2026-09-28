# Mi cartera de ETFs: backtest 2021-2026 y proyección

Proyecto personal. Analizo mi cartera real de 4 ETFs con dos preguntas:

1. **¿Qué habría pasado?** Si hubiera empezado en julio de 2021 con mi inversión y aportes mensuales. *(Terminado)*
2. **¿Qué puede pasar a partir de ahora?** Proyección a 10, 20 y 30 años con escenarios. *(En curso)*

Stack: **Python · yfinance · CSV · SQLite (SQL) · Git**

---

## La cartera

| ETF | ISIN | Ticker (Xetra) | Peso |
|---|---|---|---|
| iShares Core MSCI World | IE00B4L5Y983 | EUNL.DE | 70% |
| iShares Core MSCI EM IMI | IE00BKM4GZ66 | IS3N.DE | 15% |
| iShares Physical Gold | IE00B4ND3602 | PPFB.DE | 10% |
| VanEck Semiconductor | IE00BMC38736 | VVSM.DE | 5% |

Aportación inicial: 10.000 € + 250 € · Aportación mensual: 250 € · Mismo reparto en cada compra.

---

## 1. ¿Qué habría pasado? (backtest)

**Periodo:** 16/07/2021 – 25/09/2026 (1.897 días, 5,2 años)

| | |
|---|---|
| Total aportado | 25.750,00 € |
| Valor final | 45.363,40 € |
| Ganancia | 19.613,40 € |
| Rentabilidad total | +76,17% |
| **TIR anual** | **15,88%** |

La rentabilidad total no es anual: con aportaciones mensuales, cada euro ha estado invertido un tiempo distinto. Por eso calculo la **TIR** (tasa interna de retorno), que sí es comparable con la rentabilidad anual de cualquier otro producto.

### Valor por ETF y desviación de pesos

| ETF | Valor final | Peso actual | Peso objetivo |
|---|---|---|---|
| MSCI World | 29.178,70 € | 64,3% | 70% |
| MSCI EM IMI | 5.899,22 € | 13,0% | 15% |
| Oro | 5.200,23 € | 11,5% | 10% |
| Semiconductores | 5.085,25 € | 11,2% | 5% |

**Hallazgo:** sin rebalanceo, los semiconductores han pasado del 5% al 11,2% de la cartera. El reparto 70/15/10/5 solo se cumple el día de cada compra; después, el mercado lo mueve. Hoy la cartera es más arriesgada de lo que diseñé: entre julio y agosto de 2026 los semis cayeron un 16% en un mes.

---

## 2. ¿Qué puede pasar a partir de ahora? (proyección)

*En construcción.* Proyección a 10, 20 y 30 años con tres escenarios (pesimista, base y optimista) y resultado ajustado por inflación.

---

## Cómo funciona

```
Yahoo Finance ──► descargar_datos.py ──► datos_etfs.csv ──► carga_sqlite.py ──► etfs.db ──► simulacion.py
```

1. **Descarga** (`src/descargar_datos.py`): cierres diarios de los 4 ETFs en Xetra (en euros) con `yfinance`. Guardo en formato largo (`fecha, ticker, precio`), fecha sin hora, precios a 3 decimales y sin la fila del día en curso (si el mercado está abierto, no es un cierre).
2. **Carga** (`src/carga_sqlite.py`): paso el CSV a SQLite con clave primaria compuesta `(fecha, ticker)` e `INSERT OR REPLACE`. La carga es idempotente: da igual cuántas veces se ejecute, no duplica filas.
3. **Simulación** (`src/simulacion.py`):
   - Con SQL saco el primer día de cotización de cada mes (`GROUP BY ticker, strftime('%Y-%m', fecha)` + `MIN(fecha)`): 252 compras (4 ETFs × 63 meses).
   - Calculo las participaciones de cada compra y las acumulo.
   - Valor final = participaciones × último cierre.
   - TIR calculada **por bisección**, implementada a mano sin librerías.

La configuración de la cartera (tickers, pesos, importes y fecha de inicio) está en un único sitio: `src/config.py`.

---

## Decisiones y limitaciones

- **Ventana desde el 16/07/2021:** el ETF de oro solo tiene histórico en Xetra (Yahoo) desde esa fecha.
- **Compras el primer día de cotización de cada mes,** no el día 1 (festivos y fines de semana).
- **Participaciones fraccionarias:** en la realidad depende del broker.
- **Sin comisiones de compra ni impuestos.** Los gastos del ETF (TER) ya van descontados en el precio.
- **Sin rebalanceo.**
- **Los datos de Yahoo pueden corregirse a posteriori:** el 24/09/2026 no aparecía en la primera descarga y apareció días después.

---

## Problemas que encontré

- **Filas duplicadas en SQLite:** cada ejecución de la carga volvía a insertar todo (10.234 → 30.702 filas). Solución: clave primaria compuesta `(fecha, ticker)` + `INSERT OR REPLACE`.
- **Precio intradía como si fuera un cierre:** al descargar con el mercado abierto, el último precio cambiaba en cada ejecución. Solución: excluir la fila de la fecha actual.

---

## Cómo reproducirlo

Desde la raíz del repositorio:

```bash
pip install yfinance
python src/descargar_datos.py
python src/carga_sqlite.py
python src/simulacion.py
```

`data/etfs.db` no está en el repo porque es un archivo generado: lo crea `carga_sqlite.py` en unos segundos.

### Estructura

```
data/
  datos_etfs.csv       # precios de cierre diarios (formato largo)
src/
  config.py            # cartera, importes y fecha de inicio
  descargar_datos.py   # Yahoo Finance → CSV
  carga_sqlite.py      # CSV → SQLite
  consultas.py         # consultas de comprobación
  simulacion.py        # backtest, valor final y TIR
TASKS.md               # registro de fases, decisiones y aprendizajes
```

---

## Próximos pasos

- [ ] Proyección a 10, 20 y 30 años con escenarios y ajuste por inflación
- [ ] Validar la TIR con `XIRR`
- [ ] Simulación Monte Carlo
- [ ] Comparativa con y sin rebalanceo
- [ ] Dashboard en Power BI

---

> Este proyecto es de aprendizaje y no es una recomendación de inversión. Rentabilidades pasadas no garantizan rentabilidades futuras.

**Autor:** Dani Pernas · [LinkedIn](https://www.linkedin.com/in/dani-pernas-b96255208)
