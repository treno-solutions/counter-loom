from decimal import Decimal as D
import unittest
from engine import simulate_request, validate_request


class EngineTests(unittest.TestCase):
    def test_invalid_requests(self):
        for payload in [None, [], {}, {'annual_rate_after': True}, {'annual_rate_after': float('nan')}, {'annual_rate_after': float('inf')}, {'annual_rate_after': -.01}, {'annual_rate_after': .21}, {'annual_rate_after': .06, 'unknown': 1}]:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                validate_request(payload)

    def test_independent_monthly_accounting(self):
        for rate in [0, .02, .06, .20, .037]:
            result = simulate_request({'annual_rate_after': rate})
            self.assertEqual(result['meta']['llm_calls'], 0)
            self.assertEqual(len(result['rows']), 18)
            for case in result['cases']:
                cash, earmarked, arrears = D(1000), D(0), D(0)
                for period in range(1, 7):
                    contract = D('.02') if period < 3 or not case['variable'] else D(str(rate))
                    incoming = D(2400) + D(case['deposit'])*contract/12
                    due = D(2100) + D(case['loan'])*contract/12
                    contribution = min(D(100), max(D(0), incoming-due))
                    paid = min(due, cash+incoming)
                    cash += incoming-paid-contribution
                    earmarked += contribution
                    arrears += due-paid
                    row = next(x for x in result['rows'] if x['case'] == case['id'] and x['period'] == period)
                    for key, expected in [('cash_close', cash), ('earmarked_close', earmarked), ('arrears_close', arrears)]:
                        self.assertAlmostEqual(row[key], float(expected), places=5)
                    self.assertGreaterEqual(row['cash_close'], 0)

    def test_replay_and_targeted_events(self):
        first = simulate_request({'annual_rate_after': .06})
        second = simulate_request({'annual_rate_after': .06})
        for key in ['rows', 'baseline', 'events']:
            self.assertEqual(first[key], second[key])
        changes = [e for e in first['events'] if e['kind'] == 'contract_repriced']
        self.assertEqual({(x['period'], x['case']) for x in changes}, {(3, 'variable_loan'), (3, 'deposit')})
        fixed = [r for r in first['rows'] if r['case'] == 'fixed_loan']
        self.assertEqual([{k:v for k,v in r.items() if k != 'annual_rate'} for r in fixed], [{k:v for k,v in r.items() if k != 'annual_rate'} for r in first['baseline'] if r['case'] == 'fixed_loan'])

    def test_arrears_not_silent_overdraft(self):
        result = simulate_request({'annual_rate_after': .20})
        gaps = [r for r in result['rows'] if r['payment_gap'] > 0]
        self.assertTrue(gaps)
        self.assertTrue(any(e['kind'] == 'payment_gap' for e in result['events']))
        self.assertTrue(all(r['cash_close'] >= 0 for r in gaps))


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from server import Handler
        from http.server import ThreadingHTTPServer
        from threading import Thread
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def request(self, body, headers=None, endpoint='/api/simulate'):
        import json
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        req = Request(self.base+endpoint, data=body, headers=headers or {'Content-Type': 'application/json'})
        try:
            response = urlopen(req, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.load(response), response.headers

    def test_custom_rate_reaches_solver(self):
        status, data, headers = self.request(b'{"annual_rate_after":0.037}')
        self.assertEqual(status, 200)
        self.assertEqual(headers['Cache-Control'], 'no-store')
        row = next(x for x in data['rows'] if x['case'] == 'variable_loan' and x['period'] == 3)
        self.assertEqual(row['interest_cost'], 185)
        self.assertEqual(row['cash_close'], 1215)
        self.assertEqual(data['meta']['llm_calls'], 0)

    def test_input_and_transport_errors(self):
        for body, headers, endpoint, expected in [
            (b'{', None, '/api/simulate', 400),
            (b'{"annual_rate_after":true}', None, '/api/simulate', 400),
            (b'{"annual_rate_after":0.3}', None, '/api/simulate', 400),
            (b'{"annual_rate_after":0.06}', {'Content-Type':'text/plain'}, '/api/simulate', 415),
            (b'x'*4097, None, '/api/simulate', 413),
            (b'{}', None, '/api/unknown', 404),
            (b'{"annual_rate_after":0.06}', {'Content-Type':'application/json', 'Origin':'https://example.invalid'}, '/api/simulate', 403),
        ]:
            with self.subTest(expected=expected, endpoint=endpoint):
                status, data, _ = self.request(body, headers, endpoint)
                self.assertEqual(status, expected)
                self.assertIn('error', data)
                self.assertNotIn('rows', data)


if __name__ == '__main__':
    unittest.main()
