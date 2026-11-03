# Counterloom POC · laufender Wirtschaftskreislauf

Aktuelle Erweiterung v14: [Ausschüttungssteuer mit Brutto-/Nettoansicht](DISTRIBUTION_TAX_MODEL.md) und [kontrollierter 600-Monats-Vergleich](../qa/tax-v14-comparison.md).

Eine lokale React-/Tailwind-Ansicht zeigt eine kleine, monatlich laufende Modellwirtschaft. Jeder Schritt wird über eine lokale Python-Schnittstelle mit dem bereits geprüften BPTK-Agentenscheduler neu ausgeführt. [Modellkonzept, Regeln und Systemgrenze](WORLD_MODEL.md). Keine öffentliche Instanz, keine kalibrierte Volkswirtschaft.

Die Oberfläche folgt der Treno-Website: [Farben, Typografie und Komponenten](DESIGN_SYSTEM.md).

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

1. **Simulation starten**. Produktion, Löhne, Steuern, Konsum, mögliche Investitionen und Monatsabschlüsse laufen ohne weiteren Eingriff weiter. Ein Monat hat fünf Phasen. Die Geschwindigkeit lässt sich zwischen **0,25×, 0,5×, 1×, 2× und 4×** wechseln; bei 0,25× liegen mindestens 7,2 Sekunden zwischen den Phasen, bei 0,5× mindestens 3,6 Sekunden. **Pausieren** stoppt weitere Schritte; ein bereits angefragter Schritt kann noch abschließen. **Nächste Phase** führt im pausierten Zustand einen tatsächlichen weiteren Rechenschritt aus.
2. Die Systemkarte zeigt Haushalte, Unternehmen, Staat, Finanzsektor und einen vereinfachten Außenhandelsanschluss. Kontostände sind Bestände. Verbindungssummen zeigen tatsächlich verbuchte Zahlungen des laufenden Monats. Bewegte Marker kennzeichnen die aktuelle Buchungsphase; sie zählen keine zusätzlichen Zahlungen.
3. Kleine Kurven zeigen abgeschlossene Monatsbestände und den aktuellen Stand. Jede Box hat eine eigene Skala; die Kurven sind kein Vergleich absoluter Größen zwischen Sektoren. Veränderungen innerhalb eines Monats bewegen den letzten Punkt. Unter **Konsum nach Haushalt** zeigen sechs Diagramme Wunsch und tatsächliche Käufe auf derselben Euro-Skala für abgeschlossene Monate. Über die gemeinsame Monatsauswahl lassen sich Ereignisse, Vormonatsänderungen, Finanzierungslücken, fehlende Ware und Restbeträge prüfen. Aufklappbare Kaufpläne erklären die historischen Eingaben. Die Umschaltung **Ausgaben in Euro / Warenmengen zu Startpreisen** trennt nominale Ausgaben von realen Mengenänderungen. Eine gemeinsame Übersicht zeigt Energiekosten, Verkaufspreise, Kaufkraft, Produktion und betriebliche Beschäftigung. Die Daten sind im Laufexport enthalten; ältere Läufe benötigen einen Neustart.
4. Ein System anklicken: Erklärung, Kontensumme und Buchungen erscheinen im Inspektor. Auf schmaleren Ansichten wird dorthin gesprungen; **Zur Übersicht** führt zurück. Die Karte ist auf kleinen Bildschirmen seitlich verschiebbar.
5. **Details öffnen** zeigt seine Mitglieder; beim Staat öffnen sich Steuern, Ausgaben, Kassenfehlbetrag, Staatskredit, Zinsen, Tilgung, Kassenreserve und Schuldenverlauf. Grafische Pfeile und Belege gleichen Staatsschuld und Bankforderung ab. [Staatskreditkonzept](FISCAL_MODEL.md). Ein Haushalt öffnet Konten, Eingänge, Ausgänge und Regeln. **Unternehmen → Betrieb** zeigt Absatzplanung, Lagerbrücke, tatsächliche Produktion, Arbeitszeit, Verlusttoleranz, Stilllegung/Wiederanlauf und Gewinnverwendung neben dem Firmenkonto. Der Navigationspfad führt zurück; Zeit und Modellzustand bleiben über alle Ebenen identisch.
Die Übersicht **Guthaben im Inland und Ausland** trennt aktuelle Inlandsguthaben von dem vereinfachten Auslandskonto und zeigt jeweils die Änderung seit Start. **Geldbestände und Änderungen** zeigt den Abgleich aller Kundenkonten mit Kreditvergabe und Tilgung. Energiezahlungen verringern das Inlandsguthaben, ohne die Summe einschließlich Auslandskonto zu verringern; tatsächlich bezahlte Warenexporte führen Guthaben zurück ins Inland. Im Einzelsystem erklärt **Kontobewegungen** die Gleichung Monatsanfang + Eingänge − Ausgänge = aktuelles Konto.

