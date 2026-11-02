# Unabhängige Plausibilitätsprüfung · Unternehmenssystem v4

Stand: 2. November 2026. Separater Nachtest des begrenzten Unternehmensmodells. **Technische Buchungskonsistenz, Plausibilität innerhalb der gewählten Regeln und empirische Gültigkeit sind getrennte Aussagen.** Die bisherige V3-Prüfung und ihre Langzeitbefunde bleiben unverändert erhalten.

## Gegenstand und Version

Sechs separat konstruierte Welten durchliefen jeweils den vollständigen Horizont von 24 Monaten: Baseline, Energieanstieg ab Monat 3, Konsumzurückhaltung ab Monat 3, beide Eingriffe ab Monat 3, Konsumzurückhaltung ab Monat 3 mit Normalisierung ab Monat 13 sowie Maschinenkredit angefragt vor Monat 1. Insgesamt **144 simulierte Monate, 720 Phasen und 6.636 unabhängig rekonstruierte Journalbuchungen**. Keine neuen Akteure, keine zusätzlichen Anlageklassen, kein LLM und keine Prognosekalibrierung.

Geprüft wurden die vier tatsächlichen Kerndateien, deren SHA-256 auch im [maschinenlesbaren Bericht](company-v4-plausibility.json) stehen:

- `poc/world.py`: `cad2648d29f5594f5574af1ce35a7d26b6ad885d91324a9634e27025799ba58e`
- `poc/systems.py`: `3491c16a89d11d2cf54c637ced9a8a9f143e032b30ec26f883fb3218780bccb0`
- `poc/banking.py`: `6d0492716552d59723bb5c6be87e1e78ce3ec18c69fa72e0360af8d51f13e7f8`
- `poc/firms.py`: `8daf7a8e723e00a138a140ceac8c6f214679a16225996efa2fa6bf15110ae475`

Die Fassung entstand auf dem Arbeitsstand nach `5636695e051db6590a541e28aabc2bb9faba1b67`; der Audit bezieht sich auf die oben identifizierten Dateien, nicht auf die Behauptung, der neue Kern sei bereits Bestandteil dieses älteren Commits.

## Unabhängige Kontrollen

Die Prüfung übernahm nicht nur eingebaute `check()`-Ergebnisse:

1. Aus Anfangskonten und jeder einzelnen Belastung/Gutschrift wurden alle Konten neu rekonstruiert. Kreditgutschrift und Tilgung wurden dabei gesondert behandelt. Kreditforderungen, Kundeneinlagen, Bankkapital und feste Reserveposition wurden nach jeder Journalbuchung unabhängig abgeglichen.
2. Aus tatsächlichen Energiezahlungen und dokumentierten Stückkosten wurden produzierte Einheiten hergeleitet und mit bezahlter Arbeitskapazität, Plan und Finanzierbarkeit verglichen.
3. Aus Zahlungen für tatsächliche Güterverkäufe und festen Stückpreisen wurden die verkauften Einheiten rekonstruiert. Kein Verkauf überschritt die verfügbare Ware.
4. Anfangslager + Produktion − Verkäufe stimmte nach jeder Phase mit dem Endlager überein. Anfangskostenwert + produktive Kosten − anteilige Kosten verkaufter Ware stimmte mit dem Endkostenwert überein. Vollständig geleerte Lager hatten keinen verbleibenden Kostenwert.
5. Umsatz, Warenkosten, produktive/ungenutzte Lohnkosten, unbezahlte Löhne und vertraglicher Zinsaufwand wurden getrennt abgeglichen. Tilgung, Kreditgutschrift und Anlagenkauf gingen nicht als laufender Umsatz beziehungsweise Verbrauchsaufwand in das Ergebnis ein.
6. Steuerberechnung, Ausschüttungen und einbehaltenes Ergebnis wurden aus diesen Größen neu berechnet. Ausschüttungen überschritten weder die halbe positive Nachsteuergröße noch den verfügbaren Betriebsüberhang und erfolgten nicht bei erfassten Rückständen.
7. Zusätzlich galt je Betrieb über den gesamten Lauf die Eigenkapitalbrücke: **Konto + Lagerkostenwert + Anschaffungskosten der Anlagen − Kreditschulden − offene Verpflichtungen = Anfangseigenkapital + kumuliert einbehaltene Ergebnisse**. Die Maschine wurde dabei ohne Abschreibung mit ihrem tatsächlichen Anschaffungspreis von 1.200 € berücksichtigt. Überfällige Tilgung wurde nicht zusätzlich zur Restschuld abgezogen.
8. Die 75/25-Fortschreibung finanzierbarer Nachfrage wurde geprüft; pro Betrieb veränderte sich die Stellenzahl höchstens um eine Person je Monat. Nach dem vollständigen 24. Monat war kein weiterer Schritt möglich und keine zusätzliche Buchung entstanden.

