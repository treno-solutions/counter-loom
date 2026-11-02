from pathlib import Path
import json, hashlib, re, math
import pandas as pd

R=Path(__file__).resolve().parents[1]
def put(path,text): (R/path).write_text(text.rstrip()+'\n')
def dump(path,data): put(path,json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False))
def load(path):return json.loads((R/path).read_text())

sources=[
 {'id':'WB01','title':'World Bank Commodity Price Data (Pink Sheet), October 2026 vintage','publisher':'World Bank','url':'https://www.worldbank.org/en/research/commodity-markets','download_url':'https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx','file':'raw/world-bank-monthly-2026-10.xlsx','date':'2026-10-02','kind':'historical reference prices','coverage':'1960-01 to 2026-09; nominal monthly averages; gold/silver USD/troy oz; copper USD/metric tonne'},
 {'id':'SI26','title':'World Silver Survey 2026','publisher':'The Silver Institute; prepared by Metals Focus','url':'https://silverinstitute.org/all-world-silver-surveys-2025/','download_url':'https://silverinstitute.org/wp-content/uploads/2026/04/World-Silver-Survey-2026.pdf','file':'raw/world-silver-survey-2026.pdf','date':'2026-04 (download path; day not independently established)','kind':'industry survey with historical estimates and forecasts','coverage':'2025 historical estimates and 2026 forecasts; sponsor profiles are attributed corporate descriptions'},
 {'id':'IGWT26','title':'In Gold We Trust 2026: Back to the Monetary Future, German extended edition','publisher':'Sound Money Capital AG; co-branded Incrementum','url':'https://ingoldwetrust.report/in-gold-we-trust-report/','download_url':'https://ingoldwetrust.report/download/55994/','file':'raw/in-gold-we-trust-2026-de.pdf','date':'2026-05-20','kind':'investment research and author scenarios','coverage':'486 PDF pages; source perspective favors gold; forecasts and allocation models are author views, not observations'},
 {'id':'WGC26','title':'Gold Demand Trends Q2 2026, eight public web chapters','publisher':'World Gold Council','url':'https://www.gold.org/goldhub/research/gold-demand-trends/gold-demand-trends-q2-2026','file':'raw/wgc-gold-demand-trends-q2-2026-web.json','date':'2026-07-30','kind':'industry demand/supply estimates','coverage':'Q2 2026 and comparison quarters. PDF/XLSX download opened sign-in; public chapter text and tables were archived instead'},
 {'id':'USGS26','title':'Mineral Commodity Summaries 2026','publisher':'U.S. Geological Survey','url':'https://pubs.usgs.gov/publication/mcs2026','download_url':'https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf','file':'raw/usgs-mcs-2026.pdf','date':'2026-02; landing page revised 2026-05-27','kind':'government mineral statistics, estimates and definitions','coverage':'gold, silver and copper; 2025 estimates, country production and reserves'},
 {'id':'IEAAI25','title':'Energy and AI','publisher':'International Energy Agency','url':'https://www.iea.org/reports/energy-and-ai','download_url':'https://www.iea.org/files/de9dea13-b07d-42c5-a398-d1b3ae17d866/EnergyandAI.pdf','file':'raw/iea-energy-and-ai-2025.pdf','date':'2025-04-10','kind':'energy estimates and conditional scenario projections','coverage':'data centres, electricity, AI; not direct silver-demand forecasts'},
 {'id':'IEACM26','title':'Global Critical Minerals Outlook 2026','publisher':'International Energy Agency','url':'https://www.iea.org/reports/global-critical-minerals-outlook-2026','download_url':'https://www.iea.org/files/19c60aa0-ee07-4a20-a138-33c967ac5008/GlobalCriticalMineralsOutlook2026.pdf','file':'raw/iea-critical-minerals-2026.pdf','date':'2026 (report edition; exact date not established here)','kind':'mineral supply/demand scenarios','coverage':'copper and other critical minerals; STEPS/CPS/HDS assumptions must remain labeled'},
 {'id':'FRED01','title':'DFII10: 10-year inflation-indexed Treasury constant-maturity market yield','publisher':'Board of Governors of the Federal Reserve System, distributed by FRED/St. Louis Fed','url':'https://fred.stlouisfed.org/series/DFII10','file':'raw/fred-dfii10.csv','date':'retrieved 2026-11-01; latest available observation 2026-10-29','kind':'daily historical market yield','coverage':'2003-01-02 to 2026-10-29; percent; not seasonally adjusted; not a realized ex-post inflation-adjusted return'}
]
for s in sources:
 p=R/s['file'];assert p.exists(),p
 s.update(retrieved='2026-11-01',bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
dump('sources/source-register.json',sources)
sm=['# Quellenverzeichnis','', 'Recherche- und Abrufstand: 1. November 2026. Originale werden unverändert aufbewahrt. Datenjahre, Berichtsausgaben und Prognosen sind getrennt zu lesen.','']
for s in sources:
 sm.extend([f'## {s["id"]}: {s["title"]}',f'- Herausgeber: {s["publisher"]}',f'- Datum/Stand: {s["date"]}',f'- Quelle: {s["url"]}',f'- Lokale Datei: [{s["file"]}](../{s["file"]})',f'- Einordnung: {s["kind"]}. {s["coverage"]}',f'- SHA-256: `{s["sha256"]}`',''])
sm.extend(['## Zugriffsgrenzen','', '- IMF Fiscal Monitor April 2026: Originalseite meldete Access Denied. Die ursprüngliche Seed-Aussage zu 94 %/100 % Schuldenquote ist in diesem Paket nicht neu verifiziert.', '- Gold Demand Trends: WGC-Downloads verlangten Anmeldung. Keine Zugangssperre umgangen; acht frei lesbare Kapitel einschließlich Tabellen archiviert.', '- Der Bericht Q2 2026 war auf der besuchten WGC-Übersichtsseite als neueste Ausgabe verlinkt. Keine Aussage, dass anderweitig keine neuere Ausgabe existiert.'])
put('sources/precious-metals.md','\n'.join(sm))

# Manually transcribed selected cells; verified against SI26 PDF file page 11, printed p.9.
silver={
 'mine_production':[823.6,846.6,844.1], 'recycling':[194.5,197.6,211.3],
 'net_hedging_supply':[0.0,44.7,10.0],'net_official_sector_sales':[1.5,1.5,1.0],
 'total_supply':[1019.6,1090.4,1066.4], 'industrial_total':[679.0,657.4,639.6],
 'photovoltaics_subset_of_industrial':[197.5,186.6,151.0], 'photography':[25.5,24.2,22.5],
 'jewelry':[205.1,189.3,159.4], 'silverware':[53.5,42.1,33.5],
 'coin_and_net_bar_demand':[190.9,217.7,257.6], 'net_hedging_demand':[3.5,0.0,0.0],
 'total_demand':[1157.4,1130.6,1112.6], 'market_balance':[-137.9,-40.3,-46.3],
 'net_investment_in_etps':[67.5,278.1,30.0], 'market_balance_less_etps':[-205.4,-318.4,-76.3]}
silver_data={'source_id':'SI26','pdf_page':11,'printed_page':9,'units':'million troy ounces (Moz)',
 'periods':[{'year':2024,'status':'historical estimate revised in 2026 edition'},{'year':2025,'status':'historical estimate'},{'year':2026,'status':'forecast as of report publication, not actual'}],
 'metrics':silver,'warning':'Photovoltaics is a subset of industrial demand; do not sum both. ETP investment is separate from the headline market balance.'}
dump('processed/silver-supply-demand-selected.json',silver_data)
checks=[]
for i,year in enumerate([2024,2025,2026]):
 supply=sum(silver[m][i] for m in ['mine_production','recycling','net_hedging_supply','net_official_sector_sales'])
 demand=sum(silver[m][i] for m in ['industrial_total','photography','jewelry','silverware','coin_and_net_bar_demand','net_hedging_demand'])
 checks.append({'year':year,'supply_rounding_difference':round(supply-silver['total_supply'][i],5),'demand_rounding_difference':round(demand-silver['total_demand'][i],5),
 'headline_balance_rounding_difference':round(silver['total_supply'][i]-silver['total_demand'][i]-silver['market_balance'][i],5),
 'etp_balance_difference':round(silver['market_balance'][i]-silver['net_investment_in_etps'][i]-silver['market_balance_less_etps'][i],5)})
assert all(abs(v)<0.21 for c in checks for k,v in c.items() if k!='year')
dump('qa/silver-table-reconciliation.json',checks)

wgc=load('raw/wgc-gold-demand-trends-q2-2026-web.json')
out=['# Gold Demand Trends Q2 2026: public chapter text and tables','', 'Source WGC26. Retrieved 2026-11-01. Original HTML-derived content is retained in the raw JSON archive. Figures are estimates, not simulation results.','']
for c in wgc:
 text=re.sub(r'[ \t]{2,}',' ',c['text']);text=re.sub(r'\n{3,}','\n\n',text)
 out.extend([f'## {c["url"].split("/")[-1]}',f'Source: {c["url"]}', '',text,''])
 for i,t in enumerate(c['tables'],1):
  out.extend([f'### Structured source table {i}','', '```json',json.dumps(t,ensure_ascii=False),'```',''])
put('processed/wgc-gold-demand-trends-q2-2026.clean.md','\n'.join(out))
dump('processed/wgc-demand-tables.json',[{'url':c['url'],'tables':c['tables']} for c in wgc if c['tables']])

fred=pd.read_csv(R/'raw/fred-dfii10.csv',parse_dates=['observation_date'])
fred['DFII10']=pd.to_numeric(fred['DFII10'],errors='coerce')
assert fred['observation_date'].is_unique
monthly=fred.set_index('observation_date')['DFII10'].resample('MS').mean()
monthly.index=monthly.index.strftime('%Y-%m')
prices=pd.read_csv(R/'processed/metals-monthly-prices.csv',index_col='month')
monthly.rename('real_yield_percent').to_csv(R/'processed/real-yield-monthly-mean.csv')
merged=prices.join(monthly.rename('real_yield_percent'))
rows=[]
for m in ['gold','silver','copper']:
 col=next(c for c in prices if c.startswith(m+'_'))
 pair=pd.concat([merged[col].pct_change(fill_method=None).rename('price_change'),merged['real_yield_percent'].diff().rename('yield_change_pp')],axis=1).dropna()
 rows.append({'metal':m,'months':len(pair),'first':pair.index[0],'last':pair.index[-1],'correlation':float(pair.corr().iloc[0,1])})
dump('processed/real-yield-change-correlations.json',{'source_ids':['WB01','FRED01'],'method':'Pearson correlation: monthly simple metal price change vs change in monthly mean DFII10 yield, in percentage points. Descriptive; not causal; no trading backtest.', 'results':rows})

facts=[]
def fact(fid,statement,sid,loc,status='historical estimate',**kwargs):facts.append(dict(id=fid,statement=statement,source_id=sid,locator=loc,status=status,**kwargs))
fact('S01','Silver mine production was 846.6 Moz in 2025.','SI26','PDF p.11 / printed p.9',value=846.6,unit='Moz',period='2025')
fact('S02','Silver industrial demand was 657.4 Moz in 2025; total demand was 1130.6 Moz.','SI26','PDF p.11 / printed p.9')
fact('S03','Silver photovoltaic demand was 186.6 Moz in 2025. The report forecasts 151.0 Moz for 2026.','SI26','PDF p.11 / printed p.9','mixed historical estimate and report forecast')
fact('S04','The 2025 silver market balance was -40.3 Moz. After subtracting net ETP investment of 278.1 Moz, the balance less ETPs was -318.4 Moz.','SI26','PDF p.11 / printed p.9')
fact('S05','The 2026 headline silver market balance forecast was -46.3 Moz; balance less ETPs was -76.3 Moz.','SI26','PDF p.11 / printed p.9','forecast as of report publication')
fact('S06','Silver recycling was estimated at 197.6 Moz in 2025 and forecast at 211.3 Moz for 2026.','SI26','PDF p.11 / printed p.9','mixed historical estimate and report forecast')
fact('G01','Q2 2026 gold mine production was estimated at 965.6 tonnes; recycling at 326.1 tonnes; net producer hedging at -22.8 tonnes.','WGC26','public summary table and supply chapter')
fact('G02','Q2 2026 gold total demand including OTC and other was 1268.9 tonnes; technology demand was 80.4 tonnes.','WGC26','public summary table')
fact('G03','Q2 2026 net gold demand from central banks and other institutions was estimated at 288.9 tonnes, compared with 177.9 tonnes in Q2 2025.','WGC26','central-banks chapter table')
fact('U01','USGS estimated world silver mine production at 26000 metric tonnes in 2025. Most silver was obtained as a byproduct of lead-zinc, copper and gold mining.','USGS26','PDF p.177 / printed p.173','government estimate')
fact('U02','USGS estimated world gold mine production at 3300 metric tonnes and copper mine production at 23000 thousand metric tonnes in 2025.','USGS26','PDF pp.95 and 77 / printed pp.91 and 73','government estimate')
fact('A01','Global data-centre electricity use was estimated at 415 TWh in 2024. The IEA Base Case projects around 945 TWh in 2030 and 1200 TWh in 2035.','IEAAI25','PDF p.14','estimate and conditional Base Case projections')
fact('C01','In STEPS, copper demand increases by over 25%, adding around 7 million tonnes by 2040.','IEACM26','PDF p.114','conditional scenario projection')
fact('I01','In Gold We Trust 2026 was authored by Ronald-Peter Stoeferle and Mark J. Valek; Sound Money Capital AG is responsible for content, with Incrementum co-branding.','IGWT26','PDF pp.1 and 3','publication metadata')
fact('I02','The IGWT silver chapter distinguishes industrial-demand pressure from investment demand and cites a balance including ETP investment. Its positive mining-equity conclusions are author investment views.','IGWT26','PDF p.368','author interpretation, not an observed future outcome')
fact('P01','World Bank monthly reference prices are available for gold, silver and copper from January 1960 through September 2026 in the archived workbook.','WB01','Monthly Prices worksheet','historical reference dataset')
fact('R01','DFII10 is a daily 10-year inflation-indexed Treasury market yield quoted in percent. The archived series runs from 2003-01-02 to 2026-10-29.','FRED01','series metadata and CSV','historical market yield dataset')
dump('processed/fact-register.json',facts)

entities=[
 ('silver_institute','The Silver Institute',['Silver Institute'],'industry association and survey publisher','SI26','PDF p.8'),
 ('metals_focus','Metals Focus',[],'metals-market research firm','SI26','PDF p.8'),
 ('wgc','World Gold Council',['WGC'],'industry research publisher','WGC26','public report'),
 ('usgs','U.S. Geological Survey',['USGS','United States Geological Survey'],'government statistical agency','USGS26','cover'),
 ('iea','International Energy Agency',['IEA'],'intergovernmental energy analysis agency','IEAAI25','cover'),
 ('smc','Sound Money Capital AG',[],'IGWT publisher responsible for report content','IGWT26','PDF p.3'),
 ('incrementum','Incrementum AG',[],'IGWT co-brand; distinct entity from Sound Money Capital AG','IGWT26','PDF p.3'),
 ('stoeferle','Ronald-Peter Stöferle',['Ronald-Peter Stoeferle'],'IGWT author','IGWT26','PDF p.1'),
 ('valek','Mark J. Valek',['Mark Valek'],'IGWT author','IGWT26','PDF p.1'),
 ('coeur','Coeur Mining, Inc.',['Coeur Mining'],'precious-metals producer; corporate description within sponsored report','SI26','PDF p.4'),
 ('fresnillo','Fresnillo plc',[],'silver and gold producer; corporate description within sponsored report','SI26','PDF p.4'),
 ('penoles','Industrias Peñoles, S.A.B. de C.V.',['Peñoles'],'mining, smelting and refining group; corporate description','SI26','PDF p.4'),
 ('new_afton','New Afton',[],'gold-copper mine, British Columbia; attributed corporate description','SI26','PDF p.4'),
 ('rochester','Rochester',[],'silver-gold mine, Nevada; attributed corporate description','SI26','PDF p.4'),
 ('saucito','Saucito',[],'Mexican mine; attributed corporate description','SI26','PDF p.4'),
 ('juanicipio','Juanicipio',[],'Mexican mine; attributed corporate description','SI26','PDF p.4')]
dump('processed/entities.json',[dict(id=i,name=n,aliases=a,role=r,source_id=s,locator=l) for i,n,a,r,s,l in entities])
rels=[
 ('metals_focus','PREPARES_REPORT_FOR','silver_institute','SI26','PDF p.8','publication credit'),
 ('stoeferle','COAUTHORS_IGWT_WITH','valek','IGWT26','PDF p.1','publication credit'),
 ('smc','COBRANDS_IGWT_WITH','incrementum','IGWT26','PDF p.3','publication notice'),
 ('coeur','OPERATES','new_afton','SI26','PDF p.4','attributed sponsor corporate profile; not independently audited here'),
 ('coeur','OPERATES','rochester','SI26','PDF p.4','attributed sponsor corporate profile; not independently audited here'),
 ('fresnillo','OPERATES','saucito','SI26','PDF p.4','attributed sponsor corporate profile; not independently audited here'),
 ('fresnillo','OPERATES','juanicipio','SI26','PDF p.4','attributed sponsor corporate profile; not independently audited here')]
dump('processed/relationships.json',[dict(subject=a,predicate=b,object=c,source_id=d,locator=e,evidence_type=f) for a,b,c,d,e,f in rels])

pack=['# Precious Metals: Evidence Pack for the Next MiroFish Run','',
 'Research cut-off and retrieval date: 2026-11-01. Gold, silver and copper. This document contains research evidence and attributed interpretations; the simulation task is stored separately.', '',
 '## Named institutions, producers and documented relationships','',
 'Metals Focus prepares the World Silver Survey for The Silver Institute. The Silver Institute publishes the survey. These organizations supply evidence; their publication activity is distinct from producing or consuming metal. [SI26, PDF p.8]', '',
 'World Gold Council publishes Gold Demand Trends. U.S. Geological Survey (USGS) publishes Mineral Commodity Summaries. International Energy Agency (IEA) publishes Energy and AI and Global Critical Minerals Outlook. IMF and IEA abbreviations must not become separate organizations from their full names. IMF debt figures have not been reverified in this packet.', '',
 'Ronald-Peter Stöferle and Mark J. Valek coauthor In Gold We Trust. Sound Money Capital AG is responsible for report content; Incrementum AG is a separate co-branding organization. These are research publishers and authors, not an official forecast authority. [IGWT26, PDF pp.1,3]', '',
 'In the corporate profiles included in the sponsored World Silver Survey, Coeur Mining describes operating the New Afton gold-copper mine in British Columbia and the Rochester silver-gold mine in Nevada. Fresnillo lists Saucito and Juanicipio among its Mexican operating mines. Industrias Peñoles describes mining, smelting and refining operations. These relationships are reported by the source corporate profiles, not independently audited for this packet. Sponsorship is not proof of a supply contract. [SI26, PDF p.4]', '',
 '## Silver: observed estimates and report forecasts','',
 '|Metric, million troy ounces|2024 revised estimate|2025 estimate|2026 report forecast|','|---|---:|---:|---:|']
for m in ['mine_production','recycling','total_supply','industrial_total','photovoltaics_subset_of_industrial','coin_and_net_bar_demand','total_demand','market_balance','net_investment_in_etps','market_balance_less_etps']:
 pack.append('|'+m.replace('_',' ')+'|'+'|'.join(f'{v:,.1f}' for v in silver[m])+'|')
pack.extend(['','Source: SI26, physical PDF p.11, printed p.9. Photovoltaics is included in industrial demand. Do not add it a second time. Forecasts remain forecasts even when the simulation begins later in 2026.', '',
 'The headline 2025 deficit is 40.3 Moz. The 318.4 Moz figure additionally subtracts net ETP investment. They are different accounting definitions. ETP flows are investment flows, not industrial fabrication. A deficit is not a dated exhaustion forecast. USGS describes silver primarily as a byproduct of lead-zinc, copper and gold mining. [SI26 p.11; USGS26 p.177]', '',
 '## Gold: Q2 2026 estimates','',
 'World Gold Council reports 965.6 tonnes of mine production, 326.1 tonnes of recycling and -22.8 tonnes of net producer hedging in Q2 2026. Total demand including OTC and other is 1,268.9 tonnes. Technology demand is 80.4 tonnes. Net demand from central banks and other institutions is estimated at 288.9 tonnes versus 177.9 tonnes in Q2 2025. These quarterly estimates must not be treated as annual figures or gross central-bank purchases. [WGC26 summary, supply, technology and central-banks tables]', '',
 '## Independent mineral statistics and vintage differences','',
 'USGS estimates 2025 world mine production at 26,000 metric tonnes of silver, 3,300 metric tonnes of gold and 23 million metric tonnes of copper. SI26 estimates silver mine production at 846.6 Moz, roughly 26,332 tonnes. The two silver estimates differ by about 1.3%. Keep publisher, vintage, units and estimation methods separate; do not silently average them. Reserve stocks must not be confused with annual production flows. [USGS26 physical PDF pp.77,95,177; SI26 p.11]', '',
 '## AI, energy and copper','',
 'IEA estimates global data-centre electricity consumption at 415 TWh in 2024. Its 2025 Base Case projects around 945 TWh in 2030 and 1,200 TWh in 2035. These are electricity estimates and projections, not quantities of silver, copper or gold. Metal demand requires independent material-intensity and technology assumptions. [IEAAI25 physical PDF p.14]', '',
 'The IEA 2026 STEPS scenario increases copper demand by over 25%, adding around 7 million tonnes by 2040. Alternative policy and technology scenarios differ. This is a conditional scenario, not an observed increase or a guarantee of higher copper prices. [IEACM26 physical PDF p.114]', '',
 '## In Gold We Trust: competing investment interpretations','',
 'The 2026 report emphasizes monetary transformation, changing gold allocation and reserve diversification. The silver chapter also expects pressure on photovoltaic silver consumption and distinguishes industrial use from speculative investment demand. Its mining-equity conclusions and long-range allocation/price models are author theses. They must be tested against substitution, recycling, attractive real yields and falling investment demand. [IGWT26 contents p.5, allocation chapter pp.120–146, silver chapter p.368]', '',
 'IGWT uses an ETP-inclusive deficit measure in its silver chapter; SI26 also publishes a narrower headline market balance. Count deficit years only after choosing one consistent definition and source vintage.', '',
 '## Historical price evidence','',
 'WB01 provides 801 monthly average observations for each metal, January 1960 through September 2026. Prices are nominal USD; gold and silver are quoted per troy ounce, copper per metric tonne. The processed time series and calculations are saved separately. Monthly-average drawdowns understate some intramonth extremes and exclude inflation, spreads, storage, taxes and fees.', '',
 'The full price history spans different monetary regimes, including fixed gold prices early in the sample. Historical averages and correlations are descriptive, not a calibrated future return distribution.', '',
 '## Real interest rates','',
 'FRED01 archives daily DFII10 observations from 2003-01-02 to 2026-10-29. DFII10 is a market yield on 10-year inflation-indexed Treasury securities, quoted in percent. It is a real-yield proxy, not realized inflation-adjusted portfolio performance. Monthly means and exploratory correlations with metal price changes are separately calculated. Correlation does not establish a causal price rule.', '',
 '## Remaining data gaps','',
 'No verified bullion dealer premium time series, household metal holdings, investor social-media dataset, industrial bill of materials or firm-specific supply-contract network is included. Corporate relationships are limited to the source-attributed relationships above. The package does not establish a numerical clearing-price model, calibrated agent decision rules, scenario probabilities or a conversion from social discussion rounds to calendar years.', '',
 '## Source references',''])
for s in sources:pack.append(f'- {s["id"]}: {s["title"]}. {s["url"]}')
put('mirofish/precious-metals-evidence-pack.md','\n'.join(pack))
put('mirofish/historical-price-evidence.md',(R/'notes/historical-price-analysis.md').read_text())
put('mirofish/next-run-prompt.md','''# Separate simulation prompt

Use precious-metals-evidence-pack.md and historical-price-evidence.md as research evidence, alongside the original research seed. Preserve source IDs and distinguish observed estimates, external forecasts, author investment theses and hypothetical simulation assumptions. Resolve aliases into canonical entities. Source publishers are evidence providers and must not replace miners, manufacturers or investors. Do not invent named contracts, production quantities, missing price observations or chart values. Compare all five seed scenarios and actively search for disconfirming mechanisms. Cite the evidence IDs used in each conclusion. Separate initial seeded posts from autonomous agent actions. Explain what economic decisions are actually simulated and which are merely discussed. Simulation discussion rounds have no automatic mapping to calendar years. Any numerical price output or probability must be labeled uncalibrated unless an independently validated quantitative model supports it.
''')

notes='''# Recherchebefunde und Datenkonflikte

Stand: 1. November 2026. Der bestehende Seed wurde unverändert gelassen.

## Wichtigste Korrekturen für den nächsten Lauf

1. World Silver Survey 2026 enthält historische Schätzungen für 2025 und Prognosen für 2026. Eine inzwischen vergangene Prognose ist dadurch nicht zum Istwert geworden.
2. Das Silberdefizit 2025 beträgt in der engeren Marktbilanz 40,3 Moz; nach ETP-Nettoinvestitionen 318,4 Moz. IGWT verwendet im Silberkapitel die ETP-inklusive Betrachtung. Auch die Zahl aufeinanderfolgender Defizitjahre hängt von dieser Definition ab.
3. Die ältere Silver-Institute-Webseite nennt für 2024 819,7 Moz Minenproduktion. Der World Silver Survey 2026 revidiert 2024 auf 823,6 Moz. Vintages dürfen nicht unbemerkt vermischt werden.
4. USGS schätzt Silberförderung 2025 auf 26.000 Tonnen. Metals Focus/Silver Institute kommen auf 846,6 Moz, etwa 26.332 Tonnen. Das sind unterschiedliche Schätzstände, kein Grund, eine Quelle stillschweigend zu ersetzen.
5. IGWT ist umfangreiches Investmentresearch mit ausgeprägter Goldperspektive. Langfristige Preisziele und Wahrscheinlichkeiten bleiben Autorenannahmen. Herausgeberverantwortung liegt laut PDF bei Sound Money Capital AG; Incrementum wird co-gebrandet.
6. Die IEA-Projektion von 945 TWh Rechenzentrumsstrom 2030 sagt nichts unmittelbar über Silbermengen. Der zusätzliche Kupferbedarf von rund 7 Mio. Tonnen 2040 gehört zum STEPS-Szenario.
7. Monatsdurchschnittspreise der Weltbank eignen sich für überprüfbare deskriptive Rechnungen, bilden aber keine Tagesextreme oder tatsächlichen physischen Kauf-/Verkaufspreise ab. Die lange Reihe umfasst verschiedene Geldordnungen.
8. Die allgemeinen IMF-Schuldenzahlen des alten Seeds sind hier nicht neu verifiziert, da die Originalseite Access Denied meldete. Keine Ersatzquelle oder erfundene Bestätigung eingesetzt.

## Nachweis der Verwendung im nächsten MiroFish-Lauf

- Vor dem Start prüfen, ob die Fakten S01–S06/G01–G03 und Einheiten im Graphen bzw. in abrufbaren Textpassagen wiederzufinden sind.
- Aliase kontrollieren und Quelleninstitutionen von handelnden Marktteilnehmern unterscheiden.
- Ergebnisse müssen Quellen/Fakten nennen. Initialposts allein belegen keinen autonomen Erkenntnisgewinn.
- Berechnungen aus processed/ bleiben außerhalb des Sprachmodells die maßgebliche Rechenquelle. Das Hochladen einer Tabelle beweist keine Kalibrierung.

## Nächste Datenergänzungen

- Benannte Hersteller mit dokumentierter Silberintensität und Substitutionsplänen; Werte nach Zelltechnologie und Zeitraum.
- Primärberichte einzelner Minenbetreiber mit Produktion, Kosten, Reserven und tatsächlich belegten Eigentumsverbindungen.
- Getrennte Spot-/Referenzpreise, Händlerankauf, Verkauf, Steuern und Lieferzeiten, besonders für Schweizer physische Produkte.
- Historische Nachfrage-/Bestandsreihen mit konstanten Definitionen sowie reale Preise und CHF-Umrechnung.
- Für eine quantitative Marktsimulation: validierte Verhaltensregeln, Materialbilanzen und Backtests; Dokumente allein ersetzen diese nicht.
'''
put('notes/research-findings.md',notes)

conv=load('qa/conversion-report.json')
report=['# Konvertierung und Qualitätsprüfung','',
 'Vollständige Originale in raw/. Pro PDF: unveränderter Text je physischer Seite in .pages.json und .fulltext.txt; schlankere Textfassung in .clean.md. Keine Original-PDFs überschrieben.', '',
 '|Dokument|PDF-Seiten|Original MB|Text-MD MB|Reduktion der Dateigröße|','|---|---:|---:|---:|---:|']
for c in conv:report.append(f'|{c["file"]}|{c["pages"]}|{c["original_bytes"]/1e6:.2f}|{c["clean_bytes"]/1e6:.3f}|{1-c["clean_bytes"]/c["original_bytes"]:.1%}|')
report.extend(['','## Was bereinigt wurde','', '- Bilder sind nicht in den Textdateien enthalten; wiederkehrende Randzeilen wurden vorsichtig entfernt.', '- Originalseitenzuordnung, Zahlen, Quellen und normaler Fließtext bleiben erhalten. Die vollständige Extraktion kann auch Sponsorentexte, Inhaltsverzeichnisse und Diagrammachsen enthalten.', '- Das kompakte MiroFish-Paket ist deshalb eine separate, kuratierte Eingabe. Vollständige Konvertierung und redaktionelle Zusammenfassung sind ausdrücklich unterschiedliche Dateien.', '',
 '## Prüfgrenzen','', '- Sichtprüfung: SI26 physische Seite 11 (gedruckt 9), IGWT26 Seite 368 und USGS26 physische Seite 177 (gedruckt 173). Prüfbilder liegen in qa/. Nicht jede Seite wurde visuell geprüft.', '- Silber-Kerntabelle für 2024/2025/2026F aus dem Original kontrolliert; Summen und ETP-Bilanz mit Rundungstoleranz 0,21 Moz abgeglichen.', '- WGC-Webtabellen separat strukturiert gespeichert. Keine erfolgreiche WGC-PDF-/XLSX-Anmeldung behauptet.', '- Diagrammkurven wurden nicht automatisch digitalisiert. Achsenbeschriftungen in der Volltextextraktion sind keine vollständige Datenreihe.', '- Niedrigtextseiten und wiederkehrende entfernte Zeilen sind in conversion-report.json protokolliert. Keine automatische OCR behauptet.', '- Textdateien sind erheblich kleiner, aber weniger Bilder bedeuten nicht automatisch bessere oder vollständigere Modellinformationen.'])
put('qa/conversion-and-validation.md','\n'.join(report))

readme='''# Edelmetall-Recherche für den nächsten MiroFish-Durchlauf

Stand: **1. November 2026**. Der ursprüngliche Research Seed im Projektstamm bleibt unverändert.

## Direkt verwendbare Dateien

- [Recherchepaket für MiroFish](mirofish/precious-metals-evidence-pack.md): Fakten, benannte Akteure, dokumentierte Beziehungen, Gegenargumente und Quellen.
- [Historische Preisauswertung](mirofish/historical-price-evidence.md): berechnete Kennzahlen mit Definitionen und Grenzen.
- [Separater Simulationsprompt](mirofish/next-run-prompt.md): in das Promptfeld; nicht als Rechercheersatz hochladen.
- [Quellenverzeichnis](sources/README.md): Originaladressen, Datenstände und lokale Dateien.
- [Recherchebefunde und offene Lücken](notes/research-findings.md).
- [Konvertierung und Prüfung](qa/conversion-and-validation.md).

## Was abgelegt ist

`raw/` enthält die Original-PDFs von **In Gold We Trust 2026 (486 Seiten)**, **World Silver Survey 2026 (92 Seiten)**, USGS Mineral Commodity Summaries 2026 und zwei IEA-Berichten. Hinzu kommen die Weltbank-Originalarbeitsmappe, FRED-Originaldaten sowie acht frei zugängliche Gold-Demand-Trends-Kapitel mitsamt Tabellen. WGC-PDF-/Excel-Downloads verlangten Anmeldung; diese Dateien sind deshalb nicht enthalten.

`processed/` enthält bildfreie vollständige Textextraktionen, seitenweise JSON-Dateien, bereinigtes Markdown sowie strukturierte Preis-, Nachfrage-, Akteurs- und Beziehungsdaten. Die vollständigen Textfassungen können weiterhin Sponsorenmaterial und Diagrammbeschriftungen enthalten. Für den nächsten Upload sind zunächst die **zwei kuratierten MiroFish-Evidenzdateien** vorgesehen. Bilder und Charts sind im Originalarchiv weiterhin verfügbar.

Die Weltbankreihe umfasst Januar 1960 bis September 2026. Gold und Silber: nominale USD je Feinunze; Kupfer: nominale USD je metrischer Tonne. Die Preise sind Monatsmittel, keine Barrenpreise. Die FRED-Reihe DFII10 umfasst tägliche reale Treasury-Marktrenditen von Januar 2003 bis Oktober 2026.

## Nachvollziehbarkeit

- Quellen-IDs verbinden Fakten, Rohdateien und Textstellen.
- Originaldateien werden nicht verändert. SHA-256-Prüfsummen stehen im Quellenregister und Dateimanifest.
- Beobachtungen, historische Schätzungen, externe Prognosen, Autorenmeinungen und eigene Berechnungen werden getrennt ausgewiesen.
- Stichproben-Sichtprüfung und Zahlenkontrollen sind dokumentiert. Vollständige Konvertierung ist keine vollständige visuelle oder inhaltliche Prüfung aller Berichtsseiten.
- Verarbeitung ist in tools/ reproduzierbar. Benötigt werden Python mit PyMuPDF, pandas, numpy, openpyxl und pypdf; es werden keine Webzugänge oder Schlüssel benötigt, sobald die Rohdateien vorliegen.

## Noch nicht enthalten

Ein durchgehender Händlerprämien-Datensatz, ein überprüftes Netzwerk industrieller Lieferverträge, eine empirisch kalibrierte Markträumung oder ein belastbares Preisprognosemodell. Die erneute Verifikation der IMF-Schuldenzahlen scheiterte am Seitenzugriff. Diese Lücken werden nicht durch erfundene Daten ersetzt.
'''
# Domain output must not overwrite the curated research and source indexes.
readme = re.sub(r'\]\((?!https?://|#)([^)]+)\)', lambda m: '](../' + m.group(1) + ')', readme)
put('mirofish/research-package.md', readme)

# Independent crosschecks on the downloaded price source and the calculation output.
metrics=load('processed/historical-price-metrics.json')
for x in metrics:
 col=next(c for c in prices if c.startswith(x['metal']+'_'));s=prices.loc[x['start']:x['end'],col]
 peak=s.cummax();worst=float((s-peak).div(peak).min())
 assert abs(worst-x['max_drawdown_monthly_average'])<1e-12
assert set(f['source_id'] for f in facts)<=set(s['id'] for s in sources)
ids={e[0] for e in entities};assert all(a in ids and c in ids for a,b,c,d,e,f in rels)
dump('qa/package-validation.json',{'source_count':len(sources),'fact_count':len(facts),'entity_count':len(entities),'relationship_count':len(rels),
 'original_seed_modified':False,'source_references_resolve':True,'entity_references_resolve':True,'drawdown_crosscheck':True,'pdf_sample_pages_reviewed':['SI26 physical 11','IGWT26 physical 368','USGS26 physical 177'],
 'scope':'verification covers curated figures and sampled pages, not all claims in original reports'})
manifest=[]
for p in sorted(R.rglob('*')):
 rel=p.relative_to(R)
 research_dirs={'raw','processed','sources','mirofish','notes','qa','research'}
 research_files={'tools/check_fiscal_plausibility.py','tools/check_foreign_plausibility.py','tools/check_company_plausibility.py','tools/check_bank_plausibility.py','poc/source-manifest.json','RESEARCH.md','BUILD_PLAN.md','POC.md','tools/prepare_research.py','tools/assemble_evidence.py','tools/probe_framework_boundaries.py','tools/run_concordia_pilot.py','tools/check_concordia_pilot_workflow.py','tools/run_tinytroupe_pilot.py','tools/probe_bptk_hybrid.py'}
 if p.is_file() and (rel.parts[0] in research_dirs or str(rel) in research_files):manifest.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
dump('file-manifest.json',manifest)
print('Assembled',len(sources),'sources;',len(facts),'facts;',len(entities),'entities;',len(rels),'relationships;',len(manifest),'files.')