6. **Finanzsektor → Details öffnen** öffnet Bankbilanz und Kreditbestand. **Maschinenkredit öffnen** zeigt die Vertragsdetails. **Maschinenkredit anfragen** merkt einen Vertrag für acht Werkstatteinheiten vor (anfangs 1.200 €). Preis, Kreditbetrag und Zins werden bei Gutschrift gebunden. Die nächste Investitionsphase bucht Kreditguthaben und Forderung; die Abschlussphase bezahlt und liefert die Maschine. Ab dem folgenden Monat laufen Zinsen und die vertragliche Tilgung über zwölf Fälligkeiten (anfangs 100 € monatlich). Vier anwählbare Wege zeigen echte Vorher-/Nachher-Buchungen; die Bankbilanz bleibt im selben Weltzustand sichtbar. [Bankkonzept](BANKING_MODEL.md). Die 10.000 € Bankkapital werden getrennt von anfangs 146.000 € Kundeneinlagen geführt.
7. Optional **Ereignis auslösen**: Energieimporte verteuern oder Konsumanteil reduzieren; Energie- und Konsumannahmen können zurückgesetzt und später erneut verändert werden, auch nach Monat 24. Ein vorgemerkter Eingriff wirkt erst beim nächsten Monatsbeginn. Beschäftigungsänderungen folgen den dokumentierten Schwellen, keinem vorgegebenen Ereignisdrehbuch.
8. **Ausland → Details öffnen** zeigt Energiezahlungen, Warenexporte und den Saldo mit entgegengesetzten Güter-/Geldpfeilen. Der monatliche Plan von sechs Alltags- und zwei Werkstattgütern ist durch Anfangsguthaben und freie Ware begrenzt. Liefernachweise zeigen Stückzahl, Firmenlager vor/nach und passende Zahlungs-ID. [Außenhandelskonzept](FOREIGN_MODEL.md).
9. **Leitzins ändern**: unter **Ereignis auslösen** oder **Finanzsektor → Details öffnen** einen Modell-Leitzins von 0 bis 10 % vormerken. Er gilt ab dem nächsten Monat. Der variable Betriebskredit passt sich einen Monat später an; der feste Altvertrag bleibt bei 2 %. Neue Maschinen-/Staatskreditbeträge erhalten neue, ab Gutschrift feste Konditionen. Die Bankansicht zeigt Vertragsbeträge, Monatszinsen und einen gemeinsamen Prozentverlauf; die Staatsansicht zeigt die einzelnen festen Kreditbeträge. [Zinskonzept](RATES_MODEL.md).
10. **Lauf mit Buchungen exportieren** erzeugt JSON mit Anfangskonten, vollständigem Zahlungsjournal, aktuellen Zuständen, Annahmen, wirksamen Eingriffen und Monatsgeschichte. **Neu starten** erzeugt den identischen Anfangszustand als neuen Lauf.

