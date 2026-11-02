# BPTK-Py · erster technischer Screen

Stand: 2. November 2026 · Status: `documentation_reviewed` mit eigenem Offline-Runtime-Screen; Eignung: `conditional`. Kein generativer Persona-Pilot oder pädagogisch validierter Simulator.

## Prüfgegenstand

[transentis/BPTK-Py](https://github.com/transentis/bptk_py), installierte Paketversion 3.5.0, gelesener Quellstand `840fb9b61504c5a6e463e72a73c07e0b8cff6d5e`, MIT. Getrennte lokale Prüfumgebung, Python 3.13.12. Der untersuchte `pyproject.toml` verlangt Python >=3.13; frühere Dokumentationsangaben sind nicht die Installationsgrundlage dieser Prüfung. Vier wesentliche Pythonmodule des installierten Pakets stimmen byteweise mit dem gelesenen Checkout überein; daraus wird keine vollständige Identität aller Paketdateien behauptet.

36 ausgewählte Originaltests bestanden: Agent, Event, Scheduler und SD-DSL-Beispiele. [Maschinenlesbarer Beleg](evidence/bptk-upstream-tests-2026-11-02.json). Kein vollständiger Upstream-Testlauf und kein Rust-/Browser-/Server-Benchmark.

## Eigener technischer Durchstich

Das [Prüfskript](../../tools/probe_bptk_hybrid.py) verwendet echte BPTK-Modelle mit Beständen, Flüssen, zeitabhängigem Parameter, Agenten, Ereigniszustellung und technischem Zustandswechsel. Drei fiktive Rechenfälle, sechs Perioden, drei Parameterverläufe: 54 gespeicherte Zeilen. Ein Extremfall prüft begrenzte verfügbare Mittel und offen ausgewiesene ungedeckte Verpflichtungen. Eine unabhängige Neukonstruktion liefert denselben Verlauf. Ergebnis: Prüfungen bestanden, null LLM-Anfragen. [Alle Ergebnisse, Eingabeannahmen und Grenzen](../../qa/bptk-technical-screen-2026-11-02.json).

Die unterschiedliche Zinsbetroffenheit ist absichtlich konstruiert. Sie ist keine entdeckte Anlegerpsychologie und keine realistische geldpolitische Wirkungsschätzung. Die technische Markierung `review_due` bezeichnet ein empfangenes Vertragsereignis; eine geringere Anlagevormerkung folgt aus einer offen gelegten Rechenregel. Kein LLM hat entschieden, und es werden keine Wertpapiere gekauft. Bankgegenkonten, Tilgung, echte Leitzinstransmission, Inflationsdynamik und empirische Haushalte sind nicht Bestandteil des Fixtures.

## Einordnung

System Dynamics und ereignisabhängige Zustände lassen sich mit der Bibliothek technisch verbinden. Sie liefert Mechanismen, kein fertiges validiertes ökonomisches oder psychologisches Modell. Besonders zu prüfen bleiben Schema der wirtschaftlichen Vorgänge, Quellen/Einheiten, Schnittstelle zur Oberfläche, vollständige Zustandswiederherstellung sowie spätere generative Anbindung.

Der [begrenzte POC-Vorschlag](../../POC.md) nutzt diese Prüfung als vorhandene Ausgangsbasis. Der technische Screen legt das spätere erste Lernmodul oder die gesamte Produktdarstellung nicht fest. Frontend und öffentliche Bereitstellung sind noch nicht implementiert.
