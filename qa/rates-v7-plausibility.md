# Unabhängige Plausibilitätsprüfung: Leitzins und Kreditverträge V7

Prüfdatum: 2026-11-02. Geprüft wurde der durch sieben SHA-256-Prüfsummen in der JSON-Datei bezeichnete Kern. Zinssätze, Aufschläge, Vertragsformen und Verzögerung sind illustrative Modellannahmen, keine aktuellen Marktdaten oder empirisch kalibrierte Übertragungsregeln.

## Urteil und Umfang

**Bestanden: sämtliche geprüften Buchungs-, Waren-, Bewertungs-, Staatsfinanzierungs- und Zinsvertragsbrücken.** Neun frische Welten durchliefen jeweils 24 Monate: insgesamt 216 Weltmonate, 1.080 Phasen und 11.326 unabhängig rekonstruierte Buchungen. Elf isolierte Zinsfälle mit weiteren 208 Buchungen ergänzen den Umfang. Es wurde kein Kernfehler gefunden.

Die Basis mit unverändertem Modell-Leitzins reproduziert sämtliche bisherigen Monatswerte der archivierten V6-Standardbasis exakt. Neue Metadaten zu Zinsen und Staatskreditbeträgen sind dabei zusätzlich vorhanden; sie ersetzen keine früheren Belege. Die öffentliche Prüfroutine reproduziert die neuen Ergebnisse exakt gegen den bezeichneten Kern.

Diese Prüfung belegt technische Konsistenz und die Umsetzung der ausdrücklich festgelegten Vertragsregeln. Sie belegt keine realistische quantitative Zinswirkung, gesamtwirtschaftliche Stabilität oder Unterrichtswirkung. Die Browseroberfläche und der HTTP-Transport wurden hier nicht unabhängig geprüft; die Rate-Aktion des Python-Anwendungskerns wurde auf Revisions- und Eingabegrenzen geprüft.

## Unabhängige Prüfung

Alle Akteurskonten und Bankgegenbuchungen werden aus Anfangsbeständen und jedem einzelnen Journalbeleg erneut berechnet. Geprüft sind Quell-/Zielstände vor und nach Buchung, Einlagen-, Kredit- und Bankkapitaländerung sowie die gesamte Bankbilanz. Die bisherigen Brücken bleiben enthalten: bezahlte Produktion, Warenmengen und bewertete Lager, Wareneinsatz, GuV, Steueransprüche, Ausschüttungen, einbehaltener Gewinn und Firmen-Eigenkapital; ausländisches Anfangsbudget, Teilbudgets und eindeutige Exportlieferbelege; staatliche Kassen-/Schuldenbrücke, bezahlte Fehlbeträge, Zinsrückstände, Finanzierungslimit und tatsächliche Bankausschüttung an die Haushalte.

Die neuen Kontrollen verwenden die im Prüflauf vorgegebenen Zinsereignisse, nicht die ausgewiesenen Zinsbeträge als Berechnungsquelle:

- Der Leitzins wird an der vorgesehenen Monatsgrenze wirksam. Die variable 12.000-€-Altschuld verwendet den Leitzins des Vormonats, die feste 12.000-€-Altschuld durchgehend 2 %. Tatsächlich fällige Firmenzinsen und GuV werden daraus neu berechnet.
- Personalbedarf und Kassenreserve werden unabhängig mit dem bekannten Folgesatz, erwarteten Energiekosten, zwei Lohnrunden und dem nächsten Maschinen-Schuldendienst berechnet. Ein noch nicht wirksamer Folgesatz wird nicht als bereits fälliger Zins verrechnet.
- Der Maschinenzinssatz wird bei tatsächlicher Kreditgutschrift aus dem dann geltenden Leitzins plus 400 Basispunkten bestimmt. Restschuld, Zinsansprüche und Zahlungen werden aus den Buchungen und dem gebundenen Satz fortgeschrieben.
- Jede Staatskreditgutschrift erzeugt einen unabhängig rekonstruierten Kreditbetrag mit Beleg-ID, Abschlussmonat, ursprünglichem Betrag, Restschuld und festem Zins. Tilgungen werden unabhängig auf die ältesten offenen Beträge verteilt. Der rekonstruierte Bestand wird nach jeder Phase vollständig mit dem Kernbestand verglichen.
- Staatszinsen werden aus den Anfangsrestschulden und jeweiligen festen Sätzen berechnet. Erst die gesamte gewichtete Zinsforderung wird auf Cent abgerundet. Die verbleibenden Cents werden nach größten Restbruchteilen und bei Gleichstand nach Kreditbetrag-ID zugeordnet. Die vollständige monatliche Zinsbasis und ihre Summe werden verglichen.
- Alte Ansprüche bleiben unverändert, neue Gutschriften verzinsen sich erst im Folgemonat. Wiederholte Abrechnung verändert geschlossene Monate nicht. Leitzinsvorgaben selbst erzeugen keinen Geldbeleg.

## Neun vollständige Läufe

