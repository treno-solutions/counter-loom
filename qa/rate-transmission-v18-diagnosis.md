# Warum der Leitzinsschock im Modell schwach wirkt

Stand: 3. November 2026. Diagnose des unveränderten Modells v18 am Quellstand `d4254a4`. Grundlage sind Quellcode und die bereits archivierten [einzelnen Schockläufe](isolated-shocks-v18-report.md). Keine Wirtschaftsregel und kein laufender UI-Zustand wurden verändert. Externe Erläuterungen, Modellannahmen, simulierte Befunde und bedingte Rechenbeispiele sind nachfolgend getrennt.

## Befund

Die Zinsweitergabe funktioniert wie programmiert. Ihre wirtschaftliche Reichweite ist jedoch klein: Nur ein bestehender Betriebskredit über 12.000 € wird teurer. Es gibt im Beobachtungsfenster keine neuen Kredite, keine Maschineninvestitionen und keine Staatsschuld. Haushalte haben weder Kredite noch verzinste Sparanlagen. Die Bank reicht sämtliche erhaltenen Zinsen noch im selben Monat an dieselben sechs Haushalte weiter, die auch beide Firmen besitzen.

Zusätzlich behandelt das Modell Firmen- und Bankerträge steuerlich unterschiedlich: Firmen zahlen 20 % Gewinnsteuer; die Bank zahlt keine eigene Gewinnsteuer. Bei beiden Empfängern werden Ausschüttungen anschliessend mit 25 % belastet. Die Verschiebung von Firmengewinn zu Bankertrag kann deshalb selbst bei unveränderter Aktivität das verfügbare Haushaltseinkommen erhöhen. Das ist eine Modellasymmetrie und kein allgemeiner positiver Konsumeffekt höherer Leitzinsen.

Die Bankausschüttung allein erklärt damit nicht den gesamten Befund. Kleine Kreditexposition, fehlende Investitionsentscheidungen, identische Eigentümer, Auszahlungszeitpunkt und Besteuerung wirken zusammen. Die folgende Zerlegung ist eine Buchungsdiagnose; sie schätzt keine separaten kausalen Beiträge aus neu gerechneten Gegenwelten.

## 1. Wie gross ist die tatsächliche Belastung?

Der Leitzins steigt für zwölf Monate von 2 auf 5 %. Der variable Firmenzins folgt mit einem Monat Verzögerung. Deshalb gelten die erhöhten Vertragszinsen in den relativen Monaten 2 bis 13, obwohl der Leitzins in Monat 13 bereits wieder gesenkt ist. Der bestehende zweite Firmenkredit bleibt fest bei 2 %.

`12.000 € × (5 % − 2 %) / 12 = 30 € zusätzliche Zinsen pro betroffenem Monat`

| Grösse | Erste zwölf Eingriffsmonate | Bis einschliesslich Monat 13 | Gesamte 60 Monate |
| --- | ---: | ---: | ---: |
| Zusätzliche Firmenzinsen | 330 € | 360 € | 360 € |
| Neue Kreditgutschriften, Kontrolle und Schock | 0 € | 0 € | 0 € |
| Maschinenzahlungen, Kontrolle und Schock | 0 € | 0 € | 0 € |

In den ersten zwölf Monaten stehen 330 € Mehrzinsen rund 149.714 € Firmenumsatz der Kontrolle gegenüber: etwa 0,22 %. Eine Anhebung um drei Prozentpunkte klingt gross, erreicht hier aber nur einen kleinen Zahlungsstrom. Das feste Darlehen hat im Modell keine endliche Zinsbindung mit späterer Anschlussfinanzierung. Die variable Anfangsschuld wird nicht planmässig getilgt; der gesonderte Maschinenkredit hat dagegen Tilgungsregeln.

Belege: [Zinsweitergabe](../poc/rates.py), [Anfangsschulden und Monatsablauf](../poc/world.py), [Maschinenkredit](../poc/banking.py), [maschinelle Diagnose](rate-transmission-v18-diagnosis.json).

## 2. Wo landen die zusätzlichen Zinsen?

Für jeden beobachteten Monat wurde aus den tatsächlichen Buchungen geprüft: Bankausschüttungen entsprechen vollständig den vereinnahmten Firmen-, Maschinen- und Staatszinsen. Das Bankeigenkapital bleibt bei 10.000 €. Die Bank baut aus diesen Erträgen keine zusätzlichen Puffer auf.

