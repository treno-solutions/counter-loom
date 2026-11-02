# Unabhängiger Plausibilitätsscreen · laufende Modellwirtschaft

Stand: 2. November 2026. Separat beauftragte Prüfung. **Buchungskonsistenz, Verhaltensplausibilität und empirische Gültigkeit sind unterschiedliche Prüfstufen.** Dieses Dokument bewertet einen technischen Lernversuch, keine reale Volkswirtschaft oder Prognose. V3-Prüfung wird unten separat ergänzt; die V2-Befunde bleiben unverändert.

## Eingefrorene V2-Baseline

Quellstand `6ed95131631639ff1cdc793a54441e0dfae4b3fa`, Modell `illustrative_circular_flow_v2`. `world.py` und `systems.py` wurden vor der parallelen Weiterentwicklung getrennt eingefroren. SHA-256:

- `poc/world.py`: `9717f8bb129e7b7f8c0739e27e477efccb3b3b78cfe4f23f4ba9648e56d27eda`
- `poc/systems.py`: `8edb6ba806cc68d50ce153838665630b517a9e7347d60a36733395cfd8b2d9db`

Elf separat neu konstruierte Welten durchliefen jeweils 240 Monate beziehungsweise 1.200 Buchungsphasen: Baseline, Energie ab Monat 1, Konsumzurückhaltung ab Monat 1, beide Eingriffe ab Monat 1, beide ab Monat 13 sowie sechs Reihenfolgevarianten. Insgesamt 2.640 simulierte Monate und 13.200 Phasen. Kein LLM, keine zufällige Variation und keine empirische Kalibrierung. [Messwerte und Konfigurationen](bank-plausibility-review-2026-11-02.json).

Die unabhängige Kontenrekonstruktion verwendete Anfangsbestände und jede Belastung/Gutschrift aus dem Journal, statt nur den eingebauten Summencheck aufzurufen. V2 hielt in allen geprüften Phasen die Abrechnungssumme von 156.000 € konstant; rekonstruierte Konten stimmten mit dem jeweiligen Zustand überein. Diese ältere Kontrollsumme enthält das Bankkonto und ist noch kein sauber abgegrenztes Buchgeldaggregat. V3 muss Bankeigenkapital davon trennen.

## Was die Läufe zeigen

| V2-Bedingung · Monat 240 | Konsum in diesem Monat | Haushaltskonten | Staatskonto | Energie-Außenkonto | Lager Alltag / Werkstatt |
|---|---:|---:|---:|---:|---:|
| Ohne Eingriff | 2.450 € | 68.654,16 € | 276 € | 70.255,84 € | 6.725 / 906 |
| Energie verdoppelt ab M1 | 1.050 € | 43.955,60 € | 442 € | 91.492 € | 1.128 / 919 |
| Konsumanteil reduziert ab M1 | 2.300 € | 94.700 € | 276 € | 40.100 € | 13 / 1.161 |
| Beide ab M1 | 600 € | 60.944 € | 116 € | 77.120 € | 0 / 192 |
| Beide ab M13 | 750 € | 51.704 € | 146 € | 85.750 € | 0 / 251 |

Die gemessenen Unterschiede sind Folgen der vorgegebenen Regeln und Anfangsbestände. Sie belegen keine realen makroökonomischen Multiplikatoren, Krisenwahrscheinlichkeiten oder Anlegerreaktionen.

## Kritische V2-Befunde

