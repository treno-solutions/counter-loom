import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import path from 'node:path';

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export function python() {
  if (process.env.COUNTERLOOM_PYTHON) return process.env.COUNTERLOOM_PYTHON;
  for (const candidate of [path.join(root, '.venv/bin/python'), path.join(root, '../.framework-review/bptk-venv/bin/python')]) {
    if (existsSync(candidate)) return candidate;
  }
  return 'python3';
}
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const child = spawn(python(), process.argv.slice(2), { cwd: root, stdio: 'inherit' });
  child.on('error', () => { console.error('Python fehlt. Bitte die Einrichtung in poc/README.md ausführen.'); process.exitCode = 1; });
  child.on('exit', (code) => { process.exitCode = code ?? 1; });
  for (const signal of ['SIGTERM', 'SIGINT']) process.on(signal, () => child.kill(signal));
}
