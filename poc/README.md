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

1. **Wirtschaft starten**. Produktion, Löhne, Steuern, Konsum, mögliche Investitionen und Monatsabschlüsse laufen ohne weiteren Eingriff weiter. Ein Monat hat fünf Phasen. Die Geschwindigkeit lässt sich zwischen **0,25×, 0,5×, 1×, 2× und 4×** wechseln; bei 0,25× liegen mindestens 7,2 Sekunden zwischen den Phasen, bei 0,5× mindestens 3,6 Sekunden. **Pausieren** stoppt weitere Schritte; ein bereits angefragter Schritt kann noch abschließen. **Eine Phase weiter** führt im pausierten Zustand einen tatsächlichen weiteren Rechenschritt aus.
2. Die Systemkarte zeigt Haushalte, Unternehmen, Staat, Finanzsektor und einen vereinfachten Außenhandelsanschluss. Kontostände sind Bestände. Verbindungssummen zeigen tatsächlich verbuchte Zahlungen des laufenden Monats. Bewegte Marker kennzeichnen die aktuelle Buchungsphase; sie zählen keine zusätzlichen Zahlungen.
3. Kleine Kurven zeigen abgeschlossene Monatsbestände und den aktuellen Stand. Jede Box hat eine eigene Skala; die Kurven sind kein Vergleich absoluter Größen zwischen Sektoren. Veränderungen innerhalb eines Monats bewegen den letzten Punkt. Der Konsumverlauf zählt nur abgeschlossene Monate.
4. Ein System anklicken: Erklärung, Kontensumme und Buchungen erscheinen im Inspektor. Auf schmaleren Ansichten wird dorthin gesprungen; **Zur Systemkarte** führt zurück. Die Karte ist auf kleinen Bildschirmen seitlich verschiebbar.
5. **In das System hineingehen** zeigt seine Mitglieder; beim Staat öffnen sich Steuern, Ausgaben, Kassenfehlbetrag, Staatskredit, Zinsen, Tilgung, Kassenreserve und Schuldenverlauf. Grafische Pfeile und Belege gleichen Staatsschuld und Bankforderung ab. [Staatskreditkonzept](FISCAL_MODEL.md). Ein Haushalt öffnet Konten, Eingänge, Ausgänge und Regeln. **Unternehmen → Betrieb** zeigt Absatzplanung, Lagerbrücke, tatsächliche Produktion, Personalentscheidung und Gewinnverwendung neben dem Firmenkonto. Der Navigationspfad führt zurück; Zeit und Modellzustand bleiben über alle Ebenen identisch.
Die Übersicht **Wie viel Geld bleibt im Inland?** trennt aktuelle Inlandsguthaben von dem vereinfachten Auslandskonto und zeigt jeweils die Änderung seit Start. **Konten und Geldmenge erklären** zeigt den Abgleich aller Kundenkonten mit Kreditvergabe und Tilgung. Energiezahlungen verringern das Inlandsguthaben, ohne die Summe einschließlich Auslandskonto zu verringern; tatsächlich bezahlte Warenexporte führen Guthaben zurück ins Inland. Im Einzelsystem erklärt **Woher kommt das Geld?** die Gleichung Monatsanfang + Eingänge − Ausgänge = aktuelles Konto.

