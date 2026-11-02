#!/usr/bin/env python3
"""Check the prepared research package; never claims simulation validation.

Use --prepare only while inputs are still unexecuted to generate calculation
examples and the draft manifest. The default verifies existing checksums.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'runs/002-permissionless-finance'
INPUTS = RUN / 'inputs'
REPORT = ROOT / 'qa/permissionless-package-validation.json'


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def digest(path):
    data = path.read_bytes()
    return {'path': path.relative_to(RUN).as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def calculation_examples():
    # Integer satoshi arithmetic, matching the documented rule; not a forecast.
    rows = []
    for interval in range(4, 9):
        sats = 5_000_000_000 >> interval
        rows.append({'height': interval * 210_000, 'halving_interval': interval,
                     'subsidy_sats_per_block': sats, 'subsidy_BTC_per_block': sats / 100_000_000})
    return {
        'information_class': 'Eigene Berechnung',
        'source_ids': ['PF-S01', 'PF-S02'],
        'method': 'Integer satoshi right shift by floor(height / 210000); no calendar mapping.',
        'protocol_examples': rows,
        'scenario_example': {
            'information_class': 'Szenarioannahme',
            'description': 'Same hypothetical BTC price and fees across adjacent subsidy intervals; no observed baseline.',
            'BTCUSD': 100000, 'fees_BTC_per_block': 0.25,
            'before_height': 840000, 'after_height': 1050000,
            'before_revenue_USD_per_block': (3.125 + 0.25) * 100000,
            'after_revenue_USD_per_block': (1.5625 + 0.25) * 100000,
            'before_fee_share': 0.25 / (3.125 + 0.25),
            'after_fee_share': 0.25 / (1.5625 + 0.25),
            'limit': 'Revenue before costs; fee share rises without fee growth. No security conclusion.'
        },
        'stake_proxy_example': {
            'information_class': 'Szenarioannahme', 'effective_stake_ETH': 100,
            'ETHUSD_before': 2000, 'ETHUSD_after': 1000,
            'market_value_USD_before': 100 * 2000,
            'market_value_USD_after': 100 * 1000,
            'limit': 'Toy units, not network baseline; no attack cost or attack probability.'
        }
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    run = read_json(RUN / 'run.json')
    if args.prepare:
        assert run['execution_status'] == 'not_started', 'Do not rewrite executed inputs'
        assert not any(x.get('uploaded') or x.get('submitted') for x in run['inputs'])
        write_json(INPUTS / 'derived-calculations.json', calculation_examples())
        entries = [digest(p) for p in sorted(INPUTS.iterdir())
                   if p.is_file() and p.name != 'input-manifest.json']
        write_json(INPUTS / 'input-manifest.json', {
            'schema_version': 1, 'version': '1.0', 'run_id': run['run_id'],
            'status': 'prepared_not_uploaded', 'actual_uploads_verified': False,
            'scope': 'All prepared input files except this manifest; not a server receipt.',
            'files': entries})

    errors = []
    checks = []

    def check(condition, message):
        (checks if condition else errors).append(message)

    sources = read_json(INPUTS / 'source-register.json')['sources']
    facts = read_json(INPUTS / 'fact-register.json')['facts']
    entities = read_json(INPUTS / 'entities.json')['entities']
    relationships = read_json(INPUTS / 'relationships.json')['relationships']
    with (INPUTS / 'metrics.csv').open(newline='') as handle:
        metrics = list(csv.DictReader(handle))
    with (INPUTS / 'scenarios.csv').open(newline='') as handle:
        scenarios = list(csv.DictReader(handle))
    groups = [(sources, 'source_id'), (facts, 'fact_id'), (entities, 'entity_id'),
              (relationships, 'relationship_id'), (metrics, 'metric_id'), (scenarios, 'scenario_id')]
    for rows, field in groups:
        check(len({r[field] for r in rows}) == len(rows), 'Unique ' + field)
    source_ids = {s['source_id'] for s in sources}
    entity_ids = {e['entity_id'] for e in entities}
    for rows in (facts, entities, relationships):
        check(all(set(r['source_ids']) <= source_ids for r in rows), 'Source references resolve')
    check(all(r['subject_id'] in entity_ids and r['object_id'] in entity_ids
              for r in relationships), 'Relationship endpoints resolve')
    check(all(r['source_ids'] and r['locator'] for r in relationships
              if r['information_class'] != 'Szenarioannahme'), 'Observed relationships have evidence')
    check(all(f['locator'] and f['period'] and f['uncertainty'] for f in facts),
          'Facts retain locators, periods and limits')
    check({m['metric_id'] for m in metrics} == {f'M{i:02}' for i in range(1, 25)},
          'Metrics M01-M24 present')
    check(all(not m['baseline_value'] and m['baseline_status'] == 'not_collected'
              for m in metrics), 'Uncollected metric baselines are empty, not zero')
    check({s['scenario_id'] for s in scenarios} == {'S0', 'S1', 'S2', 'S3'} |
          {f'S{i}{v}' for i in range(4, 9) for v in ('a', 'b')}, 'Scenario matrix complete')
    seed = (INPUTS / 'research-seed.md').read_text()
    prompt = (INPUTS / 'prompt.md').read_text()
    check(all(f'### H{i}:' in seed and f'**G{i}:**' in seed and f'H{i}:' in prompt
              and f'G{i}:' in prompt for i in range(1, 9)), 'Eight hypotheses and counterhypotheses in seed and prompt')
    check(read_json(INPUTS / 'derived-calculations.json') == calculation_examples(),
          'External arithmetic examples reproduce')
    check(read_json(INPUTS / 'prior-run-findings.json')['findings'] == [],
          'No invented prior-run findings')
    check((INPUTS / 'SIMULATION_TEMPLATE.md').read_bytes() == (ROOT / 'SIMULATION_TEMPLATE.md').read_bytes(),
          'Archived standard matches version used in this preparation')
    manifest = read_json(INPUTS / 'input-manifest.json')
    actual_paths = {p.relative_to(RUN).as_posix() for p in INPUTS.iterdir()
                    if p.is_file() and p.name != 'input-manifest.json'}
    check({f['path'] for f in manifest['files']} == actual_paths, 'Manifest covers all prepared inputs')
    for entry in manifest['files']:
        path = RUN / entry['path']
        check(path.is_file() and digest(path) == entry, 'Input checksum: ' + entry['path'])
    check(all((RUN / i['path']).is_file() for i in run['inputs']), 'Named upload candidates exist')
    missing_archives = []
    for source in sources:
        path = ROOT / source['local_archive'] if source['local_archive'] else None
        if path is None or not path.exists():
            missing_archives.append(source['source_id'])
        else:
            check(hashlib.sha256(path.read_bytes()).hexdigest() == source['archive_sha256'],
                  'Local source archive checksum: ' + source['source_id'])
    # Original archives are deliberately absent in a public clone.
    check(all(s['url'].startswith('https://') for s in sources), 'Sources have original HTTPS addresses')
    docs = list(RUN.rglob('*.md'))
    bad_links = []
    private_matches = []
    for path in docs:
        text = path.read_text()
        # Archived central standard contains a fenced illustrative template.
        visible = re.sub(r'```.*?```', '', text, flags=re.S)
        for target in re.findall(r'\]\(([^)]+)\)', visible):
            if '://' in target or target.startswith('#'):
                continue
            dest = target.split('#')[0]
            base = ROOT if path == INPUTS / 'SIMULATION_TEMPLATE.md' else path.parent
            if not (base / dest).exists():
                bad_links.append(path.relative_to(ROOT).as_posix() + ': ' + target)
    for path in list(RUN.rglob('*')) + [Path(__file__)]:
        if not path.is_file():
            continue
        # Patterns intentionally assembled without embedding private example paths.
        text = path.read_text()
        patterns = [r'/' + r'Users/[^\s"<>]+', r'/' + r'home/[^\s"<>]+',
                    r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
                    r'chatgpt-conversation' + r'://', r'Bearer' + r'\s+[A-Za-z0-9._-]{12,}']
        if any(re.search(p, text) for p in patterns):
            private_matches.append(path.relative_to(ROOT).as_posix())
    check(not bad_links, 'Relative Markdown document links resolve')
    check(not private_matches, 'No selected private-path/email/session/token patterns in package')
    check(run['execution_status'] == 'not_started' and run['readiness_status'] == 'prepared_for_import',
          'Preparation and execution statuses distinct')
    report = {
        'date': '2026-11-01', 'run_id': run['run_id'], 'passed': not errors,
        'counts': {'sources': len(sources), 'facts': len(facts), 'entities': len(entities),
                   'relationships': len(relationships), 'metrics': len(metrics), 'scenarios': len(scenarios)},
        'checks': checks, 'errors': errors, 'broken_links': bad_links,
        'private_pattern_files': private_matches, 'local_archives_unavailable': missing_archives,
        'limits': ['Checks cover package integrity, references and arithmetic, not empirical truth.',
                   'Source HTML/code sections checked; no complete PDF or econometric replication.',
                   'No import, MiroFish execution, calibration or empirical forecast validation.',
                   'Privacy check covers selected patterns and needs editorial review before publication.']
    }
    write_json(REPORT, report)
    print(json.dumps({'passed': not errors, 'counts': report['counts'], 'errors': errors,
                      'broken_links': bad_links, 'local_archives_unavailable': missing_archives}, ensure_ascii=False))
    raise SystemExit(1 if errors else 0)


if __name__ == '__main__':
    main()
