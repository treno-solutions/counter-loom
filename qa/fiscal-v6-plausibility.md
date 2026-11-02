# Unabhängige Plausibilitätsprüfung: Staatsfinanzierung V6

Prüfdatum: 2026-11-02. Quelle ist der Kern mit den sechs SHA-256-Prüfsummen in der zugehörigen JSON-Datei. Parameter und Verhaltensregeln sind illustrative Modellannahmen, keine Kalibrierung realer Staatsfinanzierung.

## Urteil und Umfang

**Bestanden: Geld-, Bank-, Kreditvertrags-, Staatskassen-, Waren-, Bewertungs- und Firmen-Eigenkapitalbrücken in den geprüften Fällen.** Acht frische Welten durchliefen jeweils 24 Monate: 192 Weltmonate, 960 Phasen und 9.560 unabhängig rekonstruierte Buchungen. Elf isolierte Staatsfinanzierungsfälle ergänzen den Lauf. Kein Kernfehler wurde gefunden.

Die Vergleichsbasis ohne Staatskredit reproduziert sämtliche 24 archivierten V5-Basismonatsdatensätze exakt. Der neue Staatskredit ist eine zusätzliche Finanzierung mit Gegenforderung und Schuld. Er ist keine laufende Steuereinnahme. Der kurzfristige Erhalt einer Kassenreserve und die Verlagerung eines Teils der Zahlungen auf einen Kreditpfad sind innerhalb der Regeln nachvollziehbar. Daraus folgen keine Aussagen über fiskalische Tragfähigkeit oder langfristige Stabilität. Oberfläche und Unterrichtswirkung wurden hier nicht geprüft.

## Unabhängige Rekonstruktion

Aus Anfangsbeständen und Journalbuchungen wurden alle Akteurskonten erneut berechnet. Jede Quelle und jedes Ziel, Kontostände vor/nach Buchung sowie Einlagen-, Kredit- und Eigenkapitaländerungen werden überprüft. Staats- und Maschinenkredite schaffen gleichzeitig Einlagen und Bankforderungen; Tilgungen vermindern beide. Bankeigenkapital wird bei Kreditgutschrift und Tilgung nicht ausgezahlt beziehungsweise vereinnahmt. Staatsschuld und ausgewiesene Bankforderung stimmen überein; Bankaktiva ergeben sich aus festen Reserven, Bestands-Unternehmenskrediten, Maschinenkredit und Staatskredit.

Die bisherigen unabhängigen Kontrollen bleiben enthalten: Mengen-/Lagerwertbrücken aus bezahlter Produktion und tatsächlichen Lieferungen; Wareneinsatz und GuV; Steuern, Ausschüttungen und einbehaltener Gewinn; Firmen-Eigenkapital aus Vermögen minus Verpflichtungen; eindeutiger Exportlieferbeleg je Zahlung; ausländische Anfangsbudgetgrenze und Teilbudgets; inländische Einlagenbrücke einschließlich aller Kreditgutschriften/Tilgungen und tatsächlicher Bankerträge/-ausschüttungen.

Für jeden Monat werden Steuereinnahmen, tatsächlich bezahlte Primärausgaben, Zinsen, Kreditaufnahme und Tilgung aus dem Journal getrennt berechnet. Geprüft werden:

- Schlusskasse = Anfangskasse + Steuern + Kredit − bezahlte Primärausgaben − bezahlte Zinsen − Tilgung.
- Schlussschuld = Anfangsschuld + Kredit − Tilgung, zu keinem Buchungszeitpunkt über dem Kreditlimit oder unter null.
- Neue Zinsansprüche = Anfangsschuld × 300 / 120.000, auf Cent abgerundet. Neu aufgenommener Kredit wird erst im Folgemonat verzinst.
- Schlusszinsrückstand = Anfangsrückstand + neue Ansprüche − tatsächlich bezahlte Zinsen. Offene Zinsen werden weder doppelt berechnet noch ohne Zahlung als Bankertrag ausgeschüttet.
- Zwischenkredite werden beim Abschluss angerechnet; der verbleibende Kassenfehlbetrag wird nicht doppelt finanziert. Nicht kreditfinanzierte bezahlte Fehlbeträge verbrauchen Kassenreserve.
- Die tatsächlich vereinnahmten Monatszinsen aller Kreditarten entsprechen der Ausschüttung an die sechs Haushaltseigentümer; das Bankkapital beträgt am Monatsabschluss wieder 10.000 €.

Die im Monatsabschluss gespeicherten Staatsfinanzierungswerte werden vollständig mit den neu berechneten Werten verglichen. Wiederholter Zinsdienst und Abschluss nach geschlossenem Monat verändern den Zustand nicht. Eingebaute Kernprüfungen werden zusätzlich aufgerufen, ersetzen aber diese Rekonstruktion nicht.

