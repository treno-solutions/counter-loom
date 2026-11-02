# Unabhängige Prüfung: Preise und Kaufkraft V8

Prüfdatum: 2026-11-02. Illustrative Simulation, keine empirische Kalibrierung oder Prognose. Die acht Kernprüfsummen und vollständigen Szenarioparameter stehen in [prices-v8-plausibility.json](prices-v8-plausibility.json).

**Ergebnis:** Acht frische 24-Monatsläufe bestanden die unabhängigen Rekonstruktionen: 192 Weltmonate, 960 Phasen und 9.861 Buchungen. Vier isolierte Preis-/Maschinenfälle bestanden zusätzlich. Der zunächst bestätigte Fehler bei verzögerter Maschinenlieferung ist im finalen Kern behoben und nachgeprüft. Weitere Kernfehler wurden in diesem Umfang nicht gefunden. Oberfläche und Unterrichtswirkung wurden nicht geprüft.

## Was nachgerechnet wurde

Aus jedem Journalbeleg wurden Geldkonten, Bankeinlagen/-forderungen/-kapital, Staatskasse/-schuld/-zinsen und Auslandsflüsse unabhängig rekonstruiert. Die bisherigen Prüfungen zu festen/variablen Zinsen, Staatskreditbeträgen, FIFO-Tilgung und Centverteilung bleiben enthalten. Zusätzlich wurden geprüft:

- Preise aus **Energiekosten der Vorperiode**, 50 % der zusätzlichen Stückenergiekosten und höchstens 1 % monatlicher Preisänderung; Preisfestsetzung vor der Auslandsbudgetaufteilung.
- Jede tatsächliche Warenzahlung als Menge × gültiger Stückpreis; Produktion, Warenbestand und Lagerwert über bezahlte Produktionskosten und tatsächlichen Wareneinsatz. Eine höhere Verkaufspreisquote bewertet vorhandene Lagerware nicht neu.
- Haushaltsbudgets aus den tatsächlichen Einkommen, Steuern, Vorperiodenausschüttungen und Guthaben vor dem Kauf. Wunsch, finanzierbares Budget, bezahlte Mengen, fehlende Finanzierung, fehlende Ware und Restbeträge wegen ganzer Einheiten wurden unabhängig abgeglichen.
- Tatsächlich gekaufte Mengen zu unveränderten Startpreisen, getrennt vom nominalen Geldumsatz. Fester Referenzkorb: 33 Alltags- und 18 Werkstattgüter; Startwert 6.000 €, Ausgabenanteile 55/45. Preisindex und inverse Kaufkraft wurden aus genau diesem Korb berechnet.
- GuV, Ausschüttungen, Firmen-Eigenkapital und Personal-/Betriebspuffer. Maschinen werden für die Eigenkapitalbrücke zu ihren **tatsächlich bezahlten historischen Anschaffungskosten** rekonstruiert; die frühere Annahme „jede Maschine 1.200 €“ wäre bei variablen Preisen falsch.
- Maschinenkreditsumme aus acht Einheiten zum Gutschriftpreis, aufgerundete Monatsrate, gedeckelte letzte Rate und Rückstände. Ein unverbindlicher Antrag bedeutet weiterhin keine sofort verfügbare Maschine.

Die unveränderte Basis reproduziert alle bisherigen 24 Monatsdatensätze der V7-Basis exakt, abgesehen von zusätzlich eingeführten Preis-/Haushaltsmetadaten. Die ursprünglichen sieben vollständigen Läufe wurden nach der finalen Kernkorrektur erneut ausgeführt; ihre Ergebnisse blieben unverändert. Ein zusätzlicher Vergleich mit null Prozent Preisweitergabe wurde anschließend auf dem finalen Kern ausgeführt.

## Vollständige Läufe

Energie- und Nachfrageschocks beginnen in Monat 3. Die Zinserhöhung setzt den Modell-Leitzins ab Monat 2 auf 4 %. „Kombiniert“ enthält alle drei Ereignisse. Beide Maschinenläufe enthalten den Energieschock; die Anfragen erfolgen in Monat 1 beziehungsweise Monat 6. Der zusätzliche Energievergleich setzt ausschließlich die Preisweitergabe auf null Prozent.

| Lauf | Buchungen | Konsum Monat 24 nominal € | Gekaufte Mengen zu Startpreisen € | Arbeitsverhältnisse Monat 24 | Staatskasse Ende € |
|---|---:|---:|---:|---:|---:|
| Basis | 1.272 | 9.900 | 9.900 | 6 | 68.266,23 |
| Energie | 1.244 | 10.170 | 9.900 | 6 | 61.059,38 |
| Energie ohne Preisweitergabe | 1.254 | 9.900 | 9.900 | 6 | 59.830,36 |
| Nachfrage | 1.131 | 5.300 | 5.300 | 5 | 23.890,07 |
| Zinserhöhung | 1.271 | 9.900 | 9.900 | 6 | 67.054,36 |
| Kombiniert | 1.112 | 4.571 | 4.450 | 4 | 7.527,33 |
| Maschine vor Preissteigerung | 1.317 | 10.170 | 9.900 | 6 | 74.441,67 |
| Maschinenanfrage nach Preissteigerung | 1.260 | 10.170 | 9.900 | 6 | 61.186,63 |

