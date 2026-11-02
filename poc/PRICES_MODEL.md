# Preise, Warenmengen und Kaufkraft · Modell v8

Diese Erweiterung zeigt eine begrenzte Übertragung von Energiekosten auf Preise, Warenkäufe und betriebliche Entscheidungen. Alle Parameter sind eigene illustrative Modellannahmen. Sie sind nicht empirisch kalibriert. Der Index ist kein Verbraucherpreisindex einer realen Volkswirtschaft.

## Systemgrenze

Elf Akteure, zwei Warenarten und 24 Monate bleiben erhalten. Nominallöhne, Transfers, Steuersätze, nominaler Grundbedarfsplan und nominale öffentliche Beschaffungsbudgets bleiben fest. Keine Lohnverhandlung, allgemeine Inflationserwartung, Geldmengen-Preisgleichung, Nachfragepreisbildung, Gütersubstitution, Wechselkurse oder vollständige Zentralbank. Es gibt keine vorprogrammierten Entlassungen infolge des Energieschocks.

## Energie und Preisregel

Startpreise: Alltag 100 €, Werkstatt 150 € je Einheit. Energie kostet je produzierter Einheit anfangs 5 € beziehungsweise 9 €. Das Energieereignis verdoppelt diese Kosten ab dem folgenden Monatsbeginn.

Zu jedem Monatsbeginn wird einmal ein Zielpreis berechnet:

`Zielpreis = Startpreis + 50 % × (Energiekosten je Einheit im Vormonat − Energiekosten je Einheit am Start)`.

Der tatsächliche Stückpreis nähert sich dem Zielpreis an. Die absolute Änderung ist auf abgerundete 1 % des bisherigen Stückpreises pro Monat begrenzt. Preise werden in ganzen Cents geführt; derselbe Monatsbeginn kann die Anpassung nicht mehrfach auslösen. Die Referenz der Preisregel wird erst danach auf die Energiekosten des neuen Monats gesetzt. Folglich wirkt ein Energieereignis in Monat 3 sofort auf Produktionskosten, frühestens in Monat 4 auf Verkaufspreise.

Beispiel bei dauerhaft doppelten Energiekosten ab Monat 3:

| Monat | Alltag | Werkstatt |
|---|---:|---:|
| 3 | 100,00 € | 150,00 € |
| 4 | 101,00 € | 151,50 € |
| 5 | 102,01 € | 153,01 € |
| ab 6 | 102,50 € | 154,50 € |

Nur zusätzliche Energie-Stückkosten werden teilweise weitergegeben; weder die gesamten Energiekosten noch der gesamte Verkaufspreis werden verdoppelt. Nicht weitergegebene Mehrkosten belasten zunächst die Marge. Lagerware bleibt zu ihren historischen Herstellungskosten bewertet. Eine Preisänderung erzeugt weder Geld noch einen Bewertungsgewinn im Lager.

## Reihenfolge und Gegenbuchungen

Beim Monatsbeginn werden Leitzins- und Energie-/Konsumereignisse angewandt, danach die Preise festgesetzt und anschließend Auslandsbestellungen mit diesen Preisen geplant. Produktion, Löhne und weitere Phasen folgen unverändert. Innerhalb eines Monats bleibt jeder Stückpreis fest. Haushalt, öffentliche Beschaffung und Ausland bezahlen tatsächlich gelieferte ganze Einheiten zum Monatsstückpreis.

Die Haushaltsbudgets bleiben nominal. Höhere Preise können bei gleichem Budget weniger Einheiten erlauben. Die Budgetaufteilung 55 % Alltag und 45 % Werkstatt bleibt fest; Restbeträge werden nicht automatisch umgeschichtet. Fehlende Ware und fehlendes Geld werden weiterhin getrennt ausgewiesen.

