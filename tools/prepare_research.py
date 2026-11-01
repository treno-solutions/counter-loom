"""Offline, reproducible extraction. Run with the bundled Codex Python runtime."""
from pathlib import Path
from collections import Counter
import json, re, hashlib, math
import pandas as pd
import numpy as np
from pypdf import PdfReader
try:
    import pymupdf
except ImportError:
    pymupdf = None

ROOT = Path(__file__).resolve().parents[1]

def dump(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

def pdf_extract(filename, title, source_id):
    path = ROOT / 'raw' / filename
    reader = pymupdf.open(path) if pymupdf else PdfReader(path)
    pdf_pages = reader if pymupdf else reader.pages
    pages = []
    marginal = Counter()
    for i, page in enumerate(pdf_pages, 1):
        text = (page.get_text('text') if pymupdf else page.extract_text()) or ''
        text = text.replace('\ufb01', 'fi').replace('\ufb02', 'fl').replace('/f_i', 'fi').replace('/f_l', 'fl')
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        marginal.update(set(lines[:2] + lines[-3:]))
        pages.append({'pdf_page': i, 'text': text, 'characters': len(text), 'images': len(page.get_images()) if pymupdf else None})
    # Only strip repeated marginal strings; retain all original per-page text in JSON.
    recurring = {s for s,n in marginal.items() if n >= max(8, len(pages)*0.20) and len(s)<130}
    full, clean = [], [f'# {title}', '', f'Source: {source_id}. Retrieved 2026-11-01.', '',
        'Text-only extraction. PDF page numbers below are physical file pages, not necessarily printed page labels.',
        'Charts are not numerically digitized. Axis labels may remain. Consult the original for chart-only information.',
        'Advertisements and sponsor descriptions may remain; this full extraction is an archive, not the recommended simulation input.', '']
    low = []
    for p in pages:
        full.append(f'\n=== PDF PAGE {p["pdf_page"]} ===\n{p["text"]}')
        lines = p['text'].splitlines()
        selected = [l for j,l in enumerate(lines) if not ((j<2 or j>=len(lines)-3) and (l.strip() in recurring or re.fullmatch(r'\d{1,3}',l.strip())))]
        s = '\n'.join(selected)
        s = re.sub(r'\n{3,}', '\n\n', s).strip()
        clean.extend([f'## PDF page {p["pdf_page"]}', '', s or '[No extractable text. Visual review required.]', ''])
        if p['characters'] < 150:
            low.append(p['pdf_page'])
    stem = path.stem
    dump(f'processed/{stem}.pages.json', pages)
    (ROOT/'processed'/f'{stem}.fulltext.txt').write_text('\n'.join(full))
    cp = ROOT/'processed'/f'{stem}.clean.md'
    cp.write_text('\n'.join(clean))
    return {'file':filename,'source_id':source_id,'pages':len(pages),'original_bytes':path.stat().st_size,
        'clean_bytes':cp.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'low_text_pages':low,'repeated_marginal_strings_removed':sorted(recurring),
        'charts_digitized':False,'verification':'sample pages only; full document conversion, not full visual audit'}

def prices():
    raw=ROOT/'raw/world-bank-monthly-2026-10.xlsx'
    data=pd.read_excel(raw,sheet_name='Monthly Prices',header=None)
    cols={str(v).lower():i for i,v in enumerate(data.iloc[4]) if str(v).lower() in ['gold','silver','copper']}
    assert set(cols)=={'gold','silver','copper'}
    records=[]
    for _,r in data.iloc[6:].iterrows():
        if not re.fullmatch(r'\d{4}M\d{2}',str(r.iloc[0])):continue
        row={'month':str(r.iloc[0]).replace('M','-')}
        for metal,col in cols.items():
            val=pd.to_numeric(r.iloc[col],errors='coerce')
            row[metal]=None if pd.isna(val) else float(val)
        records.append(row)
    df=pd.DataFrame(records).set_index('month')
    assert df.index.is_unique and df.index.is_monotonic_increasing
    assert all(df[m].dropna().gt(0).all() for m in cols)
    df.rename(columns={'gold':'gold_usd_per_troy_oz','silver':'silver_usd_per_troy_oz','copper':'copper_usd_per_metric_tonne'}).to_csv(ROOT/'processed/metals-monthly-prices.csv')
    dump('processed/metals-monthly-prices.json',{'source_id':'WB01','sheet':'Monthly Prices','update_label':str(data.iloc[3,0]),'units':{m:str(data.iloc[5,c]) for m,c in cols.items()},'observations':records})
    metrics=[]
    for start in ['1960-01','2000-01']:
        for metal in ['gold','silver','copper']:
            s=df.loc[start:,metal].dropna()
            dd=s/s.cummax()-1
            trough=dd.idxmin();peak=s.loc[:trough].idxmax()
            recovery=s.loc[trough:][s.loc[trough:]>=s.loc[peak]]
            metrics.append({'metal':metal,'start':s.index[0],'end':s.index[-1],'months':len(s),
                'first':float(s.iloc[0]),'last':float(s.iloc[-1]),
                'price_cagr':float((s.iloc[-1]/s.iloc[0])**(12/(len(s)-1))-1),
                'annualized_log_return_std':float(np.log(s/s.shift()).dropna().std(ddof=1)*math.sqrt(12)),
                'max_drawdown_monthly_average':float(dd.min()),'peak_month':peak,'trough_month':trough,
                'recovered_month':None if recovery.empty else recovery.index[0]})
    dump('processed/historical-price-metrics.json',metrics)
    r=df[['gold','silver','copper']].pct_change(fill_method=None).dropna()
    corr=r.corr()
    dump('processed/monthly-return-correlations.json',{'method':'Pearson correlation of simple monthly price changes; common nonmissing months; descriptive, not causal',
        'start':r.index[0],'end':r.index[-1],'n':len(r),'matrix':corr.to_dict()})
    md=['# Historical prices: descriptive analysis','',
        'Source WB01: World Bank Pink Sheet, downloaded 2026-11-01; source workbook update: '+str(data.iloc[3,0])+'.','',
        'Gold/silver: nominal USD per troy ounce. Copper: nominal USD per metric tonne. Monthly average reference prices, not bullion transaction prices.',
        'No inflation adjustment, currency conversion, investment fees, storage costs, spreads or taxes. Monthly averages smooth intramonth extremes.',
        'CAGR uses elapsed monthly intervals. Volatility is sample standard deviation of monthly log changes multiplied by sqrt(12).',
        'Maximum drawdown is the worst decline from a previous monthly-average high. Recovery uses the same nominal monthly-average series.', '',
        '|Metal|Window|Observations|Price CAGR|Annualized log volatility|Worst drawdown|Peak|Trough|Recovery|',
        '|---|---|---:|---:|---:|---:|---|---|---|']
    for x in metrics:md.append(f'|{x["metal"]}|{x["start"]} to {x["end"]}|{x["months"]}|{x["price_cagr"]:.2%}|{x["annualized_log_return_std"]:.2%}|{x["max_drawdown_monthly_average"]:.2%}|{x["peak_month"]}|{x["trough_month"]}|{x["recovered_month"] or "not recovered within sample"}|')
    md.extend(['','## Correlation of simple monthly price changes','',f'Common sample: {r.index[0]} to {r.index[-1]}, {len(r)} months.'])
    md.extend(['','|Metal|Gold|Silver|Copper|','|---|---:|---:|---:|'])
    for m in corr.index:md.append('|'+m+'|'+'|'.join(f'{corr.loc[m,n]:.3f}' for n in ['gold','silver','copper'])+'|')
    (ROOT/'notes/historical-price-analysis.md').write_text('\n'.join(md)+'\n')
    dump('qa/price-data-validation.json',{'rows':len(df),'first':df.index[0],'last':df.index[-1],
        'missing':{m:int(df[m].isna().sum()) for m in cols},'unique_months':bool(df.index.is_unique),
        'positive_values':True,'source_sheet':'Monthly Prices','source_column_indices_zero_based':cols,
        'source_has_mismatch_details_sheet':True,'note':'Auxiliary Mismatch Details sheet retained in original. No edits or imputation to Monthly Prices.'})

if __name__=='__main__':
    reports=[]
    for filename,title,sid in [('world-silver-survey-2026.pdf','World Silver Survey 2026','SI26'),
        ('in-gold-we-trust-2026-de.pdf','In Gold We Trust 2026 (German)','IGWT26'),
        ('usgs-mcs-2026.pdf','USGS Mineral Commodity Summaries 2026','USGS26'),
        ('iea-energy-and-ai-2025.pdf','IEA Energy and AI 2025','IEAAI25'),
        ('iea-critical-minerals-2026.pdf','IEA Global Critical Minerals Outlook 2026','IEACM26')]:
        if (ROOT/'raw'/filename).exists():
            print('Extracting',filename,flush=True)
            reports.append(pdf_extract(filename,title,sid))
    dump('qa/conversion-report.json',reports)
    prices()
    print('Completed',len(reports),'PDF conversions and historical price analysis.')
