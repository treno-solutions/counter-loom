# Unabhängige Plausibilitätsprüfung: Unternehmenssystem V10

Prüfdatum: 2026-11-03. Illustrative Regeln, keine empirische Kalibrierung. Eingaben, kompakte Monatsdaten und acht finale Kernprüfsummen stehen in [company-v10-plausibility.json](company-v10-plausibility.json). Frühere Berichte bleiben unverändert.

**Ergebnis:** Neun frische 24-Monats-Vergleichsläufe und vier offene 240-Monatsläufe bestanden die unabhängigen Brücken: 1.176 Weltmonate, 5.880 Phasen und 47.252 Buchungen. Elf gezielte Unternehmensfälle mit weiteren 29 Buchungen bestanden. Drei konkret reproduzierte Widersprüche wurden während der Prüfung korrigiert und nachgeprüft. Im finalen geprüften Umfang wurden keine weiteren Kernfehler gefunden.

Die Langläufe haben weiterhin wirtschaftliche Modellgrenzen. Anders als in V9 tritt jedoch in keinem der vier 240-Monatsläufe ein Monat mit Nullproduktion beider Firmen auf. Das ist ein Befund für diese Regeln und Eingaben; es ist kein Nachweis realistischer Anpassung oder langfristigen Gleichgewichts. Oberfläche und Unterrichtswirkung wurden nicht geprüft.

## Unabhängig nachgerechnet

Aus Anfangsbeständen und jedem Journalbeleg wurden sämtliche Geldkonten, Bankeinlagen/-forderungen/-kapital sowie Staatskasse und -kreditschuld rekonstruiert. Quell-/Zielstände vor und nach Buchung, Kreditgutschriften, Tilgungen und tatsächliche Bankausschüttungen stimmen. Es entstanden keine negativen Geldkonten oder unausgeglichenen Bankbilanzen. Die Firmen-Eigenkapitalbrücke stimmt einschließlich historischer Maschinenkosten und offener Ansprüche.

Produktionsmengen wurden aus tatsächlich bezahlter proportionaler Arbeit, Maschinenkapazität und Energie hergeleitet. Lager werden nur um tatsächlich bezahlte produktive Kosten erhöht und bei Verkäufen um gleitende Durchschnittskosten vermindert; keine Preisneubewertung. Warenzahlungen, Haushaltsmengen zu Startpreisen, GuV, Steuern, Ausschüttungen, feste/variable Zinsen, Staatskreditbeträge mit FIFO-Tilgung/Centverteilung sowie Auslandsbudgets und Lieferbelege wurden unabhängig abgeglichen.

Die V10-Kontrollen ergänzen:

- Lohn und Kapazität folgen der wirksamen Arbeitszeit. Entscheidungen gelten ab dem Folgemonat. Die Quote laufender Betriebe liegt bei 25–100 % und verändert sich höchstens um 25 Prozentpunkte je Abschluss; ein Wiederanlauf beginnt mit einer neu geprüften Anfangsquote.
- Vorschau-Erlöse, notwendige Vorfinanzierung, Finanzierungslücke und zwei proportionale Lohnrunden Reserve wurden unabhängig aus dem jeweiligen Personal-/Zeitvorschlag berechnet. GuV und Cashflow bleiben getrennt; Tilgung ist kein GuV-Verlust.
- GuV-Verluste erhöhen den verwendeten Verlustspielraum; zwei profitable Monate mit gedecktem Betriebspuffer können ihn zurücksetzen. Diese Zähler erzeugen keine Einlage und keine Kreditforderung. Sämtliche Geldänderungen bleiben durch das Journal erklärt.
- Brückenentscheidungen benötigen vorhandenes Geld, passenden Restspielraum und höchstens drei aufeinanderfolgende Brückenentscheidungen. Positive Prognosen allein ersetzen keine Vorfinanzierung.
- Stilllegung entfernt Arbeitskräfte, aber weder vorhandene Waren noch Schulden. Wiederanlauf benötigt zwei tragfähige Abschlüsse, freie Arbeitskraft und gedeckten Betriebspuffer. Im laufenden Monat entsteht dadurch noch keine Produktion.
- Höchstens eine Personaländerung je regulärem Abschluss; vollständige Stilllegung ist die ausdrückliche Ausnahme. Ausschüttung nur bei regulär tragfähigem Weiterbetrieb und ohne offene Verpflichtungen.

## Neun Vergleichsfenster über 24 Monate

