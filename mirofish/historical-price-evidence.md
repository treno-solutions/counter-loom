# Historical prices: descriptive analysis

Source WB01: World Bank Pink Sheet, downloaded 2026-11-01; source workbook update: Updated on October 02, 2026.

Gold/silver: nominal USD per troy ounce. Copper: nominal USD per metric tonne. Monthly average reference prices, not bullion transaction prices.
No inflation adjustment, currency conversion, investment fees, storage costs, spreads or taxes. Monthly averages smooth intramonth extremes.
CAGR uses elapsed monthly intervals. Volatility is sample standard deviation of monthly log changes multiplied by sqrt(12).
Maximum drawdown is the worst decline from a previous monthly-average high. Recovery uses the same nominal monthly-average series.

|Metal|Window|Observations|Price CAGR|Annualized log volatility|Worst drawdown|Peak|Trough|Recovery|
|---|---|---:|---:|---:|---:|---|---|---|
|gold|1960-01 to 2026-09|801|7.49%|15.23%|-62.07%|1980-01|1999-07|2006-05|
|silver|1960-01 to 2026-09|801|6.62%|25.96%|-90.75%|1980-01|1993-03|2011-04|
|copper|1960-01 to 2026-09|801|4.62%|22.62%|-64.63%|2008-04|2008-12|2010-12|
|gold|2000-01 to 2026-09|321|10.75%|12.89%|-39.28%|2011-09|2015-12|2020-07|
|silver|2000-01 to 2026-09|321|9.91%|24.79%|-66.98%|2011-04|2015-12|2025-09|
|copper|2000-01 to 2026-09|321|8.03%|21.11%|-64.63%|2008-04|2008-12|2010-12|

## Correlation of simple monthly price changes

Common sample: 1960-02 to 2026-09, 800 months.

|Metal|Gold|Silver|Copper|
|---|---:|---:|---:|
|gold|1.000|0.700|0.247|
|silver|0.700|1.000|0.306|
|copper|0.247|0.306|1.000|
