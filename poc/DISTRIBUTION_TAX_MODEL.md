# Ausschüttungssteuer und verfügbare Eigentümereinkommen · v14

Eine illustrative Einnahmenregel ergänzt die bestehende [Staatsfinanzierung](FISCAL_MODEL.md) und das [anpassende Budget](PUBLIC_BUDGET_MODEL.md). Sie bildet keine konkrete nationale Steuergesetzgebung ab. Standard: **25 %** auf tatsächlich ausgezahlte Firmen- und Bankausschüttungen, ohne Freibeträge. Der Rechenkern erlaubt ganzzahlige Basispunkte von 0 bis 5000; die Oberfläche startet mit 2500. Ein Nullsatz reproduziert die bisherige Steuerbasis.

## Steuerbasis und Buchungen

- Reguläre Firmenausschüttungen, zusätzliche Quartalsausschüttungen und tatsächliche Bank-Zinsausschüttungen sind steuerpflichtig.
- Der Bruttobetrag wird tatsächlich auf das Eigentümerkonto überwiesen; unmittelbar danach fliesst der Einbehalt als eigene Buchung an den Staat. Nicht ausgezahlte Ansprüche werden nicht besteuert.
- Pro Haushalt und Monat ist die gesamte Steuer `floor(kumuliertes Brutto × Basispunkte / 10000)`. Bei jeder Auszahlung wird nur die Differenz zur schon einbehaltenen Steuer fällig. Aufteilen von Centbeträgen oder mehrere Zahler ändern die Monatssteuer nicht. Die Haushalte werden getrennt gerundet.
- Brutto minus Einbehalt ergibt Netto. Nur Netto erhöht den Ausschüttungsübertrag für die nächste Kaufrunde. Lohnsteuer und Nettolohn werden dadurch nicht erneut vermindert.
- Bei der Firma bleibt die Bruttoausschüttung gewinnvortragsmindernd. Der Einbehalt ist keine Betriebsausgabe und vermindert nicht nochmals den Firmengewinn. Die bisherige Gewinnsteuer bleibt getrennt.
- Der Einbehalt verschiebt vorhandene Kundeneinlagen zwischen Haushalt und Staat. Er schafft oder vernichtet selbst kein Geld.

## Abschlussreihenfolge und Rückkopplung

Firmen schliessen vor der Bank ab. Alle Ausschüttungseinbehalte müssen vor Budgetprüfung und Aufzeichnung des Staatsabschlusses vorliegen. Bankausschüttungen können dabei Steuerzahlungen ermöglichen, die offene Staatszinsen bezahlen; diese sind wiederum Bankertrag.

Der Abschluss wickelt diese Rückkopplung durch tatsächliche Zahlungen ab: offene Staatszinsen bedienen, noch nicht ausgeschüttete tatsächlich erhaltene Bankzinsen ausschütten und gegebenenfalls aus neuem Einbehalt weitere offene Staatszinsen bedienen. Erfasst werden nur tatsächliche Zinsen aus Firmen-, Maschinen- und Staatskrediten; Kapitalbewegungen oder andere Bankeingänge werden nicht als Zinsbasis ausgegeben. Bei höchstens 50 % Steuer fällt der nächste aus dem Einbehalt finanzierbare Betrag; Cent-Rundung beendet die Folge. Ohne neuen Einbehalt oder ohne offene Zinsen endet sie sofort.

Erst anschliessend prüft der Staat seine Ausgabenregel und Kreditreserve. Alle Ausschüttungssteuern zählen wie Lohn- und Gewinnsteuer zur tatsächlichen wiederkehrenden Deckung. Lohnnachzahlungssteuer bleibt von dieser wiederkehrenden Basis ausgeschlossen. Die Kassenbrücke und der Monatsendbestand enthalten sämtliche tatsächlich gezahlten Steuern. Die Steuerregel erzwingt weder ein ausgeglichenes Budget noch eine Konjunkturerholung.

## Sichtbarkeit und Prüfung

Die Staatsansicht zeigt Lohn-, Gewinn- und Ausschüttungssteuer sowie Brutto, Einbehalt und Netto pro Haushalt. Firmenabschlüsse zeigen die zugehörigen Brutto-/Nettozahlungen auch bei Auswahl älterer Monate. Einzeln betrachtete Haushalte sehen ihre aktuellen Ausschüttungsbeträge; Kaufhistorien behalten die damals tatsächlich verwendeten Nettobeträge. Der Zahlungsweg Haushalte → Staat berücksichtigt den Einbehalt.

Die letzten 36 Steuerabschlüsse stehen interaktiv bereit. Der Laufexport enthält alle Monatsabschlüsse und Einzelzuordnungen zwischen Brutto- und Steuerbeleg. [Kontrollierter 600-Monats-Vergleich](../qa/tax-v14-comparison.md). Referenz: dieselbe anpassende Budgetregel, derselbe Anfangszustand, lediglich 0 statt 25 % Einbehalt.

## Bewusste Grenzen

Keine progressive Einkommensteuer, Mehrwertsteuer, Abzüge, Freibeträge, Steuervermeidung, Vermögensteuer oder unterschiedliche Eigentumsquoten. Keine zusätzliche Kreditart, kein externer Geldzufluss und keine Rückzahlung nicht finanzierter Sozial-Referenzbedarfe. Die Erweiterung prüft eine zusätzliche Einnahmequelle und ihre Rückwirkungen innerhalb der bisherigen kleinen Modellwirtschaft.