1. **Nicht finanzierbare Wünsche werden zu Einstellsignalen.** `buy()` bildet in V2 `unmet_units` aus gewünschter Menge minus tatsächlichem Kauf. Dabei werden fehlendes Geld und fehlende Ware vermischt. Minimalfall: Staat 0 €; Alltag 100 Einheiten Lager; unbeschäftigter Haushalt vorhanden. Eine Beschaffungsabsicht von 1.200 € bucht 0 €, zählt aber 12 unbediente Einheiten. Der anschließende Personalreview stellt eine zusätzliche Person ein. Das ist keine zahlungsfähige Güternachfrage. Im tatsächlichen Baselinelauf tritt das Muster ab Monat 44 auf: Werkstatt 374 Einheiten Lager, öffentliche Zahlung 0 €, dennoch 8 unbediente Einheiten. **Fachlicher Korrekturbedarf:** finanzierbare, wegen Warenmangels unerfüllte Nachfrage von nicht finanzierbaren Wünschen trennen.
2. **Produktion kann ohne bezahlte Inputs entstehen.** Isolierter Fall: Alltag beginnt mit 0 € Kontoguthaben. V2 produziert 72 Einheiten, zahlt 0 € Lohn und 0 € Energie und erfasst 5.180 € neue Verpflichtungen. Ein begrenzter Lieferkredit oder eine kurze Fortsetzung trotz Zahlungsrückständen kann eine ausdrückliche Modellannahme sein; hier existiert aber keine entsprechende Arbeits-/Energie-Lieferregel. **Fachlicher Korrekturbedarf:** Finanzierung und Lieferfähigkeit der Inputs sichtbar begrenzen oder einen ausdrücklich begrenzten Kreditmechanismus modellieren.
3. **Arbeitsverhältnis ist nicht tatsächliches Einkommen.** In der Baseline wird der zweite Staatslohn erstmals in Monat 29 nur teilweise gezahlt (1.716 € statt 2.400 €). In Monat 97 bestehen am Monatsende vier Arbeitsverhältnisse; nur zwei Haushalte erhalten überhaupt eine Lohnzahlung. Beide Staatsverträge zahlen in diesem Monat null. Wichtig: Neueinstellungen beim Monatsabschluss gelten erst für den Folgemonat. Deshalb vergleicht der Audit die Verträge *vor der Lohnphase* mit tatsächlicher Lohnzahlung; eine reguläre Neueinstellung wird nicht als Lohnrückstand fehlklassifiziert.
4. **Volle Produktion trotz wachsender Lager ist keine plausible Bestandssteuerung.** Ohne Eingriff liegen in Monat 12 bereits 188/88, in Monat 97 3.230/536 und in Monat 240 6.725/906 Einheiten auf Lager. Produktion hängt nicht vom gewünschten Lagerbestand oder erwarteten Absatz ab. Lagerkosten, Verderb und Abschreibungen fehlen. Damit können sich wirtschaftlich fragwürdige Vorräte und Beschäftigungsreaktionen aufbauen. Diese Bestände dürfen nicht als validierte Geschäftsstrategie gedeutet werden.
5. **Stückelung erzeugt erhebliche erzwungene Ersparnis.** Im ersten Monat planen die Haushalte zusammen 9.576 €, kaufen aber nur 8.400 €. In Monat 12 stehen einem Plan von 9.613,96 € erneut 8.400 € Käufe gegenüber, obwohl Lagerbestände vorhanden sind. Die groben Stückpreise von 100/150 € halten Budgetreste auf Konten. Die 95-%-Regel ist daher kein tatsächlich realisierter Konsumanteil. Das wird bereits als Modellgrenze dokumentiert, bleibt aber für Interpretation und Kalibrierung wesentlich.
6. **Staatsreserve und einseitiger Außenanschluss treiben den Langzeitlauf.** Der Staat finanziert Defizite aus einem endlichen Anfangskonto. Das Energie-Außenkonto gibt nichts zurück. Ohne Eingriff liegen nach 240 Monaten rund 70.256 € dort. Fehlende Staatsfinanzierung und Export-/Kapitalrückflüsse sind bekannte Systemgrenzen, keine entdeckten Krisengesetze. Alte Verpflichtungen werden erfasst, aber nicht durch einen allgemeinen Nachzahlungs-/Insolvenzmechanismus abgewickelt.