Alle genannten Brücken stimmten in den sechs geprüften Läufen centgenau. Das bestätigt die rechnerische Verbindung von Zahlungs- und Kostenrechnung innerhalb dieser Modellgrenze.

## Gemessene Reaktionen

| Bedingung | Konsum M12 | Konsum M24 | Arbeitsverhältnisse M24 | Lager Alltag / Werkstatt M24 | Staatskonto M24 |
|---|---:|---:|---:|---:|---:|
| Baseline | 9.900 € | 9.900 € | 6 | 17 / 10 | 15.227,84 € |
| Energie ab M3 | 6.800 € | 6.900 € | 5 | 18 / 0 | 46,32 € |
| Konsumzurückhaltung ab M3 | 4.200 € | 5.900 € | 4 | 11 / 6 | 134,26 € |
| Beide ab M3 | 4.200 € | 5.900 € | 4 | 10 / 6 | 78,66 € |
| Konsumzurückhaltung M3, Normalisierung M13 | 4.200 € | 7.200 € | 5 | 14 / 0 | 159,50 € |
| Maschinenkredit vor M1 | 9.900 € | 9.900 € | 6 | 17 / 10 | 20.811,72 € |

Die Baseline baut im gewählten Zeitraum keinen riesigen, ungesteuerten Lagerberg auf. Ein geringeres Konsumbudget verändert finanzierbare Aufträge, geglättete Absatzerwartung und später Beschäftigung. Die Normalisierung bringt in diesem Lauf eine teilweise Erholung, aber keine sofortige Rückkehr zur Baseline. Der Maschinenkredit wurde vollständig getilgt; die gezahlten Zinsen betrugen weiterhin 39 €.

Das sind **Befunde der gewählten Regeln**, keine empirischen Effektgrößen. Insbesondere bedeutet die Maschinenkapazität nicht automatisch mehr Absatz oder Gewinn: Zusätzliche Kapazität kann nur bei entsprechendem Bedarf beziehungsweise anderer Personalplanung genutzt werden.

## Während der Prüfung gefundene und korrigierte Pufferfehler

Die erste bereitgestellte Arbeitsfassung hatte zwei begrenzte Planungsfehler; der Hauptagent korrigierte sie vor dem oben geprüften endgültigen Stand:

- **Nächste Kreditrate fehlte im Zukunftspuffer.** Nach aktuellem Schuldendienst beziehungsweise im Liefermonat lieferte die Quote für den aktuellen Monat null. Die Zukunftsreserve nutzte diese null statt der nächsten Monatsrate. Beim Kreditfall in Monat 1 wurde zunächst ein Puffer von 9.920 € statt 10.026 € ausgewiesen. Die korrigierte Fassung berücksichtigt die nächste fällige Zahlung von 106 €; der Nachlauf weist 10.026 € aus.
- **Zielstellen statt noch vorhandener Verträge geschützt.** Bei verzögertem Stellenabbau konnte die Reserve schon die kleinere Zielzahl verwenden, während die vorhandenen Verträge weiter Lohn kosteten. Baseline Monat 1, Werkstatt: zwei tatsächliche Stellen, Ziel eine Stelle; zunächst nur 5.108 € Puffer. Der Nachlauf schützt mindestens den höheren aktuellen/Zielbestand und weist 9.908 € aus. Nach einem bereits beschlossenen Abbau ist diese Regel ausdrücklich eher konservativ.

Diese Befunde werden nicht als fortbestehende Fehler der finalen Fassung ausgegeben. Die abschließende Bankanfragegrenze für Monat 24 ist im finalen Dateihash enthalten. Ihre gesonderten API-Regressionen gehören zur Hauptprüfung; dieser unabhängige Szenarioscreen fragt den Maschinenkredit vor Monat 1 an.