| Einkommensänderung gegenüber Kontrolle, erste zwölf Monate | Betrag |
| --- | ---: |
| Zusätzliche Bruttoausschüttung der Bank | +330,00 € |
| Darauf zusätzlich einbehaltene Ausschüttungssteuer | −82,53 € |
| Zusätzliche Netto-Bankausschüttung an Haushalte | **+247,47 €** |
| Geringere Netto-Firmenausschüttungen an Haushalte | **−169,08 €** |
| Übriges Nettohaushaltseinkommen, Löhne und Transfers nach Lohnsteuer | **+58,44 €** |
| Tatsächlich erhaltenes Nettohaushaltseinkommen insgesamt | **+136,83 €** |

Die Centabweichung gegenüber einer pauschalen Steuer von 25 % entsteht, weil die Ausschüttungssteuer je Haushalt auf die kumulierten Ausschüttungen des Monats berechnet wird. Die Zuordnung zum jeweils unmittelbar vorherigen Bankbeleg berücksichtigt diese tatsächliche Reihenfolge.

Die Haushalte kaufen in diesem Zeitraum 139 € beziehungsweise 0,103 % mehr. Firmengewinne vor Steuer sinken insgesamt um 281,91 €. Zusätzliche Umsätze und Arbeitsstunden sind bereits Rückwirkungen des gesamten Modells. Die beobachtete Einkommenszerlegung darf daher nicht als isolierter Nachweis verstanden werden, dass eine Änderung der Bankausschüttung allein den Konsum um einen bestimmten Betrag drehen würde.

Bankausschüttungen erfolgen nach der Kaufrunde und gehen als Nettoübertrag in spätere Kaufpläne ein. Firmen schütten monatlich einen begrenzten Anteil aus und prüfen zusätzliche Ausschüttungen quartalsweise unter Gewinn- und Liquiditätsbedingungen. Auch ohne unterschiedliche Steuern kann dieser Zeitunterschied kurzfristige Effekte erzeugen.

Belege: [vollständige Bankausschüttung und Quellensteuer](../poc/distribution_tax.py), [gleichmässige Verteilung und Haushaltsbudget](../poc/systems.py), [Firmengewinnverwendung](../poc/profit_distribution.py).

## 3. Die Steuerasymmetrie als bedingtes Rechenbeispiel

Eigene Rechnung mit eingefrorener realer Aktivität, positivem steuerpflichtigem Firmengewinn und später vollständig ausgeschüttetem Firmengewinn. Ohne Cent-Rundung; keine neue Simulation und keine Zerlegung des tatsächlich beobachteten Gesamteffekts.

| Ein zusätzlicher Zinsaufwand von 30 € | Wirkung |
| --- | ---: |
| Firmengewinn vor Steuer | −30,00 € |
| Firmengewinnsteuer bei 20 % | −6,00 € |
| Später an Eigentümer verteilbarer Firmengewinn nach Gewinnsteuer | −24,00 € |
| Netto-Firmenausschüttung nach 25 % Quellensteuer | −18,00 € |
| Netto-Bankausschüttung ohne Bankgewinnsteuer, nach 25 % Quellensteuer | +22,50 € |
| Verfügbares Einkommen derselben Haushaltseigentümer zusammen | **+4,50 €** |
| Gesamte staatliche Steuereinnahmen | **−4,50 €** |

Es entsteht kein Geld aus dem Nichts: Der Staat erhält in diesem bedingten Vergleich weniger Steuern. Die tatsächlichen Steuerveränderungen des dynamischen Laufs fallen wegen Rückwirkungen und Auszahlungsterminen anders aus. Eine gleichartige Besteuerung beider Gewinne würde diesen speziellen Rechenweg aufheben, aber noch keinen Investitions- oder Sparkanal herstellen.

## 4. Ist die Bankausschüttung plausibel?

Dass Bankeigentümer von höheren Zinserträgen profitieren und einen Teil davon ausgeben, ist ein plausibler Gegenkanal. Höhere Leitzinsen müssen Bankgewinne kurzfristig nicht senken. Die EZB-Bankenaufsicht beschreibt 2024 gestiegene Margen und unterscheidet kurzfristige Ertragsverbesserungen von nachhaltiger Profitabilität. Sie nennt für 2023 Ausschüttungen einschliesslich Rückkäufen von 53 % der Gewinne bedeutender beaufsichtigter Banken. Das ist eine historische Beobachtung, keine geeignete pauschale Zielquote für dieses Modell. [S1]