## Reihenfolgesensitivität

Unterschiedliche Varianten wurden bewusst getrennt, damit keine Wirkung fälschlich allein einer Kaufreihenfolge zugeschrieben wird:

- **Nur Kaufreihenfolge umkehren:** Haushaltsenumeration wird ausschließlich in der Einkaufsphase vor der bestehenden monatlichen Rotation umgedreht. Baseline nach 240 Monaten unverändert. Bei beiden Schocks ab Monat 1 steigt der Monatskonsum von 600 auf 750 €; die Haushaltsbestände unterscheiden sich um 210 €. Das zeigt eine diskrete Zuteilungssensitivität bei knapper Versorgung.
- **Haushaltsenumeration allgemein umkehren:** Zusätzlich sind Auswahl der nächsten einzustellenden Person, Transferpriorität und die Cent-Restverteilung von Ausschüttungen betroffen. Bei beiden Schocks sinken die Haushaltsbestände nach 240 Monaten von 60.944 auf 43.436 €. Diese große Abweichung ist ein Hinweis auf Pfad-/Prioritätsabhängigkeit, kein Beleg unterschiedlicher Psychologie.
- **Staatsbeschaffung nach den Haushaltskäufen statt davor:** Baseline unverändert. Bei beiden Schocks ab Monat 1 ändern sich die Haushaltsbestände von 60.944 auf 58.390 € und die Firmenbestände von 7.820 auf 10.922 €. Die priorisierte Zuteilung ist damit ein relevanter Teil des Szenarios.

## Urteil und Prioritäten

**Als sichtbarer Test von Zahlungswegen geeignet; als plausibles, langfristig reagierendes Gesamtwirtschaftsmodell noch nicht hinreichend.** Die unabhängige Prüfung bestätigt die Kontenrechnung der eingefrorenen V2-Fassung, nicht ihre wirtschaftliche Verhaltenslogik.

Zuerst die finanzierbare Nachfrage und die Input-/Produktionsgrenze korrigieren, Arbeitsverhältnisse und tatsächliche Löhne trennen, dann Lager-/Absatzplanung und Zahlungsrückstandsregeln eigenständig modellieren. Das neue Bankmodul soll einen vollständig nachvollziehbaren Kreditpfad liefern; es darf nicht als allgemeine Reparatur dieser offenen Wirtschaftsmechanismen verstanden werden.

## V3-Prüfung

Nach expliziter Fertigmeldung wurden `world.py`, `systems.py` und `banking.py` gesondert eingefroren. V3-SHA-256:

- `poc/world.py`: `5064d9f8740c765ac76c146a3b7a6e0767d4e93da6d15623bee5d5fbebbc6cb5`
- `poc/systems.py`: `8edb6ba806cc68d50ce153838665630b517a9e7347d60a36733395cfd8b2d9db`
- `poc/banking.py`: `feddbbf398755daa04c397502b56a3c6b4bd229d15c81c872a8b2811fee6b098`

Neun weitere Welten durchliefen jeweils 240 Monate: ohne Eingriff, Energie, Nachfrage, beide Schocks, Maschinenkredit ab Monat 1 ohne/mit beiden Schocks sowie Kreditanfragen in Monat 24, 60 und 97. Insgesamt 2.160 Monate und 10.800 Phasen. **39.892 Journalbuchungen** wurden unabhängig rekonstruiert, einschließlich Kreditforderung, Kundeneinlagen und Bankeigenkapital. Die Gegenüberstellung von Reserven + Forderungen und Kundeneinlagen + Eigenkapital stimmte vor und nach jeder Buchung. Bankeigenkapital wurde dabei ausdrücklich nicht als Kundengeld addiert.

### Kreditmechanik