Der Modell-Leitzins startet bei 2 %. Erhöhung bedeutet 4 % ab Monat 2, Senkung 1 % ab Monat 2, Nullzins 0 % ab Monat 2. Die Umkehr senkt nach der Erhöhung ab Monat 8 auf 1 %. Energie-/Nachfrageschocks gelten ab Monat 3. Ein angegebener Maschinenmonat bezeichnet die Anfrage, nicht eine zugesicherte Gutschrift.

| Lauf | Buchungen | Staatszinsen gesamt € | Staatskasse Ende € | Konsum Monat 24 € | Arbeitsverhältnisse Monat 24 |
|---|---:|---:|---:|---:|---:|
| Unveränderte Basis | 1.272 | 1.791,99 | 68.266,23 | 9.900 | 6 |
| Erhöhung ab Monat 2 | 1.271 | 2.915,86 | 67.054,36 | 9.900 | 6 |
| Senkung ab Monat 2 | 1.272 | 1.236,45 | 68.865,77 | 9.900 | 6 |
| Erhöhung, Umkehr ab Monat 8 | 1.272 | 2.141,99 | 67.924,23 | 9.900 | 6 |
| Nullzins ab Monat 2 | 1.250 | 685,33 | 69.460,89 | 9.900 | 6 |
| Erhöhung und Energie | 1.253 | 3.258,05 | 58.485,52 | 9.900 | 6 |
| Erhöhung und Nachfrage | 1.131 | 3.475,89 | 22.496,31 | 5.300 | 5 |
| Maschinenanfrage Monat 1, danach Erhöhung | 1.316 | 2.632,18 | 71.194,89 | 9.900 | 6 |
| Erhöhung, Maschinenanfrage Monat 3 | 1.289 | 2.915,55 | 67.144,25 | 9.900 | 6 |

Alle neun Läufe schließen mit 50.000 € Staatsschuld und ohne Staatszinsrückstand. In der Erhöhung bindet das Limit erstmals in Monat 19 statt Monat 20 der Basis. Zusammen mit dem Energieschock bindet es in Monat 16, mit dem Nachfrageschock in Monat 12. Die endliche Kassenreserve bleibt nach Erreichen der Grenze Teil der Finanzierung; die Laufzeit beweist keine dauerhafte Tragfähigkeit.

Bei 4 % Leitzins ab Monat 2 beträgt der variable Altkreditzins in Monat 2 noch 2 %, ab Monat 3 dann 4 %: monatlich 20 € beziehungsweise 40 € bei unveränderter Restschuld von 12.000 €. Der feste Werkstattvertrag bleibt bei monatlich 20 €. Für neue Staatskreditbeträge gilt dagegen schon in Monat 2 der neue Satz von 5 %. Die erste bestehende Tranche von 2.413,60 € bleibt bei 3 %; Ende Monat 24 sind die übrigen 47.586,40 € zu 5 % gebunden.

Die Zinssenkung nach der Erhöhung schreibt bestehende Staatsverträge nicht um. Im Umkehrlauf bleiben Ende Monat 24 noch 18.163,37 € zu 5 % und 2.413,60 € zu 3 % gebunden; 29.423,03 € tragen den neuen Satz von 2 %. Daher liegen die kumulierten Staatszinsen dieses Laufs trotz abschließend niedrigerem Leitzins über der unveränderten Basis. Das ist ein nachvollziehbarer Vertrags- und Bestandseffekt innerhalb dieses Modells.

Die Maschine aus der Anfrage in Monat 1 wird in Monat 1 zu fest 6 % gutgeschrieben und geliefert. Sie bleibt nach der Leitzinserhöhung bei 6 %, ist am Ende getilgt und verursachte insgesamt 39 € bezahlte Zinsen. Die Anfrage in Monat 3 wartet im regulären Warenpfad bis Monat 16 auf acht freie Werkstatteinheiten. Erst dann wird der Kredit zu fest 8 % gutgeschrieben und die Maschine geliefert. Ende Monat 24 sind acht Raten bezahlt, 400 € Restschuld und 45,31 € bezahlte Zinsen vorhanden. Diese beiden Zinsbeträge vergleichen unterschiedliche Laufzeiten und Restschuldpfade; sie sind kein vollständiger Preisvergleich zweier zwölfmonatiger Verträge.

Identischer Endkonsum mehrerer Läufe bedeutet keine identischen Zahlungs-/Bestandspfade. Die Wirkung des Leitzinses ist hier auf bestimmte Kreditverträge und die daraus folgenden Einkommens-/Reserve-/Produktionspfade begrenzt. Einlagenzinsen, Vermögenspreise, Wechselkurs, allgemeine Konsumerwartungen und variable Kreditnachfrage werden nicht zusätzlich modelliert.

## Elf isolierte Vertragsfälle

Manuelle Testmonate, explizite interne Umbuchungen und im Wartefall ein gesetzter Werkstattbestand dienen als Schnittstellenvoraussetzungen. Sie sind keine zusätzlichen vollständigen Weltläufe. Auch ihre vollständigen Geldjournale und festen Kreditbestände werden unabhängig rekonstruiert.