Unsere Umsetzung ist erheblich enger: Sie behandelt sämtliche Zinseinnahmen unmittelbar als ausschüttbaren Gewinn. Einlagen- und Refinanzierungszinsen, Bankbetriebskosten, Kreditausfälle, eigene Gewinnsteuern und eine risikobezogene Thesaurierung fehlen. Die Ausschüttung geht gleichmässig an alle sechs Haushalte; Unterschiede zwischen verschuldeten Haushalten und vermögenden Bankeigentümern fehlen ebenfalls. Damit ist die Bank als vollständig ausschüttende Einnahmenverteilerin modelliert, nicht als wirtschaftlich vollständig abgebildete Geschäftsbank.

Die Bilanzidentität ist trotzdem erfüllt: Ein Zinseingang verschiebt Einlagen in Bankeigenkapital; die Ausschüttung kehrt diesen Effekt um. Buchhalterische Korrektheit validiert weder Auszahlungsquote noch Eigentümerstruktur. Ein schlichtes Einbehalten aller Erträge wäre ebenfalls keine neutrale Reparatur: Es würde Geld länger beim Bankkapital binden. Banklöhne oder Einlagenzinsen würden ihrerseits Einkommen anderer Empfänger erzeugen. Für jeden späteren Vorschlag müssen Empfänger und Zahlungszeitpunkt mitgeführt werden.

## 5. Welche Übertragungswege fehlen oder bleiben inaktiv?

Die EZB beschreibt als reale Übertragungswege unter anderem Kredit- und Einlagenzinsen, Konsum- und Investitionsentscheidungen, Kreditangebot, Vermögenspreise, Wechselkurs sowie Erwartungen. Die Wirkung tritt mit variablen Verzögerungen ein; Richtung und Stärke hängen auch von Bilanzen ab. [S2] Der Abgleich darunter ist eine eigene Quellcodebewertung, keine empirische Kalibrierung.

| Weg | Zustand im Modell v18 | Konsequenz für diesen Test |
| --- | --- | --- |
| Schuldendienst vorhandener Kredite | Variabler Firmenkredit reagiert; fester Firmenkredit bleibt dauerhaft fest | Einziger unmittelbar aktiver Zinskostenkanal; nur 12.000 € variable Schuld |
| Kreditfinanzierter Haushaltskonsum und Wohnen | Keine Haushaltskredite, Hypotheken oder Anschlussfinanzierung | Kein direkter Einkommensentzug bei verschuldeten Haushalten |
| Sparanreiz und Einlagenzinsen | Guthaben unverzinst; Konsumquote und Liquiditätsziel nicht zinsabhängig | Keine Wahl zwischen heutigem Konsum und verzinster Anlage |
| Unternehmensinvestitionen | Automatischer Maschinenauftrag reagiert auf Kapazitätsengpass und Liquidität; keine erwartete Rendite gegen Finanzierungskosten | Keine direkte zinsabhängige Projektentscheidung; in beiden Zweigen keine Investition |
| Neue Firmenkredite | Maschinenkreditangebot wird teurer, aber muss explizit angefragt werden | Keine autonome Änderung der Kreditnachfrage; im Test kein Abschluss |
| Bankfinanzierung und Kreditangebot | Keine laufenden Refinanzierungskosten, Ausfallverluste oder risikobezogenen Kapitalgrenzen | Kein geldpolitisch ausgelöster Kreditangebotskanal |
| Staatsfinanzierung | Neue Tranchen zinsabhängig; bestehende fest verzinst | Keine Wirkung über Staatszinsen, weil die Staatsschuld hier null bleibt |
| Ersatzinvestitionen und Erneuerung | Anlagen verlieren keine Kapazität durch Alterung | Im reifen Zustand kann der wiederkehrende Finanzierungsbedarf dauerhaft ausbleiben |
| Vermögenspreise und Sicherheiten | Keine handelbaren Vermögenspreise und beleihbaren Sicherheiten | Kein Vermögens- oder Sicherheitenkanal |
| Aussenwirtschaft | Waren- und Geldkreislauf vorhanden, aber kein Wechselkurs und keine externe Zinsnachfrage | Kein geldpolitischer Wechselkurskanal |
| Inflationserwartungen und Realzins | Keine erwartete Inflation in Konsum- oder Investitionsentscheidungen | Kein erwarteter Realzins als Entscheidungsgrösse |
| Preisreaktion auf Nachfrage | Verkaufspreise folgen verzögert der Energiekostenregel | Sinkende Nachfrage kann keinen allgemeinen Disinflationspfad erzeugen |