Automatisch aus Betriebsmitteln gekaufte Anlagen kosten acht aktuelle Werkstatteinheiten. Beim Maschinenkredit wird ebenfalls der Preis von acht Einheiten erst bei tatsächlicher Kreditgutschrift fest gebunden; eine Anfrage fixiert weder Preis noch Zins. Reservierte Lieferungen verwenden auch bei Verzögerung den gebundenen Vertragspreis. Kredit, Lieferantenzahlung und historische Anschaffungskosten stimmen überein. Die Monats-Tilgungsrate ist der auf ganze Cents aufgerundete Kreditbetrag geteilt durch zwölf; die letzte Rate wird auf die Restschuld begrenzt. Rückstände können den ursprünglichen Kreditbetrag nicht überschreiten. Frühere Festzinsen werden durch Preisänderungen nicht verändert.

## Messgrößen

- Der feste Referenzwarenkorb enthält 33 Alltags- und 18 Werkstatteinheiten. Anfangskosten: 6.000 €, entsprechend 55/45-Ausgabenanteilen.
- Modellpreisindex: `heutige Kosten dieses Warenkorbs / Anfangskosten × 100`.
- Kaufkraftindex eines unveränderten Geldbetrags: `Anfangskosten / heutige Kosten × 100`.
- Kaufkraft von nominal 1.000 €: `1.000 € × Anfangskosten / heutige Kosten`, als Warenwert zu Startpreisen. Sie berücksichtigt keine Lagerengpässe und ist kein tatsächlich garantiert kaufbarer Warenkorb.
- Tatsächliche Warenkäufe zu Startpreisen: `Summe gelieferte Einheiten je Warenart × deren Startpreis`. Diese Größe entfernt die Preisänderung aus dem Warenwert und erhält die tatsächlich veränderte Warenzusammensetzung.
- Geplante Waren zu Startpreisen: ganze Einheiten des ursprünglichen Wunschbudgets bei den damaligen Stückpreisen, bewertet zu Startpreisen. Das nominale Wunschbudget bleibt separat sichtbar.

Indexstände werden in Basispunkten abgerundet gespeichert. Euro-Kaufkraft wird direkt aus den exakten Warenkorbkosten berechnet; sie verwendet nicht den bereits abgerundeten Index.

## Produktion und Beschäftigung

Höhere Stückpreise verändern die mit nominalen Kaufbudgets finanzierbaren Einheiten. Die vorhandene Absatzglättung übernimmt Verkäufe und finanzierbare unbediente Einheiten; daraus folgen Produktionsplanung und verzögerte Personalprüfung. Höhere Energie-Stückkosten und Verkaufserlöse beeinflussen außerdem die finanzierbaren Stellen und den Betriebspuffer. Personal kann unverändert bleiben oder sich mit Verzögerung verändern. Preisweitergabe stabilisiert nicht zwangsläufig die Beschäftigung: Sie kann Margen entlasten und gleichzeitig Mengenabsatz begrenzen.

Ein Einzelverlauf zeigt die zeitliche Abfolge. Um einen isolierten Effekt zu prüfen, werden gleiche Ausgangsbedingungen und Eingriffszeitpunkte mit Basis- beziehungsweise Kontrollläufen verglichen. Ein Stellenabbau, der schon im Basislauf vorkommt, ist kein eigenständiger Nachweis eines Schockeffekts.

## Darstellung und Export

Die gemeinsame Monatsauswahl unter **Konsum nach Haushalt** steuert Energiekosten, Preise, Kaufkraft, Produktion, Verkäufe und betriebliche Beschäftigung sowie die sechs Haushaltsdiagramme. Die Haushaltskurven können nominale Ausgaben oder Warenmengen zu Startpreisen zeigen. Tatsächlich gekaufte Stückzahlen und damalige Einzelpreise stehen zusätzlich als Beträge in jeder Haushaltskarte. Preisänderungen erhalten Ereignismarkierungen.

Betriebsdetails zeigen aktuellen Stückpreis, Zielpreis und die Energiekostenreferenz. Markt- und Haushaltswerte werden beim Monatsabschluss unveränderlich gespeichert und mit dem vollständigen Lauf exportiert. V7-Läufe benötigen einen Neustart; Oberfläche und Rechenkern erwarten `illustrative_circular_flow_v8`.

Prüfung: [unabhängiger V8-Plausibilitätsbericht](../qa/prices-v8-plausibility.md). Frühere Audits bleiben Belege der jeweiligen früheren Modellfassungen.