6. **Finanzsektor → In das System hineingehen** öffnet Bankbilanz und Kreditbestand. **Maschinenkredit öffnen** zeigt die Vertragsdetails. **Maschinenkredit anfragen** merkt den 1.200-€-Vertrag vor. Die nächste Investitionsphase bucht Kreditguthaben und Forderung; die Abschlussphase bezahlt und liefert die Maschine. Ab dem folgenden Monat laufen Zinsen und 100 € Tilgung. Vier anwählbare Wege zeigen echte Vorher-/Nachher-Buchungen; die Bankbilanz bleibt im selben Weltzustand sichtbar. [Bankkonzept](BANKING_MODEL.md). Die 10.000 € Bankkapital werden getrennt von anfangs 146.000 € Kundeneinlagen geführt.
7. Optional **Ereignis auslösen**: Energieimporte verteuern oder Konsumanteil reduzieren; nach dem Konsumschock kann die Konsumneigung wiederhergestellt werden. Ein vorgemerkter Eingriff wirkt erst beim nächsten Monatsbeginn. Beschäftigungsänderungen folgen den dokumentierten Schwellen, keinem vorgegebenen Ereignisdrehbuch.
8. **Ausland → In das System hineingehen** zeigt Energiezahlungen, Warenexporte und den Saldo mit entgegengesetzten Güter-/Geldpfeilen. Der monatliche Plan von sechs Alltags- und zwei Werkstattgütern ist durch Anfangsguthaben und freie Ware begrenzt. Liefernachweise zeigen Stückzahl, Firmenlager vor/nach und passende Zahlungs-ID. [Außenhandelskonzept](FOREIGN_MODEL.md).
9. **Lauf mit Buchungen exportieren** erzeugt JSON mit Anfangskonten, vollständigem Zahlungsjournal, aktuellen Zuständen, Annahmen, wirksamen Eingriffen und Monatsgeschichte. **Neu starten** erzeugt den identischen Anfangszustand als neuen Lauf.

Modell v6: [Systemgrenze und Unternehmenskonzept](COMPANY_MODEL.md). Der Grundbedarfsplan von 1.000 € pro Haushalt und Monat darf auch aus vorhandenem Kontoguthaben finanziert werden. Höhere einkommensabhängige Kaufpläne bleiben möglich. Geld- und Warenmangel begrenzen die tatsächlichen Käufe. Die früheren V1-Regeln und ihre Langzeitgrenzen sind [dokumentiert](../qa/circular-flow-v1-limitations-2026-11-02.json).

Läufe leben im Arbeitsspeicher des lokalen Servers. Die Berechnung schreitet durch Anfragen des geöffneten Browsers voran; es gibt keinen unabhängigen Hintergrunddienst nach dem Schließen. Maximal 24 Monate pro Lauf, bis zu 64 gleichzeitig gespeicherte Läufe. Serverneustart verliert die laufenden Welten; ein JSON-Export ist kein implementierter Wiederherstellungspunkt. Bei Fehlern hält die Ansicht an und zeigt den letzten bestätigten Zustand ausdrücklich weiter.

Der frühere Haushaltsversuch bleibt unter **http://127.0.0.1:5173/?view=household** verfügbar. Er ist ein separater, fiktiver Vertragsvergleich, keine Detailberechnung der neuen Welt.

## Prüfen und gebaute Ansicht starten

```sh
npm test
npm run build
npm start
```

Die gebaute Ansicht und API sind gemeinsam unter **http://127.0.0.1:8765/** erreichbar. Dies ist ein lokaler POC-Server, keine Produktionsbereitstellung.

Tests prüfen unter anderem unabhängige Ledger-Rekonstruktion, identische Gegenbuchungen, Geld-/Lagerbestände, Systemregeln ohne laufende Welt, Investitionslieferung und spätere Kapazität, steuerfreie Transfers, reproduzierbare Verläufe, Wirkung an Monatsgrenzen, echte HTTP-Schritte, Wiederholschutz und die 24-Monats-Grenze. Der [V6-Staatsfinanzierungsaudit](../qa/fiscal-v6-plausibility.md) ergänzt Kredit-, Zins- und Schuldentests. Der [V5-Außenhandelsaudit](../qa/foreign-v5-plausibility.md) prüft die Exporterweiterung. Der [V4-Unternehmensaudit](../qa/company-v4-plausibility.md) prüft ausgewählte 24-Monats-Verläufe; er ist keine Kalibrierung. Die früheren sechs Tests des Haushaltsversuchs bleiben enthalten. Der [technische V3-Prüfstand](../qa/banking-v3-verification-2026-11-02.json) dokumentiert Bank-UI und Versionsabgleich. Der [unabhängige Plausibilitätsaudit](../qa/bank-plausibility-review-2026-11-02.md) trennt Bankprüfung und verbleibende Langzeitprobleme. Der frühere Stand ist im [V2-Prüfprotokoll](../qa/fiscal-and-household-v2-2026-11-02.json) dokumentiert; der [ursprüngliche Prüfstand](../qa/world-poc-verification-2026-11-02.json) bleibt erhalten.

