import { spawn } from 'node:child_process';
import path from 'node:path';
import { root, python } from './python.mjs';

let web;
let stopping = false;
const api = spawn(python(), ['server.py'], { cwd: root, stdio: 'inherit' });
function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  api.kill('SIGTERM'); web?.kill('SIGTERM'); process.exitCode = code;
}
function watch(child) {
  child.on('error', error => { console.error(error.message); stop(1); });
  child.on('exit', code => { if (!stopping) stop(code ?? 1); });
}
watch(api);
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => stop());
// Only expose the frontend after the Python model imports and API are ready.
let ready = false;
for (let attempt = 0; attempt < 100 && !stopping; attempt++) {
  try {
    const response = await fetch('http://127.0.0.1:8765/api/health', { signal: AbortSignal.timeout(500) });
    if (response.ok) { ready = true; break; }
  } catch { /* API is still starting. */ }
  await new Promise(resolve => setTimeout(resolve, 100));
}
if (ready && !stopping) {
  web = spawn(process.execPath, [path.join(root, 'node_modules/vite/bin/vite.js')], { cwd: root, stdio: 'inherit' });
  watch(web);
} else if (!stopping) {
  console.error('Der lokale Rechenkern konnte nicht gestartet werden. Bitte die Python-Einrichtung prüfen.');
  stop(1);
}