11. **Befristete Betriebsschliessung** unter **Ereignis auslösen**: Betrieb, Dauer und mit/ohne Kurzarbeitsleistung wählen. **Vormerken** verändert den laufenden Versuch ab nächstem Monat. **Mit / ohne Kurzarbeit vergleichen** rechnet zwei getrennte Fortsetzungen ohne Veränderung des laufenden Versuchs. Kurven, Monatswerte und Export zeigen Einkommen, Konsum, Konten und Staatsfinanzierung. [Krisenregeln und Grenzen](CRISIS_MODEL.md). [600-Monats-Vergleich und offene Modellgrenzen](../qa/crisis-v11-plausibility.md).

12. **Unternehmen → Betrieb → Gewinnrücklagen und Ausschüttungen** erklärt den Gewinnvortrag, geschützte Liquidität sowie reguläre und zusätzliche Quartalsüberweisungen. Monatsauswahl und getrennte Verläufe zeigen Entscheidungen und Zahlungen. [Gewinnverwendungsregeln](PROFIT_POLICY.md), [600-Monats-Vergleich](../qa/profit-v12-comparison.md).

13. **Staat → Details öffnen → Ausgabenplan und finanzierte öffentliche Arbeit** zeigt Defizitreaktion, genehmigte und bezahlte Stellen, Beschaffung, Soziallücken und alte Lohnansprüche. Monatsauswahl und Verläufe trennen Bedarfssaldo und tatsächlichen Zahlungssaldo. [Budgetregel](PUBLIC_BUDGET_MODEL.md), [600-Monats-Vergleich](../qa/fiscal-v13-comparison.md).

Modell v14: [Systemgrenze und Unternehmenskonzept](COMPANY_MODEL.md). Der Grundbedarfsplan von 1.000 € pro Haushalt und Monat darf auch aus vorhandenem Kontoguthaben finanziert werden. Höhere einkommensabhängige Kaufpläne bleiben möglich. Geld- und Warenmangel begrenzen die tatsächlichen Käufe. Die früheren V1-Regeln und ihre Langzeitgrenzen sind [dokumentiert](../qa/circular-flow-v1-limitations-2026-11-02.json).

Läufe leben im Arbeitsspeicher des lokalen Servers. Die Berechnung schreitet durch Anfragen des geöffneten Browsers voran; es gibt keinen unabhängigen Hintergrunddienst nach dem Schließen. Kein automatischer Stopp nach 24 Monaten; bis zu 64 gleichzeitig gespeicherte Läufe. Die Anzeige zeigt die letzten 36 Abschlüsse, der Export behält die gesamte Vergangenheit. Es gibt keine Zusicherung unbegrenzt langer Rechenzeit oder empirischer Langzeitgültigkeit. Serverneustart verliert die laufenden Welten; ein JSON-Export ist kein implementierter Wiederherstellungspunkt. Bei Fehlern hält die Ansicht an und zeigt den letzten bestätigten Zustand ausdrücklich weiter.

Der frühere Haushaltsversuch bleibt unter **http://127.0.0.1:5173/?view=household** verfügbar. Er ist ein separater, fiktiver Vertragsvergleich, keine Detailberechnung der neuen Welt.

## Prüfen und gebaute Ansicht starten

```sh
npm test
npm run build
npm start
```

Die gebaute Ansicht und API sind gemeinsam unter **http://127.0.0.1:8765/** erreichbar. Dies ist ein lokaler POC-Server, keine Produktionsbereitstellung.

