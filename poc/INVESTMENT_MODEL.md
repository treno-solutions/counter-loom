# Wirtschaftlichkeitsprüfung von Maschinen · v20

Stand: 3. November 2026. Neue Investitionsvariante des bestehenden Maschinenfalls: Alltag & Versorgung als Käufer, Werkstatt & Technik als Lieferant. Die Grundregeln für Produktion, Bankgewinn, Steuern, Löhne, Staat und Aussenhandel bleiben erhalten. Alle Parameter und Erwartungen sind illustrative Modellannahmen. [Vergleichsplan](../qa/investment-v20-plan.md).

## Erwarteter Nutzen und Bewertung

Die Investitionsphase vergleicht für denselben geglätteten Absatz zwei einfache Betriebsbilder: vorhandene Kapazität und eine zusätzliche Maschine. Die Maschine liefert wie bisher vier ursprüngliche Wareneinheiten Vollzeitkapazität. Bei gleichem Personal kann sie zusätzliche Verkäufe oder weniger notwendige Arbeitszeit ermöglichen. Die Rechnung verwendet die bestehende Untergrenze von 25 % Arbeitszeit sowie aktuelle Preise und Energiekosten.

Monatlicher Mehrertrag vor Steuer = zusätzliche Verkäufe + eingesparte Löhne − zusätzliche Energie.

Von positivem Mehrertrag werden 20 % marginale Gewinnsteuer abgezogen. Bestehende Schulden und ihre Kosten verändern sich zwischen den beiden Betriebsbildern nicht; zusätzliche Finanzierungskosten werden separat bewertet. Diese eingefrorene Rechnung ersetzt weder die tatsächliche Personalplanung noch die spätere Erfolgsrechnung. Insbesondere muss sich eine prognostizierte Stundenersparnis im dynamischen Verlauf nicht genau erfüllen.

Bewertet werden 24 operative Monate, ohne Restwert und ohne Preis-/Absatzwachstum. Der Zeitraum beendet keine Maschine: Anlagen werden weiterhin nicht abgeschrieben oder automatisch ersetzt. Ist die Ware bereits lieferbar, beginnt der erwartete Ertragsstrom im Folgemonat; sonst wird ein weiterer Monat Wartezeit angenommen. Die tatsächliche Lieferung bleibt von Produktion und Reservierung abhängig und kann später erfolgen.

Der monatliche Diskontfaktor ist 1 + jährlicher Bewertungszins in Basispunkten / 120000. Die Rechnung verwendet Dezimalarithmetik mit 40 Stellen und rundet erst veröffentlichte Kapitalwerte auf ganze Cent. Für die Grafik liefert der Rechenkern die bereits berechneten kumulierten Barwertpunkte.

## Eigenmittel und Kredit getrennt

**Eigenmittel:** Der Kaufbetrag gilt ab der Auftragsentscheidung wirtschaftlich als gebunden. Kapitalwert = negativer Kaufbetrag plus Barwert der erwarteten Nachsteuer-Mehrerträge. Bewertungszins ist der aktuelle Modell-Leitzins als interne Renditeanforderung. Das ist eine bewusst gesetzte Annahme, keine empirisch geschätzte Eigenkapitalrendite und keine im Modell tatsächlich gezahlte Guthabenverzinsung. Die reale Zahlung erfolgt erst bei vollständiger Lieferung.

**Kredit:** Der bestehende Maschinenvertrag bleibt auf einen Kredit je Welt begrenzt. Kreditgutschrift und Kauf gleichen sich anfangs aus. Danach werden Nachsteuer-Mehrerträge abzüglich voller Tilgung und Zinsen bewertet. Zinsen werden nur soweit steuerlich entlastet, wie positiver marginaler Projektgewinn vorhanden ist; bestehende andere Firmengewinne werden für diesen konservativen Steuerentlastungstest nicht hinzugerechnet. Der Diskontierungszins bleibt dieselbe interne Renditeanforderung. Der angebotene Kreditzins ist Leitzins plus vier Prozentpunkte und wird erst bei Gutschrift gebunden; zwölf Tilgungsraten mit begrenzter Schlussrate bleiben erhalten.

Maschinenpreis und Tilgung werden nicht gleichzeitig als zwei Investitionsausgaben abgezogen. Tilgung ist keine steuerliche Betriebsausgabe. Der Kapitalwert eines kreditfinanzierten Projekts ist der erwartete Nettovermögensvorteil nach Schuldendienst, kein anfängliches Kontoguthaben.

## Vom Vorschlag zum Kauf

