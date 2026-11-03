# Bankbilanz · Grundlage v3, erweitert bis v8

Die aktuelle Referenz [v18](STABILITY_MODEL.md) ergänzt eigenfinanzierte Maschinenaufträge mit Produktionsplanung und reserviertem Kaufgeld. Der hier beschriebene gesondert angefragte Bankvertrag bleibt bestehen; während eines offenen eigenfinanzierten Auftrags ist eine parallele Kreditanfrage gesperrt.

Stand: 2. November 2026. Begrenzter Einbank-Test innerhalb der laufenden Welt; keine empirische Kreditvergabe- oder Regulierungsstudie. Alle Beträge und Vertragsbedingungen sind illustrative Annahmen.

## Aktueller Umfang v8

Der Maschinenvertrag und die Einlagenbrücke bleiben erhalten. Seit [V8](PRICES_MODEL.md) kostet die Maschine acht aktuelle Werkstatteinheiten; Preis und Kreditbetrag werden bei Gutschrift gebunden. Die Tilgungsrate wird aus diesem Betrag für zwölf Monate centweise aufgerundet, die Schlussrate auf die Restschuld begrenzt. Auch eine verzögerte Lieferung behält den Vertragspreis. Die folgenden Zahlen beschreiben den unveränderten Startpreisfall. Die [Leitzinsregeln v7](RATES_MODEL.md) trennen den verzögert variablen Alltagskredit, den festen Werkstattkredit sowie bei Gutschrift fest gebundene Maschinen- und Staatskreditbeträge. Die nachfolgend genannten 6 % und 39 € beschreiben den unveränderten Basisfall bei 2 % Modell-Leitzins. Seit v5 sind [Warenexporte](FOREIGN_MODEL.md) enthalten; v6 ergänzt einen [Staatskredit](FISCAL_MODEL.md) bei derselben Bank. Neue Kredit- und Tilgungssummen umfassen Maschinen- und Staatskredit. Die Bankforderung an den Staat stimmt mit dessen Schuld überein; tatsächlich bezahlte Staatszinsen fließen in Bankertrag und Haushaltsausschüttung ein. Die nachfolgenden Abschnitte erklären den ursprünglichen Maschinenfall; die dortige Grenze eines neuen Kredits pro Welt gilt nur für diesen Vertrag.

## Bilanzgrenze und Eröffnung

Alle Nichtbanken einschließlich Staat und Energie-Außenanschluss halten ihr Guthaben bei einer einzigen modellierten Bank. Die bisherigen 10.000 € des Finanzsektors werden ausdrücklich als Bankeigenkapital geführt und nicht zum Kundenguthaben addiert. Anfangsbestand an Kundeneinlagen: 146.000 €. Bestehende Kreditforderungen: 24.000 €. Vereinfachte feste Reserveposition als Eröffnungsannahme: 132.000 €. Damit gilt auf der Bankbilanz: Reserven 132.000 + Kreditforderungen 24.000 = Kundeneinlagen 146.000 + Eigenkapital 10.000. Die Summe der Kundenguthaben ist ein Modellaggregat, keine Behauptung über reale Geldmengendefinitionen M1/M3.

`cash_cents` bleibt aus Kompatibilitätsgründen der Feldname; bei Nichtbanken bezeichnet er eine Einlage, beim Bankknoten Eigenkapital. Diese Positionen sind in der Oberfläche und bei den Prüfungen getrennt. Reserven werden nicht als Kundengeld gezählt. Interbankzahlung, Bargeld, Wechselkurse und aktive Zentralbankoperationen sind nicht implementiert.

## Ein Vertrag

Alltag & Versorgung kann einen Kredit von 1.200 € für eine Maschine der Werkstatt anfragen: acht Werkstatteinheiten zu je 150 €, zusätzliche Kapazität vier Einheiten ab dem folgenden Produktionsmonat. Zinssatz 6 % jährlich auf die jeweilige Restschuld, monatlich geteilt durch zwölf. Gleichmäßige Tilgung 100 € monatlich über zwölf Fälligkeiten; erste Fälligkeit im Monat nach Lieferung. Bei pünktlicher Zahlung: erste Zinsen 6 €, letzte 0,50 €, insgesamt 39 €. Keine Gebühren oder Zinseszinsen.

Eine Anfrage ist noch keine Auszahlung. Die Investitionsphase prüft positives Bankeigenkapital, mindestens einen Beschäftigten des Kreditnehmers und acht verfügbare Lieferanteneinheiten. Die Maschine wird reserviert. Diese einfache Zulässigkeitsprüfung ist keine Bonitätsbewertung oder bankaufsichtliche Kapitalprüfung. Je Welt ist höchstens dieser eine neue Kredit möglich.

