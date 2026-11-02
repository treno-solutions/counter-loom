# Leitzins und Vertragszinsen · Modell v7

Stand: 2. November 2026. Eigene illustrative Vertrags-/Übertragungsregeln, keine Darstellung aktueller Zentralbankzinsen oder empirische Kalibrierung. Ergänzt die [Bankbilanz](BANKING_MODEL.md) und [Staatsfinanzierung](FISCAL_MODEL.md). Elf Akteure, 24 Monate, bestehende Produktions-/Kaufregeln und Kreditgrenzen bleiben erhalten. Keine zusätzliche Zentralbankbilanz, Einlagenverzinsung oder allgemeiner Kreditmarkt.

## Leitzinsvorgabe

Der Modell-Leitzins startet bei 2 %. Er kann zwischen 0 % und 10 % in Schritten ganzer Basispunkte gewählt werden. Eine Vorgabe wird erst am nächsten Monatsbeginn wirksam; bis dahin kann sie ersetzt oder durch Wahl des noch geltenden Zinses zurückgenommen werden. Im letzten Monat sind keine Änderungen für einen nicht existierenden Folgemonat zulässig. Die Zinsvorgabe ist ein Parameterereignis und keine Geldbuchung.

## Drei Vertragsregeln

- **Variabler Altvertrag:** Alltag & Versorgung, 12.000 € Anfangsschuld, zunächst 2 %, Modellaufschlag 0 Prozentpunkte. Am Monatsbeginn wird der Leitzins des Vormonats übernommen. Ein höherer Leitzins ab Monat 2 verändert daher den Vertragszins ab Monat 3. Zahlungen und Personal-/Liquiditätsplanung verwenden denselben wirksamen Vertragszins. Keine rückwirkende Neuberechnung bereits fälliger Zinsen.
- **Fester Altvertrag:** Werkstatt & Technik, 12.000 € Anfangsschuld, 2 % über den gesamten 24-Monats-Lauf. Eine Leitzinsänderung lässt diesen Vertragszins unverändert.
- **Neuverträge:** Maschinenkredit mit 4 Prozentpunkten Aufschlag, neue Staatskreditbeträge mit 1 Prozentpunkt Aufschlag. Bei 2 % Leitzins gelten damit 6 % beziehungsweise 3 %. Bei 4 % gelten für neue Abschlüsse 8 % beziehungsweise 5 %. Der maßgebliche Zeitpunkt ist die tatsächliche Kreditgutschrift, nicht die Anfrage. Eine wartende Anfrage bindet den Angebotszins nicht. Nach Gutschrift bleibt der jeweilige Vertragszins fest.

Die unterschiedlichen Vertragstypen sind eine explizite Festlegung dieses Lernfalls. Bestehende Firmenkredite werden weiterhin nicht getilgt. Der eine Maschinenkredit behält Betrag, Lieferbedingungen und zwölf Tilgungsraten. Zinsen auf unterschiedliche Restschulden sind nicht ohne Berücksichtigung des Betrags vergleichbar; Angebote zeigen deshalb Betrag und erste Monatszinsen.

## Staatskreditbeträge und Zinsbasis

Jede staatliche Kreditgutschrift bildet einen eigenen fest verzinsten Kreditbetrag mit Monat, ursprünglichem Betrag, Restschuld, Leitzins bei Abschluss und vereinbartem Jahreszins. Bestehende Beträge behalten ihren Zins, zusätzliche Beträge erhalten die neuen Konditionen. Tilgung reduziert zuerst die ältesten Beträge. Kumulierte Aufnahmen dürfen wegen Wiederverwendung nach Tilgung weiterhin die feste Bestandsgrenze übersteigen; die aktuelle Gesamtschuld darf es nicht.

Die Zinsbasis wird am Monatsbeginn pro Kreditbetrag festgehalten. Der Monatszins ist die Summe aus Anfangsrestschuld×jeweiligem Jahreszins, geteilt durch 120.000 bei Verwendung von Basispunkten. Erst die Gesamtsumme wird auf Cents abgerundet. Die Centzuordnung zu den einzelnen Beträgen erfolgt deterministisch anhand der größten Restbruchteile; ihre Summe stimmt mit der Gesamtforderung überein. Das erhält bei identischen Zinsen die bisherige V6-Abrechnung, statt je Teilbetrag Rundungsverluste zu summieren. Neue Gutschriften verzinsen sich wie bisher erst ab Folgemonat. Zinsrückstände bleiben von neuer Zinsberechnung und Tilgung getrennt.

Der angezeigte gewichtete Bestandszins ist ein auf ganze Basispunkte abgerundeter Informationswert. Die Berechnung verwendet die einzelnen Vertragszinsen, nicht diesen Anzeigewert. Bei abweichenden Startparametern des Offline-Prüflaufs wird der Staatsaufschlag aus anfänglichem Staatszins minus anfänglichem Leitzins gebildet; angebotene Zinsen werden bei null begrenzt.

## Sichtbarkeit und Prüfung

**Ereignis auslösen** enthält eine Leitzinsvorgabe. Unter **Finanzsektor → Details öffnen** zeigt eine Verzweigung den Leitzins, den verzögert angepassten variablen Vertrag, den festen Altvertrag und die Angebote für neue Kredite. Kreditbetrag, Vertragszins und monatliche Zinsforderung werden gemeinsam ausgewiesen. Ein gemeinsamer Prozentverlauf zeigt Leitzins, variablen und festen Vertragszins. Die Pfeile stellen Zinsregeln dar; tatsächliche Zahlungen stehen in den bestehenden Belegen.

Die Staatsansicht trennt Angebot für neue Beträge, gewichteten Bestandszins, einzelne fest vereinbarte Beträge und ihre Monatszinsbasis. Der Maschinenvertrag zeigt den bei Gutschrift gebundenen Zins und das aktuelle Neukreditangebot getrennt.

Fertigkriterien: unveränderte V6-Basis bei unverändertem Leitzins; Erhöhung/Senkung erst am Monatsbeginn; explizite Verzögerung des variablen Vertrags; feste Alt-/Maschinen-/Staatssätze bleiben erhalten; Preisbindung erst bei Gutschrift; richtige Zinsen aus gemischten Staatsbeträgen und FIFO-Tilgung; keine Änderung offener alter Zinsansprüche; identische Geld-/Bank-/Firmen-/Staats-/Außenhandelsbrücken und vollständiger Export. Zinsänderungen garantieren weder eine bestimmte Konsumreaktion noch eine empirisch gültige Übertragungsstärke.