Energie-/Nachfrageschocks beginnen in Monat 3. „Kombiniert“ enthält beide und 4 % Leitzins ab Monat 2. Standard: 80.000 € Staatsanfangskasse, 50.000 € Staatskreditlimit, ein Reservemonat. Der Maschinenlauf enthält Energie und eine Anfrage vor Monat 1. Die 24 Monate sind ein optionaler Testhorizont; der Produktstandard bleibt offen.

| Lauf | Buchungen | Konsum Monat 24 nominal € | Arbeitsverhältnisse gesamt | Staatskasse Ende € | Staatskreditschuld Ende € |
|---|---:|---:|---:|---:|---:|
| Basis | 1.246 | 9.900 | 6 | 22.710,39 | 0 |
| Energie | 1.240 | 9.347 | 6 | 20.785,78 | 0 |
| Nachfrage | 1.251 | 5.900 | 6 | 7.212,56 | 8.505,13 |
| Kombiniert | 1.244 | 5.443 | 6 | 7.219,51 | 8.161,68 |
| Staatsanfangskasse 7.200 € | 1.288 | 8.350 | 6 | 1.264,62 | 50.000 |
| Staatskreditlimit null | 1.246 | 9.900 | 6 | 22.710,39 | 0 |
| Null Reservemonate | 1.246 | 9.900 | 6 | 22.710,39 | 0 |
| Zwei Reservemonate | 1.246 | 9.900 | 6 | 22.710,39 | 0 |
| Maschine und Energie | 1.260 | 9.142 | 6 | 19.437,34 | 0 |

Alle vier betrieblichen Stellen bestehen in diesen Monatsendzuständen weiter, jedoch mit unterschiedlicher Arbeitszeit. Im Nachfrageszenario liegen die Quoten bei 66,67/67,50 %. Sechs Arbeitsverhältnisse bedeuten deshalb keine sechs Vollzeitstellen. Nominaler Geldumsatz und gekaufte Warenmengen bleiben ebenfalls getrennte Größen.

## Vier offene Langläufe über 240 Monate

Die offene Basis bleibt unverändert. Der späte Schock setzt Energie, Nachfrage und 4 % Leitzins ab Monat 25. Die Zyklen wechseln ab Monat 25 im Abstand von 24 Monaten zwischen diesem Schock und Energie-/Nachfrageerholung mit 1 % Leitzins; letzte Erholung ab Monat 193. Der arme Staat startet mit 7.200 € und Kreditlimit null. Exakte Ereignispläne stehen im JSON.

| Lauf | Buchungen | Nominaler Konsum Monat 240 € | Private Arbeitskräfte Ende | Gesamte Arbeitsverhältnisse Ende | Offene öffentliche Löhne Ende € |
|---|---:|---:|---:|---:|---:|
| Basis | 10.778 | 2.800 | 2 | 4 | 882.081,97 |
| Schock ab Monat 25 | 9.995 | 2.310 | 2 | 4 | 937.572,97 |
| Wiederholte Zyklen | 8.394 | 1.300 | 1 | 3 | 932.730,92 |
| Armer Staat ohne Kredit | 6.818 | 600 | 1 | 3 | 1.124.927,03 |

Die Basis arbeitet Ende Monat 240 mit je einer Person bei 50/40 % Arbeitszeit. Im Zykluslauf wird die Werkstatt ab Monat 104 stillgelegt, nach Entscheidung in Monat 103; im armen Staat ab Monat 80, nach Entscheidung in Monat 79. In diesen vier regulären Pfaden wurde kein tatsächlicher Wiederanlauf beobachtet. Dessen technische Funktionsfähigkeit wird durch den kontrollierten Fall belegt, nicht durch ein behauptetes natürliches Wiederaufleben dieser Läufe.

Der vorherige vollständige Produktionsstillstand wird mit diesen Parametern vermieden. Gleichzeitig bleiben öffentliche Löhne trotz fortbestehender Verträge oft unbezahlt; zwei öffentliche Arbeitsverhältnisse dürfen nicht als zwei gesicherte Einkommen gelesen werden. Kreditschuld, offene Löhne und offene Zinsen sind verschiedene Bestände. Die Produktionsanpassung löst dieses fiskalische und institutionelle Modellproblem nicht.

Alle 240 Monatsgeschichten und das vollständige Journal bleiben im Export erhalten; die normale `history`-Antwort enthält die letzten 36 Monate. Neue Vorgaben und Weiterlauf in Monat 241 funktionieren. Diese Fortsetzung ist ein technischer Probeaufruf außerhalb des bilanziell rekonstruierten 240-Monatsfensters.

## Elf gezielte Fälle und behobene Widersprüche