- Kredite angefragt in Monat 1, 24 und 60 wurden in den geprüften Bedingungen tatsächlich ausgezahlt und geliefert. Die passenden Forderungen und Guthaben entstanden gemeinsam; der Betrag wurde nicht aus Bankeigenkapital entnommen.
- Der Kredit bei Anfrage in Monat 1 wurde in Monat 13 vollständig getilgt: zwölf Tilgungen à 100 €, Zinsen von 6 € abnehmend bis 0,50 €, insgesamt 39 €. Nach Tilgung entstanden keine zusätzlichen Raten.
- Die Anfrage in Monat 97 blieb mangels aktivem Betrieb im Status `requested`. Sie erzeugte weder Guthaben noch eine neue Schuld. Das ist eine sinnvolle Unterscheidung zwischen Anfrage und tatsächlicher Kreditvergabe.
- Sechs weitere **isolierte Zahlungsport-Verläufe** mit je 24 monatlichen Bedienungsprüfungen (zwölf planmäßige Tilgungsfälligkeiten, danach gegebenenfalls Rückstände und weitere Zinsen) wurden gegen eine separat formulierte arithmetische Rekurrenz geprüft: pünktlich, zwei ausgefallene Raten mit Nachzahlung, kleine Teilzahlungen, völliger Zahlungsausfall, eine späte große Zahlung und abwechselnd ausfallende/hohe Zahlungen. Die verfügbaren Zahlungsmittel kamen durch ausdrücklich verbuchte Testüberweisungen aus einem anderen Kundenkonto; es wurde kein Testgeld hinzugefügt. Restschuld, Zinsrückstand, bezahlte Tilgung, verfügbare Mittel und Bankbilanz stimmten durchgehend.
- Bei zwei ausgefallenen Raten und späterer Nachzahlung betrugen die tatsächlich bezahlten Zinsen 40,50 € statt 39 €. Ohne jede Zahlung über 24 Monate blieben 1.200 € Restschuld und 144 € vertraglicher Zinsrückstand. Die Bank vereinnahmte in diesem Fall keinen Zinsertrag. Das passt zur ausdrücklich gewählten zahlungsbezogenen Ertragsrechnung; eine vollständige periodengerechte Zinsabgrenzung und Kreditwertberichtigung ist nicht implementiert.

### Bestätigte Korrekturen gegenüber V2

Die beiden minimalen V2-Gegenbeispiele wurden mit denselben Zustandsvoraussetzungen wiederholt:

- Staat 0 €, 100 Einheiten Lager: finanzierbare unbediente Nachfrage jetzt 0, separat ausgewiesene nicht finanzierbare Wünsche 12 Einheiten. Es wird dadurch keine zusätzliche Person eingestellt.
- Unternehmen 0 €: Produktionsplan 72 Einheiten, tatsächlich produziert 0. Unfinanzierte Löhne und Energie erzeugen keine gratis verkaufbare Produktion mehr. Die teilweise Vorfinanzierung von Inputs bleibt eine eigene vereinfachte Annahme.

### Verbleibende Plausibilitätsgrenzen

Die Bankrechnung repariert nicht automatisch den gesamten Wirtschaftskreislauf. Nach den Korrekturen verschwindet ein Teil der früher künstlich fortgesetzten Aktivität. In der V3-Baseline stehen nach 240 Monaten **102.226 € Firmenkonten**, **934 € Haushaltskonten**, **0 € Staatskonto** und **42.840 € Energie-Außenkonto** gegenüber. Beide Firmen haben keine Beschäftigten; der Konsum beträgt null, während beim Alltagsbetrieb noch 697 Einheiten lagern. Geld ist vorhanden, aber über die derzeitigen Regeln unzureichend in Löhne oder andere private Einnahmen zurückgeführt.

Damit bleiben insbesondere Absatz-/Lagerplanung, Personalentscheidungen bei verfügbaren Unternehmensreserven, die Verwendung einbehaltener Gewinne beziehungsweise Eigentümereinkommen, Zahlungsrückstände, staatliche Finanzierung und außenwirtschaftliche Rückflüsse offen. Eine weitere pauschale Geldzufuhr wäre kein Nachweis einer korrekten Reaktionslogik. Das nächste sinnvolle Fachmodul ist eine explizite Unternehmensentscheidung über Produktion, Lager, Personal und Gewinnverwendung.