| Fall | Geprüftes Ergebnis |
|---|---|
| Vormerkung ersetzen und zurücknehmen | 4 % durch 3 % ersetzbar, anschließend durch Wahl der geltenden 2 % aufgehoben; kein Zinsereignis wirksam und kein Geldbeleg |
| Eingabegrenzen und letzter Monat | Negative, über 10 %, boolesche, nicht ganzzahlige und fehlende Werte abgewiesen; 10 % angenommen; neue Vorgabe im letzten Monat ohne Zustandsänderung abgewiesen |
| Kern-API | Veraltete Revision und fehlendes Zinsfeld abgewiesen; erfolgreiche Vormerkung erzeugt keinen Geldfluss |
| Monatsgrenze und variable Verzögerung | Monat 2: 4 % Leitzins, aber noch 2 % variabler Vertrag und 4 % Planungssatz; Monat 3: 4 % variabler Vertrag; Werkstatt weiter 2 % |
| Wartende Maschine | Anfrage zu 6-%-Angebot bindet nichts; Gutschrift nach Erhöhung zu 8 %; spätere Senkung verändert diesen Satz nicht; erste Zinszahlung 8 € |
| Gemischte Staatsverträge und FIFO | 1.000,01 € zu 3 %, 2.000,03 € zu 5 %, 1.500 € Tilgung: erste Tranche null, zweite 1.500,04 €; nach Senkung weiter 6,25 € Monatszins |
| Gleiche Zinsen, Centaggregation | Drei Beträge zu je 2 € und 3 %: zusammen ein Cent Forderung; Gleichstand deterministisch erster Betrag; kein Verlust durch drei Einzelabrundungen |
| Unterschiedliche Zinsen, größte Restfraktion | 1,99 € zu 3 %, 1,99 € zu 5 %, 4,01 € zu 1 %: Gesamtforderung ein Cent, zugeordnet dem zweiten Betrag |
| Alte Staatszinsrückstände | Je 2,50 € neue Zinsen auf bestehenden 3-%-Vertrag trotz Erhöhung auf 10 % und Senkung auf 0 %; zusammen 5 € Rückstand ohne Doppelberechnung |
| Alte variable Zinsverpflichtung | Offene 20-€-Forderung aus Monat 1 bleibt nach Erhöhung auf 4 % unverändert |
| Abweichender anfänglicher Staatsaufschlag | Bei anfänglich 1 % Staatszins und 2 % Leitzins bleibt der negative Aufschlag erhalten; neues Angebot nach Nullzins bei null begrenzt; alter 1-%-Vertrag bleibt bestehen |

## Grenzen und nächste Erkenntnisstufe

Die drei Vertragsregeln sind Festlegungen des Lernfalls. Ein einmonatiger Übertragungsverzug, Aufschläge von null/vier/einem Prozentpunkt, eine feste Altschuld und feste neue Staatskreditbeträge sind plausible darstellbare Vertragsarten, aber hier keine repräsentative Messung realer Finanzierungsstrukturen. Marktbasierte Zinsbildung, Zentralbankbilanz, Ausfallbewertung und Refinanzierung der Bank fehlen weiterhin.

Der gewichtete ausgewiesene Staatsbestandszins ist eine gerundete Information. Die Abrechnung verwendet die einzelnen festen Beträge. Entscheidend für Erkenntnisse ist daher der Vergleich von gleichen Beträgen, Zeitpunkten und Restschuldpfaden. Eine höhere angezeigte Prozentzahl allein beschreibt keine höhere gesamte Belastung eines anderen Vertrags.

Buchungskonsistenz und korrekte Verzögerung machen die Regeln erklärbar. Ob Lernende die Übertragung verstehen, ob Annahmen das gewünschte Lernziel treffen und welche Kombinationen wirtschaftlich belastbar sind, bleibt gesondert zu prüfen. Frühere Modellgrenzen und archivierte Belege werden durch diesen Audit nicht aufgehoben.

## Wiederholung

[rates-v7-plausibility.json](rates-v7-plausibility.json) enthält die tatsächlichen Ereignisse, Monatswerte, festen Staatskreditbeträge, elf isolierte Fälle und sieben Kernprüfsummen. Der öffentliche Prüfer [check_rates_plausibility.py](../tools/check_rates_plausibility.py) prüft diese Quellen und wiederholt exakt denselben Umfang.

Aus dem Repository mit installierten POC-Python-Abhängigkeiten:

```sh
poc/.venv/bin/python tools/check_rates_plausibility.py
poc/.venv/bin/python tools/check_rates_plausibility.py --output poc/.runtime/rates-repeat.json
```

Standardmäßig schreibt er keinen neuen Beleg; bestehende Ausgabedateien werden nicht überschrieben. Python `-O` ist ausgeschlossen, weil Assertions benötigt werden. Die Wiederholung stimmt exakt mit den gespeicherten Ergebnissen überein. Technische Regression, empirische Validierung und Unterrichtsvalidierung bleiben getrennte Aussagen.