## Acht vollständige Läufe

Schocks gelten ab Monat 3; die Nachfrageerholung ab Monat 13. Der Maschinenkredit wird vor Monat 1 angefragt. Das Standardlimit beträgt 50.000 €, der niedrige Grenzfall 100 €. Alle Läufe haben dieselben sonstigen Anfangsbedingungen.

| Lauf | Buchungen | Staatsschuld Ende € | Staatszinsen gesamt € | Staatskasse Ende € | Konsum Monat 24 € | Arbeitsverhältnisse Monat 24 |
|---|---:|---:|---:|---:|---:|---:|
| Basis ohne Staatskredit | 1.229 | 0 | 0 | 20.058,22 | 9.900 | 6 |
| Basis | 1.272 | 50.000 | 1.791,99 | 68.266,23 | 9.900 | 6 |
| Energie | 1.254 | 50.000 | 2.001,21 | 59.830,36 | 9.900 | 6 |
| Nachfrage | 1.131 | 50.000 | 2.138,13 | 23.890,07 | 5.300 | 5 |
| Beide Schocks | 1.082 | 50.000 | 2.143,46 | 7.355,17 | 4.200 | 4 |
| Nachfrage mit Erholung | 1.163 | 50.000 | 2.138,13 | 38.803,60 | 9.900 | 6 |
| Maschinenkredit | 1.316 | 50.000 | 1.620,83 | 72.294,24 | 9.900 | 6 |
| Nachfrage, Kreditlimit 100 € | 1.113 | 0 | 5,12 | 170,13 | 5.900 | 4 |

Alle acht vollständigen Läufe enden ohne Staatszinsrückstand. Das Standardlimit bindet erstmals in Monat 20 der Basis, Monat 17 bei Energie, Monat 12 bei Nachfrage/beiden Schocks/Erholung und Monat 21 beim Maschinenkredit. Danach bleibt die Kasse endlich und nimmt bei weiteren nicht kreditfinanzierten Fehlbeträgen ab. In der Kombination beider Schocks liegt sie Ende Monat 24 nur noch bei 7.355,17 €; dies ist kein dauerhaftes Gleichgewicht.

In Monat 1 der Standardbasis betragen die bezahlten Primärausgaben 7.200 €, tatsächliche Steuern 4.786,40 € und der Kassenfehlbetrag 2.413,60 €. Genau dieser Betrag wird als Kredit gebucht; die Staatskasse bleibt 80.000 €, die Schuld steigt auf 2.413,60 €. In Monat 2 entstehen daraus 6,03 € Zinsen. Sie fließen als zusätzliche Ausschüttung an die Bankeigentümer. Der Monatsfehlbetrag einschließlich dieser Zinsen beträgt 2.613,37 € und wird zusätzlich finanziert; die Schuld erreicht 5.026,97 €. Die Zinsen werden weder auf den höheren Monatsendbestand zurückgerechnet noch zweimal berechnet.

Der niedrige Grenzfall erreicht mehrfach sein Limit und tilgt zwischenzeitlich. Kumuliert werden 350,10 € aufgenommen und 350,10 € getilgt; der ausstehende Bestand überschreitet trotzdem nie 100 €. Eine Kreditobergrenze begrenzt hier den gleichzeitigen Bestand, nicht die Summe aller historischen Kreditgutschriften. Ende Monat 24 bleiben 170,13 € Staatskasse; das niedrigste Monatsendguthaben beträgt 86,22 €.

Mehr Kredit bedeutet in diesem Parametersatz keinen monoton höheren Endkonsum. Beispielsweise endet der Nachfragelauf mit Standardlimit bei 5.300 € Konsum, der Grenzfall mit 100-€-Limit bei 5.900 €. Die Pfade enthalten unterschiedliche Zinsausschüttungen, Personal-, Produktions-, Beschaffungs- und Lagerentwicklungen. Diese Rückkopplungen sind buchhalterisch nachgerechnet; daraus darf ohne gezielte weitere Vergleichsbedingungen keine allgemeine Aussage über reale Fiskalpolitik abgeleitet werden.

## Elf isolierte Fälle

Explizite interne Umbuchungen, manuell gesetzte Testmonate und in zwei Fällen gesetzte Warenbestände sind Testvoraussetzungen. Sie sind keine zusätzlichen gesamtwirtschaftlichen Szenarien und schaffen kein Geld außerhalb des protokollierten Kredits.