Der neue Kreditzins ist somit ein Angebot, das im untersuchten Zustand niemand nutzt. Der reife Startzustand ist für den isolierten Vergleich sinnvoll, macht aber einen Teil der vorhandenen Kreditfunktionen inaktiv. Ein Zinstest nur dieses Zustands prüft keine vollständige geldpolitische Transmission.

## 6. Schlussfolgerung vor weiteren Regeln

1. **Kein Rechenfehler bei der vereinbarten Zinsanpassung nachgewiesen.** Die zwölf erhöhten Zahlungen ergeben exakt 360 € Mehrzinsen; eine davon fällt nach der Leitzinssenkung an.
2. **Eine wirtschaftlich starke Vereinfachung und eine Steuerasymmetrie sind nachgewiesen.** Die Bank schüttet Zinseinnahmen sofort vollständig aus; dieselben Haushalte erhalten beide Gewinnquellen, die aber vor der Ausschüttung unterschiedlich besteuert werden.
3. **Die schwache Gesamtwirkung ist vor allem eine Frage der Reichweite des Tests und des Modells.** Breite Kredit-, Spar-, Investitions- und Preiskanäle werden damit nicht geprüft. Aus den beobachteten +0,10 % Käufen folgt keine positive gesamtwirtschaftliche Wirkung realer Zinserhöhungen.
4. **Keine neue Regel ist bereits durch diese Diagnose gerechtfertigt oder kalibriert.** Für den nächsten begrenzten Vergleich wären zunächst Bankgewinn und Auszahlung fachlich konsistent zu definieren sowie aktive Kreditexposition und eine konkrete Investitionsentscheidung zu wählen. Nicht alle fehlenden Kanäle müssen eingebaut werden. Ein vollständiger Hypothekenmarkt oder Wechselkursmechanismus ist für den ersten Lernpfad nicht erforderlich.

Eine spätere isolierte Variante könnte zunächst ausschliesslich die steuerliche Behandlung prüfen; eine weitere den Auszahlungszeitpunkt beziehungsweise einen begründeten Puffer. Erst getrennte Gegenläufe würden deren kausalen Anteil zeigen. Eine pauschale Ausschüttungsquote zu senken, nur um einen erwarteten Konsumeinbruch zu erhalten, wäre kein geeigneter Nachweis.

## Quellen und Reproduktion

- **S1, externe Erläuterung und historische Beobachtung:** EZB-Bankenaufsicht, *Bank profitability: a mirror of the past, creating a vision for the future*, Rede vom 16. Oktober 2024; Abschnitte zu Margen, nachhaltiger Profitabilität und Ausschüttungen. [Original](https://www.bankingsupervision.europa.eu/press/speeches/date/2024/html/ssm.sp241016~c532e5246d.en.html), abgerufen am 3. November 2026. Keine Übernahme als Modellparameter.
- **S2, externe Mechanismenbeschreibung:** EZB, *Transmission mechanism of monetary policy*, undatierte Überblicksseite, Abschnitte zu Sparen, Investitionen, Kreditangebot, Erwartungen und Vermögenspreisen. [Original](https://www.ecb.europa.eu/mopo/intro/transmission/html/index.en.html), abgerufen am 3. November 2026. Kein quantitatives Wirkungsmodell für unsere Konfiguration.
- **Simulierte Befunde:** [unverändertes Ergebnisarchiv](isolated-shocks-v18-2026-11-03.json), gemeinsamer Zustand nach Monat 1440 und 60 Folgemonate; Kontrolle und Zinszweig. Ursprüngliche Regeln, Quellprüfsummen und Eingriffe bleiben im Archiv dokumentiert.
- **Eigene Berechnung:** [Diagnoseskript](../poc/scripts/diagnose_rate_transmission.py) und [Ausgabedaten](rate-transmission-v18-diagnosis.json). Das Skript prüft alle im Ausgangsarchiv verzeichneten Quellprüfsummen, gleicht monatliche Zinserträge und Bankausschüttungen ab und zerlegt das tatsächliche Haushaltseinkommen. Das bedingte Steuerbeispiel wird getrennt mit rationalen Zahlen gerechnet und saldiert auf null. Keine zusätzliche Simulation wurde ausgeführt.

Aus dem Repository-Stamm reproduzierbar mit `python3 poc/scripts/diagnose_rate_transmission.py`. Wirtschaftslogik und Oberfläche bleiben unverändert. Die 199 Tests des Ausgangsstands sind im [Schocknachweis](isolated-shocks-v18-verification.json) archiviert; diese Diagnose hat sie nicht erneut ausgeführt.