1. Bestehender Auftrag, Schliessung, fehlendes Personal, nicht regulär aktiver Betrieb, fehlende Nachfrage oder die dreimonatige Kaufpause sperren eine neue Investition.
2. Positiver Eigenmittel-Kapitalwert und Geld für Betriebspuffer plus Kaufbetrag erlauben einen Produktionsauftrag. Ein Lieferengpass ist in dieser Variante nicht erforderlich: Eine reine Arbeitszeitersparnis kann ebenfalls wirtschaftlich sein.
3. Fehlt nur Geld für den vollen Eigenmittelkauf, darf die Firma den bestehenden Maschinenkredit anfragen. Kredit-Kapitalwert muss positiv sein; zusätzlich zur laufenden Betriebsreserve muss Geld für den ersten zusätzlichen Schuldendienst vorhanden sein.
4. Eine Anfrage ist keine Zusage oder Gutschrift. Die Bank prüft Wirtschaftlichkeit und Puffer erneut, ferner eigenes Kapital, Beschäftigte und vorhandene lieferbare Ware. Ein zwischenzeitlich unwirtschaftliches Projekt erhält keinen Kredit.
5. Eigenfinanzierter Kaufbetrag bleibt während des Auftrags auf dem Käuferkonto gebunden. Fehlende Maschinenteile gehen in die Lieferantenproduktion ein. Erst vollständige Lieferung gegen Zahlung erhöht den Anlagenbestand; zusätzliche Kapazität wirkt im nächsten Produktionsmonat.
6. Auch ein kreditfinanzierter Kauf startet die dreimonatige Kaufpause. Keine doppelte Reservierung oder parallele Kredit-/Eigenmittelbestellung.

Vorschlag, Wirtschaftlichkeit, Finanzierung und tatsächliche Buchung bleiben getrennte Zustände. Die Bewertung selbst erzeugt kein Geld, keine Ware und kein Einkommen. Der Kreditweg ist eine begrenzte Erweiterung des bereits vorhandenen Vertrags, keine allgemeine Firmenfinanzierung oder Bonitätsmodellierung.

## Ansicht und Schnittstelle

Der laufende Referenzaufruf World.stable() verwendet investment_policy='valuation'. Die alte Auftragsregel bleibt mit orders, die frühere Spotregel mit spot explizit verfügbar. Neue Oberflächenläufe verwenden die neue Referenz; alte Archive werden nicht geändert. Schnittstellenkennung: illustrative_circular_flow_v20. Nach Rechenkernwechsel sind Neuladen und ein neuer Lauf erforderlich.

Die Unternehmensansicht zeigt im bestehenden Maschinenauftrag:

- Erwartete Mehrverkäufe, Arbeitszeitersparnis und zusätzliche Energie.
- Nachsteuer-Mehrertrag und Bewertungs-/Kreditzins.
- Kapitalwertkurven für Eigenmittel und Kredit als Erwartungsrechnung, ausdrücklich keine Kontostände.
- Erforderlichen Betriebspuffer, Kaufbetrag, aktuelles Guthaben und konkreten Entscheidungsgrund.
- Die tatsächliche Auftragsfinanzierung, Produktion, Reservierung, Lieferung und Zahlung getrennt darunter.

capital_orders.assessment enthält die letzte Investitionsprüfung. assessment_history enthält die letzten 36 Prüfmonate. Die Erwartungswerte sind an den damaligen Entscheidungsmonat gebunden und werden nicht rückwirkend durch spätere Informationen ersetzt. Die Erwartung kennt die spätere Rücknahme eines von aussen gesetzten Zinsschocks nicht. Die Offlineversuche speichern alle 60 beobachteten Prüfungen und die vollständigen neuen Zahlungsbelege.

## Prüfungen und wirtschaftliche Grenzen

[Gezielte Tests](test_investment.py) prüfen Abzinsung, Vorzeichenwechsel bei unverändertem Projekt, Zins-/Tilgungsabgrenzung, Energie, Lieferzeit, fehlende Nachfrage oder Beschäftigte, Cashbindung, Kreditanfrage, reale Gutschrift und Lieferung sowie die Kaufpause. Ein [UI-Vertragstest](scripts/check_investment_contract.mts) prüft tatsächliche niedrige/hohe Zinsszenarien und weist beschädigte Werte zurück.

Der gezielt gesuchte Grenzfall demonstriert den Mechanismus, bestimmt aber keinen durchschnittlichen geldpolitischen Multiplikator. Investitionen sind hier häufig Automatisierung bei gegebener Nachfrage. Weniger Investitionen können zunächst Löhne höher halten und Werkstattware für Haushaltskäufe freigeben. Eine ausbleibende oder positive Konsumwirkung ist deshalb kein Grund, die Regeln nachträglich auf einen Rückgang einzustellen. Neue Märkte, Demografie, Lohnverhandlung, technologische Alterung und autonome Nachfrageexpansion sind weiterhin nicht enthalten.

[Ergebnisse des erneuten Zinsschocks](../qa/investment-v20-report.md).