Im Energielauf verdoppeln sich die Stückenergiekosten in Monat 3 von 5/9 € auf 10/18 €. Die Verkaufspreise bleiben zunächst 100/150 €. Ab Monat 4 steigen sie auf 101/151,50 €, in Monat 5 auf 102,01/153,01 € und erreichen in Monat 6 die Ziele 102,50/154,50 €. Die Weitergabe betrifft die zusätzlichen **Energiekosten**, nicht 50 % des gesamten Verkaufspreises. Der Referenzkorb kostet dann 6.163,50 €; der auf Basispunkte abgerundete Index beträgt 102,72 und die inverse Kaufkraft 97,34 bei Startwert 100.

Die 10.170 € nominalen Konsumausgaben am Ende des Energielaufs entsprechen gekauften Mengen mit einem Startpreiswert von 9.900 €. Der höhere Geldumsatz belegt hier keinen höheren realen Warenverbrauch. Ebenso darf die feste Referenzkorb-Kaufkraft nicht mit der individuell tatsächlich gekauften Warenmischung gleichgesetzt werden.

Auch Personal reagiert zeitlich: In der Basis fällt bereits Ende Monat 2 ein Arbeitsverhältnis weg, **vor** dem Energieschock. Während der Produktion hat die Basis in Monat 1–2 vier betriebliche Stellen, in Monat 3–4 drei und ab Monat 5 wieder vier. Mit Energie und 50 % Weitergabe bleiben es in Monat 3–9 drei, ab Monat 10 wieder vier. Bei gleichem Energieschock ohne Preisweitergabe kehrt die vierte Stelle bereits in Monat 8 zurück. Die beiden öffentlichen Stellen bestehen in diesen Vergleichspfaden weiter. Der durch den Vergleich gestützte Befund ist die verzögerte Wiederbesetzung; der erste Stellenverlust besteht bereits in der Basis. Die Weitergabe führt in diesem Parametersatz trotz höherer Stückpreise nicht zu einer früheren Wiederbesetzung. Aus einem beobachteten Stellenrückgang allein folgt daher keine eindeutige Energiepreisursache. Im kombinierten Lauf überlagern sich Energie-, Budget-, Zins-, Lager- und Personalpfade; seine niedrigeren Mengen sind kein isolierter Nachweis einer einzigen Ursache.

Der erste Maschinenkredit wird in Monat 1 über 1.200 € zu 6 % gutgeschrieben und geliefert, vollständig getilgt und verursacht 39 € Zinsen. Die Anfrage in Monat 6 wartet bis Monat 17 auf acht freie Werkstatteinheiten. Erst dann entstehen 1.236 € Kredit zum Stückpreis von 154,50 €. Ende Monat 24 sind sieben Raten zu 103 € bezahlt, 515 € Restschuld und 32,43 € bezahlte Zinsen vorhanden. Unterschiedliche Laufzeiten und Restschulden verhindern einen unmittelbaren Vergleich der kumulierten Zinsbeträge.

## Grenzfälle und behobener Befund

1. **Nicht durch zwölf teilbare Kreditsumme:** Acht Einheiten zu 153,01 € ergeben 1.224,08 €. Elf Raten zu 102,01 € und eine letzte Rate zu 101,97 € tilgen den Betrag exakt; Zinsen insgesamt 39,75 €, Restschuld und fiktive Tilgungsrückstände null. Die vorher zu 720 € bewertete Ware geht zum historischen Lagerwert ab, ohne Preisneubewertung.
2. **Keine Weitergabe:** Bei null Prozent Kostenweitergabe bleiben die Verkaufspreise trotz verdoppelter Energiepreise bei 100/150 €.
3. **Verzögerte Lieferung:** Vor der Korrektur lieferte ein bei 153,01 € gebundener Vertrag nach Anstieg auf 154,50 € nur sieben Einheiten, gab die Reservierung frei und brach nach bereits erfolgter Teilzahlung ab. Dieser Fehler wurde mit expliziten internen Testumbuchungen reproduziert; er trat in den acht regulären Läufen nicht auf. Im finalen Kern wird der gebundene Vertragspreis an den Warenkauf übergeben: acht Einheiten, 1.224,08 € Zahlung, vollständiger Lagerabgang, korrekte Reservierungsauflösung, keine Ausnahme.
4. **Wiederholter Monatsbeginn:** Ein zweiter Aufruf der Preisfestsetzung im selben Monat verändert weder Preis noch Preisquote oder Zustand. Der vorher fehlende Schutz ist im finalen Kern ergänzt und nachgeprüft.

Die isolierten Fälle benutzen manuell gesetzte Monate und Warenbestände; der Verzögerungsfall zusätzlich eine explizite interne Geldumbuchung. Sie prüfen Vertragsgrenzen und sind keine weiteren vollständigen Wirtschaftsszenarien.

## Reichweite

Feste Weitergabequote, Monatsdeckel, Startpreiskorb und ganzzahlige Güter sind gewählte Lernregeln. Nachfrageabhängige Preisbildung, Substitution, Lohnanpassungen, Einlagenzinsen, Erwartungen und ein allgemeines Marktgleichgewicht werden dadurch nicht modelliert. Die Lagerbewertung beruht auf historischen Produktionskosten, nicht auf Marktpreisen. Maschinenkosten werden historisch aus tatsächlichen Käufen rekonstruiert, ohne zusätzliche Abschreibungs-/Neubewertungslogik.

Die geprüften Geld-, Waren- und Vertragsbrücken sind konsistent. Das ist kein Nachweis realer Übertragungsstärken oder langfristiger Stabilität. Für Lernfragen sollten nominale Ausgaben, Mengen zu Startpreisen, individuelle Budgetengpässe und der feste Referenzindex stets getrennt gezeigt werden. Archivierte frühere Auditdateien bleiben unverändert.
