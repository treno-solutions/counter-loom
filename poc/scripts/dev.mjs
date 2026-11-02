import { spawn } from 'node:child_process';
import path from 'node:path';
import { root, python } from './python.mjs';

const api = spawn(python(), ['server.py'], { cwd: root, stdio: 'inherit' });
const web = spawn(process.execPath, [path.join(root, 'node_modules/vite/bin/vite.js')], { cwd: root, stdio: 'inherit' });
let stopping = false;
function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  api.kill('SIGTERM'); web.kill('SIGTERM'); process.exitCode = code;
}
for (const child of [api, web]) {
  child.on('error', (error) => { console.error(error.message); stop(1); });
  child.on('exit', (code) => { if (!stopping) stop(code ?? 1); });
}
for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => stop());