| Fall | Geprüftes Ergebnis |
|---|---|
| Zinsbasis und wiederholter Aufruf | 1.000 € neuer Kredit im ersten Monat unverzinst; im Folgemonat 2,50 €; nach vollständiger Tilgung im nächsten Monat keine neuen Zinsen |
| Zwischenkredit bei anfangs leerer Staatskasse | Zunächst 4.800 € für öffentliche Löhne; nach Steuern/Abschluss netto genau 2.413,60 € Schuld, keine doppelte Finanzierung |
| Überschuss nach Kreditaufnahme | Tilgung auf vorhandene Schuld begrenzt; Restüberschuss bleibt Kasse; keine Erhöhung des Bankkapitals durch Tilgung |
| Bindendes Limit und unbezahlte Zinsen | Zweimal je 2,50 € entstehen als insgesamt 5 € Rückstand; kein zusätzlicher Zins auf Rückstände, kein Doppelanspruch |
| Späte Steuer bei Zinsrückstand | Von 100 € Steuer zuerst 2,50 € Zinsen, dann 97,50 € Tilgung; Restschuld 902,50 € |
| Beschaffung ohne Ware | Kein Kauf und keine Beschaffungskreditgutschrift |
| Teilweise reservierte Ware | Nur zwei frei lieferbare Güter werden kreditfinanziert gekauft; drei reservierte Einheiten bleiben geschützt |
| Beschaffung am Kreditlimit | Bei 100 € Kreditspielraum nur ein Gut bezahlt/geliefert; kein negativer Kassenbestand |
| Keine Kasse und kein Kredit | 4.800 € öffentliche Löhne bleiben als Verpflichtung sichtbar; kein fingierter Geldfluss |
| Bankkapital null | Neue Staatskreditgutschrift wird blockiert |
| Staatszinsen und Haushaltseigentümer | Monat 2: 6,03 € Staatszins plus 40 € übrige Zinsen = 46,03 € tatsächliche Bankeinnahmen und exakt 46,03 € Ausschüttung |

Auch diese Fälle rekonstruieren ihre vollständigen Journale und Bankgegenbuchungen unabhängig. Rückstände sind sichtbare offene Ansprüche; sie sind keine bereits bezahlten Staatsausgaben. Vollständige automatisierte Abwicklung alter öffentlicher Lohnrückstände ist weiterhin nicht modelliert.

## Grenzen der Aussage

Ein Staatskredit bei einer einzelnen Geschäftsbank ist eine vereinfachte Finanzierungsform. Es gibt keinen Zentralbankmechanismus, Anleihemarkt, Risikozins, Bonitäts-/Inflationspfad oder empirisch begründetes Kreditlimit. Die Regel, Kassenfehlbeträge schon vor Verbrauch der 80.000-€-Reserve zu finanzieren, ist eine bewusste Politikannahme des Lernfalls. Das bewahrte Guthaben ist keine verbesserte Nettovermögensposition aus dem Nichts: ihm steht eine Schuld gegenüber.

Staatszinsen erhöhen hier das verfügbare Einkommen der sechs gleichgewichteten Bankeigentümer. Das ist eine Verteilungsannahme; daraus entstehende Konsum-/Lager-/Personalpfade sind nicht gesellschaftlich repräsentativ. Offene Zinsansprüche sind separat ausgewiesen; die Bankbilanz vereinnahmt Bankertrag erst bei Zahlung. Das Modell ist kein vollständiges Rechnungslegungssystem für notleidende Kredite.

Die geprüfte Laufzeit bleibt 24 Monate. Richtig verbuchte Bestände und begrenzte Kredite beweisen weder Schuldentragfähigkeit noch makroökonomische Stabilität. Vor weitergehenden Aussagen wären konkrete Lernfragen, Sensitivität gegenüber den ausdrücklich gewählten Regeln sowie externe Kalibrierung nötig. Frühere V3-/V4-/V5-Berichte und ihre Modellgrenzen bleiben bestehen.

## Reproduzierbarkeit

[fiscal-v6-plausibility.json](fiscal-v6-plausibility.json) enthält Szenarioparameter, alle Monatswerte, elf isolierte Fälle und sechs Kernprüfsummen. Der öffentliche Prüfer [check_fiscal_plausibility.py](../tools/check_fiscal_plausibility.py) überprüft diese Prüfsummen, führt denselben Umfang erneut aus und vergleicht die Ergebnisse exakt mit den Belegen.

Mit den installierten Python-Abhängigkeiten des POC aus dem Repository starten:

```sh
poc/.venv/bin/python tools/check_fiscal_plausibility.py
poc/.venv/bin/python tools/check_fiscal_plausibility.py --output poc/.runtime/fiscal-repeat.json
```

Standardmäßig wird kein neuer Beleg geschrieben. Existierende Ausgabedateien werden nicht überschrieben. Assertions müssen aktiviert sein; Python `-O` wird abgewiesen. Die Wiederholung bestand mit identischen Ergebnissen. Sie ist eine technische Konsistenz- und Regressionsprüfung, keine empirische oder pädagogische Validierung.