Die Fälle verwenden ausdrücklich gesetzte physische Ausgangsbestände oder kontrollierte Abschluss-Eingaben. Insbesondere synthetische GuV-Eingaben dienen der isolierten Entscheidungskontrolle, nicht als zusätzliche vollständige Wirtschaftssimulation. Alle dabei tatsächlich erzeugten Geldbuchungen wurden separat rekonstruiert.

1. **Kapazitätsrundung:** Eine Person, eine Maschine, 32,50 % Zeit: 780 € Lohn und 13 Einheiten. Vor der Korrektur versprach die Vorschau 13, die Ausführung lieferte wegen getrennter Abrundungen nur 12. Die finale gemeinsame Rundung stimmt; produktive Kosten und Lagerzugang 845 €.
2. **Kein Geld für anteiligen Lohn:** 780 € bleiben als Anspruch offen; keine bezahlte Arbeit und keine kostenlosen Güter.
3. **Einstellprüfung bei 7.000 €:** Eine vorhandene Person bei 100 %, Prognose 37. Zwei Personen können wegen der Übergangsgrenze zunächst nur auf 75 % sinken: Reserve 7.455 €, Vorschaulücke 155 €. Die Einstellung wird mangels Reserve abgewiesen. Vor der Korrektur wurde mit sofortigen 65,28 % und nur 6.521,88 € Reserve geprüft.
4. **Einstellprüfung bei 24.000 €:** Derselbe Übergangsplan ist als vorfinanzierte, budgetgedeckte Brücke zulässig; die neue Stelle entsteht mit tatsächlich geplanten 75 %.
5. **Investitionspuffer:** Höhere schon geplante Arbeitszeit bleibt in der Reservenprüfung geschützt; im kontrollierten Fall 9.855 €.
6. **Reset vor Folgeentscheidung:** Nach dem zweiten profitablen Monat und gedeckter Reserve steht der erneuerte Spielraum bereits für den Folgeplan zur Verfügung. Der 380-€-Werkstattübergang ist dann `buffered`; vor der Korrektur wurde zuerst stillgelegt und erst danach der Zähler zurückgesetzt.
7. **Drei Brücken:** Nach drei `buffered`-Entscheidungen führt die vierte nicht tragfähige Vorschau zur Stilllegung. Verlustzähler verändern die Kasse nicht; kein Kredit entsteht aus dem Budget.
8. **Restspielraum überschritten:** Auch bei hoher Kasse kann eine zu große prognostizierte Lücke zur Stilllegung führen.
9. **Vorfinanzierung fehlt:** Ungenutztes Verlustbudget ersetzt fehlendes Geld nicht; Stilllegung.
10. **Realer Wiederanlauf:** Nach zwei gedeckten Prüfungen wird eine freie Person eingestellt; alter Brückenzähler zurückgesetzt. Lager, historische Lagerkosten und Altschuld bleiben erhalten. Produktion und Lohnzahlung beginnen erst in der folgenden Produktionsphase, aus tatsächlicher Kasse und ohne magische Kreditgutschrift.
11. **Wiederanlauf ohne Kasse:** Bleibt trotz positiver Nachfrage gesperrt.

## Reichweite und Version

Die Verlustbrücke ist eine begrenzte Prognose-/Entscheidungsregel, keine Versicherung gegen jeden tatsächlichen Verlust und kein Geldkonto. Feste Lohnsätze, Mindestzeit, Personenteilung, Margenrechnung und Prognoseglättung sind Modellannahmen. Bei 25 % Arbeit entstehen 600 € brutto beziehungsweise 420 € nach der festen Steuer, während Arbeitslosigkeit hier 1.000 € Transfer erhält. Eine Aufstockung oder realistische Kurzarbeitsregel fehlt; dies kann Konsum- und Betriebszyklen beeinflussen.

Langfristige Tragfähigkeit, repräsentative Personalpolitik und Unterrichtswirkung sind nicht validiert. V10 zeigt für die geprüften Eingaben mehr betriebliche Anpassung; eine gesund laufende Gesamtwirtschaft ist damit nicht nachgewiesen.

Nach Beginn des Langtests wurden nur drei Erklärungstexte in `world.py`/`banking.py` aktualisiert. Der Rechenkern wurde durch strukturellen AST-Vergleich als unverändert geprüft. Alle neun kurzen Läufe und elf Ports wurden auf dem finalen Textstand wiederholt und reproduzieren ihre Ergebnisse exakt. Finale Quellen und vorherige Textprüfsummen sind im JSON bezeichnet. Kerndateien und frühere Auditdateien wurden durch den unabhängigen Prüfer nicht verändert.
