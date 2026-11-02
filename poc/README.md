# Counterloom POC · lokale 2D-Lernansicht

Eine React-/Tailwind-Seite zeigt einen kleinen, algorithmisch berechneten Verlauf aus BPTK-Py. Der POC ist lokal ausführbar; es gibt keine bereitgestellte öffentliche Instanz. [Umfang und Grenzen](../POC.md).

## Einrichten

Voraussetzungen: Node.js >=20.19 beziehungsweise >=22.12, npm und Python >=3.13. Die Frontend-Abhängigkeiten sind durch `package-lock.json` gebunden; BPTK-Py ist auf 3.5.0 festgelegt. Mit installiertem `uv` vom Repository-Stamm aus:

```sh
uv venv --python 3.13 poc/.venv
uv pip install --python poc/.venv/bin/python -r poc/requirements.txt
cd poc
npm ci
npm run dev
```

Die Ansicht öffnet sich unter **http://127.0.0.1:5173/**. Die lokale Schnittstelle läuft auf Port 8765. Beide Prozesse binden ausschließlich an die lokale Loopback-Adresse. Beenden mit Strg+C. Für andere Umgebungen kann `COUNTERLOOM_PYTHON` auf einen Python-Interpreter mit installiertem BPTK-Py zeigen. Die Launcher erkennen außerdem die bereits vorhandene private BPTK-Prüfumgebung; sie ist für einen frischen Clone nicht erforderlich.

## Verwenden

1. Drei bebilderte Haushalte und ihre Ausgangslage kennenlernen. Zu Beginn gilt überall der Ausgangszins von 2 %; die Änderung ist noch nicht ausgelöst.
2. Eine Vermutung bilden und **Zinsen auf 6 % erhöhen** wählen. Alle drei Fälle werden neu berechnet und zeigen direkt Monat 3, in dem der neue Vertragszins erstmals wirkt.
3. **Zeig mir, warum** bei einem Haushalt wählen. Die Geldansicht erklärt Einkommen, Alltagskosten, Zinsen, Überschuss beziehungsweise Fehlbetrag und den separaten Geldtopf für eine spätere Anlage.
4. Die sechs Monate einzeln ansehen oder abspielen. **Zur Ausgangslage** stellt den unveränderten Vergleich wieder dar.
5. Optional **Anderen Zins ausprobieren** öffnen. Freie Eingaben werden erst mit dem grünen Knopf angewandt. **Rechnung und Modellgrenzen** enthält die Periodentabelle und vollständigen Annahmen.

Eine geänderte Eingabe wird als noch nicht berechnet gekennzeichnet. Bei einem Fehler verschwindet die Ergebnisansicht; es gibt keine Ersatzdaten. Für Berechnung, Auswahl und Wiedergabe werden keine LLMs verwendet.

## Prüfen und gebaute Ansicht starten

```sh
npm test
npm run build
npm start
```

Die gebaute Ansicht und API sind dann gemeinsam unter **http://127.0.0.1:8765/** erreichbar. Kein Vite-Prozess nötig. Die lokale API ist ein kleiner POC-Server, keine Produktionsbereitstellung.

`npm test` führt die unabhängige Decimal-Gegenrechnung, Reproduktions-/Ereignisprüfungen und HTTP-Eingabe-/Fehlerprüfungen aus. `npm run build` prüft TypeScript und erstellt die Webansicht. Visuelle und interaktive Browserprüfungen sind im [ersten Prüfprotokoll](../qa/poc-verification-2026-11-02.json) und im [Prüfprotokoll der geführten Ansicht](../qa/poc-guided-view-2026-11-02.json) dokumentiert; sie werden nicht automatisch von `npm test` ausgeführt.

## Aufbau

- `src/`: React-Ansicht, Tailwind-Einstieg, eigene Styles und Zod-Prüfung der API-Antwort.
- `engine.py`: Adapter um den [bereits geprüften BPTK-Durchstich](../tools/probe_bptk_hybrid.py). BPTK berechnet die wirtschaftlichen Größen; React stellt sie dar.
- `server.py`: lokale, begrenzte JSON-Schnittstelle und Auslieferung der gebauten Ansicht.
- `test_engine.py`: unabhängige Rechen- und HTTP-Prüfungen.

Die Oberfläche orientiert sich an der vorhandenen internen Gestaltungsreferenz. Private Produktquellen, Designpakete und Fontdateien wurden nicht kopiert. Die verwendeten IBM-Plex-Sans-Dateien kommen aus dem öffentlichen Paket `@fontsource/ibm-plex-sans`; dessen Font-Lizenz liegt im Paket. Lucide-Symbole und weitere Abhängigkeiten behalten ihre jeweiligen Lizenzen. Die Gestaltung und Anbindung dieses POC sind neu erstellt.

## Fachliche Grenzen

Die Zinsänderung ist direkt auf die variablen Verträge angewandt, kein Modell einer EZB-Leitzinsübertragung. Einlagensumme/Restschuld bleiben konstant, es gibt keine Tilgung. Bankbilanzen, Inflation und Marktpreise sind nicht enthalten. Der Anlagebetrag wird nur in einen separaten Geldtopf umgebucht; es findet kein Wertpapierkauf statt. `review_due` ist ein technischer Ereignisstatus und keine Persona-Abwägung. Die erste Entscheidung über den Anlagebetrag folgt einer festen Regel.

Eine spätere LLM-Entscheidung und der Nachweis eines Workshop-Lerneffekts sind gesonderte nächste Schritte. Dieser POC implementiert keinen vollständigen volkswirtschaftlichen Kreislauf.