**V3-Urteil:** Der begrenzte Bankkreditpfad ist in den geprüften Fällen buchhalterisch und vertraglich nachvollziehbar. Keine Abweichung in den unabhängigen Rekonstruktionen gefunden. Als Demonstration von Einlagenschöpfung, Lieferantenzahlung, Zinsen und Tilgung geeignet; keine Validierung der Gesamtwirtschaft oder von Kreditrisikoprognosen. Oberfläche, Bedienbarkeit und pädagogische Wirkung wurden durch diesen Agenten nicht geprüft.


## Öffentliche Wiederholung der V3-Prüfung

Die bereits verwendete unabhängige Prüfroutine liegt in [tools/check_bank_plausibility.py](../tools/check_bank_plausibility.py). Mit der gemäß [POC-Anleitung](../poc/README.md) eingerichteten Python-Umgebung vom Repository-Stamm aus:

```sh
poc/.venv/bin/python tools/check_bank_plausibility.py
```

Sie wiederholt dieselben neun 240-Monats-Szenarien und sechs isolierten Zahlungsport-Verläufe. Vorher müssen die SHA-256-Werte der drei Kerndateien mit dem aufgezeichneten V3-Stand übereinstimmen. Danach werden sämtliche Ergebnisse mit den bereits gespeicherten V3-Messwerten verglichen. Der bestätigte Wiederholungslauf rekonstruierte erneut 39.892 Buchungen und lieferte identische Szenario- und Zahlungsport-Ergebnisse. Die Routine erweitert den Auditumfang nicht und verändert die ursprüngliche QA-Datei nicht.

Optional lässt sich die Wiederholung in eine neue Datei schreiben:

```sh
poc/.venv/bin/python tools/check_bank_plausibility.py --output poc/.runtime/bank-plausibility-repeat.json
```

Ein bereits vorhandenes Ausgabeziel wird nicht überschrieben. Ohne `--output` wird nur eine Konsolenzusammenfassung ausgegeben; gegebenenfalls von BPTK erzeugte Laufzeitdateien verbleiben in der ignorierten POC-Laufzeitablage. Bei späteren Kernänderungen stoppt der Versionsvergleich, statt die früheren Ergebnisse als Prüfung des neuen Kerns auszugeben.

### V2 getrennt wiederholen

Die V2-Auswertung bleibt an Git-Stand `6ed95131631639ff1cdc793a54441e0dfae4b3fa` gebunden. Der öffentliche Runner oben führt ausschließlich V3 aus. Für eine getrennte Wiederholung können die ursprünglichen beiden Kerndateien in eine eigene lokale Laufzeitablage extrahiert werden:

```sh
mkdir -p poc/.runtime/v2-audit
git show 6ed95131631639ff1cdc793a54441e0dfae4b3fa:poc/world.py > poc/.runtime/v2-audit/world.py
git show 6ed95131631639ff1cdc793a54441e0dfae4b3fa:poc/systems.py > poc/.runtime/v2-audit/systems.py
```

Eine frische Python-Ausführung muss dann diese extrahierten Module importieren, die oben festgehaltenen V2-Dateihashes prüfen und die in der JSON-Datei angegebenen Eingriffe zu den jeweiligen Monatsgrenzen anwenden. Die Reihenfolgevarianten sind im Abschnitt „Reihenfolgesensitivität“ getrennt beschrieben. Ergebnisse dieses alten Kerns dürfen nicht als Ergebnisse der V3-Fassung ausgegeben werden; die vorliegenden V2-Messwerte wurden beim Bereitstellen des Runners nicht ersetzt oder neu etikettiert.