## Annahmen und verbleibende Grenzen

- 60/32 Einheiten Startabsatz, 25 % Zielbestand, 75/25 Glättung, feste Stückpreise/Löhne, 5/9 € Energiestückkosten, maximal vier Zielstellen je Betrieb, Zwei-Monats-Signal und Ausschüttung bis 50 % sind eigene Testannahmen. Dieser Audit liefert keine externe Evidenz für diese Parameter oder eine reale Personalpolitik.
- Die sechs Haushalte besitzen gleiche Anteile an beiden Betrieben. Daraus folgt eine bestimmte Einkommensverteilung. Kontoguthaben allein sind kein vollständiges Haushaltsvermögen; Unternehmensanteile werden hier nicht als zusätzliche, laufend bewertete Vermögensposition der Eigentümer ausgewiesen.
- Die Personalstückelung und die Reihenfolge von Zahlungen und Käufen bleiben relevante Modellannahmen. Eine formale Stelle ist nicht zwingend eine tatsächlich vollständig bezahlte Stelle; geplante Änderungen gelten für die folgende Lohnphase.
- Maschinen werden im begrenzten Lauf nicht abgeschrieben. Vollständige Investitions-, Finanzierungskosten- und Gewinnsteuerregeln oder unternehmensrechtliche Ausschüttungsgrenzen werden nicht beansprucht.
- Der Staat finanziert seine festen Regeln weiter aus einer endlichen Anfangskasse; der Energie-Außenanschluss führt Geld nicht zurück. In mehreren Schockläufen ist die Staatskasse schon innerhalb der 24 Monate praktisch erschöpft. Solche späteren Ergebnisse sind deshalb gemeinsam durch Unternehmensregeln und diese offenen Außenbedingungen bestimmt.
- Der Horizont von 24 Monaten ist eine bewusste Untersuchungsgrenze. Er ist kein Beweis langfristiger Stabilität. Alte V3-240-Monatsbefunde werden dadurch nicht widerlegt oder als neue V4-Befunde ausgegeben.
- Oberfläche, Bedienbarkeit und Verständnis durch Workshop-Teilnehmer wurden von diesem separaten Agenten nicht geprüft. Rechnerische Konsistenz ersetzt keinen pädagogischen oder empirischen Nachweis.

## Urteil

**Die geprüfte V4-Fassung ist als begrenzter, regeloffener Unternehmens-Lernlauf deutlich nachvollziehbarer als die vorherige ungesteuerte Produktion.** Konten, Bankbilanz, Gütermenge, Lagerkosten, Ergebnis, Eigentümerausschüttung und einbehaltenes Eigenkapital schließen in den sechs Szenarien. Die zwei im Nachtest gefundenen Pufferfehler sind im finalen Stand korrigiert.

Die Richtungsreaktionen sind innerhalb der eigenen Annahmen erklärbar. Eine empirisch plausible Gesamtwirtschaft oder eine langfristige Prognosefähigkeit ist damit nicht nachgewiesen. Weitere Modellgrenzen wurden für diesen Auftrag nicht erweitert.

## Reproduzierbare Wiederholung

Der öffentliche [Prüflauf](../tools/check_company_plausibility.py) wiederholt dieselben sechs Szenarien und vergleicht alle Monatswerte mit dem gespeicherten Ergebnis. Vom Repository-Stamm mit der eingerichteten POC-Python-Umgebung:

```sh
poc/.venv/bin/python tools/check_company_plausibility.py
```

Die vier Kernhashes müssen zum aufgezeichneten Stand passen. Eine Wiederholung mit dem endgültigen unveränderten Kern bestätigte erneut alle 6.636 Buchungen und sämtliche Brücken. Originale QA-Ergebnisse werden nicht überschrieben. Optional kann ein neuer Wiederholungsbeleg geschrieben werden:

```sh
poc/.venv/bin/python tools/check_company_plausibility.py --output poc/.runtime/company-repeat.json
```

Bei späteren Kernänderungen stoppt der Quellenvergleich. Dann ist eine neue, eigens bezeichnete Prüfung erforderlich; frühere Befunde dürfen nicht als Prüfung einer neueren Fassung ausgegeben werden.