Tests prüfen unter anderem unabhängige Ledger-Rekonstruktion, identische Gegenbuchungen, Geld-/Lagerbestände, Systemregeln ohne laufende Welt, Investitionslieferung und spätere Kapazität, steuerfreie Transfers, reproduzierbare Verläufe, Wirkung an Monatsgrenzen, echte HTTP-Schritte, Wiederholschutz sowie optionale feste Beobachtungshorizonte und offene Läufe über Monat 24 hinaus. Die [V8-Preisregeln](PRICES_MODEL.md) und der [V8-Plausibilitätsaudit](../qa/prices-v8-plausibility.md) ergänzen die historischen Belege. Der [V7-Leitzinsaudit](../qa/rates-v7-plausibility.md) prüft Vertragsbindung, verzögerte Anpassung und gemischte Staatszinsen. Der [V6-Staatsfinanzierungsaudit](../qa/fiscal-v6-plausibility.md) ergänzt Kredit-, Zins- und Schuldentests. Der [V5-Außenhandelsaudit](../qa/foreign-v5-plausibility.md) prüft die Exporterweiterung. Der [V4-Unternehmensaudit](../qa/company-v4-plausibility.md) prüft ausgewählte 24-Monats-Verläufe; er ist keine Kalibrierung. Die früheren sechs Tests des Haushaltsversuchs bleiben enthalten. Der [technische V3-Prüfstand](../qa/banking-v3-verification-2026-11-02.json) dokumentiert Bank-UI und Versionsabgleich. Der [unabhängige Plausibilitätsaudit](../qa/bank-plausibility-review-2026-11-02.md) trennt Bankprüfung und verbleibende Langzeitprobleme. Der frühere Stand ist im [V2-Prüfprotokoll](../qa/fiscal-and-household-v2-2026-11-02.json) dokumentiert; der [ursprüngliche Prüfstand](../qa/world-poc-verification-2026-11-02.json) bleibt erhalten.

## Aufbau und Grenzen

- `systems.py`: explizite Systemeingänge und geplante Ausgänge; Regeln ohne Oberfläche oder globale Welt ausführbar.
- `rates.py`: vorgemerkter Modell-Leitzins, variable Referenz mit Verzögerung, neue Kreditangebote und Zinsverlauf.
- `treasury.py`: begrenzte Staatskredite, Zwischenfinanzierung, Anfangsschuld-Zinsen, Überschusstilgung und Staatskassen-/Schuldenverlauf.
- `foreign.py`: begrenzte Auslandsbestellungen aus vorhandenem Anfangsguthaben, Liefernachweise und Außenhandelsabgleich.
- `firms.py`: reine Absatz-, Produktions-, Personal- und Pufferplanung, unabhängig von Scheduler und Oberfläche.
- `banking.py`: Einbankbilanz und begrenzter Maschinenkredit mit einzeln nachvollziehbaren Buchungen.
- `world.py`: Konten, Lager, Gegenparteien, Journal, globale Zeit und native BPTK-Systemagenten. Centgenaue Buchungen sind die maßgebliche Quelle für die Grafik.
- `server.py`: begrenzte lokale JSON-Schnittstelle; Revisionen verhindern doppelte Ausführung desselben Schritts.
- `src/App.tsx`, `src/world-schema.ts`: gemeinsame laufende Welt mit Systemnavigation und Prüfung der Antworten.
- `test_world.py`: Rechen-, System- und Schnittstellentests. `engine.py`, `test_engine.py` und `src/HouseholdApp.tsx` erhalten POC 01.

Alle Beträge, Kaufbudgets und Verhaltensschwellen sind eigene illustrative Szenarioannahmen. Unternehmen führen eine vereinfachte Kosten-/Ergebnisrechnung; sie ersetzt keine vollständige handelsrechtliche Gewinnrechnung. Vereinfachte Abrechnungskonten sind keine vollständigen Zentralbank-/Bankeinlagenbilanzen. Ein begrenzter Maschinenkredit mit Geldschöpfung, Zinsen und Tilgung ist integriert. Ein Staatskredit bis 50.000 € mit anfänglich 3 % Jahreszins finanziert Kassenfehlbeträge; Überschüsse tilgen Schuld. Ein allgemeiner Kreditmarkt, staatliche Anleihefinanzierung, Interbankverkehr, Wertberichtigungen, Inflation, Abschreibung, Wertpapiermärkte oder LLM-Entscheidungen sind nicht enthalten. Staat und Ausland sind bewusst begrenzt; ein dauerhaftes Gleichgewicht wird nicht zugesichert. Kontenkonsistenz ist kein Nachweis empirischer oder pädagogischer Gültigkeit.

