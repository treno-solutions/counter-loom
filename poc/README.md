# Counterloom POC · laufender Wirtschaftskreislauf

Eine lokale React-/Tailwind-Ansicht zeigt eine kleine, monatlich laufende Modellwirtschaft. Jeder Schritt wird über eine lokale Python-Schnittstelle mit dem bereits geprüften BPTK-Agentenscheduler neu ausgeführt. [Modellkonzept, Regeln und Systemgrenze](WORLD_MODEL.md). Keine öffentliche Instanz, keine kalibrierte Volkswirtschaft.

## Einrichten

Voraussetzungen: Node.js >=20.19 beziehungsweise >=22.12, npm und Python >=3.13. Frontend-Abhängigkeiten sind durch `package-lock.json` gebunden; BPTK-Py ist auf 3.5.0 festgelegt. Mit installiertem `uv` vom Repository-Stamm aus:

```sh
uv venv --python 3.13 poc/.venv
uv pip install --python poc/.venv/bin/python -r poc/requirements.txt
cd poc
npm ci
npm run dev
```

Die Ansicht ist unter **http://127.0.0.1:5173/** erreichbar. Der Launcher wartet auf die lokale Python-Schnittstelle (Port 8765), bevor er die Webansicht startet. Beide binden ausschließlich an die Loopback-Adresse. Beenden mit Strg+C. `COUNTERLOOM_PYTHON` kann einen anderen Interpreter mit installiertem BPTK-Py auswählen. Eine vorhandene private BPTK-Prüfumgebung wird ebenfalls erkannt; sie ist für einen frischen Clone nicht erforderlich.

## Beobachten und bedienen

1. **Wirtschaft starten**. Produktion, Löhne, Steuern, Konsum, mögliche Investitionen und Monatsabschlüsse laufen ohne weiteren Eingriff weiter. Ein Monat hat fünf Phasen. **Pausieren** stoppt weitere Schritte; ein bereits angefragter Schritt kann noch abschließen. **Eine Phase weiter** führt im pausierten Zustand einen tatsächlichen weiteren Rechenschritt aus.
2. Die Systemkarte zeigt Haushalte, Unternehmen, Staat, Finanzsektor und einen vereinfachten Energie-Außenanschluss. Kontostände sind Bestände. Verbindungssummen zeigen tatsächlich verbuchte Zahlungen des laufenden Monats. Bewegte Marker kennzeichnen die aktuelle Buchungsphase; sie zählen keine zusätzlichen Zahlungen.
3. Kleine Kurven zeigen abgeschlossene Monatsbestände und den aktuellen Stand. Jede Box hat eine eigene Skala; die Kurven sind kein Vergleich absoluter Größen zwischen Sektoren. Veränderungen innerhalb eines Monats bewegen den letzten Punkt. Der Konsumverlauf zählt nur abgeschlossene Monate.
4. Ein System anklicken: Erklärung, Kontensumme und Buchungen erscheinen im Inspektor. Auf schmaleren Ansichten wird dorthin gesprungen; **Zur Systemkarte** führt zurück. Die Karte ist auf kleinen Bildschirmen seitlich verschiebbar.
5. **In das System hineingehen** zeigt seine Mitglieder. Ein Haushalt oder Betrieb öffnet Konten, Eingänge, Ausgänge und Regeln. Der Navigationspfad führt zurück; Zeit und Modellzustand bleiben über alle Ebenen identisch.
6. Optional **Ereignis auslösen**: Energieimporte verteuern oder Konsumanteil reduzieren. Ein vorgemerkter Eingriff wirkt erst beim nächsten Monatsbeginn. Beschäftigungsänderungen folgen den dokumentierten Schwellen, keinem vorgegebenen Ereignisdrehbuch.
7. **Lauf mit Buchungen exportieren** erzeugt JSON mit Anfangskonten, vollständigem Zahlungsjournal, aktuellen Zuständen, Annahmen, wirksamen Eingriffen und Monatsgeschichte. **Neu starten** erzeugt den identischen Anfangszustand als neuen Lauf.