1. **Investitionsphase:** Bank bucht Kreditforderung +1.200 € und Kundeneinlage des Kreditnehmers +1.200 €. Bankeigenkapital und Reserveposition bleiben unverändert. Das neue Guthaben ist vor dem Kauf sichtbar.
2. **Abschlussphase desselben Monats, vor der Überschusssteuer:** Zahlung des Käufers an die Werkstatt. Käufereinlage −1.200 €, Lieferanteneinlage +1.200 €, Kundeneinlagen insgesamt unverändert. Lagerbestand des Lieferanten sinkt um acht Einheiten; Anlagebestand des Käufers steigt um eins. Die neue Kapazität wirkt erst im Folgemonat.
3. **Ab Folgemonat in der Lohn-/Produktionsphase:** Nach Löhnen, Energie und Zinsen der bestehenden Kredite werden zunächst fällige Maschinenzinsen und dann die fällige Tilgung bezahlt, jeweils begrenzt durch die Käufereinlage. Die bereits bestehende 2-%-Verzinsung wird nur auf die alten Kredite angewandt; der neue Kredit wird nicht doppelt verzinst.
4. **Zinsen:** Kundeneinlage sinkt, Bankeigenkapital/vereinnahmter Ertrag steigt. Die Kreditforderung bleibt durch diese Zinszahlung unverändert. Im bestehenden Abschluss verteilt die Bank ihre tatsächlich vereinnahmten Zinsen wieder an die Haushalte; dabei steigen Kundeneinlagen und sinkt Bankeigenkapital.
5. **Tilgung:** Kundeneinlage und Kreditforderung sinken um denselben Betrag. Bankeigenkapital steigt dadurch nicht. Nach vollständiger Tilgung wird kein weiterer Betrag abgebucht.

Ausstehende Zinsen und fällige, nicht bezahlte Tilgung werden getrennt am Vertrag ausgewiesen. Eine ausgefallene Zahlung gilt nicht als bezahlt und reduziert die Restschuld nicht. Nachzahlungen decken bestehende Fälligkeiten; dieselbe überfällige Rate wird nicht jeden Monat erneut als neue Schuld angelegt. Für Zinsen verwendet dieser POC eine ausdrücklich vereinfachte zahlungsbezogene Ertragsrechnung; keine Zinsabgrenzung, Abschreibung oder Wertberichtigung. Überfällige Tilgung steckt bereits in der Restschuld und wird bei Vermögensbeständen nicht doppelt gezählt.

## Nachvollziehbarkeit und Prüfung

Jede Buchung enthält Anfangs-/Endwerte der beteiligten Einlage beziehungsweise des Bankkapitals, Änderung der Kundeneinlagen, Änderung der Kreditforderungen und eine Bankbilanz vor/nach dem Vorgang. Bilanzidentität gilt nach jedem einzelnen Vorgang. Gegenüber dem Anfang gilt für Kundeneinlagen:

`Einlagen = Anfangseinlagen + neue Kredite − Tilgungen − an die Bank gezahlte Zinsen + Ausschüttungen der Bank`.

Die ältere Kontrollsumme über Kundenkonten und Bankkapital ist kein Geldmengenaggregat. Ihre Änderung entspricht neuen Krediten minus Tilgungen. Finanzierungsvorgänge und Güterlieferung bleiben im vollständigen Journal exportierbar. Alte Modellstände und Prüfergebnisse bleiben erhalten.

Geprüft werden getrennte Kreditgutschrift und Lieferung, tatsächliche Gegenparteien, keine Entnahme des Kreditbetrags aus Bankeigenkapital, 12 Fälligkeiten und 39 € Zinsen bei pünktlicher Zahlung, Geldabbau durch Tilgung, Zins-/Tilgungsunterscheidung, ausbleibende/teilweise Zahlungen und korrekte Nachzahlung, Wiederholschutz, ein begrenzter Kredit je Welt sowie unabhängige Rekonstruktion sämtlicher Konten und Bankbilanz.

## Fachliche Herkunft

- Deutsche Bundesbank, [Wie Geld entsteht](https://www.bundesbank.de/de/aufgaben/themen/wie-geld-entsteht-665288), 25. April 2017; am 2. November 2026 geprüft: Kreditvergabe kann gleichzeitig Kreditforderung und Kundeneinlage erzeugen; Geldschöpfung ist durch wirtschaftliche, regulatorische und finanzielle Bedingungen begrenzt. Die neue Einbank-Demonstration modelliert diese Grenzen nur im ausdrücklich beschriebenen Umfang.
- Bank of England, [Money creation in the modern economy](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy), 14. März 2014, und [How is money created?](https://www.bankofengland.co.uk/explainers/how-is-money-created); am 2. November 2026 geprüft: Einlagenschöpfung durch Bankkredit und Abbau bei Rückzahlung. Quellen sind Mechanismusbelege, keine Kalibrierung der gewählten 1.200 €, 6 % oder zwölf Monate.

Staatliche Anleihemärkte und Zentralbankoperationen bleiben außerhalb des Modells. Unternehmens-, Außenhandels- und Staatskreditregeln sind in ihren jeweiligen Erweiterungskonzepten dokumentiert; keine Behauptung einer vollständig realistischen Volkswirtschaft.