Die Oberfläche folgt einer internen Gestaltungsreferenz. Private Produktquellen, Designpakete oder Fontdateien wurden nicht kopiert. Die verwendeten IBM-Plex-Sans-Dateien stammen aus dem öffentlichen Paket `@fontsource/ibm-plex-sans`; dessen Font-Lizenz liegt im Paket. Lucide-Symbole und weitere Abhängigkeiten behalten ihre jeweiligen Lizenzen.


## Weiterentwicklung der sichtbaren Vorschau

Inkompatible Modell-/Antwortformatänderungen zunächst getrennt vorbereiten und Kern und Oberfläche gemeinsam prüfen. Erst danach die sichtbare Vorschau umstellen. Die Oberfläche prüft die Modellversion ausdrücklich; bei Abweichungen erscheint eine kurze Meldung und der letzte bestätigte Zustand bleibt erhalten. Ein neuer Modellstand erfordert einen neuen Lauf. Technische Schemafehler gehören nicht in die Bedienoberfläche.

### Staatsreserve und Belastungsgrenzen

Unter **Staat → Details öffnen** stehen Kasse, Liquiditätsziel, Schuld und Kasse abzüglich Bankschuld nebeneinander. Die Monatsauswahl synchronisiert vier Finanzverläufe mit der tatsächlichen Abschlussentscheidung. Anfangs beträgt das Ziel einen Monat geplanter Ausgaben einschließlich neuer Zinsen, also 7.200 €. Guthaben oberhalb des Ziels finanziert Defizite; Kredit füllt nur eine Ziellücke auf. Tilgung darf das Ziel nicht unterschreiten. Ein verfehltes Ziel ist keine tatsächliche offene Rechnung: Lohnansprüche und Zinsrückstände stehen gesondert. [Regeln und Grenzen](FISCAL_MODEL.md), [V9-Audit](../qa/fiscal-policy-v9-plausibility.md).

Die frühen Monate sind eine Einlaufphase ohne eingeregeltes Gleichgewicht. Ein Knick im Konsum kann aus Startlager, Personalregel und gemeinsamen Ausschüttungen entstehen. Für äußere Schocks ist ein unveränderter Basislauf zum gleichen Zeitpunkt als Vergleich erforderlich. Spätere Stillstände werden als Ergebnisse der gewählten Regeln untersucht; sie werden nicht durch einen künstlichen Monatsstopp verdeckt.

### Arbeitszeit und Betriebsentscheidung

**Unternehmen → Betrieb** zeigt aktuellen und geplanten Zustand, Arbeitszeitanteil, Lohn, benötigte Liquidität, Verlusttoleranz und konkrete Prüfbedingungen. Änderungen gelten ab Folgemonat. Die Zeitkurve trennt aktuelle Quote und Folgeplan. Stilllegung löscht weder Anlagen noch Schulden; ein Wiederanlauf benötigt zwei tragfähige Prüfungen und einen finanzierten Start mit einer freien Arbeitskraft. [Betriebsregeln](BUSINESS_MODEL.md), [unabhängiger V10-Audit](../qa/company-v10-plausibility.md). Reduzierte Arbeit erhält im bestehenden Sozialmodell keine staatliche Aufstockung.

## Gegenlauf mit kleineren Gütereinheiten

Der [600-Monats-Vergleich zur Güterstückelung](../qa/goods-granularity-comparison.md) verwendet 100 Teile je bisheriger Einheit und dieselben Steuer- und Verhaltensregeln. [Umrechnung, Systemgrenze und Prüfungen](GOODS_GRANULARITY_EXPERIMENT.md). Die normale Oberfläche startet weiterhin mit den bisherigen Einheiten; der Gegenlauf ist als reproduzierbares Forschungsexperiment verfügbar.