Läufe leben im Arbeitsspeicher des lokalen Servers. Die Berechnung schreitet durch Anfragen des geöffneten Browsers voran; es gibt keinen unabhängigen Hintergrunddienst nach dem Schließen. Maximal 240 Monate pro Lauf, bis zu 64 gleichzeitig gespeicherte Läufe. Serverneustart verliert die laufenden Welten; ein JSON-Export ist kein implementierter Wiederherstellungspunkt. Bei Fehlern hält die Ansicht an und zeigt den letzten bestätigten Zustand ausdrücklich weiter.

Der frühere Haushaltsversuch bleibt unter **http://127.0.0.1:5173/?view=household** verfügbar. Er ist ein separater, fiktiver Vertragsvergleich, keine Detailberechnung der neuen Welt.

## Prüfen und gebaute Ansicht starten

```sh
npm test
npm run build
npm start
```

Die gebaute Ansicht und API sind gemeinsam unter **http://127.0.0.1:8765/** erreichbar. Dies ist ein lokaler POC-Server, keine Produktionsbereitstellung.

Tests prüfen unter anderem unabhängige Ledger-Rekonstruktion, identische Gegenbuchungen, Geld-/Lagerbestände, Systemregeln ohne laufende Welt, Investitionslieferung und spätere Kapazität, steuerfreie Transfers, reproduzierbare Verläufe, Wirkung an Monatsgrenzen, echte HTTP-Schritte, Wiederholschutz und die 240-Monats-Grenze. Die früheren sechs Tests des Haushaltsversuchs bleiben enthalten. Browserprüfungen sind separat im [Prüfprotokoll](../qa/world-poc-verification-2026-11-02.json) dokumentiert.

## Aufbau und Grenzen

- `systems.py`: explizite Systemeingänge und geplante Ausgänge; Regeln ohne Oberfläche oder globale Welt ausführbar.
- `world.py`: Konten, Lager, Gegenparteien, Journal, globale Zeit und native BPTK-Systemagenten. Centgenaue Buchungen sind die maßgebliche Quelle für die Grafik.
- `server.py`: begrenzte lokale JSON-Schnittstelle; Revisionen verhindern doppelte Ausführung desselben Schritts.
- `src/App.tsx`, `src/world-schema.ts`: gemeinsame laufende Welt mit Systemnavigation und Prüfung der Antworten.
- `test_world.py`: Rechen-, System- und Schnittstellentests. `engine.py`, `test_engine.py` und `src/HouseholdApp.tsx` erhalten POC 01.

Alle Beträge, Kaufbudgets und Verhaltensschwellen sind eigene illustrative Szenarioannahmen. Positive operative Zahlungsüberschüsse sind keine vollständige handelsrechtliche Gewinnrechnung. Vereinfachte Abrechnungskonten sind keine vollständigen Zentralbank-/Bankeinlagenbilanzen. Es gibt keine neuen Kredite, Geldschöpfung, Tilgung, Inflation, Abschreibung, Wertpapiermärkte oder LLM-Entscheidungen. Staat und Ausland sind bewusst begrenzt; ein dauerhaftes Gleichgewicht wird nicht zugesichert. Kontenkonsistenz ist kein Nachweis empirischer oder pädagogischer Gültigkeit.

Die Oberfläche folgt einer internen Gestaltungsreferenz. Private Produktquellen, Designpakete oder Fontdateien wurden nicht kopiert. Die verwendeten IBM-Plex-Sans-Dateien stammen aus dem öffentlichen Paket `@fontsource/ibm-plex-sans`; dessen Font-Lizenz liegt im Paket. Lucide-Symbole und weitere Abhängigkeiten behalten ihre jeweiligen Lizenzen.