## Aufbau und Grenzen

- `systems.py`: explizite Systemeingänge und geplante Ausgänge; Regeln ohne Oberfläche oder globale Welt ausführbar.
- `treasury.py`: begrenzte Staatskredite, Zwischenfinanzierung, Anfangsschuld-Zinsen, Überschusstilgung und Staatskassen-/Schuldenverlauf.
- `foreign.py`: begrenzte Auslandsbestellungen aus vorhandenem Anfangsguthaben, Liefernachweise und Außenhandelsabgleich.
- `firms.py`: reine Absatz-, Produktions-, Personal- und Pufferplanung, unabhängig von Scheduler und Oberfläche.
- `banking.py`: Einbankbilanz und begrenzter Maschinenkredit mit einzeln nachvollziehbaren Buchungen.
- `world.py`: Konten, Lager, Gegenparteien, Journal, globale Zeit und native BPTK-Systemagenten. Centgenaue Buchungen sind die maßgebliche Quelle für die Grafik.
- `server.py`: begrenzte lokale JSON-Schnittstelle; Revisionen verhindern doppelte Ausführung desselben Schritts.
- `src/App.tsx`, `src/world-schema.ts`: gemeinsame laufende Welt mit Systemnavigation und Prüfung der Antworten.
- `test_world.py`: Rechen-, System- und Schnittstellentests. `engine.py`, `test_engine.py` und `src/HouseholdApp.tsx` erhalten POC 01.

Alle Beträge, Kaufbudgets und Verhaltensschwellen sind eigene illustrative Szenarioannahmen. Unternehmen führen eine vereinfachte Kosten-/Ergebnisrechnung; sie ersetzt keine vollständige handelsrechtliche Gewinnrechnung. Vereinfachte Abrechnungskonten sind keine vollständigen Zentralbank-/Bankeinlagenbilanzen. Ein begrenzter Maschinenkredit mit Geldschöpfung, Zinsen und Tilgung ist integriert. Ein Staatskredit bis 50.000 € mit 3 % Jahreszins finanziert Kassenfehlbeträge; Überschüsse tilgen Schuld. Ein allgemeiner Kreditmarkt, staatliche Anleihefinanzierung, Interbankverkehr, Wertberichtigungen, Inflation, Abschreibung, Wertpapiermärkte oder LLM-Entscheidungen sind nicht enthalten. Staat und Ausland sind bewusst begrenzt; ein dauerhaftes Gleichgewicht wird nicht zugesichert. Kontenkonsistenz ist kein Nachweis empirischer oder pädagogischer Gültigkeit.

Die Oberfläche folgt einer internen Gestaltungsreferenz. Private Produktquellen, Designpakete oder Fontdateien wurden nicht kopiert. Die verwendeten IBM-Plex-Sans-Dateien stammen aus dem öffentlichen Paket `@fontsource/ibm-plex-sans`; dessen Font-Lizenz liegt im Paket. Lucide-Symbole und weitere Abhängigkeiten behalten ihre jeweiligen Lizenzen.


## Weiterentwicklung der sichtbaren Vorschau

Inkompatible Modell-/Antwortformatänderungen zunächst getrennt vorbereiten und Kern und Oberfläche gemeinsam prüfen. Erst danach die sichtbare Vorschau umstellen. Die Oberfläche prüft die Modellversion ausdrücklich; bei Abweichungen erscheint eine kurze Meldung und der letzte bestätigte Zustand bleibt erhalten. Ein neuer Modellstand erfordert einen neuen Lauf. Technische Schemafehler gehören nicht in die Bedienoberfläche.
