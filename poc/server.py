"""Loopback-only POC API and production static server; no external services."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json
import os

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / '.runtime'
RUNTIME.mkdir(exist_ok=True)
os.chdir(RUNTIME)
from engine import simulate_request
from world import world_request


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE / 'dist'), **kwargs)

    def send_json(self, status, value):
        data = json.dumps(value, ensure_ascii=False, allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if urlsplit(self.path).path == '/api/health':
            return self.send_json(200, {'status': 'ok', 'llm_calls': 0})
        if urlsplit(self.path).path.startswith('/api/'):
            return self.send_json(404, {'error': 'Endpunkt nicht gefunden.'})
        target = HERE / 'dist' / urlsplit(self.path).path.lstrip('/')
        if target.is_dir() and urlsplit(self.path).path != '/':
            return self.send_json(404, {'error': 'Nicht gefunden.'})
        if not (HERE / 'dist/index.html').exists():
            return self.send_json(503, {'error': 'Webansicht fehlt. Bitte npm run dev oder zuerst npm run build verwenden.'})
        return super().do_GET()

    def list_directory(self, path):
        return self.send_json(404, {'error': 'Nicht gefunden.'})

    def do_POST(self):
        route = urlsplit(self.path).path
        world_routes = {'/api/world': 'create', '/api/world/step': 'step', '/api/world/event': 'event', '/api/world/export': 'export'}
        if route != '/api/simulate' and route not in world_routes:
            return self.send_json(404, {'error': 'Endpunkt nicht gefunden.'})
        origin = self.headers.get('Origin')
        if origin and origin not in {'http://127.0.0.1:5173', 'http://localhost:5173', 'http://127.0.0.1:8765', 'http://localhost:8765'}:
            return self.send_json(403, {'error': 'Diese Herkunft ist für den lokalen POC nicht freigegeben.'})
        if self.headers.get_content_type() != 'application/json':
            return self.send_json(415, {'error': 'Bitte JSON senden.'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 4096:
                return self.send_json(413, {'error': 'Ungültige Größe der Anfrage.'})
            payload = json.loads(self.rfile.read(size))
            result = world_request(world_routes[route], payload) if route in world_routes else simulate_request(payload)
        except (ValueError, UnicodeDecodeError) as error:
            if route in world_routes:
                return self.send_json(400, {'error': str(error)})
            return self.send_json(400, {'error': 'Ungültige Eingabe. Erlaubt ist ein jährlicher Zinssatz von 0 bis 20 %.'})
        except Exception:
            return self.send_json(500, {'error': 'Die Berechnung ist fehlgeschlagen. Es wurde kein Ersatzresultat erzeugt.'})
        return self.send_json(200, result)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8765), Handler)
    print('Counterloom POC API / lokale Ansicht: http://127.0.0.1:8765', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
